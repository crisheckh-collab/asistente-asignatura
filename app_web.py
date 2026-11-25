"""Interfaz web del asistente de Fundamentos de IA (Streamlit).

Uso:
    streamlit run app_web.py
"""

import asyncio
import queue
import threading

import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage

from app.config import CARPETA_CHROMA, CARPETA_DOCS
from app.grafo import construir_grafo

st.set_page_config(page_title="Asistente Fundamentos de IA", page_icon="🎓", layout="centered")

EJEMPLOS = [
    "Tengo un 6 en prácticas y un 7 en participación. ¿Qué nota necesito en el examen para aprobar?",
    "¿Qué pasa si entrego tarde una práctica?",
    "¿Puedo usar asistentes de IA en las prácticas?",
    "Si saco un 8 en el examen, un 5 en prácticas y un 9 en participación, ¿qué nota final tengo?",
]
ICONOS = {"supervisor": "🧭", "documentalista": "📚", "calculadora": "🧮"}


# --- Motor: el grafo vive en un bucle asyncio propio, en un hilo aparte ---
# Streamlit vuelve a ejecutar el script en cada interacción; con cache_resource
# el grafo (y el servidor MCP) se construyen una sola vez.

@st.cache_resource(show_spinner="Arrancando agentes y servidor MCP...")
def motor():
    bucle = asyncio.new_event_loop()
    threading.Thread(target=bucle.run_forever, daemon=True).start()
    grafo = asyncio.run_coroutine_threadsafe(construir_grafo(), bucle).result()
    return bucle, grafo


async def _ejecutar(grafo, mensajes, cola: queue.Queue):
    """Recorre el grafo y va metiendo cada paso en la cola."""
    try:
        async for paso in grafo.astream({"messages": mensajes}, stream_mode="updates"):
            for nodo, cambios in paso.items():
                cola.put((nodo, cambios))
    except Exception as error:  # se muestra en la interfaz
        cola.put(("error", error))
    finally:
        cola.put(None)


def describir(nodo: str, cambios: dict) -> str:
    if nodo == "supervisor":
        if cambios["siguiente"] == "FIN":
            return "🧭 **Supervisor**: ya hay información suficiente."
        icono = ICONOS.get(cambios["siguiente"], "➡️")
        return f"🧭 **Supervisor** → {icono} *{cambios['siguiente']}*: {cambios['tarea']}"
    hallazgo = cambios["hallazgos"][-1]
    nombre, _, texto = hallazgo.partition("] ")
    return f"{ICONOS.get(nodo, '•')} **{nodo.capitalize()}**:\n\n{texto}"


# --- Barra lateral ---

with st.sidebar:
    st.header("🎓 Fundamentos de IA")
    st.caption("Supervisor (LangGraph) + documentalista (RAG con ChromaDB vía MCP) "
               "+ calculadora de notas.")
    st.subheader("Documentos")
    for fichero in sorted(CARPETA_DOCS.glob("*.md")):
        st.markdown(f"- `{fichero.name}`")
    if not CARPETA_CHROMA.exists():
        st.warning("No existe chroma_db/. Ejecuta `python -m app.ingesta`.")
    ver_pasos = st.toggle("Mostrar razonamiento de los agentes", value=True)
    if st.button("🗑️ Nueva conversación", use_container_width=True):
        st.session_state.historial = []
        st.rerun()


# --- Chat ---

st.title("Asistente de la asignatura")
st.caption("Pregunta sobre evaluación, prácticas o normas, o pide que te calcule notas.")

if "historial" not in st.session_state:
    st.session_state.historial = []  # lista de dicts: rol, texto, pasos

for msg in st.session_state.historial:
    with st.chat_message(msg["rol"]):
        if msg.get("pasos") and ver_pasos:
            with st.expander("Cómo se ha resuelto", expanded=False):
                for linea in msg["pasos"]:
                    st.markdown(linea)
        st.markdown(msg["texto"])

pregunta = st.chat_input("Escribe tu pregunta...") or st.session_state.pop("pendiente", None)
if not st.session_state.historial and not pregunta:
    st.write("**Prueba con:**")
    for ejemplo in EJEMPLOS:
        if st.button(ejemplo, use_container_width=True):
            st.session_state.pendiente = ejemplo  # se procesa tras recargar, sin botones
            st.rerun()

if pregunta:
    st.session_state.historial.append({"rol": "user", "texto": pregunta})
    with st.chat_message("user"):
        st.markdown(pregunta)

    # Memoria: se pasan los últimos mensajes para entender preguntas de seguimiento
    mensajes = [
        HumanMessage(m["texto"]) if m["rol"] == "user" else AIMessage(m["texto"])
        for m in st.session_state.historial[-6:]
    ]

    with st.chat_message("assistant"):
        bucle, grafo = motor()
        cola: queue.Queue = queue.Queue()
        asyncio.run_coroutine_threadsafe(_ejecutar(grafo, mensajes, cola), bucle)

        pasos, respuesta = [], None
        with st.status("Pensando...", expanded=ver_pasos) as estado:
            while (item := cola.get()) is not None:
                nodo, cambios = item
                if nodo == "error":
                    respuesta = f"⚠️ Error: `{cambios}`"
                    if "429" in str(cambios):
                        respuesta += "\n\nLímite por minuto de Groq: espera unos segundos y repite."
                elif nodo == "responder":
                    respuesta = cambios["messages"][-1].text
                else:
                    linea = describir(nodo, cambios)
                    pasos.append(linea)
                    st.markdown(linea)
            estado.update(label="Resuelto", state="complete", expanded=False)

        st.markdown(respuesta or "No he obtenido respuesta.")
    st.session_state.historial.append(
        {"rol": "assistant", "texto": respuesta or "", "pasos": pasos}
    )

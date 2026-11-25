"""Orquestación con LangGraph: un supervisor reparte el trabajo entre especialistas.

INICIO -> supervisor -> (documentalista | calculadora) -> supervisor -> ...
       -> responder -> FIN
"""

import operator
from typing import Annotated, Literal

from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import END, START, MessagesState, StateGraph
from pydantic import BaseModel, Field

from app.agentes import crear_especialistas
from app.config import crear_modelo

MAX_PASOS = 4  # límite de seguridad para que el supervisor no entre en bucle


class Estado(MessagesState):
    """Estado compartido del grafo. La clave "messages" ya viene de MessagesState."""

    siguiente: str  # a quién le toca actuar
    tarea: str  # encargo para ese especialista
    hallazgos: Annotated[list[str], operator.add]  # se acumulan, no se sustituyen


class Decision(BaseModel):
    """Respuesta estructurada del supervisor."""

    siguiente: Literal["documentalista", "calculadora", "FIN"] = Field(
        description="Quién actúa ahora, o FIN si ya hay información suficiente."
    )
    tarea: str = Field(description="Encargo completo, con los datos. Vacío si FIN.")


PROMPT_SUPERVISOR = """Eres el supervisor del asistente de Fundamentos de IA.
No respondes al alumno: decides qué especialista actúa.

- documentalista: busca en la guía docente, las normas de prácticas y las FAQ.
- calculadora: hace cálculos de notas (medias, nota necesaria en el examen).

Si un cálculo necesita datos de los documentos (por ejemplo, los pesos),
pide primero los datos al documentalista y luego pasa los números a la calculadora.
Al documentalista pídele SIEMPRE, además de los datos, cualquier norma, nota mínima,
requisito o excepción relacionada con la pregunta.

Información recogida hasta ahora:
{hallazgos}

Reglas para decidir:
- No vuelvas a llamar a un especialista para algo que ya aparece arriba.
- En cuanto la calculadora haya dado su resultado, responde FIN.
- Si ya hay información suficiente, o la pregunta no es de la asignatura, responde FIN."""

PROMPT_RESPUESTA = """Eres el asistente de la asignatura Fundamentos de IA.
Responde al alumno con claridad usando SOLO esta información, y cita las fuentes:

{hallazgos}

Antes de responder, comprueba que el resultado de cualquier cálculo cumple las normas
de los documentos (por ejemplo, notas mínimas) y corrígelo si no las cumple.
Responde en texto plano o Markdown sencillo, sin fórmulas LaTeX.
Si no hay información suficiente, dilo."""


def _texto(estado: Estado) -> str:
    return "\n".join(estado.get("hallazgos", [])) or "Ninguna todavía."


async def construir_grafo(modelo=None, herramientas_mcp=None):
    modelo = modelo or crear_modelo()
    especialistas = await crear_especialistas(modelo, herramientas_mcp)
    decisor = modelo.with_structured_output(Decision)  # responde con el esquema Decision

    # --- Nodos: reciben el estado y devuelven solo lo que cambian ---

    async def supervisor(estado: Estado) -> dict:
        if len(estado.get("hallazgos", [])) >= MAX_PASOS:
            return {"siguiente": "FIN", "tarea": ""}
        prompt = PROMPT_SUPERVISOR.format(hallazgos=_texto(estado))
        decision = await decisor.ainvoke([SystemMessage(prompt), *estado["messages"]])
        return {"siguiente": decision.siguiente, "tarea": decision.tarea}

    def crear_nodo(nombre: str):
        async def nodo(estado: Estado) -> dict:
            # El especialista solo recibe su encargo, no toda la conversación
            entrada = {"messages": [HumanMessage(estado["tarea"])]}
            resultado = await especialistas[nombre].ainvoke(entrada)
            return {"hallazgos": [f"[{nombre}] {resultado['messages'][-1].text}"]}

        return nodo

    async def responder(estado: Estado) -> dict:
        prompt = PROMPT_RESPUESTA.format(hallazgos=_texto(estado))
        respuesta = await modelo.ainvoke([SystemMessage(prompt), *estado["messages"]])
        return {"messages": [respuesta]}

    # --- Grafo: nodos y aristas ---

    grafo = StateGraph(Estado)
    grafo.add_node("supervisor", supervisor)
    grafo.add_node("responder", responder)
    for nombre in especialistas:
        grafo.add_node(nombre, crear_nodo(nombre))
        grafo.add_edge(nombre, "supervisor")  # cada especialista vuelve al supervisor

    grafo.add_edge(START, "supervisor")
    # Arista condicional: el destino depende de estado["siguiente"]
    rutas = {"documentalista": "documentalista", "calculadora": "calculadora",
             "FIN": "responder"}
    grafo.add_conditional_edges("supervisor", lambda estado: estado["siguiente"], rutas)
    grafo.add_edge("responder", END)
    return grafo.compile()

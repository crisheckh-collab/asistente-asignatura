"""Batería de pruebas: lanza varias preguntas y guarda la traza en resultados.md.

Cubre los casos típicos: solo documentalista, solo calculadora, los dos,
y una pregunta fuera de la asignatura.

Uso:
    python probar_preguntas.py
"""

import asyncio
import os
from datetime import datetime

from langchain_core.messages import HumanMessage

from app.config import RAIZ
from app.grafo import construir_grafo

PREGUNTAS = [
    ("Solo documentalista", "¿Qué pasa si entrego tarde una práctica?"),
    ("Solo documentalista", "¿Puedo usar asistentes de IA en las prácticas?"),
    ("Solo calculadora", "¿Cuál es la media ponderada de un 8 con peso 50, un 5 con peso 30 y un 9 con peso 20?"),
    ("Documentalista + calculadora",
     "Tengo un 6 en prácticas y un 7 en participación. ¿Qué nota necesito en el examen para aprobar?"),
    ("Documentalista + calculadora",
     "Si saco un 8 en el examen, un 5 en prácticas y un 9 en participación, ¿qué nota final tengo?"),
    ("Fuera de la asignatura", "¿Cuál es la capital de Australia?"),
]


async def una_pregunta(grafo, pregunta: str) -> tuple[list[str], str]:
    pasos, respuesta = [], ""
    async for paso in grafo.astream({"messages": [HumanMessage(pregunta)]}, stream_mode="updates"):
        for nodo, cambios in paso.items():
            if nodo == "supervisor":
                if cambios["siguiente"] == "FIN":
                    pasos.append("**supervisor** → FIN")
                else:
                    pasos.append(f"**supervisor** → {cambios['siguiente']}: {cambios['tarea']}")
            elif nodo == "responder":
                respuesta = cambios["messages"][-1].text
            else:
                texto = cambios["hallazgos"][-1].split("] ", 1)[-1].replace("\n", " ")
                pasos.append(f"**{nodo}**: {texto}")
    return pasos, respuesta


async def main() -> None:
    grafo = await construir_grafo()
    lineas = [
        "# Resultados de las pruebas",
        "",
        f"Fecha: {datetime.now():%d/%m/%Y %H:%M} · Modelo: `{os.getenv('MODELO')}`",
        "",
    ]
    for i, (tipo, pregunta) in enumerate(PREGUNTAS, 1):
        print(f"[{i}/{len(PREGUNTAS)}] {pregunta}")
        try:
            pasos, respuesta = await una_pregunta(grafo, pregunta)
        except Exception as error:
            pasos, respuesta = [], f"ERROR: {error}"
        lineas += [f"## {i}. {pregunta}", "", f"*Caso: {tipo}*", "", "**Traza:**", ""]
        lineas += [f"{n}. {p}" for n, p in enumerate(pasos, 1)]
        lineas += ["", "**Respuesta:**", "", respuesta, "", "---", ""]
        await asyncio.sleep(5)  # margen para el límite por minuto de Groq

    destino = RAIZ / "resultados.md"
    destino.write_text("\n".join(lineas), encoding="utf-8")
    print(f"\nGuardado en {destino}")


if __name__ == "__main__":
    asyncio.run(main())

"""Herramientas locales del agente calculadora.

Una herramienta es una función normal con el decorador @tool. El modelo lee
el docstring para saber cuándo usarla y los tipos para saber qué pasarle.
"""

from langchain_core.tools import tool


@tool
def media_ponderada(notas: list[float], pesos: list[float]) -> float:
    """Calcula la media ponderada de unas notas.
    Los pesos pueden ir en tanto por uno (0.3) o en porcentaje (30)."""
    total = sum(n * p for n, p in zip(notas, pesos))
    return round(total / sum(pesos), 2)


@tool
def nota_necesaria(
    nota_objetivo: float, notas: list[float], pesos: list[float], peso_pendiente: float
) -> float:
    """Calcula la nota que hace falta en la parte pendiente (p. ej. el examen) para
    llegar a nota_objetivo, conociendo las notas y pesos del resto de partes.
    Todos los pesos en la misma escala (tanto por uno o porcentaje)."""
    peso_total = sum(pesos) + peso_pendiente
    conseguido = sum(n * p for n, p in zip(notas, pesos))
    return round((nota_objetivo * peso_total - conseguido) / peso_pendiente, 2)

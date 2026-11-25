"""Agentes especialistas.

Agente = modelo + instrucciones (system prompt) + herramientas.
create_agent monta el bucle: pensar -> usar herramienta -> leer resultado -> responder.
"""

import sys

from langchain.agents import create_agent
from langchain_mcp_adapters.client import MultiServerMCPClient

from app.config import RAIZ
from app.herramientas import media_ponderada, nota_necesaria


async def cargar_herramientas_mcp() -> list:
    """Arranca nuestro servidor MCP y convierte sus herramientas al formato LangChain."""
    cliente = MultiServerMCPClient(
        {
            "apuntes": {
                "transport": "stdio",
                "command": sys.executable,  # el mismo Python que ejecuta este programa
                "args": ["-m", "app.servidor_mcp"],
                "cwd": str(RAIZ),
            }
        }
    )
    return await cliente.get_tools()


async def crear_especialistas(modelo, herramientas_mcp=None) -> dict:
    """Devuelve un diccionario {nombre: agente}."""
    if herramientas_mcp is None:
        herramientas_mcp = await cargar_herramientas_mcp()

    documentalista = create_agent(
        modelo,
        tools=herramientas_mcp,  # buscar_apuntes, que llega desde el servidor MCP
        system_prompt="Eres el documentalista de la asignatura. Busca SIEMPRE con tu "
        "herramienta y responde solo con lo que digan los documentos, citando el "
        "fichero de la fuente. Incluye también cualquier nota mínima, requisito o "
        "excepción que aparezca junto a la información pedida. "
        "Si no está en los documentos, dilo.",
        name="documentalista",
    )
    calculadora = create_agent(
        modelo,
        tools=[media_ponderada, nota_necesaria],
        system_prompt="Eres la calculadora de notas. Haz las cuentas SIEMPRE con tus "
        "herramientas y explica el resultado en una frase.",
        name="calculadora",
    )
    return {"documentalista": documentalista, "calculadora": calculadora}

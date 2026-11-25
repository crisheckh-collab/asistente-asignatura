"""Servidor MCP hecho con FastMCP: ofrece la búsqueda en ChromaDB como herramienta.

Lo puede usar cualquier cliente MCP: nuestro agente, Claude Code, Claude Desktop...
Normalmente lo arranca el cliente; para lanzarlo a mano:
    python -m app.servidor_mcp
"""

from fastmcp import FastMCP
from langchain_chroma import Chroma

from app.config import CARPETA_CHROMA, COLECCION, crear_embeddings

servidor = FastMCP("apuntes")

# Abrimos la base vectorial que creó la ingesta (no la volvemos a crear)
base = Chroma(
    collection_name=COLECCION,
    embedding_function=crear_embeddings(),
    persist_directory=str(CARPETA_CHROMA),
)


@servidor.tool
def buscar_apuntes(consulta: str, k: int = 3) -> str:
    """Busca en la guía docente, las normas de prácticas y las preguntas
    frecuentes de la asignatura. Devuelve los k fragmentos más parecidos."""
    resultados = base.similarity_search(consulta, k=k)
    return "\n\n".join(
        f"[Fuente: {doc.metadata['fuente']}]\n{doc.page_content}" for doc in resultados
    )


if __name__ == "__main__":
    # stdio: el cliente habla con el servidor por la entrada y salida estándar
    servidor.run(transport="stdio", show_banner=False, log_level="WARNING")

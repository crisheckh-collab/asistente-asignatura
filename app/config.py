"""Configuración común: rutas, modelo de lenguaje y modelo de embeddings."""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.embeddings import Embeddings

# Lee las variables del fichero .env (por ejemplo, GROQ_API_KEY)
load_dotenv()

RAIZ = Path(__file__).parent.parent
CARPETA_DOCS = RAIZ / "docs"          # documentos de los que aprende el RAG
CARPETA_CHROMA = RAIZ / "chroma_db"   # donde ChromaDB guarda la base vectorial
COLECCION = "apuntes"                 # nombre de la "tabla" dentro de ChromaDB

# Modelo de embeddings multilingüe que se ejecuta en tu ordenador (gratis, sin clave)
MODELO_EMBEDDINGS = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"


def crear_modelo():
    """Modelo de lenguaje (LLM) del plan gratuito de Groq.

    El manual usaba Llama 3.3, pero Groq lo ha retirado; usamos gpt-oss-120b.
    """
    return init_chat_model(os.getenv("MODELO", "groq:openai/gpt-oss-120b"))


class EmbeddingsLocales(Embeddings):
    """Convierte textos en vectores con la librería fastembed.

    Hereda de la clase Embeddings de LangChain para que ChromaDB sepa usarla.
    """

    def __init__(self):
        from fastembed import TextEmbedding

        # La primera vez descarga el modelo (unos 220 MB) y lo guarda en caché
        self.modelo = TextEmbedding(MODELO_EMBEDDINGS)

    def embed_documents(self, textos: list[str]) -> list[list[float]]:
        return [vector.tolist() for vector in self.modelo.embed(textos)]

    def embed_query(self, texto: str) -> list[float]:
        return self.embed_documents([texto])[0]


def crear_embeddings() -> Embeddings:
    return EmbeddingsLocales()

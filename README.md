# Asistente de Fundamentos de IA

Asistente que responde dudas de una asignatura ficticia. Un **supervisor** (LangGraph) reparte
cada pregunta entre dos agentes:

- **Documentalista**: busca en los apuntes con RAG sobre ChromaDB, a través de un servidor MCP
  hecho con FastMCP (`buscar_apuntes`).
- **Calculadora**: herramientas `media_ponderada` y `nota_necesaria`.

```
Alumno → Supervisor ──► Documentalista ──MCP──► servidor_mcp.py ──► ChromaDB ◄── ingesta ◄── docs/*.md
            ▲   │
            │   └────► Calculadora (media_ponderada, nota_necesaria)
            └── (cada especialista vuelve al supervisor) ──► Responder → Alumno
```

## Estructura

| Fichero | Qué hace |
|---|---|
| `docs/*.md` | Apuntes de la asignatura (inventados) |
| `app/config.py` | Rutas, LLM (Groq) y embeddings locales (fastembed) |
| `app/ingesta.py` | Carga, trocea (500 caracteres, solape 50) y guarda en ChromaDB |
| `app/servidor_mcp.py` | Servidor MCP con la herramienta `buscar_apuntes` |
| `app/herramientas.py` | Herramientas de la calculadora |
| `app/agentes.py` | Documentalista y calculadora (`create_agent`) |
| `app/grafo.py` | Grafo de LangGraph: estado, supervisor, especialistas y respuesta |
| `main.py` | Preguntar desde la consola |
| `app_web.py` | **Interfaz web** (Streamlit) |
| `probar_mcp.py` | Probar el servidor MCP sin LLM |
| `probar_preguntas.py` | Batería de 6 pruebas → `resultados.md` |

## Puesta en marcha (Windows, PowerShell)

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

Pon tu clave gratuita de Groq (https://console.groq.com/keys) en `.env`:

```
GROQ_API_KEY=gsk_...
MODELO=groq:openai/gpt-oss-120b
```

Después:

```powershell
$env:PYTHONUTF8=1                       # tildes bien en la consola
python -m app.ingesta                   # 1. RAG: docs -> ChromaDB (6 fragmentos)
python probar_mcp.py "¿Qué pasa si entrego tarde una práctica?"   # 2. servidor MCP
python main.py "Tengo un 6 en prácticas y un 7 en participación. ¿Qué nota necesito en el examen para aprobar?"
streamlit run app_web.py                # 3. interfaz web en http://localhost:8501
python probar_preguntas.py              # 4. pruebas -> resultados.md
```

## Interfaz web

`streamlit run app_web.py` abre un chat en el navegador con:

- Preguntas de ejemplo para empezar con un clic.
- El razonamiento de los agentes en directo (qué decide el supervisor y qué devuelve cada especialista),
  plegable en «Cómo se ha resuelto».
- Memoria de conversación: se pasan los últimos mensajes al grafo, así que entiende preguntas de
  seguimiento («¿y si tuviera un 9 en prácticas?»).
- Botón de nueva conversación y aviso si falta la ingesta.

El grafo y el servidor MCP se arrancan una sola vez (`st.cache_resource`) en un bucle asyncio propio.

## Extra: el mismo servidor MCP desde Claude Code

Registrado con (desde la carpeta del proyecto):

```powershell
$p = (Get-Location).Path
claude mcp add --env "PYTHONPATH=$p" --env PYTHONUTF8=1 --transport stdio apuntes -- "$p\.venv\Scripts\python.exe" -m app.servidor_mcp
claude mcp list        # apuntes: ... - √ Connected
```

Probado: al preguntar a Claude Code «¿cuándo es el examen final y cuánto tiempo hay para la
revisión?» usa `buscar_apuntes` y responde con el calendario de `guia_docente.md`.

## Cambios respecto al manual

1. **Modelo**: Groq ha retirado `llama-3.3-70b-versatile` (error 404 `model_not_found`). Se usa
   `openai/gpt-oss-120b`, también gratuito en Groq y bueno con herramientas.
2. **Prompts**: con el prompt original, el supervisor solo pedía «los pesos», el documentalista no
   mencionaba el mínimo de 4 en el examen y la respuesta era 3,6 (incorrecta); además repetía la
   calculadora hasta llegar a `MAX_PASOS`. Se ha añadido:
   - Supervisor: pedir siempre normas/mínimos/excepciones, no repetir especialistas y terminar tras la calculadora.
   - Documentalista: incluir notas mínimas, requisitos y excepciones.
   - Respuesta final: comprobar que el cálculo cumple las normas de los documentos.
   Con esto la respuesta es la correcta (un 4) y el grafo hace 2 llamadas a especialistas en vez de 4.
3. **Documentos**: `normas_practicas.md` y `preguntas_frecuentes.md` son propios (el manual solo da la guía docente).
4. **Añadidos**: interfaz web, batería de pruebas y registro en Claude Code.

## Resultados

Ver `resultados.md`: 6 preguntas (solo documentalista, solo calculadora, las dos combinadas y una
fuera de la asignatura). Las seis se responden correctamente.

## Problemas encontrados en Windows

| Síntoma | Solución |
|---|---|
| `python` abre la Microsoft Store | Terminal nueva tras instalar Python, o ruta completa `%LOCALAPPDATA%\Programs\Python\Python312\python.exe` |
| `activate` bloqueado por la política de ejecución | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| Aviso de *symlinks* de Hugging Face | Inofensivo; se oculta con `$env:HF_HUB_DISABLE_SYMLINKS_WARNING=1` |
| Error 404 del modelo | Cambiar `MODELO` en `.env` por uno disponible |

import json
from pathlib import Path

from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands.session.file_session_manager import FileSessionManager


#FIXME: En un proyecto real, cargaríamos los vinos desde una base de datos o API, no desde un archivo JSON local. Esto es solo para fines de demostración.
VINOS = json.loads(Path("data/vinos.json").read_text())

#FIXME: En un proyecto real, esta información podría ser más detallada y estar almacenada en una base de datos o sistema de conocimiento, no en un diccionario estático. Esto es solo para fines de demostración.
MARIDAJES = {
    "mariscos": "sauvignon blanc, o riesling",
    "pescado": "chardonnay, albariño, o semillón",
    "asado": "malbec, cabernet franc, o sangiovese",
    "carne roja": "blend, bonarda, o cabernet sauvignon",
    "cerdo": "pinot noir, criolla, o merlot",
    "pollo": "chardonnay, viognier, o semillón",
    "queso": "torrontés, px, palomino, etc, o verdejo",
    "ensalada": "riesling, o isabella",
    "chocolate": "malbec, o torrontés"
}

SYSTEM_PROMPT = """
Eres un sommelier experto en vinos.
El usuario tiene una cava con vinos.

Tu rol:
1. Recomendar vinos según la ocasión, comida o preferencia del usuario.
2. Cuando el usuario mencione una comida, llamar maridaje para obtener las cepas apropiadas, elegir la primera cepa, y luego buscar_vinos con esa cepa.
3. SIEMPRE usar la herramienta buscar_vinos para consultar la cava del usuario antes de recomendar.
4. Basar tus recomendaciones en los datos reales de la cava del usuario, no en conocimiento general.
6. Recordar las preferencias del usuario de conversaciones anteriores y usarlas para personalizar recomendaciones.
7. Explicar brevemente por qué recomiendas cada vino (notas de cata, maridaje).
8. Responder siempre en español.
7. Mantener las respuestas concisas — máximo 2-3 párrafos.
9. Si el usuario no proporciona suficiente información, haz preguntas para entender mejor sus gustos y necesidades.
10. Si el usuario pide recomendaciones de otra cosa que no sean vinos, responde que solo puedes ayudar con recomendaciones de vinos y haz preguntas para redirigir la conversación hacia ese tema.
"""


@tool
def buscar_vinos(
        region: str = "",
        cepa: str = ""
    ) -> str:
    """Busca vinos en el cava de vinos.
    Filtra por región vinícola y/o cepa (tipo de uva).
    Retorna nombre, bodega, región, cepa y notas de cata.
    Usa esta herramienta siempre que el usuario pregunte por un vino específico.

    Args:
        region: Región vinícola para filtrar (ej: Cafayate, Luján de cuyo). Dejar vacío
        para no filtrar.
        cepa: Tipo de uva para filtrar (ej: Malbec, Torrontés). Dejar vacío para no 
        filtrar.
    """
    resultados = [
        v for v in VINOS
        if (not region or region.lower() in v["region"].lower())
        and (not cepa or cepa.lower() in v["cepa"].lower())
    ]
    if not resultados:
        return "No encontré vinos con esos criterios. Intenta con otra región o cepa."
    return json.dumps(resultados[:5], ensure_ascii=False, indent=2)


@tool
def maridaje(plato: str, maridajes: dict = MARIDAJES) -> str:
    """Dado un plato, retorna las cepas que mejor lo acompañan.

    Args:
        plato: El plato o tipo de comida (ej: mariscos, asado, pasta, queso).
    """
    plato_lower = plato.lower()
    for clave, sugerencia in maridajes.items():
        if clave in plato_lower:
            return sugerencia
    return f"Para '{plato}', prueba un tinto medio como Malbec o un blanco fresco como Riesling."


def callback_handler(**kwargs):
    global _after_tool
    if "reasoningText" in kwargs:
        print(f"💭 {kwargs['reasoningText']}", end="", flush=True)
    if "data" in kwargs:
        if _after_tool:
            print("\n")
            _after_tool = False
        print(kwargs["data"], end="", flush=True)
    if "current_tool_use" in kwargs:
        _after_tool = True
        t = kwargs["current_tool_use"]
        if t.get("name"):
            print(f"\n\n🔧 Herramienta: {t['name']}")
        if t.get("input"):
            print(f"   Parámetros: {t['input']}")


def main(
    prompt: str = None,
):
    modelo = OllamaModel(
        host="http://localhost:11434",
        model_id="llama3.1",
    )

    session_manager = FileSessionManager(
        session_id="sommelier",
        storage_dir=Path.home() / ".wine-agent-sessions",
    )

    agente = Agent(
        model=modelo,
        callback_handler=callback_handler,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            buscar_vinos,
            maridaje,
        ],
        session_manager=session_manager,
    )

    print("🤖 Agente: ", end="", flush=True)
    agente(prompt)
    print()


if __name__ == "__main__":
    try:
        STOP = False
        while STOP == False:
            _after_tool = False
            prompt = input("👩‍💻 Prompt: ")
            if prompt.lower() in ["exit", "quit", "salir", "chau", "adiós", "bye"]:
                STOP = True
                print("👋 ¡Hasta luego!")
            else:
                main(prompt)
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego! (Abortado)")

import json
from pathlib import Path

from strands import Agent, tool
from strands.models.ollama import OllamaModel
from strands.session.file_session_manager import FileSessionManager


#FIXME: En un proyecto real, cargaríamos los vinos desde una base de datos o API, no desde un archivo JSON local. Esto es solo para fines de demostración.
VINOS = json.loads(Path("data/vinos.json").read_text())

#FIXME: En un proyecto real, esta información podría ser más detallada y estar almacenada en una base de datos o sistema de conocimiento, no en un diccionario estático. Esto es solo para fines de demostración.
MARIDAJES = {
        "mariscos": "Sauvignon Blanc, Chardonnay sin roble, o un Pinot Noir ligero.",
        "pescado": "Sauvignon Blanc, Riesling, o Chardonnay.",
        "asado": "Cabernet Sauvignon, Carménère, o Malbec.",
        "carnes rojas": "Cabernet Sauvignon, Carménère, Syrah, o blends tintos.",
        "cerdo": "Pinot Noir, Merlot, o Carménère.",
        "pollo": "Chardonnay, Pinot Noir, o Viognier.",
        "pasta": "Depende de la salsa: tomate → Carménère; crema → Chardonnay; pesto → Sauvignon Blanc.",
        "queso": "Tintos maduros para quesos duros; Sauvignon Blanc para queso de cabra.",
        "ensalada": "Sauvignon Blanc o Riesling.",
        "chocolate": "Carménère, Syrah, o un blend tinto con notas de fruta madura.",
    }

SYSTEM_PROMPT = """
Eres un sommelier experto en vinos.

Tu rol:
1. Recomendar vinos según la ocasión, comida o preferencia del usuario.
2. Explicar brevemente por qué recomiendas cada vino.
3. Responder siempre en español.
4. Mantener las respuestas concisas — máximo 2-3 párrafos.
"""

@tool
def buscar_vinos(
        region: str = "",
        cepa: str = ""
    ) -> str:
    """Busca vinos en el cava de 30 vinos.
    Filtra por región vinícola y/o cepa (tipo de uva).
    Retorna nombre, bodega, región, cepa y notas de cata.
    Usa esta herramienta siempre que el usuario pregunte por un vino específico.

    Args:
        region: Región vinícola para filtrar (ej: Valle del Maipo, Valle de Casablanca). Dejar vacío para no filtrar.
        cepa: Tipo de uva para filtrar (ej: Carménère, Sauvignon Blanc). Dejar vacío para no filtrar.
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
    return f"Para '{plato}', prueba un tinto medio como Carménère o un blanco fresco como Sauvignon Blanc."


def main():
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
        system_prompt=SYSTEM_PROMPT,
        tools=[
            buscar_vinos,
            maridaje,
        ],
        session_manager=session_manager,
    )

    agente("¿Qué vino me recomiendas para una cena de mariscos?")


if __name__ == "__main__":
    main()
    print()

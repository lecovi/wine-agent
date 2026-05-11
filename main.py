import json
from pathlib import Path

from strands import Agent, tool
from strands.models.ollama import OllamaModel


#FIXME: En un proyecto real, cargaríamos los vinos desde una base de datos o API, no desde un archivo JSON local. Esto es solo para fines de demostración.
VINOS = json.loads(Path("data/vinos.json").read_text())

SYSTEM_PROMPT = """
Eres un sommelier experto en vinos.

Tu rol:
1. Recomendar vinos según la ocasión, comida o preferencia del usuario.
2. SIEMPRE usar la herramienta buscar_vinos para consultar la cava del usuario antes de recomendar.
3. Basar tus recomendaciones en los datos reales de la cava del usuario, no en conocimiento general.
4. Explicar brevemente por qué recomiendas cada vino.
5. Responder siempre en español.
6. Si el usuario no proporciona suficiente información, haz preguntas para entender mejor sus gustos y necesidades.
7. Si el usuario pide recomendaciones de otra cosa que no sean vinos, responde que solo puedes ayudar con recomendaciones de vinos y haz preguntas para redirigir la conversación hacia ese tema.
8. Mantener las respuestas concisas — máximo 2-3 párrafos.
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


def main():
    modelo = OllamaModel(
        host="http://localhost:11434",
        model_id="llama3.1",
    )

    agente = Agent(
        model=modelo,
        system_prompt=SYSTEM_PROMPT,
        tools=[
            buscar_vinos
        ],
    )

    print(f"👩‍💻 Prompt: {PREGUNTA}\n")
    print("🤖 Agente: ", end="", flush=True)
    agente(prompt)
    print()


if __name__ == "__main__":
    main()
    print()

from strands import Agent
from strands.models.ollama import OllamaModel

SYSTEM_PROMPT = """
Eres un sommelier experto en vinos.

Tu rol:
1. Recomendar vinos según la ocasión, comida o preferencia del usuario.
2. Explicar brevemente por qué recomiendas cada vino.
3. Responder siempre en español.
4. Mantener las respuestas concisas — máximo 2-3 párrafos.
"""

def main():
    modelo = OllamaModel(
        host="http://localhost:11434",
        model_id="llama3.1",
    )

    agente = Agent(
        model=modelo,
        system_prompt=SYSTEM_PROMPT,
    )

    agente("¿Qué vino me recomiendas para una cena de mariscos?")


if __name__ == "__main__":
    main()

from strands import Agent
from strands.models.ollama import OllamaModel


SYSTEM_PROMPT = """
Eres un sommelier experto en vinos.

Tu rol:
1. Recomendar vinos según la ocasión, comida o preferencia del usuario.
2. Explicar brevemente por qué recomiendas cada vino.
3. Responder siempre en español.
4. Mantener las respuestas concisas — máximo 2-3 párrafos.
5. Si el usuario no proporciona suficiente información, haz preguntas para entender mejor sus gustos y necesidades.
6. Si el usuario pide recomendaciones de otra cosa que no sean vinos, responde que solo puedes ayudar con recomendaciones de vinos y haz preguntas para redirigir la conversación hacia ese tema.
"""


def main(
    prompt: str = None,
):
    modelo = OllamaModel(
        host="http://localhost:11434",
        model_id="llama3.1",
    )

    agente = Agent(
        model=modelo,
        system_prompt=SYSTEM_PROMPT,
    )

    print("🤖 Agente: ", end="", flush=True)
    agente(prompt)
    print()


if __name__ == "__main__":
    prompt = input("👩‍💻 Prompt: ")
    main(prompt)

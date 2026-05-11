from strands import Agent
from strands.models.ollama import OllamaModel

PREGUNTA = "¿Qué vino me recomiendas para una cena de mariscos?"


def main(
    prompt: str = PREGUNTA,
):
    modelo = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
    )

    agente = Agent(model=modelo)

    print(f"👩‍💻 Prompt: {PREGUNTA}\n")
    print("🤖 Agente: ", end="", flush=True)
    agente(prompt)
    print()


if __name__ == "__main__":
    main()

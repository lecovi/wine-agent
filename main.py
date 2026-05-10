from strands import Agent
from strands.models.ollama import OllamaModel

def main():
    modelo = OllamaModel(
    host="http://localhost:11434",
    model_id="llama3.1",
    )

    agente = Agent(model=modelo)

    agente("¿Qué vino me recomiendas para una cena de mariscos?")


if __name__ == "__main__":
    main()

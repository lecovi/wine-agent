import json
from pathlib import Path

from strands import Agent
from strands.models.ollama import OllamaModel
from strands.session.file_session_manager import FileSessionManager

from tools import buscar_vinos, maridaje


#FIXME: En un proyecto real, cargaríamos los vinos desde una base de datos o 
# API, no desde un archivo JSON local. Esto es solo para fines de demostración.
VINOS = json.loads(Path("data/vinos.json").read_text())

#FIXME: En un proyecto real, esta información podría ser más detallada y estar
# almacenada en una base de datos o sistema de conocimiento, no en un 
# diccionario estático. Esto es solo para fines de demostración.
MARIDAJES = json.loads(Path("data/maridajes.json").read_text())

SYSTEM_PROMPT = Path("data/SYSTEM_PROMPT.md").read_text()


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
            if prompt.lower() in ["exit", "quit", "salir"]:
                STOP = True
                print("👋 ¡Hasta luego!")
            else:
                main(prompt)
    except KeyboardInterrupt:
        print("\n👋 ¡Hasta luego! (Abortado)")

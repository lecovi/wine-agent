# Wine Agent — Crecimiento & FLISOL CABA 2026

Companion repo para la charla ["¿Este prompt tiene notas de roble? Creando agentes de IA para catar bebidas"](https://eventol.flisol.org.ar/events/flisol-caba-2026/activity/804/) en el **FLISOL CABA 2026**.

Construye un sommelier de vinos que corre **100% en tu laptop** usando [Strands Agents SDK](https://github.com/strands-agents/sdk-python) y Ollama. Cada branch es un paso del tutorial — progresivo, desde cero.

---

## Pasos del tutorial

Cada branch es un paso incremental. Empezá por el 1 y seguí en orden.

| # | Branch | Concepto |
|---|--------|----------|
| 1 | [`main`](https://github.com/lecovi/wine-agent/tree/main) | El agente más básico — modelo + loop |
| 2 | [`feature/01b-primer-agente`](https://github.com/lecovi/wine-agent/tree/feature/01b-primer-agente) | Agente interactivo — aceptá prompts del usuario |
| 3 | [`feature/02-system-prompt`](https://github.com/lecovi/wine-agent/tree/feature/02-system-prompt) | Personalidad del agente con system prompt |
| 4 | [`feature/03-herramientas`](https://github.com/lecovi/wine-agent/tree/feature/03-herramientas) | Tu primera herramienta (`@tool`) |
| 5 | [`feature/03b-herramientas-callback`](https://github.com/lecovi/wine-agent/tree/feature/03b-herramientas-callback) | Visualizá lo que hace el agente (callback) |
| 6 | [`feature/04-varias-tools`](https://github.com/lecovi/wine-agent/tree/feature/04-varias-tools) | Múltiples herramientas — decisión del modelo |
| 7 | [`feature/05-memoria`](https://github.com/lecovi/wine-agent/tree/feature/05-memoria) | Sesiones para que recuerde entre ejecuciones |
| 8 | [`feature/06-loop`](https://github.com/lecovi/wine-agent/tree/feature/06-loop) | Loop interactivo — conversá con el agente |
| 9 | [`feature/07-mejoras`](https://github.com/lecovi/wine-agent/tree/feature/07-mejoras) | Mejorando el proyecto Python |
| 10 | [`feature/08-modelos`](https://github.com/lecovi/wine-agent/tree/feature/08-modelos) | Cambiando al modelo de la nube |

```
git switch feature/01b-primer-agente
```

---

## Setup

### Requisitos

- Python 3.10+
- [uv](https://docs.astral.sh/uv/getting-started/installation/) para manejar deps y entornos virtuales
- [Ollama](https://ollama.com/download)

### Instalación

```bash
# Descargar modelo (una sola vez)
ollama pull llama3.1

# Instalar dependencias con uv
uv sync
```

### Dataset

```bash
mkdir -p data
curl -o data/vinos.json \
  https://raw.githubusercontent.com/lecovi/wine-agent/refs/heads/feature/03-herramientas/data/vinos.json
```

### Ejecutar

```bash
uv run main.py
```

---

## ¿Qué aprendés?

```
[Paso 1-2] Modelo + Prompt → Agente con personalidad
[Paso 3-4] Agente + @tool → Consulta datos reales, el modelo decide que tool usar
[Paso 5-6] Session Manager + Loop → Memoria + interfaz interactiva 
[Paso 7-8] Mejoras + Modelos → Código más limpio y cambio de modelo sin drama
[Bonus] Explorá el repo que podés ver cómo hacer lo mismo con ADK (Google)
```

---

## Recursos

- [Strands Agents SDK](https://github.com/strands-agents/sdk-python)
  - [Strands Agents Docs](https://strandsagents.com/)
- [Ollama](https://ollama.com/download)
- [Repo original — Nerdear.la Chile 2026](https://github.com/anacunha/strands-agents-wine-agent-sample)
  - [Video del workshop](https://www.youtube.com/watch?v=jhRdbiwcDGs)
- [ADK](https://adk.dev/get-started/python/)

---

## Agradecimientos

Esta presentación está basada en el workshop ["Construye un Sommelier de IA con Strands Agents y Ollama"](https://github.com/anacunha/strands-agents-wine-agent-sample) presentado en **Nerdear.la Chile 2026** por [anacunha](https://github.com/anacunha) — equipo de AWS.

---

## License

MIT
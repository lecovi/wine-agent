from strands import Agent, tool


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
def maridaje(
    plato: str, 
    maridajes: dict,
) -> str:
    """Dado un plato, retorna las cepas que mejor lo acompañan.

    Args:
        plato: El plato o tipo de comida (ej: mariscos, asado, pasta, queso).
    """
    plato_lower = plato.lower()
    for clave, sugerencia in maridajes.items():
        if clave in plato_lower:
            return sugerencia
    return f"Para '{plato}', prueba un tinto medio como Malbec o un blanco fresco como Riesling."
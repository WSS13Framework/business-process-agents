"""
Lead scoring — turns conversation signals into hot / warm / cold.
Pontuação de lead — transforma sinais em quente / morno / frio.
"""


def classificar_lead(pontos: int, regua: dict) -> str:
    """
    A régua vem da config do cliente (tenant), não fica fixa no código.
    The thresholds come from the client's config, not hardcoded.
    """
    if pontos >= regua["quente"]:
        return "quente"
    elif pontos >= regua["morno"]:
        return "morno"
    else:
        return "frio"
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


def pontuar_enriquecimento(
    resultados: list[dict], tipo_lead: str, pesos: dict
) -> tuple[int, list[str]]:
    """
    Transforma o enriquecimento em duas coisas: pontos e observações.
    Turns enrichment into two things: points and observations.

    Pontos alimentam a régua. Observações alimentam a conversa — inclusive as
    falhas, que viram assunto ("teu site não respondeu agora").
    Só status 'ok' pontua; 'vazio' e 'falha' não valem ponto, mas falam.

    Os pesos vêm por parâmetro (config do tenant), nunca fixos no código.
    """
    tabela = pesos.get(tipo_lead, {})

    pontos = 0
    observacoes = []

    for resultado in resultados:
        fonte = resultado.get("fonte", "desconhecida")
        status = resultado.get("status")
        detalhe = resultado.get("detalhe")

        if status == "ok":
            pontos += tabela.get(fonte, 0)
            observacoes.append(f"{fonte}: {_resumir(resultado.get('dados') or {})}")

        elif status == "vazio":
            observacoes.append(f"{fonte}: busquei e não achei ({detalhe})")

        elif status == "falha":
            observacoes.append(f"{fonte}: não consegui consultar ({detalhe})")

        else:
            # O contrato de saída não é imposto por código (ver GUIA-DE-ESTUDO).
            # Se chegar formato torto, aparece aqui em vez de sumir calado.
            observacoes.append(f"{fonte}: resultado em formato inesperado ({status!r})")

    return pontos, observacoes


def _resumir(dados: dict) -> str:
    """Vira uma frase curta pro agente usar na conversa."""
    if dados.get("titulo"):
        return str(dados["titulo"])
    if dados.get("descricao"):
        return str(dados["descricao"])
    if dados:
        return "achei " + ", ".join(sorted(dados))
    return "achei, mas sem detalhe legível"
"""
Signal extraction — turns the lead's own words into scoreable signals.
Extração de sinais — transforma o que o lead escreveu em sinais pontuáveis.

Isto fecha o buraco central: até aqui o 'message' chegava no agente e morria lá.
This closes the central gap: until now 'message' reached the agent and died there.
"""

import json
from typing import Any

import anthropic

from core.base_enricher import BaseEnricher

MODELO = "claude-opus-5"

# Teto de saída. O modelo pensa por padrão no Opus 5, e o pensamento conta
# aqui dentro junto com a resposta — apertado demais, a resposta trunca.
MAX_TOKENS = 8192

INSTRUCAO = """Você lê a mensagem de um lead e extrai sinais de intenção de compra.

Extraia só o que a mensagem sustenta. Não deduza, não invente, não seja generoso:
um sinal falso vale menos que sinal nenhum, porque manda o vendedor pra ligação errada.

- orcamento: a pessoa citou valor, verba, faixa de preço ou capacidade de pagar.
- urgencia: a pessoa citou prazo, pressa ou data.
- autoridade: a pessoa indicou que decide ou representa quem decide.
- descadastro: a pessoa pediu pra sair, parar de receber ou não tem interesse.
- resumo: uma frase curta, em português, do que a pessoa quer — pro vendedor ler."""

ESQUEMA_SINAIS: dict[str, Any] = {
    "type": "object",
    "properties": {
        "orcamento": {"type": "boolean"},
        "urgencia": {"type": "boolean"},
        "autoridade": {"type": "boolean"},
        "descadastro": {"type": "boolean"},
        "resumo": {"type": "string"},
    },
    "required": ["orcamento", "urgencia", "autoridade", "descadastro", "resumo"],
    "additionalProperties": False,
}


class MensagemEnricher(BaseEnricher):
    """
    A mensagem do lead tratada como fonte, igual site ou YouTube.
    The lead's message treated as a source, same as site or YouTube.

    Herda de BaseEnricher de propósito: assim o enriquecer() já dá isolamento
    de falha de graça — LLM fora do ar não derruba o atendimento do lead.
    """

    nome = "mensagem"

    def __init__(self, cliente: Any = None):
        # Costura para teste: em produção fica None e cria o cliente real.
        # Test seam: None in production, so a real client is created.
        self._cliente = cliente

    def buscar(self, pista: str) -> dict:
        """A 'pista' aqui é a própria mensagem do lead."""
        if not pista.strip():
            return self._vazio("mensagem vazia")

        cliente = self._cliente or anthropic.Anthropic()

        resposta = cliente.messages.create(
            model=MODELO,
            max_tokens=MAX_TOKENS,
            system=INSTRUCAO,
            messages=[{"role": "user", "content": pista}],
            # output_config ainda não é parâmetro tipado nesta versão do SDK;
            # extra_body entrega igual. Vira parâmetro direto quando subirmos.
            extra_body={
                "output_config": {
                    "effort": "low",
                    "format": {"type": "json_schema", "schema": ESQUEMA_SINAIS},
                }
            },
        )

        # O modelo pode recusar por segurança: vem HTTP 200 com content vazio.
        # Ler content[0] direto quebraria aqui.
        if resposta.stop_reason == "refusal":
            return self._vazio("o modelo recusou analisar esta mensagem")

        # A resposta pode trazer blocos que não são texto (pensamento, tools).
        # Pegar content[0] às cegas é como ler a primeira linha e chamar de resposta.
        texto = ""
        for bloco in resposta.content:
            if getattr(bloco, "type", "") == "text":
                texto = str(getattr(bloco, "text", ""))
                break

        if not texto:
            return self._vazio("o modelo não devolveu texto")

        return self._ok(json.loads(texto))


def pontuar_sinais(resultado: dict, pesos: dict) -> tuple[int, list[str]]:
    """
    Transforma os sinais em pontos e observações, igual pontuar_enriquecimento.
    Turns signals into points and observations, like pontuar_enriquecimento.

    Os pesos vêm por parâmetro (config do tenant), nunca fixos no código.

    Devolve a soma CRUA, que pode ser negativa. É de propósito: o peso negativo
    do descadastro só cancela os pontos do enriquecimento se chegar negativo até
    o total. Zerar aqui deixaria "me tira do mailing" valendo os pontos do site.
    Returns the RAW sum, possibly negative — clamping happens at the total.
    """
    status = resultado.get("status")
    detalhe = resultado.get("detalhe")

    if status == "vazio":
        return 0, [f"mensagem: sem sinal de compra ({detalhe})"]

    if status == "falha":
        return 0, [f"mensagem: não consegui analisar ({detalhe})"]

    if status != "ok":
        return 0, [f"mensagem: resultado em formato inesperado ({status!r})"]

    sinais = resultado.get("dados") or {}

    pontos = 0
    observacoes = []

    if sinais.get("resumo"):
        observacoes.append(f"mensagem: {sinais['resumo']}")

    for nome, peso in pesos.items():
        if sinais.get(nome) is True:
            pontos += peso
            observacoes.append(f"sinal: {nome} ({peso:+d})")

    return pontos, observacoes

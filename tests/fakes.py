"""
Dublês da Claude API — para os testes rodarem offline, de graça e sempre igual.
Claude API stand-ins — so tests run offline, free, and identical every time.
"""

import json


class BlocoTexto:
    type = "text"

    def __init__(self, text: str):
        self.text = text


class RespostaFalsa:
    def __init__(self, sinais: dict | None = None, stop_reason: str = "end_turn"):
        self.stop_reason = stop_reason
        self.content = [BlocoTexto(json.dumps(sinais))] if sinais is not None else []


class ClienteFalso:
    """Imita o anthropic.Anthropic() só no pedaço que usamos."""

    def __init__(
        self,
        resposta: RespostaFalsa | None = None,
        estoura: Exception | None = None,
    ):
        self._resposta = resposta
        self._estoura = estoura
        self.chamadas: list[dict] = []
        self.messages = self

    def create(self, **kwargs: object) -> RespostaFalsa | None:
        self.chamadas.append(kwargs)
        if self._estoura is not None:
            raise self._estoura
        return self._resposta


# Sinais de exemplo, como a API os devolveria.
COMPRADOR = {
    "orcamento": True,
    "urgencia": True,
    "autoridade": False,
    "descadastro": False,
    "resumo": "quer fechar identidade visual esta semana",
}
SAINDO = {
    "orcamento": False,
    "urgencia": False,
    "autoridade": False,
    "descadastro": True,
    "resumo": "pediu para sair da lista",
}
NEUTRO = {
    "orcamento": False,
    "urgencia": False,
    "autoridade": False,
    "descadastro": False,
    "resumo": "só perguntou o que a empresa faz",
}


def cliente_com(sinais: dict | None = None, estoura: Exception | None = None) -> ClienteFalso:
    return ClienteFalso(RespostaFalsa(sinais), estoura=estoura)

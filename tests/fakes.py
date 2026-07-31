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


class MensagemOpenAIFalsa:
    def __init__(
        self,
        sinais: dict | None = None,
        refusal: str | None = None,
    ):
        self.content = json.dumps(sinais) if sinais is not None else None
        self.refusal = refusal


class EscolhaFalsa:
    def __init__(self, mensagem: MensagemOpenAIFalsa, finish_reason: str = "stop"):
        self.message = mensagem
        self.finish_reason = finish_reason


class RespostaOpenAIFalsa:
    def __init__(
        self,
        sinais: dict | None = None,
        refusal: str | None = None,
        finish_reason: str = "stop",
    ):
        self.choices = [EscolhaFalsa(MensagemOpenAIFalsa(sinais, refusal), finish_reason)]


class ClienteOpenAIFalso:
    """Imita o openai.OpenAI() só no pedaço que usamos: chat.completions.create."""

    def __init__(
        self,
        resposta: RespostaOpenAIFalsa | None = None,
        estoura: Exception | None = None,
    ):
        self._resposta = resposta
        self._estoura = estoura
        self.chamadas: list[dict] = []
        self.chat = self
        self.completions = self

    def create(self, **kwargs: object) -> RespostaOpenAIFalsa | None:
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
    "agente_indicado": "comercial",
    "resumo": "quer fechar identidade visual esta semana",
}
SAINDO = {
    "orcamento": False,
    "urgencia": False,
    "autoridade": False,
    "descadastro": True,
    "agente_indicado": "indefinido",
    "resumo": "pediu para sair da lista",
}
NEUTRO = {
    "orcamento": False,
    "urgencia": False,
    "autoridade": False,
    "descadastro": False,
    "agente_indicado": "indefinido",
    "resumo": "só perguntou o que a empresa faz",
}


def cliente_com(sinais: dict | None = None, estoura: Exception | None = None) -> ClienteFalso:
    return ClienteFalso(RespostaFalsa(sinais), estoura=estoura)

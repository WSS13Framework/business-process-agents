"""
Prova o cliente da Evolution sem instância e sem rede.
Proves the Evolution client with no instance and no network.

ATENÇÃO: estes testes provam que o código trata CORRETAMENTE o contrato
DOCUMENTADO. Eles não provam que o contrato documentado é o real — não houve
acesso a instância. Quando houver credencial, `Evolution.bruto()` mostra o
formato de verdade, e é ele que manda.
These tests prove handling of the DOCUMENTED contract, not that it is the real one.
"""

import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import httpx
import pytest

from core.evolution import Evolution, _normalizar, _registros

RECEBIDA = {
    "key": {"remoteJid": "5511999990000@s.whatsapp.net", "fromMe": False, "id": "MSG1"},
    "pushName": "Marcos",
    "message": {"conversation": "tenho uma clinica em Botafogo"},
    "messageTimestamp": 1780000000,
}
ENVIADA = {
    "key": {"remoteJid": "5511999990000@s.whatsapp.net", "fromMe": True, "id": "MSG2"},
    "message": {"conversation": "oi, tudo bem?"},
}
AUDIO = {
    "key": {"remoteJid": "5511888880000@s.whatsapp.net", "fromMe": False, "id": "MSG3"},
    "message": {"audioMessage": {"url": "..."}},
}


def montar(carga: object, status: int = 200) -> Evolution:
    def responder(_: httpx.Request) -> httpx.Response:
        return httpx.Response(status, text=json.dumps(carga))

    return Evolution(
        url="https://evo.exemplo",
        chave="k",
        instancia="i",
        transport=httpx.MockTransport(responder),
    )


# ---- _registros: as duas formas de envelope ----
def test_aceita_lista_nua():
    assert _registros([RECEBIDA]) == [RECEBIDA]


def test_aceita_envelope_aninhado():
    """As fontes divergem entre lista nua e messages.records — aceitar as duas."""
    assert _registros({"messages": {"records": [RECEBIDA]}}) == [RECEBIDA]
    assert _registros({"messages": [RECEBIDA]}) == [RECEBIDA]
    assert _registros({"records": [RECEBIDA]}) == [RECEBIDA]


def test_formato_desconhecido_devolve_vazio_em_vez_de_quebrar():
    """Envelope inesperado não pode derrubar o polling — devolve nada e segue."""
    assert _registros({"algo": "inesperado"}) == []
    assert _registros("texto") == []
    assert _registros(None) == []


# ---- _normalizar ----
def test_mensagem_recebida_vira_o_minimo_que_o_pipeline_usa():
    n = _normalizar(RECEBIDA)

    assert n == {
        "id": "MSG1",
        "telefone": "5511999990000",
        "remote_jid": "5511999990000@s.whatsapp.net",
        "texto": "tenho uma clinica em Botafogo",
        "nome": "Marcos",
        "quando": 1780000000,
    }


def test_telefone_sai_sem_o_sufixo_do_jid():
    """O telefone vira lead_id; '@s.whatsapp.net' não faz parte da identidade."""
    assert _normalizar(RECEBIDA)["telefone"] == "5511999990000"


def test_mensagem_que_nos_enviamos_e_ignorada():
    """fromMe é resposta nossa, não mensagem de lead."""
    assert _normalizar(ENVIADA) is None


def test_audio_e_ignorado():
    """O pipeline só lê texto. Descartar é honesto; inventar transcrição não."""
    assert _normalizar(AUDIO) is None


def test_registro_torto_nao_quebra():
    assert _normalizar({}) is None
    assert _normalizar({"key": "nao e dict"}) is None
    assert _normalizar({"key": {"fromMe": False}, "message": {"conversation": "  "}}) is None


# ---- o cliente monta o pedido certo ----
def test_manda_apikey_e_o_caminho_da_instancia():
    capturado = {}

    def responder(req: httpx.Request) -> httpx.Response:
        capturado["url"] = str(req.url)
        capturado["apikey"] = req.headers.get("apikey")
        capturado["corpo"] = json.loads(req.content)
        return httpx.Response(200, text="[]")

    Evolution(
        url="https://evo.exemplo",
        chave="segredo",
        instancia="forja",
        transport=httpx.MockTransport(responder),
    ).mensagens()

    assert capturado["url"] == "https://evo.exemplo/chat/findMessages/forja"
    assert capturado["apikey"] == "segredo"
    assert capturado["corpo"] == {"where": {}}


def test_filtro_por_conversa_entra_no_corpo():
    capturado = {}

    def responder(req: httpx.Request) -> httpx.Response:
        capturado["corpo"] = json.loads(req.content)
        return httpx.Response(200, text="[]")

    Evolution(
        url="https://e", chave="k", instancia="i", transport=httpx.MockTransport(responder)
    ).mensagens("5511999990000@s.whatsapp.net")

    assert capturado["corpo"] == {
        "where": {"key": {"remoteJid": "5511999990000@s.whatsapp.net"}}
    }


def test_filtra_enviadas_e_audio_numa_carga_mista():
    recebidas = montar([RECEBIDA, ENVIADA, AUDIO]).mensagens()

    assert len(recebidas) == 1
    assert recebidas[0]["id"] == "MSG1"


def test_bruto_devolve_sem_interpretar():
    """Existe para descobrir o formato real; não pode normalizar nada."""
    carga = {"formato": "que eu nao previ", "messages": {"records": []}}

    assert montar(carga).bruto() == carga


def test_erro_http_sobe():
    """Quem trata é o chamador, igual aos enrichers."""
    with pytest.raises(httpx.HTTPStatusError):
        montar([], status=500).mensagens()


def test_config_ausente_falha_antes_de_chamar_a_rede():
    with pytest.raises(ValueError, match="EVOLUTION_URL"):
        Evolution(url="", chave="", instancia="").mensagens()

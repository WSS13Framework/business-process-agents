"""
Prova os quatro caminhos do SiteEnricher sem tocar na rede.
Proves the four SiteEnricher paths without touching the network.

httpx.MockTransport intercepta a requisição e devolve uma resposta de mentira,
então o teste roda offline, sempre igual, e sem incomodar servidor de ninguém.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

import httpx

from core.base_enricher import enriquecer
from enrichers.site_enricher import SiteEnricher

PAGINA_COMPLETA = """
<html><head>
  <title>Forja Criativa</title>
  <meta name="description" content="Estúdio de design e marca">
</head><body>oi</body></html>
"""

PAGINA_PELADA = "<html><head></head><body>só texto solto</body></html>"

ROBOTS_LIBERADO = "User-agent: *\nDisallow: /admin\n"
ROBOTS_PROIBIDO = "User-agent: *\nDisallow: /\n"


def montar_fonte(robots: str, pagina: str = "", estoura: Exception | None = None):
    """Monta um SiteEnricher que fala com um servidor falso."""

    def responder(requisicao: httpx.Request) -> httpx.Response:
        if requisicao.url.path == "/robots.txt":
            return httpx.Response(200, text=robots)
        if estoura is not None:
            raise estoura
        return httpx.Response(200, text=pagina)

    return SiteEnricher(transport=httpx.MockTransport(responder))


# ---- 1. ok: achou título e description ----
def test_ok_com_titulo_e_description():
    resultado = montar_fonte(ROBOTS_LIBERADO, PAGINA_COMPLETA).buscar("empresa.com")

    assert resultado["status"] == "ok"
    assert resultado["fonte"] == "site"
    assert resultado["detalhe"] is None
    assert resultado["dados"]["titulo"] == "Forja Criativa"
    assert resultado["dados"]["descricao"] == "Estúdio de design e marca"


# ---- 2. vazio: página carregou pelada ----
def test_vazio_quando_pagina_nao_tem_nada():
    resultado = montar_fonte(ROBOTS_LIBERADO, PAGINA_PELADA).buscar("empresa.com")

    assert resultado["status"] == "vazio"
    assert resultado["dados"] == {}
    assert "sem título nem description" in resultado["detalhe"]


# ---- 3. vazio: robots.txt proibindo ----
def test_vazio_quando_robots_proibe():
    resultado = montar_fonte(ROBOTS_PROIBIDO, PAGINA_COMPLETA).buscar("empresa.com")

    assert resultado["status"] == "vazio"
    assert resultado["dados"] == {}, "proibido é proibido: não lê nem guarda nada"
    assert "robots.txt" in resultado["detalhe"]


# ---- 4. falha: timeout subindo até o enriquecer() ----
def test_timeout_vira_falha_no_enriquecer():
    fonte = montar_fonte(
        ROBOTS_LIBERADO, estoura=httpx.ConnectTimeout("timeout após 10s")
    )

    resultados = enriquecer("empresa.com", [fonte])

    assert len(resultados) == 1, "o pipeline devolve resultado mesmo quando a fonte quebra"
    assert resultados[0]["status"] == "falha"
    assert resultados[0]["fonte"] == "site"
    assert resultados[0]["dados"] == {}
    assert resultados[0]["detalhe"] == "ConnectTimeout: timeout após 10s"


def test_a_excecao_sobe_se_ninguem_tratar():
    """O SiteEnricher NÃO engole exceção — quem trata é o enriquecer()."""
    fonte = montar_fonte(ROBOTS_LIBERADO, estoura=httpx.ConnectTimeout("caiu"))

    try:
        fonte.buscar("empresa.com")
    except httpx.ConnectTimeout:
        return
    raise AssertionError("a exceção deveria ter subido")

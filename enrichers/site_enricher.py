"""
Site enricher — reads a company's homepage: title and meta description.
Enriquecedor de site — lê a página inicial da empresa: título e meta description.

Fonte aberta: só o que qualquer visitante veria, e só se o robots.txt deixar.
Open source of data: only what any visitor would see, and only if robots.txt allows.
"""

from urllib.parse import urlparse
from urllib.robotparser import RobotFileParser

import httpx
from bs4 import BeautifulSoup

from core.base_enricher import BaseEnricher

TIMEOUT = 10.0

# O bot se identifica: quem for olhar o log do servidor sabe quem passou e onde reclamar.
USER_AGENT = (
    "BusinessProcessAgentsBot/0.1 "
    "(+https://github.com/WSS13Framework/business-process-agents; enriquecimento de lead)"
)


class SiteEnricher(BaseEnricher):
    """Recebe um domínio como pista e lê a home. / Takes a domain, reads the homepage."""

    nome = "site"

    def __init__(self, transport: httpx.BaseTransport | None = None):
        # Costura para teste: em produção fica None e o httpx usa a rede real.
        # Test seam: None in production, so httpx uses the real network.
        self._transport = transport

    def buscar(self, pista: str) -> dict:
        url = self._normalizar(pista)

        with httpx.Client(
            timeout=TIMEOUT,
            headers={"User-Agent": USER_AGENT},
            follow_redirects=True,
            transport=self._transport,
        ) as cliente:
            if not self._permitido(cliente, url):
                return self._vazio("robots.txt não permite ler esta página")

            resposta = cliente.get(url)
            resposta.raise_for_status()

            html = resposta.text
            url_final = str(resposta.url)  # pode ter mudado por redirect

        titulo, descricao = self._extrair(html)

        if not titulo and not descricao:
            return self._vazio("página carregou, mas sem título nem description")

        dados = {"url": url_final}
        if titulo:
            dados["titulo"] = titulo
        if descricao:
            dados["descricao"] = descricao

        return self._ok(dados)

    @staticmethod
    def _normalizar(pista: str) -> str:
        """'empresa.com' -> 'https://empresa.com'. Aceita URL já completa."""
        pista = pista.strip()
        partes = urlparse(pista)

        if not partes.scheme:
            pista = f"https://{pista}"
            partes = urlparse(pista)

        if not partes.netloc:
            raise ValueError(f"pista não parece um domínio: {pista!r}")

        return pista

    @staticmethod
    def _permitido(cliente: httpx.Client, url: str) -> bool:
        """
        Consulta o robots.txt do domínio antes de ler qualquer coisa.
        Checks the domain's robots.txt before reading anything.
        """
        partes = urlparse(url)
        resposta = cliente.get(f"{partes.scheme}://{partes.netloc}/robots.txt")

        # RFC 9309: robots.txt indisponível (5xx) = tratar como proibido.
        if resposta.status_code >= 500:
            return False

        # Sem robots.txt (4xx) = nada proibido.
        if resposta.status_code >= 400:
            return True

        leitor = RobotFileParser()
        leitor.parse(resposta.text.splitlines())
        return leitor.can_fetch(USER_AGENT, url)

    @staticmethod
    def _extrair(html: str) -> tuple[str, str]:
        """Tira o <title> e a <meta name="description"> da página."""
        sopa = BeautifulSoup(html, "html.parser")

        titulo = sopa.title.get_text(strip=True) if sopa.title else ""

        descricao = ""
        for meta in sopa.find_all("meta"):
            if _texto(meta.get("name")).lower() == "description":
                descricao = _texto(meta.get("content"))
                break

        return titulo, descricao


def _texto(valor: object) -> str:
    """
    Atributo do bs4 pode vir string OU lista (atributos multi-valor).
    A bs4 attribute can be a string OR a list (multi-valued attributes).
    """
    if isinstance(valor, str):
        return valor.strip()
    if isinstance(valor, list):
        return " ".join(str(item) for item in valor).strip()
    return ""

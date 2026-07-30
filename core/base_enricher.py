"""
Base Enricher — the shared contract for every enrichment source.
Enriquecedor Base — o contrato compartilhado de toda fonte de enriquecimento.

Cada fonte busca sozinha e falha sozinha. O orquestrador nunca para, porque
o lead está esperando resposta.
Each source searches alone and fails alone. The orchestrator never stops,
because the lead is waiting for an answer.
"""

from abc import ABC, abstractmethod


class BaseEnricher(ABC):
    """Contrato comum: toda fonte recebe uma pista e devolve um resultado com procedência."""

    # Sobrescrito por cada fonte concreta ("site", "youtube", "github"...).
    nome: str = "desconhecida"

    @abstractmethod
    def buscar(self, pista: str) -> dict:
        """
        Contrato: toda fonte DEVE implementar 'buscar'.
        Recebe uma pista (domínio, nome, handle) e devolve um resultado padronizado.
        Contract: every source MUST implement 'buscar'.
        """
        ...

    def _ok(self, dados: dict) -> dict:
        """Achou. / Found something."""
        return {
            "fonte": self.nome,
            "status": "ok",
            "dados": dados,
            "detalhe": None,
        }

    def _vazio(self, motivo: str) -> dict:
        """Buscou e não tinha nada — não é falha. / Searched, found nothing — not a failure."""
        return {
            "fonte": self.nome,
            "status": "vazio",
            "dados": {},
            "detalhe": motivo,
        }


def enriquecer(pista: str, fontes: list[BaseEnricher]) -> list[dict]:
    """
    Percorre as fontes e devolve um resultado por fonte, com procedência.
    Uma fonte que quebra vira status 'falha' e não derruba as outras.

    Walks the sources and returns one result per source, carrying provenance.
    A source that breaks becomes status 'falha' and doesn't take down the rest.
    """
    resultados = []

    for fonte in fontes:
        try:
            resultados.append(fonte.buscar(pista))
        except Exception as erro:
            resultados.append(
                {
                    "fonte": fonte.nome,
                    "status": "falha",
                    "dados": {},
                    "detalhe": f"{type(erro).__name__}: {erro}",
                }
            )

    return resultados

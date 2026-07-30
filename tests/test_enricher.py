"""
Prova o isolamento de falha: uma fonte quebra, a outra entrega.
Proves failure isolation: one source breaks, the other still delivers.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from core.base_enricher import BaseEnricher, enriquecer


class FonteFake(BaseEnricher):
    """Fonte falsa que se comporta. / Fake source that behaves."""

    nome = "fake"

    def buscar(self, pista: str) -> dict:
        return self._ok({"titulo": "Empresa Exemplo"})


class FonteSemNada(BaseEnricher):
    """Fonte falsa que busca e não acha — resposta legítima, não é falha."""

    nome = "sem_nada"

    def buscar(self, pista: str) -> dict:
        return self._vazio("página sem título nem description")


class FonteQuebrada(BaseEnricher):
    """Fonte falsa que estoura — simula site fora do ar."""

    nome = "quebrada"

    def buscar(self, pista: str) -> dict:
        raise ConnectionError("site fora do ar")


FONTES = [FonteFake(), FonteSemNada(), FonteQuebrada()]


def test_uma_fonte_quebrada_nao_derruba_as_outras():
    resultados = enriquecer("empresa.com", FONTES)

    assert len(resultados) == 3, "toda fonte devolve um resultado, mesmo quebrando"
    assert [r["status"] for r in resultados] == ["ok", "vazio", "falha"]


def test_resultado_carrega_procedencia():
    for r in enriquecer("empresa.com", FONTES):
        assert set(r) == {"fonte", "status", "dados", "detalhe"}
        assert r["fonte"] in {"fake", "sem_nada", "quebrada"}


def test_ok_traz_os_dados():
    ok = enriquecer("empresa.com", FONTES)[0]

    assert ok["status"] == "ok"
    assert ok["dados"] == {"titulo": "Empresa Exemplo"}
    assert ok["detalhe"] is None


def test_vazio_e_diferente_de_falha():
    vazio, falha = enriquecer("empresa.com", FONTES)[1:]

    # Os dois vêm sem dados — só o status distingue "não tem" de "não consegui".
    assert vazio["dados"] == falha["dados"] == {}
    assert vazio["status"] == "vazio"
    assert vazio["detalhe"] == "página sem título nem description"


def test_falha_guarda_o_tipo_e_a_mensagem():
    falha = enriquecer("empresa.com", FONTES)[2]

    assert falha["status"] == "falha"
    assert falha["dados"] == {}
    assert falha["detalhe"] == "ConnectionError: site fora do ar"


if __name__ == "__main__":
    for resultado in enriquecer("empresa.com", FONTES):
        print(resultado)

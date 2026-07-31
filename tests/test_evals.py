"""
Testa a infraestrutura de eval, não a instrução.
Tests the eval infrastructure, not the instruction.

A suíte de casos precisa de rede e chave — roda com `python3 -m evals.rodar`.
Estes testes aqui rodam na CI e garantem que o mecanismo que decide "isto é
uma regressão" está correto. Um comparador quebrado deixaria passar regressão
de verdade e ninguém veria.
"""

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.lead_triage.signals import AGENTES
from evals.casos import CASOS, CATEGORIAS
from evals.comparar import MAX_PALAVRAS_RESUMO, checar_resumo, comparar, resumir

RESUMO_BOM = "Quero vídeo institucional para minha clínica até outubro."


# ---- o conjunto de casos está sadio ----
def test_tem_pelo_menos_50_casos():
    assert len(CASOS) >= 50


def test_ids_sao_unicos():
    ids = [c["id"] for c in CASOS]
    assert len(ids) == len(set(ids))


def test_toda_categoria_declarada_tem_caso():
    usadas = {c["categoria"] for c in CASOS}
    assert usadas == set(CATEGORIAS), f"divergência: {usadas ^ set(CATEGORIAS)}"


def test_todo_caso_esta_bem_formado():
    booleanos = {"orcamento", "urgencia", "autoridade", "descadastro"}

    for c in CASOS:
        assert c["mensagem"].strip(), f"{c['id']}: mensagem vazia"
        assert c["esperado"], f"{c['id']}: gabarito vazio não testa nada"
        for campo, valor in c["esperado"].items():
            if campo in booleanos:
                assert isinstance(valor, bool), f"{c['id']}: {campo} deveria ser bool"
            elif campo == "agente_indicado":
                assert valor in AGENTES, f"{c['id']}: agente {valor!r} fora do catálogo"
            else:
                raise AssertionError(f"{c['id']}: campo {campo!r} não existe")


def test_autoridade_tem_os_dois_lados():
    """Um gabarito só com 'false' seria satisfeito por um modelo que nunca acerta."""
    valores = [c["esperado"]["autoridade"] for c in CASOS if "autoridade" in c["esperado"]]

    assert valores.count(True) >= 15, "poucos casos positivos de autoridade"
    assert valores.count(False) >= 15, "poucos casos negativos de autoridade"


# ---- checar_resumo ----
def test_resumo_bom_passa():
    assert checar_resumo(RESUMO_BOM) == []


def test_resumo_longo_demais_reprova():
    longo = " ".join(["quero"] * (MAX_PALAVRAS_RESUMO + 1))
    problemas = checar_resumo(longo)

    assert any("máximo" in p for p in problemas)


def test_resumo_em_terceira_pessoa_reprova():
    problemas = checar_resumo("A pessoa quer um vídeo institucional para a clínica.")

    assert "começa em terceira pessoa" in problemas


def test_resumo_sem_marca_de_primeira_pessoa_reprova():
    problemas = checar_resumo("Vídeo institucional para clínica em outubro.")

    assert "sem marca de primeira pessoa" in problemas


def test_resumo_vazio_reprova():
    assert checar_resumo("") == ["resumo vazio"]
    assert checar_resumo("   ") == ["resumo vazio"]


# ---- comparar ----
def test_sem_divergencia_quando_bate():
    caso = {"esperado": {"autoridade": True}}
    devolvido = {"autoridade": True, "resumo": RESUMO_BOM}

    assert comparar(caso, devolvido) == []


def test_aponta_o_campo_divergente():
    caso = {"esperado": {"autoridade": True}}
    devolvido = {"autoridade": False, "resumo": RESUMO_BOM}

    d = comparar(caso, devolvido)

    assert d == [{"campo": "autoridade", "esperado": True, "devolvido": False}]


def test_so_cobra_o_que_o_gabarito_declarou():
    """Campo fora do gabarito não é divergência — ninguém opina sobre ele."""
    caso = {"esperado": {"autoridade": True}}
    devolvido = {"autoridade": True, "urgencia": True, "resumo": RESUMO_BOM}

    assert comparar(caso, devolvido) == []


def test_resumo_ruim_conta_como_divergencia():
    caso = {"esperado": {"autoridade": True}}
    devolvido = {"autoridade": True, "resumo": "A pessoa quer um vídeo."}

    d = comparar(caso, devolvido)

    assert any(x["campo"] == "resumo" for x in d)


def test_campo_ausente_na_resposta_diverge():
    caso = {"esperado": {"autoridade": True}}
    devolvido = {"resumo": RESUMO_BOM}

    d = comparar(caso, devolvido)

    assert d[0]["devolvido"] is None


# ---- resumir ----
def test_resumo_da_rodada_conta_certo():
    resultados = [
        {"categoria": "gerente", "divergencias": [], "erro": None},
        {
            "categoria": "gerente",
            "divergencias": [{"campo": "autoridade", "esperado": True, "devolvido": False}],
            "erro": None,
        },
        {"categoria": "spam", "divergencias": [], "erro": "falha: caiu"},
    ]

    s = resumir(resultados)

    assert s["total"] == 3
    assert s["passaram"] == 1
    assert s["falharam"] == 2
    assert s["por_campo"] == {"autoridade": 1}
    assert s["por_categoria"]["gerente"] == 1

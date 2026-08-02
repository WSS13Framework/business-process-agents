"""
Preparo compartilhado dos testes.
Shared test setup.

O que mora aqui: a fixture `memoria`, que roda o MESMO teste de contrato contra
as três implementações de MemoriaLead. Antes, um `for` dentro do teste
percorria duas — e um `for` esconde ausência: se o Postgres não estivesse na
lista, nada na saída do pytest diria isso. Como fixture parametrizada, cada
implementação vira uma linha própria, e a que não roda aparece como SKIPPED com
o motivo escrito.
As a parametrized fixture, a skipped backend is visible instead of silent.
"""

import subprocess
import sys
from collections.abc import Iterator
from pathlib import Path

import psycopg
import pytest
from alembic.config import Config as ConfigAlembic
from alembic.script import ScriptDirectory

RAIZ = Path(__file__).resolve().parent.parent
sys.path.append(str(RAIZ))

from core import config  # noqa: E402
from core.memoria import (  # noqa: E402
    MemoriaEmMemoria,
    MemoriaLead,
    MemoriaPostgres,
    MemoriaSQLite,
)


def cabecas_do_alembic() -> list[str]:
    """
    As cabeças declaradas em migrations/versions/, lidas do disco sem tocar em
    banco nenhum.
    Alembic heads, read from disk without touching any database.
    """
    return list(
        ScriptDirectory.from_config(ConfigAlembic(str(RAIZ / "alembic.ini"))).get_heads()
    )


@pytest.fixture(scope="session")
def migracoes_aplicadas() -> str:
    """
    Aplica as migrações no banco de TESTE e devolve a URL.
    Applies migrations to the TEST database and returns its URL.

    Chama o `alembic` como processo, e não pela API Python, de propósito: é
    exatamente o comando que o deploy roda. Teste que exercita um caminho
    diferente do de produção prova o caminho errado.
    Runs the real CLI — the same command a deploy runs.

    `banco_url_de_teste()` recusa devolver a URL se ela for igual à de produção,
    então este fixture não tem como apontar para o banco de cliente.
    """
    url = config.banco_url_de_teste()

    if not url:
        pytest.skip("DATABASE_URL_TESTE não definida — Postgres não foi testado")

    # GUARDA ESTRITA. Pular só quando o Alembic está LEGITIMAMENTE sem revisão:
    # nesse estado não existe schema de domínio nenhum, e não há o que exercer.
    #
    # A condição é a contagem de cabeças, lida do disco — NÃO é `except
    # UndefinedTable`. A diferença decide o valor deste portão:
    #
    #   zero revisões        + tabela ausente  →  consequência do estado. SKIP.
    #   qualquer revisão     + tabela ausente  →  migração não aplicada, ou
    #                                             aplicada errada. ERRO VERMELHO.
    #
    # Um try/except transformaria os dois casos em skip e esconderia o segundo,
    # que é justamente uma falha de deploy em produção.
    #
    # Isto se desfaz sozinho: no dia em que a Fase A criar a primeira migração,
    # `cabecas_do_alembic()` deixa de ser vazia e os testes voltam a rodar sem
    # ninguém lembrar de nada.
    # Self-healing: the skip disappears the moment a real migration exists.
    if not cabecas_do_alembic():
        pytest.skip(
            "Alembic com zero revisões — ainda não existe schema de domínio "
            "para exercer. Estes testes voltam sozinhos quando a Fase A criar "
            "a primeira migração."
        )

    subprocess.run(
        ["alembic", "-x", f"url={url}", "upgrade", "head"],
        cwd=RAIZ,
        check=True,
        capture_output=True,
        text=True,
    )
    return url


@pytest.fixture(params=["em-memoria", "sqlite", "postgres"])
def memoria(request: pytest.FixtureRequest, tmp_path: Path) -> Iterator[MemoriaLead]:
    """Uma implementação de MemoriaLead por rodada, sempre limpa."""
    banco: MemoriaLead

    if request.param == "em-memoria":
        banco = MemoriaEmMemoria()
    elif request.param == "sqlite":
        banco = MemoriaSQLite(tmp_path / "contrato.db")
    else:
        url = request.getfixturevalue("migracoes_aplicadas")
        # Limpa ANTES de entregar, não depois: assim um teste que quebrou no
        # meio não deixa lixo para o próximo interpretar como dado seu.
        # Cleans before handing over, so a crashed test can't poison the next.
        _esvaziar(url)
        banco = MemoriaPostgres(url)

    yield banco
    # Sai igual para as três porque `fechar()` está no contrato. Fosse método
    # só das concretas, este preparo teria que perguntar o tipo antes.
    banco.fechar()


def _esvaziar(url: str) -> None:
    """
    Zera a tabela entre testes.

    Só recebe a URL de teste — `config.banco_url_de_teste()` recusa devolver
    qualquer coisa igual à de produção, então este TRUNCATE não alcança dado de
    cliente. Conexão direta em vez de reaproveitar o pool da MemoriaPostgres:
    preparo de teste não deve depender do interior da classe que ele testa.
    Direct connection — test setup shouldn't reach into the class under test.
    """
    with psycopg.connect(url) as con:
        con.execute("TRUNCATE TABLE lead")

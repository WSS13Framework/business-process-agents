"""
Lead memory — the contract that makes a returning lead recognizable.
Memória do lead — o contrato que faz quem volta ser reconhecido.

Até aqui o `lead_id` entrava no handle e saía no resultado sem tocar em nada:
identidade decorativa. Cada mensagem apagava a anterior.
Until now `lead_id` went in and came out untouched — decorative identity.

Armazenamento fica aqui porque é compartilhado; as REGRAS de acumulação ficam
em agents/lead_triage/acumulo.py, porque conhecem o nome de cada sinal.
Storage lives here because it is shared; the accumulation RULES live with the
agent, because they know each signal by name.

QUEM MANDA NO SCHEMA — e isto é uma tensão conhecida, não um descuido:

  Postgres  o schema é das migrações (migrations/versions/). MemoriaPostgres
            NÃO cria tabela: se ela não existir, é erro de deploy e tem que
            aparecer, não ser remendado em silêncio no construtor.
  SQLite    cria a tabela inline, como sempre fez. É conveniência local de uma
            tabela só, sem migração.

São duas fontes de verdade sobre o schema. Unificar exigiria migrações
portáteis entre dialetos, o que proibiria JSONB e índice específico do
Postgres. Na divergência, PRODUÇÃO MANDA: o Postgres é o certo e o SQLite é
que se ajusta.
Two schema sources on purpose; Postgres wins on divergence.
"""

import json
import sqlite3
import threading
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from psycopg.types.json import Jsonb
from psycopg_pool import ConnectionPool

# Teto para o pool abrir. Banco fora do ar tem que falhar na partida com o
# motivo à vista, não na primeira mensagem de lead disfarçado de lentidão.
TIMEOUT_CONEXAO_SEGUNDOS = 10.0


class MemoriaLead(ABC):
    """Contrato comum: carrega o estado de um lead, salva o estado de um lead."""

    @abstractmethod
    def carregar(self, tenant_id: str, lead_id: str) -> dict[str, Any]:
        """
        Devolve o estado guardado, ou dicionário vazio se o lead é novo.
        Returns the stored state, or an empty dict if the lead is new.

        Vazio é resposta legítima, não erro — é a primeira mensagem de alguém.
        """
        ...

    @abstractmethod
    def salvar(self, tenant_id: str, lead_id: str, estado: dict[str, Any]) -> None:
        """Grava o estado. Sobrescreve o anterior."""
        ...

    @abstractmethod
    def fechar(self) -> None:
        """
        Solta o que estiver aberto.
        Releases whatever is held open.

        Está no contrato porque sem isto quem segura um MemoriaLead não
        consegue fechar sem antes descobrir qual implementação recebeu — e
        perguntar o tipo concreto para decidir o que chamar é o contrário de
        contrato.

        Abstrato, e não um método vazio herdável, de propósito: implementação
        nova que segure conexão e esqueça de fechar vazaria em silêncio.
        Obrigada a escrever o método, ela é obrigada a decidir.
        Abstract on purpose — an implementation that holds a connection and
        forgets to close it would leak silently.
        """
        ...


class MemoriaEmMemoria(MemoriaLead):
    """
    Guarda num dicionário do processo. Some quando o processo morre.
    Keeps state in a process dict — gone when the process dies.

    Não é dublê de teste: é implementação legítima para rodar sem persistência.
    Os testes usam ela justamente porque o comportamento é o mesmo do SQLite,
    sem tocar em disco.
    """

    def __init__(self) -> None:
        self._dados: dict[tuple[str, str], dict[str, Any]] = {}

    def carregar(self, tenant_id: str, lead_id: str) -> dict[str, Any]:
        # Cópia: quem chamou não deve conseguir mutar o guardado por acidente.
        return dict(self._dados.get((tenant_id, lead_id), {}))

    def salvar(self, tenant_id: str, lead_id: str, estado: dict[str, Any]) -> None:
        self._dados[(tenant_id, lead_id)] = dict(estado)

    def fechar(self) -> None:
        """Não segura recurso nenhum: o dicionário morre com o processo."""


class MemoriaSQLite(MemoriaLead):
    """
    SQLite com um blob JSON por (tenant_id, lead_id).
    SQLite with one JSON blob per (tenant_id, lead_id).

    Blob e não colunas de propósito: o formato do estado ainda vai mudar, e
    migração de schema a cada campo novo custaria mais que o ganho de consultar
    por coluna, que ninguém precisa fazer ainda.
    JSON blob on purpose — the state shape is still moving.

    O tenant faz parte da chave desde já. Multi-tenant não está no MVP, mas
    chave errada é a migração mais cara que existe.
    """

    def __init__(self, caminho: str | Path = "memoria.db"):
        # Conexão única, não uma por chamada. Com ':memory:' cada connect()
        # cria um banco NOVO e vazio — a tabela criada aqui não existiria na
        # leitura seguinte. Em arquivo funcionava por acidente: o disco guardava.
        # One connection, not one per call — ':memory:' would otherwise create
        # a fresh empty database on every connect().
        self._con = sqlite3.connect(str(caminho), check_same_thread=False)
        # check_same_thread=False permite uso de várias threads, mas NÃO torna
        # a conexão segura sozinha. O lock é que faz isso.
        self._lock = threading.Lock()
        self._criar_tabela()

    def _criar_tabela(self) -> None:
        with self._lock, self._con:
            self._con.execute(
                """
                CREATE TABLE IF NOT EXISTS lead (
                    tenant_id TEXT NOT NULL,
                    lead_id   TEXT NOT NULL,
                    estado    TEXT NOT NULL,
                    PRIMARY KEY (tenant_id, lead_id)
                )
                """
            )

    def carregar(self, tenant_id: str, lead_id: str) -> dict[str, Any]:
        with self._lock:
            linha = self._con.execute(
                "SELECT estado FROM lead WHERE tenant_id = ? AND lead_id = ?",
                (tenant_id, lead_id),
            ).fetchone()

        if linha is None:
            return {}

        carregado: dict[str, Any] = json.loads(linha[0])
        return carregado

    def salvar(self, tenant_id: str, lead_id: str, estado: dict[str, Any]) -> None:
        with self._lock, self._con:
            self._con.execute(
                """
                INSERT INTO lead (tenant_id, lead_id, estado) VALUES (?, ?, ?)
                ON CONFLICT (tenant_id, lead_id) DO UPDATE SET estado = excluded.estado
                """,
                (tenant_id, lead_id, json.dumps(estado, ensure_ascii=False)),
            )

    def fechar(self) -> None:
        with self._lock:
            self._con.close()


class MemoriaPostgres(MemoriaLead):
    """
    Postgres com uma coluna JSONB por (tenant_id, lead_id).
    Postgres with one JSONB column per (tenant_id, lead_id).

    Três diferenças em relação ao SQLite, e nenhuma é cosmética:

    1. NÃO cria tabela. O schema é das migrações. Tabela ausente é erro de
       deploy e tem que estourar; construtor que remenda schema é como o
       sistema fica com duas versões de tabela em produção sem ninguém notar.
       Does not create the table — migrations own the schema.

    2. Pool em vez de conexão única com lock. A conexão única do SQLite serializa
       tudo num mutex, o que basta para um CLI e vira gargalo atrás de HTTP.
       O pool também reabre conexão que o servidor derrubou.

    3. JSONB em vez de TEXT. Mesmo blob, mas indexável e consultável quando o
       CRM precisar filtrar por sinal — sem migração de dados na hora.
    """

    def __init__(self, url: str, pool: ConnectionPool | None = None):
        # Costura para teste, mesmo padrão do transport/cliente das outras
        # fontes: quem chama pode injetar um pool já pronto.
        # Test seam, same pattern as transport=/cliente= elsewhere.
        if pool is not None:
            self._pool = pool
            return

        # open=False + open(wait=True): sem isto o pool tenta conectar numa
        # thread de fundo e o construtor devolve um objeto que parece bom e
        # falha só na primeira consulta. Preferimos o erro aqui.
        self._pool = ConnectionPool(url, min_size=1, open=False)
        self._pool.open(wait=True, timeout=TIMEOUT_CONEXAO_SEGUNDOS)

    def carregar(self, tenant_id: str, lead_id: str) -> dict[str, Any]:
        with self._pool.connection() as con:
            linha = con.execute(
                "SELECT estado FROM lead WHERE tenant_id = %s AND lead_id = %s",
                (tenant_id, lead_id),
            ).fetchone()

        if linha is None:
            return {}

        # JSONB já volta como dict do psycopg — não há json.loads aqui de
        # propósito. Variável anotada porque o driver devolve Any.
        carregado: dict[str, Any] = linha[0]
        return carregado

    def salvar(self, tenant_id: str, lead_id: str, estado: dict[str, Any]) -> None:
        with self._pool.connection() as con:
            con.execute(
                """
                INSERT INTO lead (tenant_id, lead_id, estado) VALUES (%s, %s, %s)
                ON CONFLICT (tenant_id, lead_id) DO UPDATE SET estado = excluded.estado
                """,
                (tenant_id, lead_id, Jsonb(estado)),
            )

    def fechar(self) -> None:
        self._pool.close()

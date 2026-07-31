#!/usr/bin/env bash
# Cópia diária do memoria.db — a única cópia do estado dos leads.
# Daily copy of memoria.db — the only copy of lead state.
#
# Instalar no cron (03:00 todo dia):
#   crontab -e
#   0 3 * * * /home/sea/Projetos/business-process-agents/deploy/backup.sh
#
# Usa `sqlite3 .backup` e não `cp`: cópia de SQLite com escrita em andamento
# pode sair corrompida, e a API de backup online do SQLite é segura com
# escritor concorrente. O comando certo custa o mesmo que o errado.
# Uses `sqlite3 .backup`, not `cp`: copying SQLite mid-write can corrupt.

set -euo pipefail

RAIZ="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BANCO="${1:-$RAIZ/memoria.db}"
DESTINO="$RAIZ/backup"

if [ ! -f "$BANCO" ]; then
    echo "sem banco em $BANCO — nada a copiar" >&2
    exit 0
fi

mkdir -p "$DESTINO"
COPIA="$DESTINO/memoria-$(date +%F).db"

sqlite3 "$BANCO" ".backup '$COPIA'"

# Só o dono lê: o banco guarda sinal de negócio por lead, e a cópia herda o
# mesmo dever. O umask padrão criaria 644.
# Owner-only: the copy carries the same business data as the original.
chmod 600 "$COPIA"

echo "$(date -Iseconds) copiado: $COPIA ($(stat -c%s "$COPIA") bytes)"

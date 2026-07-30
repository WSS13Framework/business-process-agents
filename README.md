# Autonomous Business-Process Agents

[![CI](https://github.com/WSS13Framework/business-process-agents/actions/workflows/ci.yml/badge.svg)](https://github.com/WSS13Framework/business-process-agents/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11%20|%203.12-blue)](https://github.com/WSS13Framework/business-process-agents)

A shared foundation for building production AI agents that do real work,
fail safely, and hand off to humans when they should — not chatbots or demos.

Uma base compartilhada para construir agentes de IA de produção que fazem
trabalho real, falham com segurança e passam para humanos quando devem.

## Why this exists / Por que existe

Most "AI agents" are one-off scripts. This project is the opposite: one shared
base (logging, retries, error handling, human hand-off) that every agent inherits,
so the 12th agent is faster to build than the 1st.

A maioria dos "agentes de IA" são scripts avulsos. Este projeto é o oposto: uma
base compartilhada que todo agente herda, então o 12º agente é mais rápido de
construir que o 1º.

## Design → see ARCHITECTURE.md

The full reasoning — interface contracts, per-tenant scoring, retry vs. circuit
breaker, autonomy limits vs. red lines — is documented in
[ARCHITECTURE.md](./ARCHITECTURE.md).

## Setup

```bash
pip install -r requirements-dev.txt

cp .env.example .env          # preencha com a sua chave / fill in your key
set -a; source .env; set +a   # exporta pro ambiente / export to the environment

pytest                        # roda offline, sem chave / runs offline, no key needed
```

A chave **nunca** entra no código. O SDK lê `ANTHROPIC_API_KEY` do ambiente
sozinho — por isso o cliente é construído sem argumento: `anthropic.Anthropic()`.
O `.env` é ignorado pelo git; só o `.env.example`, sem segredo, é versionado.

The key **never** goes in the code. The SDK reads `ANTHROPIC_API_KEY` from the
environment on its own — which is why the client takes no argument.

> Chave commitada em repositório público é revogada pela Anthropic em minutos
> por varredura automática. Até lá, roda no seu crédito.

## Stack

`Python` · `Claude API` · `n8n` · `PostgreSQL` · vector store · structured logging

## Status

🚧 Work in progress — building the shared base and a reference agent (lead triage)
first, then scaling to more agents on top of it.

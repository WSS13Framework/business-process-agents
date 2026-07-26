# Autonomous Business-Process Agents — Architecture
# Agentes Autônomos de Processos de Negócio — Arquitetura

> A shared foundation for building production agents that do real work,
> fail safely, and hand off to humans when they should.
>
> Uma base compartilhada para construir agentes de produção que fazem trabalho
> real, falham com segurança e passam para humanos quando devem.

---

## Design principles / Princípios de design

**EN** — Precision over hype. An agent should do useful work with minimal
supervision, and when it isn't sure, it says so and escalates. It never fails
silently.

**PT** — Precisão em vez de propaganda. Um agente deve fazer trabalho útil com
supervisão mínima, e quando não tem certeza, ele avisa e escala. Nunca falha
silenciosamente.

---

## 1. Shared base + interface contracts
## 1. Base compartilhada + contratos de interface

**EN** — All agents inherit from one shared base (logging, retries, error
handling, hand-off). Fixing something in the base improves all agents at once
(DRY, maintainability). The base and the agents talk through **stable interface
contracts**: a fixed input/output shape. As long as the contract holds, the
base's internals can evolve without breaking existing agents.

**PT** — Todos os agentes herdam de uma base compartilhada (logging, retries,
tratamento de erro, handoff). Corrigir algo na base melhora todos os agentes de
uma vez (DRY, manutenibilidade). A base e os agentes conversam por **contratos
de interface estáveis**: um formato fixo de entrada/saída. Enquanto o contrato
se mantém, as tripas da base podem evoluir sem quebrar os agentes existentes.

> *Interview line:* "I protect existing agents with stable interface contracts —
> the base implementation can change, but the contract doesn't break its callers."

---

## 2. Identity & memory per lead
## 2. Identidade e memória por lead

**EN** — When a new lead arrives, the first thing the agent does is create a
**record with a unique ID**. Every time that person comes back, the agent
recognizes them — it doesn't start over or ask the same questions twice. It
builds the profile **progressively**, across conversations, instead of forcing
everything up front.

**PT** — Quando um lead novo chega, a primeira coisa que o agente faz é criar um
**registro com um ID único**. Toda vez que essa pessoa volta, o agente a
reconhece — não recomeça nem repete as mesmas perguntas. Ele constrói o perfil
**progressivamente**, ao longo das conversas, em vez de forçar tudo de uma vez.

- **Structured facts** (name, score, stage) → normal database, keyed by ID.
- **Conversation history** → vector store, so the agent can recall what the lead
  said before. That's memory *for the relationship*, not for scoring.

---

## 3. Scoring: LLM signals + client rules (no ML at first)
## 3. Pontuação: sinais do LLM + regras do cliente (sem ML no início)

**EN** — To qualify a lead I don't need a trained ML model at first. The **LLM
reads the conversation and extracts signals** — urgency, budget, fit — and the
**client's rules** turn those into a score. This is enough to start and, crucially,
it's **explainable**: I can show the client *why* a lead scored 80.

ML comes later (v2), once we've collected enough real conversations to train on a
clean dataset — to catch patterns the rules miss. Training a model on day one,
with no data, is a guess dressed up as science.

**PT** — Para qualificar um lead eu não preciso de um modelo de ML treinado no
começo. O **LLM lê a conversa e extrai sinais** — urgência, orçamento, perfil —
e as **regras do cliente** transformam isso em pontuação. Isso já basta para
começar e, o mais importante, é **explicável**: consigo mostrar ao cliente *por
que* um lead pontuou 80.

ML vem depois (v2), quando já juntamos conversas reais suficientes para treinar
num dataset limpo — para pegar padrões que as regras não pegam. Treinar um modelo
no dia um, sem dado, é chute disfarçado de ciência.

> *Interview line:* "I start simple and explainable, and move to ML only when the
> data justifies it."

---

## 4. Not enough signal? Discover, don't fake
## 4. Sinal insuficiente? Descobre, não inventa

**EN** — If a new lead hasn't given enough to score them ("hi, how much is it?"),
the agent doesn't force a number. It flags *"not enough information yet"* and asks
a few natural questions to fill the gaps. A confident score on no data is worse
than admitting uncertainty.

Design intent: the agent **listens before it sells**. No barrage of forms —
people are saturated with questionnaires. Qualification happens quietly underneath
a natural conversation; the sale grows from the relationship, not from pressure.

**PT** — Se um lead novo não deu o suficiente para pontuar ("oi, quanto custa?"),
o agente não força um número. Ele marca *"ainda não tenho informação"* e faz
algumas perguntas naturais para preencher as lacunas. Um score confiante sem dado
é pior que admitir incerteza.

Intenção de design: o agente **escuta antes de vender**. Nada de enxurrada de
formulário — as pessoas estão saturadas de questionário. A qualificação acontece
por baixo de uma conversa natural; a venda nasce da relação, não da pressão.

---

## 5. Failure handling: retry, circuit breaker, hand-off
## 5. Tratamento de falha: retry, circuit breaker, handoff

**EN**
- **Retry with backoff** (one lead): a call fails → retry a few times with
  increasing delays (1s, 2s, 4s). Most failures are temporary.
- **Cap the retries** (~3): retrying forever hides the problem and wastes money.
- **Circuit breaker** (many leads): when failures pile up across the board, the
  breaker trips — stop hammering a service that's clearly down, route everything
  to humans, and recover when it's back.
- **Hand-off with context**: if it still fails, the agent logs what happened,
  saves its progress, and escalates with a clear reason. **Never fails silently.**

**PT**
- **Retry com backoff** (um lead): uma chamada falha → tenta de novo poucas vezes
  com intervalos crescentes (1s, 2s, 4s). A maioria das falhas é temporária.
- **Limita as tentativas** (~3): tentar para sempre esconde o problema e gasta
  dinheiro.
- **Circuit breaker** (muitos leads): quando as falhas se acumulam em geral, o
  breaker desarma — para de insistir num serviço que caiu, manda tudo para
  humanos, e religa quando volta.
- **Handoff com contexto**: se ainda falha, o agente registra o que aconteceu,
  salva o progresso e escala com um motivo claro. **Nunca falha em silêncio.**

---

## 6. Autonomy: config limit vs. red line
## 6. Autonomia: limite de config vs. linha vermelha

**EN** — There's no single fixed line. Two separate cases decide what the agent
handles alone versus what goes to a human:

1. **Config limit (per client).** The agent checks *that client's* configuration
   for how much authority it has. "Give me 50% off" → if it's within the discount
   limit the client granted, act; if beyond, hand off. Autonomy is defined in the
   contract, per tenant — **not hardcoded**.
2. **Red line (always human).** Some things no one should automate, no matter the
   config: legal threats, minors, someone in distress, reputation-critical
   complaints. These escalate **regardless of confidence**. Some decisions are too
   high-stakes for an agent, period.

**PT** — Não existe uma linha única fixa. Dois casos separados decidem o que o
agente resolve sozinho versus o que vai para um humano:

1. **Limite de config (por cliente).** O agente consulta a configuração *daquele
   cliente* para saber quanta autoridade tem. "Me dá 50% de desconto" → se está
   dentro do limite concedido, age; se passa, faz handoff. A autonomia é definida
   no contrato, por tenant — **não fixa no código**.
2. **Linha vermelha (sempre humano).** Algumas coisas ninguém deveria automatizar,
   não importa a config: ameaça jurídica, menor de idade, alguém em crise,
   reclamação crítica de reputação. Essas escalam **independente da confiança**.
   Algumas decisões são sérias demais para um agente, ponto.

> *Interview line:* "I separate permission limits, which are configurable per
> client, from red lines, which always escalate no matter what the config says."

---

## 7. Multi-tenant by design
## 7. Multi-tenant por design

**EN** — Scoring rules and autonomy limits aren't hardcoded. Each client has their
own definition of a good lead and their own authority limits. The agent loads
*that client's* rules at runtime. One codebase serves many clients, each isolated.

**PT** — Regras de pontuação e limites de autonomia não são fixos no código. Cada
cliente tem sua própria definição de bom lead e seus próprios limites de
autoridade. O agente carrega as regras *daquele cliente* em tempo de execução. Um
código serve muitos clientes, cada um isolado.

---

## Definition of done (per agent) / Definição de concluído (por agente)

**EN** — An agent is accepted when it: runs the target process end-to-end with no
manual steps for the agreed cases; handles common failure paths without crashing
or losing data; logs its actions auditably; escalates to a human on the defined
exceptions; and ships with a short operating manual.

**PT** — Um agente é aceito quando: roda o processo alvo de ponta a ponta sem
etapas manuais nos casos acordados; lida com os caminhos de falha comuns sem
travar ou perder dados; registra suas ações de forma auditável; escala para humano
nas exceções definidas; e vem com um manual de operação curto.

---

## Stack

`Python` · `Claude API` · `n8n` (orchestration) · `PostgreSQL` (structured state)
· vector store (relationship memory) · structured logging.

---

*This document is the "Milestone 0" foundation: the shared standard agreed before
scaling to individual agents. / Este documento é a fundação "Marco 0": o padrão
compartilhado acordado antes de escalar para os agentes individuais.*

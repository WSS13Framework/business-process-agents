# Guia de Estudo — Agentes de Automação de Negócio
# Study Guide — Business-Process Agents

> **Como usar:** leia cada conceito, tente explicar em voz alta pra uma pessoa
> que nunca programou. Se travar, releia a analogia. Só passe adiante quando
> conseguir ensinar. No fim de cada bloco tem a frase pra falar numa entrevista
> em inglês e um "teste você mesmo".
>
> **Regra de ouro (Feynman):** se você não consegue explicar simples,
> você ainda não entendeu. Explicar é o estudo.

---

## 0. A visão geral em uma frase

**Pra um leigo:** "Eu construo assistentes de computador que fazem trabalho
sozinhos — atender cliente, organizar pedido, gerar documento — mas que sabem
a hora de chamar uma pessoa quando a coisa é séria demais pra máquina decidir."

**Interview (EN):** *"I build autonomous agents that do real business work and
hand off to a human when a decision is too important to automate."*

---

## 1. Base compartilhada (a classe base)

**O conceito:** em vez de cada agente ter seu próprio jeito de trabalhar, todos
seguem UM padrão central. Esse padrão é a "base", e cada agente "herda" dela.

**Analogia (construção):** uma construtora com 12 obras. Em vez de cada mestre
inventar seu jeito de controlar segurança, existe UM padrão de segurança que
todas as obras seguem. Achou um jeito melhor? Muda no padrão, e as 12 obras
melhoram juntas.

**Por que importa:** corrijo num lugar só → todos melhoram. Não repito o mesmo
código 12 vezes (isso se chama **DRY** — Don't Repeat Yourself, "não se repita").

**Interview (EN):** *"All agents inherit from one shared base, so fixing
something once improves every agent. That's DRY and it keeps the system
maintainable."*

**Teste você mesmo:** explique pra alguém por que 12 agentes com uma base comum
são mais fáceis de manter que 12 agentes independentes.

---

## 2. Contrato de interface (o @abstractmethod)

**O conceito:** a base OBRIGA todo agente a ter um método chamado `handle`, com
um formato fixo de entrada e saída. Quem não cumprir, o programa nem roda.

**Analogia (encaixe):** a rosca do cano de meia polegada. Qualquer cano de meia
polegada encaixa em qualquer conexão de meia polegada. Você troca a marca, o
material — mas a rosca é a mesma, então nada quebra na instalação. O contrato é
a rosca.

**Por que importa:** enquanto todos respeitam o contrato, eu posso melhorar as
tripas da base à vontade que nenhum agente quebra. E é o CÓDIGO que obriga isso,
não a boa vontade de quem programa — por isso é uma regra de verdade, não um
pedido.

**A diferença que impressiona:** regra na documentação depende da pessoa lembrar.
Regra imposta pelo código é impossível de furar. Sempre prefira a segunda.

**Interview (EN):** *"The base defines an abstract method every agent must
implement — a contract enforced by the language itself. If an agent doesn't
follow the input/output shape, it won't even run."*

**Teste você mesmo:** por que é mais seguro o código obrigar o contrato do que
só escrever "por favor, siga o padrão" na documentação?

---

## 3. Multi-tenant (um código, muitos clientes)

**O conceito:** o mesmo programa atende vários clientes, e cada um tem suas
próprias regras. O agente carrega as regras DAQUELE cliente na hora de trabalhar.

**Analogia:** um contador que atende 50 empresas. É o mesmo contador, mas ele
aplica as regras de cada empresa quando mexe nos livros dela. Não mistura o caixa
de uma com o da outra.

**Por que importa:** não preciso de um programa diferente pra cada cliente. Um
código só, e a "régua" muda por cliente. E os dados de um cliente NUNCA se
misturam com os de outro (isso se chama **isolamento de tenant**).

**No código:** o agente já nasce sabendo qual cliente atende (`tenant_id`
passado na criação). Desde a primeira ação ele sabe quais regras aplicar.

**Interview (EN):** *"It's multi-tenant: one codebase serves many clients, each
with their own rules loaded at runtime, fully isolated from each other."*

**Teste você mesmo:** o que poderia dar errado se o agente descobrisse tarde
demais qual cliente está atendendo?

---

## 4. Pontuação de lead (scoring: quente / morno / frio)

**O conceito:** o agente lê a conversa, extrai sinais (a pessoa tem pressa? tem
orçamento? é o perfil certo?), soma pontos, e classifica: quente, morno ou frio.

**Analogia:** um bom vendedor de loja sente, conversando, quem veio comprar hoje
(quente), quem está pesquisando (morno) e quem só está passeando (frio). O agente
faz isso com pontos.

**A sacada importante — não precisa de "inteligência artificial treinada" pra
isso no começo:** o LLM (o Claude/GPT) LÊ a conversa e extrai os sinais, e regras
simples transformam em pontos. É explicável — eu mostro ao cliente POR QUE o lead
pontuou 80. Modelo treinado (machine learning) vem depois, quando eu já tiver
muitos dados. Treinar modelo sem dado é chute com cara de ciência.

**A régua vem de fora (config), não fica fixa no código:** cada cliente decide o
que é "quente" (um acha 70, outro acha 85). O código é o mesmo; a régua muda por
cliente. Isso se chama **separar configuração de código**.

**Interview (EN):** *"The LLM extracts signals from the conversation and the
client's rules turn them into a score. It's explainable — I can show why a lead
scored 80. ML comes later, only when the data justifies it."*

**Teste você mesmo:** por que começar SEM machine learning é a decisão certa no
dia 1? (Duas razões: dado e explicabilidade.)

---

## 5. Quando falta informação: descobre, não inventa

**O conceito:** se o lead não deu informação suficiente pra pontuar, o agente NÃO
chuta um número. Ele reconhece que não sabe, e conversa pra descobrir mais.

**Analogia:** um médico bom não dá diagnóstico com meia informação. Ele pergunta
mais antes de concluir. Chutar diagnóstico é pior que dizer "preciso de mais
exames".

**A filosofia:** o agente ESCUTA antes de vender. Nada de enxurrada de perguntas
— as pessoas estão saturadas de formulário. Conversa natural, e a qualificação
acontece por baixo. A venda nasce da relação, não da pressão.

**Interview (EN):** *"The agent won't fake a score without enough signal — it
flags uncertainty and asks a few natural questions. It listens before it sells."*

**Teste você mesmo:** por que um score confiante baseado em nada é PIOR que
admitir "ainda não sei"?

---

## 6. Quando dá erro: tentar de novo, desarmar, chamar humano

Três camadas, do menor problema pro maior:

**a) Retry com backoff (falha de UM lead)**
- A chamada falhou? Tenta de novo — mas com paciência: espera 1s, tenta; 2s,
  tenta; 4s, tenta.
- **Analogia:** a linha telefônica caiu. Você não fica apertando "rediscar"
  feito louco — espera um pouco e tenta de novo, dando tempo do problema passar.

**b) Limite de tentativas (~3)**
- Depois de 3 tentativas, para. Tentar pra sempre trava tudo e gasta dinheiro.
- **Analogia:** você liga 3 vezes, ninguém atende, você para e tenta outra coisa.
  Não fica ligando 500 vezes.

**c) Circuit breaker (falha em MASSA)**
- Se TODOS os leads estão falhando (o serviço caiu), o "disjuntor" desarma: para
  de tentar, manda tudo pro humano, e religa quando o serviço voltar.
- **Analogia:** o disjuntor da sua casa. Deu curto? Ele desarma pra não queimar a
  casa inteira. Depois você religa.

**A regra de ouro que junta tudo:** o agente NUNCA falha em silêncio. Se ele não
conseguiu, ele registra o que houve, salva o que já tinha, e avisa um humano com
o motivo. Nunca finge que deu certo, nunca some.

**Interview (EN):** *"Retry with backoff for a single failure, a circuit breaker
when failures pile up across the board, and always a hand-off with context. It
never fails silently."*

**Teste você mesmo:** qual a diferença entre RETRY (um lead) e CIRCUIT BREAKER
(muitos leads)? Por que preciso dos dois?

---

## 7. Autonomia: até onde o agente decide sozinho

Duas categorias diferentes decidem o que o agente faz sozinho vs. o que vai
pro humano:

**a) Limite de permissão (configurável por cliente)**
- O cliente A deixou o agente dar até 10% de desconto. O B, até 20%. O agente
  consulta o limite DAQUELE cliente. Pediu 50% e o limite é 10%? Vai pro humano.
- **Analogia:** o gerente de loja pode aprovar desconto até certo valor. Acima
  disso, tem que ligar pro dono. Cada loja define esse teto.

**b) Linha vermelha (SEMPRE humano, não importa a config)**
- Coisas que ninguém deveria automatizar, mesmo que quisesse: ameaça de processo,
  menor de idade, pessoa em crise, reclamação grave de reputação.
- **Analogia:** tem decisões que nenhum funcionário toma sozinho, nem o gerente —
  vão direto pra diretoria/jurídico, sempre.

**A distinção que impressiona:** permissão é CONFIGURÁVEL (varia por cliente);
linha vermelha é FIXA (nunca se cruza). Saber separar as duas é o "bom senso" que
o cliente procura.

**Interview (EN):** *"I separate permission limits — configurable per client —
from red lines, which always escalate no matter what the config says. Some
decisions are too high-stakes for an agent, period."*

**Teste você mesmo:** dê um exemplo de cada: uma coisa que É permissão
configurável, e uma que É linha vermelha.

---

## 8. Memória por cliente (o ID)

**O conceito:** cada lead ganha um ID único. Quando ele volta, o agente já o
reconhece — não recomeça do zero, não repete perguntas. Vai acumulando o que
sabe a cada conversa.

**Analogia:** o dono da padaria que já sabe seu pedido. Você chega, ele já
lembra que você gosta do pão quentinho. Não pergunta tudo de novo toda vez.

**Onde guardar o quê:**
- Fatos organizados (nome, pontuação, etapa) → banco de dados comum, achado
  pelo ID.
- Histórico de conversa (o que ele já falou) → banco vetorial, pra o agente
  "lembrar" o que foi dito. Isso é memória DO RELACIONAMENTO — não é pra pontuar.

**Interview (EN):** *"Each lead has a stable ID, so when they come back the agent
already knows them and builds the profile progressively, across conversations."*

**Teste você mesmo:** por que o histórico de conversa vai num banco vetorial, mas
a pontuação NÃO usa banco vetorial? (Dica: buscar informação ≠ aplicar critério.)

---

## Como praticar (rotina sugerida)

1. **Leia um bloco** (1 a 8).
2. **Feche o documento** e explique aquele bloco em voz alta, como se ensinasse
   um amigo que nunca programou. Use a analogia.
3. **Responda o "teste você mesmo"** sem olhar.
4. **Treine a frase em inglês** até sair natural — não decorada, entendida.
5. Só passe pro próximo bloco quando conseguir ensinar o atual.

**Meta final:** conseguir contar a história inteira — do lead que chega até a
decisão de escalar pro humano — de forma natural, numa conversa, em português e
em inglês. Quando isso sair leve, você está pronto pra qualquer entrevista sobre
esse projeto.
## Fase 1 — ABC (Abstract Base Class) ✅

### 1. O contrato
- `ABC` + `@abstractmethod` transformam "todo agente TEM que ter handle"
  de convenção informal em garantia forçada pelo runtime.
- Indentação em Python é ESTRUTURA, não estética. Define o que pertence
  à classe. Sempre 4 espaços, nunca tab (PEP 8).
- `ABC` funciona por baixo através de uma metaclass (ABCMeta).
- LIMITE: o ABC garante que o método EXISTE, não que a ASSINATURA está
  certa. Pra isso, combinar com typing.Protocol ou mypy. (→ próximo estudo)

### 2. Os três estados (vistos rodando na máquina)
- Recusa instanciar a base abstrata direta.
- Recusa o filho que herda mas não implementa (abstrato é herdado).
- Aceita o filho que implementa o handle.

### 3. Dicionário vs JSON
- dict = objeto vivo dentro do Python, fácil de manipular.
- JSON = formato de texto pra enviar/guardar (aspas duplas, true/false/null).
- Converter: json.dumps (dict → JSON), json.loads (JSON → dict). = serializar.
- Chave → valor: chave é pergunta, valor é resposta. Chave é única.

### 4. Fail fast (a resposta de entrevista)
"Usei ABC porque ele faz o erro aparecer cedo — na criação do agente, na
minha máquina — em vez de tarde, em produção com cliente real. É a diferença
entre trocar um cano antes de assentar e quebrar a parede depois de entregue.
Código é feito de camadas que dependem umas das outras: se a base sobe
quebrada, tudo que construo em cima herda o defeito. Quanto mais tarde o
erro aparece, mais caro. ABC é fail fast."

### Próximos passos
- [x] Plugar classificar_lead (scoring.py) dentro do handle do LeadTriageAgent
- [ ] Estudar typing.Protocol (comparar com ABC)
- [ ] Seguir para os demais agentes sobre a base sólida

## Pendências assumidas (dívida consciente)

### Contrato de SAÍDA não é imposto por código
O ABC garante que `buscar()` EXISTE, não que o retorno tem o formato certo.
Uma fonte pode ignorar `_ok`/`_vazio` e devolver um dict torto — o
`enriquecer()` aceita numa boa. Mesma limitação do ABC anotada na Fase 1:
ele cobre a existência do método, não a assinatura nem o retorno.

Decisão: DEIXAR ASSIM por enquanto, e anotar. Motivo: primeiro provar que a
estrutura roda, depois endurecer. Mesma ordem do stub — não se endurece o
que ainda não se viu funcionar.

Quando endurecer, as opções são:
- validar o formato dentro do `enriquecer()` (barato, imediato)
- `typing.Protocol` + mypy (pega antes de rodar) — ver item acima
- TypedDict pro formato do resultado

### Campo `detalhe` (era `erro`)
Renomeado porque carrega duas coisas diferentes: o MOTIVO no status `vazio`
("não achei página sobre") e a MENSAGEM DA EXCEÇÃO no status `falha`.
`erro` mentia no caso `vazio` — vazio não é erro, é resposta legítima.
Ler como: "por que este resultado não traz dados".
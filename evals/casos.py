"""
Casos de regressão da INSTRUCAO — o gabarito contra o qual toda mudança roda.
Regression cases for INSTRUCAO — the answer key every change runs against.

Cada caso declara só os campos que aquele cenário deve travar. O que não está
declarado não é cobrado: ninguém precisa opinar sobre 'urgencia' num caso que
existe pra testar autoridade.

Each case declares only the fields that scenario should pin down.
"""

from typing import Any

# categoria -> por que este grupo existe
CATEGORIAS = {
    "proprietario_explicito": "diz com todas as letras que é dono",
    "proprietario_implicito": "possessivo aplicado ao negócio, sem dizer 'sou dono'",
    "socio": "sociedade declarada",
    "fundador": "fundou o negócio",
    "gerente": "cargo de gestão, com ou sem poder de compra declarado",
    "compras": "responsável por compra/aprovação de orçamento",
    "funcionario": "trabalha lá, sem poder de decisão declarado",
    "agencia": "fala em nome de clientes de terceiros",
    "consultor": "presta serviço para quem decide",
    "estudante": "pesquisa acadêmica",
    "curioso": "quer informação, sem vínculo declarado",
    "spam": "mensagem que não é lead",
    "curta": "texto curto demais para sustentar sinal",
    "ambigua": "evidência insuficiente ou contraditória",
    "descadastro": "pede para sair",
    "sinais_combinados": "autoridade junto com orçamento/urgência",
    "agente_comercial": "dor de oportunidade perdida",
    "agente_atendimento": "dor no trato com quem já escreveu",
    "agente_marketing": "dor de não ser encontrado ou não ter o que mostrar",
    "agente_operacional": "dor de trabalho repetitivo que não é conversa",
    "agente_indefinido": "sem mecanismo de dor descrito — não chutar",
    "agente_armadilha": "produto aponta pra um time, dor aponta pra outro",
}

CASOS: list[dict[str, Any]] = [
    # ---- proprietário explícito ----
    {
        "id": "prop_exp_01",
        "categoria": "proprietario_explicito",
        "mensagem": "sou dono de uma clínica odontológica e quero divulgar melhor",
        "esperado": {"autoridade": True, "descadastro": False},
    },
    {
        "id": "prop_exp_02",
        "categoria": "proprietario_explicito",
        "mensagem": "sou proprietário de um restaurante no Leblon, quero fotos do salão",
        "esperado": {"autoridade": True},
    },
    {
        "id": "prop_exp_03",
        "categoria": "proprietario_explicito",
        "mensagem": "eu que sou o dono do negócio, então falo direto com vocês",
        "esperado": {"autoridade": True},
    },
    {
        "id": "prop_exp_04",
        "categoria": "proprietario_explicito",
        "mensagem": "administro uma rede de academias e preciso padronizar a comunicação",
        "esperado": {"autoridade": True},
    },
    # ---- proprietário implícito (o alvo do marco: falso negativo) ----
    {
        "id": "prop_imp_01",
        "categoria": "proprietario_implicito",
        "mensagem": "tenho uma clínica em Botafogo, quero vídeo institucional",
        "esperado": {"autoridade": True},
    },
    {
        "id": "prop_imp_02",
        "categoria": "proprietario_implicito",
        "mensagem": "minha empresa precisa de uma identidade visual nova",
        "esperado": {"autoridade": True},
    },
    {
        "id": "prop_imp_03",
        "categoria": "proprietario_implicito",
        "mensagem": "meu consultório está sem site, dá pra resolver?",
        "esperado": {"autoridade": True},
    },
    {
        "id": "prop_imp_04",
        "categoria": "proprietario_implicito",
        "mensagem": "abri uma clínica de estética mês passado e preciso aparecer",
        "esperado": {"autoridade": True},
    },
    {
        "id": "prop_imp_05",
        "categoria": "proprietario_implicito",
        "mensagem": "nossa loja no centro precisa de vídeos pro Instagram",
        "esperado": {"autoridade": True},
    },
    {
        "id": "prop_imp_06",
        "categoria": "proprietario_implicito",
        "mensagem": "quero implantar isso na minha empresa ainda esse ano",
        "esperado": {"autoridade": True, "urgencia": True},
    },
    {
        "id": "prop_imp_07",
        "categoria": "proprietario_implicito",
        "mensagem": "preciso para minha clínica, o que vocês oferecem?",
        "esperado": {"autoridade": True},
    },
    {
        "id": "prop_imp_08",
        "categoria": "proprietario_implicito",
        "mensagem": "montei um petshop e não sei por onde começar no marketing",
        "esperado": {"autoridade": True},
    },
    # ---- sócio ----
    {
        "id": "socio_01",
        "categoria": "socio",
        "mensagem": "sou sócio de uma corretora e queremos rebranding",
        "esperado": {"autoridade": True},
    },
    {
        "id": "socio_02",
        "categoria": "socio",
        "mensagem": "eu e meu sócio abrimos um escritório de arquitetura esse ano",
        "esperado": {"autoridade": True},
    },
    {
        "id": "socio_03",
        "categoria": "socio",
        "mensagem": "sou sócio-administrador da empresa, quem fecha contrato sou eu",
        "esperado": {"autoridade": True},
    },
    # ---- fundador ----
    {
        "id": "fund_01",
        "categoria": "fundador",
        "mensagem": "sou fundador de uma startup de saúde e preciso de posicionamento",
        "esperado": {"autoridade": True},
    },
    {
        "id": "fund_02",
        "categoria": "fundador",
        "mensagem": "fundei a empresa em 2019 e nunca investimos em marca",
        "esperado": {"autoridade": True},
    },
    {
        "id": "fund_03",
        "categoria": "fundador",
        "mensagem": "sou cofundadora e cuido de tudo de marketing aqui",
        "esperado": {"autoridade": True},
    },
    # ---- gerente ----
    {
        "id": "ger_01",
        "categoria": "gerente",
        "mensagem": "sou gerente de marketing da Acme e estamos avaliando fornecedores",
        "esperado": {"autoridade": False},
    },
    {
        "id": "ger_02",
        "categoria": "gerente",
        "mensagem": "sou gerente e eu que aprovo o orçamento de marketing aqui",
        "esperado": {"autoridade": True},
    },
    {
        "id": "ger_03",
        "categoria": "gerente",
        "mensagem": "trabalho como gerente comercial, meu diretor pediu pra buscar opções",
        "esperado": {"autoridade": False},
    },
    {
        "id": "ger_04",
        "categoria": "gerente",
        "mensagem": "gerencio a unidade da Barra, mas a decisão é da matriz",
        "esperado": {"autoridade": False},
    },
    # ---- responsável por compras ----
    {
        "id": "compras_01",
        "categoria": "compras",
        "mensagem": "sou responsável pelas compras da rede e preciso de proposta",
        "esperado": {"autoridade": True},
    },
    {
        "id": "compras_02",
        "categoria": "compras",
        "mensagem": "eu aprovo o orçamento, me manda os valores por favor",
        "esperado": {"autoridade": True},
    },
    {
        "id": "compras_03",
        "categoria": "compras",
        "mensagem": "sou eu que decido o fornecedor, mas quero comparar antes",
        "esperado": {"autoridade": True},
    },
    {
        "id": "compras_04",
        "categoria": "compras",
        "mensagem": "trabalho no setor de compras e coleto orçamentos pra diretoria decidir",
        "esperado": {"autoridade": False},
    },
    # ---- funcionário ----
    {
        "id": "func_01",
        "categoria": "funcionario",
        "mensagem": "sou analista de marketing na Acme, meu chefe pediu pra pesquisar preços",
        "esperado": {"autoridade": False},
    },
    {
        "id": "func_02",
        "categoria": "funcionario",
        "mensagem": "trabalho na recepção da clínica e me pediram pra entrar em contato",
        "esperado": {"autoridade": False},
    },
    {
        "id": "func_03",
        "categoria": "funcionario",
        "mensagem": "sou estagiária e estou levantando fornecedores pra equipe",
        "esperado": {"autoridade": False},
    },
    {
        "id": "func_04",
        "categoria": "funcionario",
        "mensagem": "faço parte do time de comunicação, quem decide é a diretoria",
        "esperado": {"autoridade": False},
    },
    # ---- agência ----
    {
        "id": "agencia_01",
        "categoria": "agencia",
        "mensagem": "somos uma agência e buscamos parceiro de vídeo para nossos clientes",
        "esperado": {"autoridade": False},
    },
    {
        "id": "agencia_02",
        "categoria": "agencia",
        "mensagem": "atendo vários clientes e preciso terceirizar a produção audiovisual",
        "esperado": {"autoridade": False},
    },
    {
        "id": "agencia_03",
        "categoria": "agencia",
        "mensagem": "minha agência tem um cliente que precisa de institucional em novembro",
        "esperado": {"autoridade": False, "urgencia": True},
    },
    # ---- consultor / prestador ----
    {
        "id": "cons_01",
        "categoria": "consultor",
        "mensagem": "sou consultor de marketing e recomendo fornecedores pros meus clientes",
        "esperado": {"autoridade": False},
    },
    {
        "id": "cons_02",
        "categoria": "consultor",
        "mensagem": "presto serviço pra uma rede de clínicas e me pediram indicações",
        "esperado": {"autoridade": False},
    },
    {
        "id": "cons_03",
        "categoria": "consultor",
        "mensagem": "sou freelancer de design e às vezes preciso de parceiro de vídeo",
        "esperado": {"autoridade": False},
    },
    # ---- estudante / pesquisador ----
    {
        "id": "est_01",
        "categoria": "estudante",
        "mensagem": "faço TCC sobre marketing digital, pode me explicar como funciona?",
        "esperado": {"autoridade": False},
    },
    {
        "id": "est_02",
        "categoria": "estudante",
        "mensagem": "sou pesquisador e estudo precificação no setor criativo",
        "esperado": {"autoridade": False},
    },
    {
        "id": "est_03",
        "categoria": "estudante",
        "mensagem": "estudo publicidade e queria entender como vocês cobram",
        "esperado": {"autoridade": False},
    },
    # ---- curioso ----
    {
        "id": "cur_01",
        "categoria": "curioso",
        "mensagem": "quanto custa um vídeo institucional?",
        "esperado": {"autoridade": False, "orcamento": False},
    },
    {
        "id": "cur_02",
        "categoria": "curioso",
        "mensagem": "vocês trabalham com que tipo de cliente?",
        "esperado": {"autoridade": False},
    },
    {
        "id": "cur_03",
        "categoria": "curioso",
        "mensagem": "vi o portfólio de vocês, ficou muito bom o trabalho",
        "esperado": {"autoridade": False},
    },
    {
        "id": "cur_04",
        "categoria": "curioso",
        "mensagem": "queria entender melhor como funciona o processo de vocês",
        "esperado": {"autoridade": False},
    },
    # ---- spam ----
    {
        "id": "spam_01",
        "categoria": "spam",
        "mensagem": "GANHE DINHEIRO EM CASA!!! CLIQUE AQUI bit.ly/xyz",
        "esperado": {"autoridade": False, "orcamento": False, "urgencia": False},
    },
    {
        "id": "spam_02",
        "categoria": "spam",
        "mensagem": "Promoção imperdível: 500 seguidores por R$ 19,90, só hoje!",
        "esperado": {"autoridade": False},
    },
    {
        "id": "spam_03",
        "categoria": "spam",
        "mensagem": "asdkjhasd 123 !!! ???",
        "esperado": {"autoridade": False, "orcamento": False, "urgencia": False},
    },
    # ---- muito curtas ----
    {
        "id": "curta_01",
        "categoria": "curta",
        "mensagem": "oi",
        "esperado": {"autoridade": False, "orcamento": False, "urgencia": False},
    },
    {
        "id": "curta_02",
        "categoria": "curta",
        "mensagem": "bom dia",
        "esperado": {"autoridade": False, "orcamento": False},
    },
    {
        "id": "curta_03",
        "categoria": "curta",
        "mensagem": "info",
        "esperado": {"autoridade": False},
    },
    {
        "id": "curta_04",
        "categoria": "curta",
        "mensagem": "orçamento",
        "esperado": {"autoridade": False, "orcamento": False},
    },
    # ---- ambíguas ----
    {
        "id": "amb_01",
        "categoria": "ambigua",
        "mensagem": "estamos precisando de vídeo institucional",
        "esperado": {"autoridade": False},
    },
    {
        "id": "amb_02",
        "categoria": "ambigua",
        "mensagem": "a empresa quer renovar a marca esse ano",
        "esperado": {"autoridade": False},
    },
    {
        "id": "amb_03",
        "categoria": "ambigua",
        "mensagem": "me pediram pra falar com vocês sobre o projeto novo",
        "esperado": {"autoridade": False},
    },
    {
        "id": "amb_04",
        "categoria": "ambigua",
        "mensagem": "trabalho com estética e queria melhorar minha divulgação",
        "esperado": {"autoridade": False},
    },
    # ---- descadastro ----
    {
        "id": "desc_01",
        "categoria": "descadastro",
        "mensagem": "me tira do mailing, não quero mais receber nada",
        "esperado": {"descadastro": True, "autoridade": False},
    },
    {
        "id": "desc_02",
        "categoria": "descadastro",
        "mensagem": "não tenho interesse, obrigado",
        "esperado": {"descadastro": True},
    },
    {
        "id": "desc_03",
        "categoria": "descadastro",
        "mensagem": "tenho uma clínica mas não quero mais receber mensagens de vocês",
        "esperado": {"descadastro": True, "autoridade": True},
    },
    # ---- sinais combinados ----
    {
        "id": "comb_01",
        "categoria": "sinais_combinados",
        "mensagem": (
            "oi, tenho uma clínica em Botafogo, quero vídeo institucional, "
            "orçamento até 8 mil, preciso pra outubro"
        ),
        "esperado": {
            "autoridade": True,
            "orcamento": True,
            "urgencia": True,
            "descadastro": False,
        },
    },
    {
        "id": "comb_02",
        "categoria": "sinais_combinados",
        "mensagem": "sou dono da empresa, tenho 50 mil de verba e preciso fechar até sexta",
        "esperado": {"autoridade": True, "orcamento": True, "urgencia": True},
    },
    {
        "id": "comb_03",
        "categoria": "sinais_combinados",
        "mensagem": "minha loja precisa de fotos, mas ainda não tenho verba definida",
        "esperado": {"autoridade": True, "orcamento": False},
    },
    {
        "id": "comb_04",
        "categoria": "sinais_combinados",
        "mensagem": "sou analista aqui, temos 30 mil aprovados pra esse projeto",
        "esperado": {"autoridade": False, "orcamento": True},
    },
    # ---- agente_indicado: quem manda é a dor descrita, não o produto pedido ----
    {
        "id": "ag_arm_01",
        "categoria": "agente_armadilha",
        # O produto pedido e midia paga, mas a dor descrita e perda por demora no retorno ao lead,
        # que e comercial.
        "mensagem": (
            "queria contratar trafego pago pra chegar mais lead. na verdade lead ja chega "
            "uns 40 por mes do google, o problema e que meu vendedor liga 3 dia depois e o "
            "cara ja fechou com o concorrente"
        ),
        "esperado": {"agente_indicado": "comercial"},
    },
    {
        "id": "ag_arm_02",
        "categoria": "agente_armadilha",
        # O produto pedido aponta atendimento, mas a dor descrita e documento repetitivo montado a
        # mao, que e operacional.
        "mensagem": (
            "queria um robo pra atender os cliente no whats. o que mata mesmo aqui e que "
            "pra cada pedido eu monto o orçamento na mao no word, copiando preco da tabela, "
            "umas 30 vez por dia"
        ),
        "esperado": {"agente_indicado": "operacional"},
    },
    {
        "id": "ag_arm_03",
        "categoria": "agente_armadilha",
        # O produto pedido e ferramenta de vendas, mas a dor e ausencia total de demanda entrante
        # por desconhecimento da marca.
        "mensagem": (
            "me indicaram um crm pra organizar o funil de vendas. so que funil nao tem, faz "
            "uns 4 mes que nao entra um contato novo aqui, ninguem na regiao conhece a "
            "marca"
        ),
        "esperado": {"agente_indicado": "marketing"},
    },
    {
        "id": "ag_arm_04",
        "categoria": "agente_armadilha",
        # O produto pedido e social media, mas a dor e volume de mensagens sem resposta, que e
        # atendimento.
        "mensagem": (
            "queria contratar alguem pra cuidar das redes sociais da loja. seguidor a gente "
            "tem 20 mil, o buraco e que chega uns 100 direct por dia perguntando preco e "
            "prazo e a gente responde uns 10"
        ),
        "esperado": {"agente_indicado": "atendimento"},
    },
    {
        "id": "ag_arm_05",
        "categoria": "agente_armadilha",
        # Ha produto pedido com nome de area, mas nenhuma dor descrita, entao rotular como
        # atendimento seria inferir do produto.
        "mensagem": (
            "quero contratar um chatbot de atendimento pro meu site, igual aquele que vi na "
            "empresa do meu primo. me passa como funciona e quanto custa?"
        ),
        "esperado": {"agente_indicado": "indefinido"},
    },
    {
        "id": "ag_arm_06",
        "categoria": "agente_armadilha",
        # produto pedido e operacional; a dor descrita e lead sem follow-up
        "mensagem": (
            "queria automatizar minha planilha de clientes. o problema real e que a "
            "planilha tem 400 lead que pediram orcamento e ninguem nunca voltou pra eles"
        ),
        "esperado": {"agente_indicado": "comercial"},
    },
    {
        "id": "ag_atd_01",
        "categoria": "agente_atendimento",
        # A dor e volume de mensagens repetidas sem resposta em tempo, que e sobrecarga de
        # atendimento.
        "mensagem": (
            "tenho uma clinica de fisio, chega uns 80 whats por dia perguntando horario, "
            "convenio e valor da sessão. a menina da recepção nao da conta e as vez "
            "responde so no outro dia"
        ),
        "esperado": {"agente_indicado": "atendimento"},
    },
    {
        "id": "ag_atd_02",
        "categoria": "agente_atendimento",
        # A dor e fila de mensagens recorrentes sem resposta, nao ausencia de publico ou de
        # conteudo.
        "mensagem": (
            "meu direct ta com umas 3 semana de acumulo. eu abro, olho, fecho e nao "
            "respondo pq e sempre a mesma pergunta e eu ja to cansado de digitar a mesma "
            "coisa"
        ),
        "esperado": {"agente_indicado": "atendimento"},
    },
    {
        "id": "ag_atd_03",
        "categoria": "agente_atendimento",
        # A dor e o cliente ja comprado ficando sem resposta, o que e suporte e nao venda.
        "mensagem": (
            "vendemos equipamento de cozinha industrial e o pos venda ta um caos. cliente "
            "manda duvida de uso e a gente leva 2 dia pra retornar, ja apareceu reclamação "
            "no google por causa disso"
        ),
        "esperado": {"agente_indicado": "atendimento"},
    },
    {
        "id": "ag_atd_04",
        "categoria": "agente_atendimento",
        # A dor e janela de silencio e acumulo de mensagens, um problema de cobertura de
        # atendimento.
        "mensagem": (
            "sabado e domingo nao tem ninguem aqui pra responder nada, ai na segunda tem "
            "umas 200 mensagem esperando. o pessoal ja fala que a gente some no fim de "
            "semana"
        ),
        "esperado": {"agente_indicado": "atendimento"},
    },
    {
        "id": "ag_atd_05",
        "categoria": "agente_atendimento",
        # A dor e a demanda de resposta durante o pedido em curso, tipica de atendimento e nao de
        # processo interno.
        "mensagem": (
            "delivery aqui e por whats mesmo. o cliente manda o pedido, depois pergunta se "
            "ja saiu, ninguem responde pq ta todo mundo na cozinha, ai ele liga irritado no "
            "meio do movimento"
        ),
        "esperado": {"agente_indicado": "atendimento"},
    },
    {
        "id": "ag_com_01",
        "categoria": "agente_comercial",
        # a dor e o follow-up que ninguem fez, nao o tempo de produzir a proposta
        "mensagem": (
            "tenho uma revenda de maquina de corte. mando a proposta na sexta e so lembro "
            "de cobrar resposta uma semana depois. quando ligo o cara ja comprou de outro"
        ),
        "esperado": {"agente_indicado": "comercial"},
    },
    {
        "id": "ag_com_02",
        "categoria": "agente_comercial",
        # A dor e o abandono do lead depois do interesse demonstrado, ou seja, perda por falta de
        # acompanhamento comercial.
        "mensagem": (
            "sou dona de imobiliaria. a pessoa visita o imovel, gosta, e depois disso "
            "ninguem liga de volta pra ela. mes passado escapou dois negocio desse jeito"
        ),
        "esperado": {"agente_indicado": "comercial"},
    },
    {
        "id": "ag_com_03",
        "categoria": "agente_comercial",
        # A dor e negociacao aberta esfriando sem que ninguem note, que e perda de oportunidade em
        # andamento.
        "mensagem": (
            "montei um time de 3 pra prospectar e ninguem sabe me dizer em que pe ta cada "
            "negociação. tem cliente que sumiu faz uns 2 mes e ninguem percebeu que ele "
            "tinha sumido"
        ),
        "esperado": {"agente_indicado": "comercial"},
    },
    {
        "id": "ag_com_04",
        "categoria": "agente_comercial",
        # A dor e a negociacao interrompida na objeacao de preco sem retomada, que e trabalho de
        # reengajamento comercial.
        "mensagem": (
            "quando o cliente fala que ta caro a conversa morre ali e ninguem volta a falar "
            "com ele nunca mais. deve ter uns 200 parado desse jeito no meu caderno"
        ),
        "esperado": {"agente_indicado": "comercial"},
    },
    {
        "id": "ag_com_05",
        "categoria": "agente_comercial",
        # A dor esta no avanco da venda ate o fechamento, e o proprio lead descarta atendimento
        # como problema.
        "mensagem": (
            "a gente atende bem, responde rapido, o pessoal elogia. so que na hora de puxar "
            "pro fechamento ninguem puxa, fica todo mundo esperando o cliente decidir "
            "sozinho"
        ),
        "esperado": {"agente_indicado": "comercial"},
    },
    {
        "id": "ag_ind_01",
        "categoria": "agente_indefinido",
        # Ha interesse declarado mas nenhuma dor descrita, entao qualquer rotulo seria chute.
        "mensagem": (
            "boa tarde! vi o trabalho de voces pelo linkedin de um amigo e achei bem "
            "interessante o que faz. queria entender melhor como funciona pra ver se faz "
            "sentido pra gente aqui"
        ),
        "esperado": {"agente_indicado": "indefinido"},
    },
    {
        "id": "ag_ind_02",
        "categoria": "agente_indefinido",
        # Formulario preenchido com pedido generico de informacao, sem nenhum problema descrito.
        "mensagem": (
            "Nome: Ricardo Alves / Empresa: RC Distribuidora de Bebidas / Mensagem: "
            "gostaria de receber mais informações sobre os serviços prestados e a tabela de "
            "valores. Atenciosamente"
        ),
        "esperado": {"agente_indicado": "indefinido"},
    },
    {
        "id": "ag_ind_03",
        "categoria": "agente_indefinido",
        # Sem operacao rodando nao existe dor concreta descrita, so intencao preventiva vaga.
        "mensagem": (
            "to abrindo uma empresa de importação, ainda nao comecei a operar. quero ja "
            "deixar tudo redondo desde o comeco pra nao ter dor de cabeca depois. como "
            "voces trabalham?"
        ),
        "esperado": {"agente_indicado": "indefinido"},
    },
    {
        "id": "ag_ind_04",
        "categoria": "agente_indefinido",
        # O contato e por indicacao de terceiro e o proprio lead nao sabe qual e o problema, entao
        # nao ha sinal.
        "mensagem": (
            "meu socio falou que voces resolveram um problema serio na empresa do primo "
            "dele e mandou eu chamar aqui. sinceramente eu nem sei direito o que voces "
            "fazem, ele que entende disso"
        ),
        "esperado": {"agente_indicado": "indefinido"},
    },
    {
        "id": "ag_ind_05",
        "categoria": "agente_indefinido",
        # Desorganizacao generica nao aponta area nenhuma; falta o fato concreto que sustentaria
        # um rotulo.
        "mensagem": (
            "a gente cresceu bastante nos ultimo 2 ano e ficou tudo meio desorganizado, "
            "sinto que da pra melhorar muita coisa. voces conseguem me ajudar nisso?"
        ),
        "esperado": {"agente_indicado": "indefinido"},
    },
    {
        "id": "ag_mkt_01",
        "categoria": "agente_marketing",
        # A dor e ausencia de gente nova chegando por desconhecimento da marca, ou seja, falta de
        # presenca e conteudo.
        "mensagem": (
            "tenho um petshop no bairro ha 6 anos e gente que mora a 3 quadra daqui nao "
            "sabe que existe. so entra cliente antigo, novo mesmo nao aparece"
        ),
        "esperado": {"agente_indicado": "marketing"},
    },
    {
        "id": "ag_mkt_02",
        "categoria": "agente_marketing",
        # A dor e a producao de conteudo parada secando a entrada de contatos, causa tipicamente
        # de marketing.
        "mensagem": (
            "a gente parou de postar em fevereiro porque ninguem aqui tem tempo de sentar e "
            "produzir. de la pra ca nao chegou mais nenhum contato novo, so os de sempre"
        ),
        "esperado": {"agente_indicado": "marketing"},
    },
    {
        "id": "ag_mkt_03",
        "categoria": "agente_marketing",
        # A dor e a dependencia de boca a boca sem canal proprio de atracao, que e geracao de
        # demanda.
        "mensagem": (
            "meu escritorio de contabilidade so cresce por indicação. quando a indicação "
            "seca o mes morre, pq nao tem nada trazendo gente de fora pra dentro"
        ),
        "esperado": {"agente_indicado": "marketing"},
    },
    {
        "id": "ag_mkt_04",
        "categoria": "agente_marketing",
        # A dor e falta de reconhecimento em praca nova, resolvida por posicionamento e
        # divulgacao.
        "mensagem": (
            "abri a segunda unidade em outra cidade e la ninguem me conhece. na primeira "
            "era 10 ano de boca a boca, aqui to comecando do zero e o salão fica vazio de "
            "terça"
        ),
        "esperado": {"agente_indicado": "marketing"},
    },
    {
        "id": "ag_mkt_05",
        "categoria": "agente_marketing",
        # A dor e mensagem e conteudo que nao comunicam a oferta, nao volume de atendimento nem
        # processo interno.
        "mensagem": (
            "a gente ate tem foto boa dos produto, mas ninguem escreve nada junto. quem cai "
            "na pagina olha e vai embora sem entender o que a gente faz de verdade"
        ),
        "esperado": {"agente_indicado": "marketing"},
    },
    {
        "id": "ag_ope_01",
        "categoria": "agente_operacional",
        # A dor e tarefa repetitiva de transporte de dados feita a mao, sem envolver lead ou
        # cliente.
        "mensagem": (
            "toda segunda eu gasto umas 4h copiando as venda do sistema pra uma planilha "
            "pra mandar pro contador. e sempre a mesma coisa, todo santo mes"
        ),
        "esperado": {"agente_indicado": "operacional"},
    },
    {
        "id": "ag_ope_02",
        "categoria": "agente_operacional",
        # A dor e documento manual repetido com erro de digitacao, um gargalo de processo interno.
        "mensagem": (
            "meu juridico monta contrato um por um, muda so nome, cpf e valor. mes passado "
            "foi cpf trocado em dois e deu retrabalho pra caramba"
        ),
        "esperado": {"agente_indicado": "operacional"},
    },
    {
        "id": "ag_ope_03",
        "categoria": "agente_operacional",
        # A dor e montagem manual de documento consolidando fontes, tarefa operacional repetitiva.
        "mensagem": (
            "cada obra gera um relatorio que a engenheira monta na mao, juntando foto que "
            "chega no zap com a planilha de medição. leva o dia inteiro dela e ela deveria "
            "ta em campo"
        ),
        "esperado": {"agente_indicado": "operacional"},
    },
    {
        "id": "ag_ope_04",
        "categoria": "agente_operacional",
        # A dor e digitacao manual de documento em sistema, com erro decorrente do proprio
        # processo.
        "mensagem": (
            "recebo nota em pdf de uns 40 fornecedor por mes e alguem daqui digita item por "
            "item no erp. ja aconteceu de lançar quantidade errada e a gente so descobrir "
            "no inventario"
        ),
        "esperado": {"agente_indicado": "operacional"},
    },
    {
        "id": "ag_ope_05",
        "categoria": "agente_operacional",
        # A dor e retrabalho de cadastro duplicado entre sistemas, nao a venda em si que ja foi
        # fechada.
        "mensagem": (
            "toda vez que fecha um contrato alguem tem que cadastrar o mesmo cliente em 3 "
            "lugar diferente, e sempre esquecem um. dai o financeiro cobra errado"
        ),
        "esperado": {"agente_indicado": "operacional"},
    },
]

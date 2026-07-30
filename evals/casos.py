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
]

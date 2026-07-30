"""
Lead triage agent — the first concrete agent built on the shared base.
Agente de triagem de lead — o primeiro agente concreto sobre a base compartilhada.
"""

from typing import Any

from agents.lead_triage.scoring import classificar_lead, pontuar_enriquecimento
from agents.lead_triage.signals import MensagemEnricher, pontuar_sinais
from core.base_agent import BaseAgent
from core.base_enricher import enriquecer

# Régua e pesos ficam aqui por enquanto; vêm da config do tenant depois.
# Thresholds and weights live here for now; they'll come from tenant config.
REGUA_PADRAO = {"quente": 70, "morno": 40}

PESOS_PADRAO = {
    "empresa": {"site": 25, "youtube": 15, "github": 10},
    "pessoa": {"github": 25, "youtube": 20, "site": 10},
}

# Peso negativo é proposital: quem pede pra sair da lista não pode pontuar,
# por mais bonito que seja o site da empresa.
PESOS_SINAIS = {
    "orcamento": 25,
    "urgencia": 20,
    "autoridade": 15,
    "descadastro": -100,
}


class LeadTriageAgent(BaseAgent):
    """Recebe uma mensagem do lead e devolve a classificação quente/morno/frio."""

    def __init__(self, tenant_id: str, cliente: Any = None):
        super().__init__(tenant_id)
        # Costura para teste: repassada ao MensagemEnricher.
        # Test seam: handed down to MensagemEnricher.
        self._cliente = cliente

    def handle(
        self,
        message: str,
        lead_id: str,
        enriquecimento: list[dict] | None = None,
        tipo_lead: str = "empresa",
    ) -> dict:
        """
        Cumpre o contrato da base: entra mensagem + lead_id, sai resultado padronizado.
        Fulfills the base contract: message + lead_id in, standard result out.

        A nota soma duas origens: o que a pessoa DISSE (sinais da mensagem) e o
        que ela É (enriquecimento). Dizer pesa mais que existir na internet.
        """
        pontos_ext, obs_ext = pontuar_enriquecimento(
            enriquecimento or [], tipo_lead, PESOS_PADRAO
        )

        # enriquecer() envolve a chamada em try/except: LLM fora do ar vira
        # status 'falha' e o lead continua sendo atendido.
        resultado_msg = enriquecer(message, [MensagemEnricher(cliente=self._cliente)])[0]
        pontos_msg, obs_msg = pontuar_sinais(resultado_msg, PESOS_SINAIS)

        pontos = max(pontos_ext + pontos_msg, 0)

        return {
            "lead_id": lead_id,
            "pontos": pontos,
            "classificacao": classificar_lead(pontos, REGUA_PADRAO),
            "observacoes": obs_msg + obs_ext,
        }

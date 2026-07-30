"""
Lead triage agent — the first concrete agent built on the shared base.
Agente de triagem de lead — o primeiro agente concreto sobre a base compartilhada.
"""

from core.base_agent import BaseAgent
from agents.lead_triage.scoring import classificar_lead


class LeadTriageAgent(BaseAgent):
    """Recebe uma mensagem do lead e devolve a classificação quente/morno/frio."""

    def handle(self, message: str, lead_id: str) -> dict:
        """
        Cumpre o contrato da base: entra mensagem + lead_id, sai resultado padronizado.
        Fulfills the base contract: message + lead_id in, standard result out.
        """
        # STUB temporário — será substituído pela extração de sinais via LLM.
        pontos = 75

        # régua fixa por enquanto; virá da config do tenant.
        regua = {"quente": 70, "morno": 40}

        return {
            "lead_id": lead_id,
            "pontos": pontos,
            "classificacao": classificar_lead(pontos, regua),
        }

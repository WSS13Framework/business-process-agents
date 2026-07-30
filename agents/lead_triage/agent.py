"""
Lead triage agent — the first concrete agent built on the shared base.
Agente de triagem de lead — o primeiro agente concreto sobre a base compartilhada.
"""

from core.base_agent import BaseAgent
from agents.lead_triage.scoring import classificar_lead, pontuar_enriquecimento

# Régua e pesos ficam aqui por enquanto; vêm da config do tenant depois.
# Thresholds and weights live here for now; they'll come from tenant config.
REGUA_PADRAO = {"quente": 70, "morno": 40}

PESOS_PADRAO = {
    "empresa": {"site": 25, "youtube": 15, "github": 10},
    "pessoa": {"github": 25, "youtube": 20, "site": 10},
}


class LeadTriageAgent(BaseAgent):
    """Recebe uma mensagem do lead e devolve a classificação quente/morno/frio."""

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

        Sem enriquecimento a pontuação é zero — o agente não inventa sinal que
        não tem. With no enrichment the score is zero: no faking signal.
        """
        pontos, observacoes = pontuar_enriquecimento(
            enriquecimento or [], tipo_lead, PESOS_PADRAO
        )

        return {
            "lead_id": lead_id,
            "pontos": pontos,
            "classificacao": classificar_lead(pontos, REGUA_PADRAO),
            "observacoes": observacoes,
        }

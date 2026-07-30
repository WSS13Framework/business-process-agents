"""
Base Agent — the shared foundation every agent inherits from.
Agente Base — a fundação compartilhada que todo agente herda.
"""

from abc import ABC, abstractmethod


class BaseAgent(ABC):
    """Contrato comum: todo agente recebe uma entrada e devolve um resultado."""

    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id

    @abstractmethod
    def handle(self, message: str, lead_id: str) -> dict:
        """
        Contrato: todo agente DEVE implementar 'handle'.
        Recebe uma mensagem + o ID do lead, devolve um resultado padronizado.
        Contract: every agent MUST implement 'handle'.
        """
        ...

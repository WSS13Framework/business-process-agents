"""
Testa a classificação de lead — prova que quente/morno/frio funciona.
Tests lead classification — proves hot/warm/cold works.
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from agents.lead_triage.scoring import classificar_lead

# régua de exemplo (na vida real vem da config do cliente)
regua = {"quente": 70, "morno": 40}

# testa os três casos
print("Lead com 85 pontos:", classificar_lead(85, regua))
print("Lead com 55 pontos:", classificar_lead(55, regua))
print("Lead com 20 pontos:", classificar_lead(20, regua))
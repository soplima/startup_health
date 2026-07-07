from app.benchmarks import get_benchmarks
from app.kpis.utils import status


def compute_financial_kpis(current, previous, sector):
    b = get_benchmarks(sector)
    indicators = []

    # Crescimento do MRR
    growth_rate = (
        ((current.mrr - previous.mrr) / previous.mrr) * 100 if previous.mrr else 0.0
    )

    indicators.append(
        {
            "label": "Crescimento do MRR",
            "value": round(growth_rate, 1),
            "unit": "%",
            "status": (
                "good" if growth_rate > 5 else "warn" if growth_rate > 2 else "bad"
            ),
            "note": (
                "Ritmo saudável"
                if growth_rate > 5
                else "Desacelerando"
                if growth_rate > 2
                else "Crescimento estagnado"
            ),
        }
    )

    # Burn Multiple
    net_new_arr = (current.mrr - previous.mrr) * 12

    burn_multiple = current.monthly_burn / net_new_arr if net_new_arr > 0 else 99.0

    burn_status = status(
        burn_multiple,
        b["burn_multiple_good"],
        b["burn_multiple_ok"],
        False,
    )

    indicators.append(
        {
            "label": "Múltiplo de Queima (Burn Multiple)",
            "value": round(burn_multiple, 1),
            "unit": "x",
            "status": burn_status,
            "note": {
                "good": "Queima eficiente",
                "warn": "Monitore de perto",
                "bad": "Queimando muito rápido para o crescimento",
            }[burn_status],
        }
    )

    # Runway

    runway = (
        current.cash_balance / current.monthly_burn if current.monthly_burn else 0.0
    )

    runway_status = status(
        runway,
        b["runway_good"],
        b["runway_ok"],
        True,
    )

    indicators.append(
        {
            "label": "Runway (Tempo de Caixa)",
            "value": round(runway, 1),
            "unit": "meses",
            "status": runway_status,
            "note": {
                "good": "Confortável",
                "warn": "Planeje uma captação em breve",
                "bad": "Urgente, aja agora",
            }[runway_status],
        }
    )

    return indicators

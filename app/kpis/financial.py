from app.benchmarks import get_benchmarks
from app.kpis.utils import status


def compute_financial_kpis(current, previous, sector):
    b = get_benchmarks(sector)
    indicators = []

    arr = current.mrr * 12

    indicators.append(
        {
            "label": "ARR",
            "value": round(arr, 2),
            "unit": "R$",
            "status": "good",
            "note": "Receita recorrente anualizada",
        }
    )

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

    net_new_arr = (current.mrr - previous.mrr) * 12

    burn_multiple = current.monthly_burn / net_new_arr if net_new_arr > 0 else 99.0

    burn_status = status(
        burn_multiple,
        b["burn_multiple_good"],
        b["burn_multiple_ok"],
        False,
    )

    if current.ebitda_margin is not None:
        rule_of_40 = growth_rate + current.ebitda_margin

    rule40_status = status(
        rule_of_40,
        b["rule40_good"],
        b["rule40_ok"],
        higher_is_better=True,
    )

    indicators.append(
        {
            "label": "Rule of 40",
            "value": round(rule_of_40, 1),
            "unit": "%",
            "status": rule40_status,
            "note": {
                "good": "Acima da referência do setor",
                "warn": "Próximo da referência do setor",
                "bad": "Abaixo da referência do setor",
            }[rule40_status],
        }
    )

    # Burn Rate
    burn_rate_status = status(
        current.monthly_burn,
        b["burn_rate_good"],
        b["burn_rate_ok"],
        higher_is_better=False,
    )

    indicators.append(
        {
            "label": "Burn Rate/ Mensal",
            "value": round(current.monthly_burn, 2),
            "unit": "R$",
            "status": burn_rate_status,
            "note": {
                "good": "Queima controlada",
                "warn": "Monitore os gastos",
                "bad": "Queima elevada",
            }[burn_rate_status],
        }
    )

    # Gross Margin
    gross_margin_status = status(
        current.gross_margin,
        80,
        70,
        True,
    )

    indicators.append(
        {
            "label": "Gross Margin",
            "value": round(current.gross_margin, 1),
            "unit": "%",
            "status": gross_margin_status,
            "note": {
                "good": "Margem saudável",
                "warn": "Margem aceitável",
                "bad": "Margem baixa",
            }[gross_margin_status],
        }
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

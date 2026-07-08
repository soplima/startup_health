from app.benchmarks import get_benchmarks
from app.kpis.utils import status


def compute_sales_kpis(current, previous, sector):
    b = get_benchmarks(sector)

    indicators = []

    if current.total_customers:
        avg_account_revenue = current.mrr / current.total_customers
    elif current.new_customers:
        avg_account_revenue = current.mrr / (current.new_customers * 8)
    else:
        avg_account_revenue = 0.0

    cac = current.sales_spend / current.new_customers if current.new_customers else 0.0

    cac_payback = (
        cac / (avg_account_revenue * (current.gross_margin / 100))
        if avg_account_revenue
        else 0.0
    )

    cac_status = status(
        cac_payback,
        b["cac_payback_good"],
        b["cac_payback_ok"],
        higher_is_better=False,
    )

    indicators.append(
        {
            "label": "Meses para Payback do CAC",
            "value": round(cac_payback, 1),
            "unit": "meses",
            "status": cac_status,
            "note": {
                "good": "Mais rápido que a mediana do setor",
                "warn": "Próximo à mediana do setor",
                "bad": "Mais lento que a mediana do setor",
            }[cac_status],
            "category": "sales",
        }
    )

    monthly_churn_rate = current.mrr_churned / previous.mrr if previous.mrr else 0.0

    ltv = (
        (avg_account_revenue * (current.gross_margin / 100)) / monthly_churn_rate
        if monthly_churn_rate
        else 0.0
    )

    ltv_cac = ltv / cac if cac else 0.0

    ltv_status = status(
        ltv_cac,
        b["ltv_cac_good"],
        b["ltv_cac_ok"],
        higher_is_better=True,
    )

    indicators.append(
        {
            "label": "Proporção LTV para CAC",
            "value": round(ltv_cac, 1),
            "unit": "x",
            "status": ltv_status,
            "note": {
                "good": "Economia unitária forte",
                "warn": "Viável, mas margem estreita",
                "bad": "Economia unitária fraca",
            }[ltv_status],
            "category": "sales",
        }
    )

    channels = [
        (
            "Google Ads",
            current.google_ads_spend,
            current.google_customers,
        ),
        (
            "Meta Ads",
            current.meta_ads_spend,
            current.meta_customers,
        ),
        (
            "Outbound",
            current.outbound_spend,
            current.outbound_customers,
        ),
    ]

    for name, spend, customers in channels:
        channel_cac = spend / customers if customers else 0.0

        channel_status = status(
            channel_cac,
            b["cac_channel_good"],
            b["cac_channel_ok"],
            higher_is_better=False,
        )

        indicators.append(
            {
                "label": f"CAC - {name}",
                "value": round(channel_cac, 2),
                "unit": "R$",
                "status": channel_status,
                "note": {
                    "good": "Aquisição eficiente",
                    "warn": "Monitorar custo",
                    "bad": "Aquisição cara",
                }[channel_status],
                "category": "sales",
            }
        )

    funnel_conversion = (
        current.deals_won / current.leads * 100 if current.leads else 0.0
    )

    funnel_status = status(
        funnel_conversion,
        b["funnel_conversion_good"],
        b["funnel_conversion_ok"],
        higher_is_better=True,
    )

    indicators.append(
        {
            "label": "Conversão do Funil",
            "value": round(funnel_conversion, 1),
            "unit": "%",
            "status": funnel_status,
            "note": {
                "good": "Excelente eficiência comercial",
                "warn": "Conversão aceitável",
                "bad": "Baixa conversão",
            }[funnel_status],
            "category": "sales",
        }
    )

    cycle_status = status(
        current.avg_sales_cycle_days,
        b["sales_cycle_good"],
        b["sales_cycle_ok"],
        higher_is_better=False,
    )

    indicators.append(
        {
            "label": "Ciclo Médio de Vendas",
            "value": round(current.avg_sales_cycle_days, 1),
            "unit": "dias",
            "status": cycle_status,
            "note": {
                "good": "Fechamento rápido",
                "warn": "Dentro do esperado",
                "bad": "Ciclo longo",
            }[cycle_status],
            "category": "sales",
        }
    )

    total_closed = current.deals_won + current.deals_lost

    win_rate = current.deals_won / total_closed * 100 if total_closed else 0.0

    win_status = status(
        win_rate,
        b["win_rate_good"],
        b["win_rate_ok"],
        higher_is_better=True,
    )

    indicators.append(
        {
            "label": "Win Rate",
            "value": round(win_rate, 1),
            "unit": "%",
            "status": win_status,
            "note": {
                "good": "Equipe comercial eficiente",
                "warn": "Taxa razoável",
                "bad": "Poucos negócios fechados",
            }[win_status],
            "category": "sales",
        }
    )

    return indicators

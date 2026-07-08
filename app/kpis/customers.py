from app.benchmarks import get_benchmarks
from app.kpis.utils import status


def compute_customer_kpis(current, previous, sector):
    b = get_benchmarks(sector)

    indicators = []

    # Clientes ativos
    indicators.append(
        {
            "label": "Clientes Ativos",
            "value": current.total_customers or 0,
            "unit": "",
            "status": "good",
            "note": "Total de clientes ativos no mês",
            "category": "customers",
        }
    )

    # Novos clientes
    indicators.append(
        {
            "label": "Novos Clientes",
            "value": current.new_customers,
            "unit": "",
            "status": "good",
            "note": "Clientes adquiridos no mês",
            "category": "customers",
        }
    )

    # Clientes perdidos
    lost_customers = None

    if previous.total_customers is not None and current.total_customers is not None:
        lost_customers = max(
            previous.total_customers + current.new_customers - current.total_customers,
            0,
        )

        indicators.append(
            {
                "label": "Clientes Perdidos",
                "value": lost_customers,
                "unit": "",
                "status": "good",
                "note": "Clientes cancelados no mês",
                "category": "customers",
            }
        )

        # Customer Churn
        customer_churn = (
            (lost_customers / previous.total_customers) * 100
            if previous.total_customers
            else 0.0
        )

        customer_churn_status = status(
            customer_churn,
            2,
            5,
            higher_is_better=False,
        )

        indicators.append(
            {
                "label": "Churn de Clientes",
                "value": round(customer_churn, 1),
                "unit": "%",
                "status": customer_churn_status,
                "note": {
                    "good": "Baixa perda de clientes",
                    "warn": "Perda moderada de clientes",
                    "bad": "Churn elevado",
                }[customer_churn_status],
                "category": "customers",
            }
        )

    # Revenue Churn
    revenue_churn = (current.mrr_churned / previous.mrr) * 100 if previous.mrr else 0.0

    revenue_churn_status = status(
        revenue_churn,
        1,
        3,
        higher_is_better=False,
    )

    indicators.append(
        {
            "label": "Churn de Receita",
            "value": round(revenue_churn, 1),
            "unit": "%",
            "status": revenue_churn_status,
            "note": {
                "good": "Baixa perda de receita",
                "warn": "Perda moderada de receita",
                "bad": "Perda elevada de receita",
            }[revenue_churn_status],
            "category": "customers",
        }
    )

    # Net Revenue Retention (NRR)
    nrr = (
        (previous.mrr - current.mrr_churned + current.mrr_expansion)
        / previous.mrr
        * 100
        if previous.mrr
        else 0.0
    )

    nrr_status = status(
        nrr,
        b["nrr_good"],
        b["nrr_ok"],
        higher_is_better=True,
    )

    indicators.append(
        {
            "label": "Retenção Líquida (NRR)",
            "value": round(nrr, 1),
            "unit": "%",
            "status": nrr_status,
            "note": {
                "good": "Acima da referência do setor",
                "warn": "Próximo da referência do setor",
                "bad": "Abaixo da referência do setor",
            }[nrr_status],
            "category": "customers",
        }
    )

    return indicators

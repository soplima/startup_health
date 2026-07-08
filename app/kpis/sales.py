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

    # CAC Payback

    cac_payback = (
        cac / (avg_account_revenue * (current.gross_margin / 100))
        if avg_account_revenue
        else 0.0
    )

    cac_status = status(
        cac_payback,
        b["cac_payback_good"],
        b["cac_payback_ok"],
        False,
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
        True,
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

    return indicators

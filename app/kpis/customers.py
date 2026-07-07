from app.benchmarks import get_benchmarks
from app.kpis.utils import status


def compute_customer_kpis(current, previous, sector):
    b = get_benchmarks(sector)

    indicators = []

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
        True,
    )

    indicators.append(
        {
            "label": "Retenção Líquida (NRR)",
            "value": round(nrr, 1),
            "unit": "%",
            "status": nrr_status,
            "note": {
                "good": "Acima da mediana do setor",
                "warn": "Próximo à mediana do setor",
                "bad": "Abaixo da mediana do setor",
            }[nrr_status],
        }
    )

    return indicators

from app.benchmarks import get_benchmarks


def _status(
    value: float, good_threshold: float, ok_threshold: float, higher_is_better: bool
) -> str:
    if higher_is_better:
        if value >= good_threshold:
            return "good"
        if value >= ok_threshold:
            return "warn"
        return "bad"
    else:
        if value <= good_threshold:
            return "good"
        if value <= ok_threshold:
            return "warn"
        return "bad"


def compute_kpis(current, previous, sector: str) -> list[dict]:
    """
    current / previous: Metric ORM objects (or anything with the same attributes).
    previous is the prior month's snapshot, used to compute growth and deltas.
    Returns a list of dicts matching the KPIIndicator schema.
    """
    b = get_benchmarks(sector)
    indicators = []

    # 1. Crescimento do MRR
    growth_rate = (
        ((current.mrr - previous.mrr) / previous.mrr) * 100 if previous.mrr else 0.0
    )
    indicators.append(
        {
            "label": "Crescimento do MRR",
            "value": round(growth_rate, 1),
            "unit": "%",
            "status": "good"
            if growth_rate > 5
            else "warn"
            if growth_rate > 2
            else "bad",
            "note": "Ritmo saudável"
            if growth_rate > 5
            else "Desacelerando"
            if growth_rate > 2
            else "Crescimento estagnado",
        }
    )

    # 2. Retenção Líquida de Receita (NRR)
    nrr = (
        ((previous.mrr - current.mrr_churned + current.mrr_expansion) / previous.mrr)
        * 100
        if previous.mrr
        else 0.0
    )
    nrr_status = _status(nrr, b["nrr_good"], b["nrr_ok"], higher_is_better=True)
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

    # Média de receita por conta (ARPU) para cálculos internos
    if current.total_customers:
        avg_account_revenue = current.mrr / current.total_customers
    elif current.new_customers:
        avg_account_revenue = current.mrr / (current.new_customers * 8)
    else:
        avg_account_revenue = 0.0

    # 3. CAC Payback
    cac = current.sales_spend / current.new_customers if current.new_customers else 0.0
    cac_payback = (
        cac / (avg_account_revenue * (current.gross_margin / 100))
        if avg_account_revenue
        else 0.0
    )
    cac_status = _status(
        cac_payback, b["cac_payback_good"], b["cac_payback_ok"], higher_is_better=False
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
        }
    )

    # 4. Relação LTV:CAC
    monthly_churn_rate = current.mrr_churned / previous.mrr if previous.mrr else 0.0
    ltv = (
        (avg_account_revenue * (current.gross_margin / 100)) / monthly_churn_rate
        if monthly_churn_rate
        else 0.0
    )
    ltv_cac = ltv / cac if cac else 0.0
    ltv_status = _status(
        ltv_cac, b["ltv_cac_good"], b["ltv_cac_ok"], higher_is_better=True
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
        }
    )

    # 5. Múltiplo de Queima (Burn Multiple)
    net_new_arr = (current.mrr - previous.mrr) * 12
    burn_multiple = current.monthly_burn / net_new_arr if net_new_arr > 0 else 99.0
    burn_status = _status(
        burn_multiple,
        b["burn_multiple_good"],
        b["burn_multiple_ok"],
        higher_is_better=False,
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

    # 6. Runway
    runway = (
        current.cash_balance / current.monthly_burn if current.monthly_burn else 0.0
    )
    runway_status = _status(
        runway, b["runway_good"], b["runway_ok"], higher_is_better=True
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

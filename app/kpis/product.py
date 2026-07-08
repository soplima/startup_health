from app.benchmarks import get_benchmarks
from app.kpis.utils import status


def compute_product_kpis(current, previous, sector):
    b = get_benchmarks(sector)

    indicators = []

    # DAU / MAU

    dau_mau = (
        current.daily_active_users / current.monthly_active_users * 100
        if current.monthly_active_users
        else 0.0
    )

    dau_mau_status = status(
        dau_mau,
        b["dau_mau_good"],
        b["dau_mau_ok"],
        True,
    )

    indicators.append(
        {
            "label": "DAU / MAU",
            "value": round(dau_mau, 1),
            "unit": "%",
            "status": dau_mau_status,
            "note": {
                "good": "Excelente engajamento dos usuários",
                "warn": "Engajamento moderado",
                "bad": "Baixo nível de usuários recorrentes",
            }[dau_mau_status],
            "category": "product",
        }
    )

    # Activation Rate

    activation_rate = (
        current.activated_users / current.new_signups * 100
        if current.new_signups
        else 0.0
    )

    activation_status = status(
        activation_rate,
        b["activation_good"],
        b["activation_ok"],
        True,
    )

    indicators.append(
        {
            "label": "Activation Rate",
            "value": round(activation_rate, 1),
            "unit": "%",
            "status": activation_status,
            "note": {
                "good": "Usuários alcançam valor rapidamente",
                "warn": "Ativação razoável",
                "bad": "Poucos usuários ativam o produto",
            }[activation_status],
            "category": "product",
        }
    )

    # Trial → Paid Conversion

    trial_conversion = (
        current.paid_conversions / current.trial_users * 100
        if current.trial_users
        else 0.0
    )

    trial_status = status(
        trial_conversion,
        b["trial_conversion_good"],
        b["trial_conversion_ok"],
        True,
    )

    indicators.append(
        {
            "label": "Trial → Paid",
            "value": round(trial_conversion, 1),
            "unit": "%",
            "status": trial_status,
            "note": {
                "good": "Alta conversão para clientes pagantes",
                "warn": "Conversão dentro do esperado",
                "bad": "Baixa conversão do trial",
            }[trial_status],
            "category": "product",
        }
    )

    # Time to First Value

    time_to_value = current.avg_time_to_value_days

    ttfv_status = status(
        time_to_value,
        b["time_to_value_good"],
        b["time_to_value_ok"],
        False,
    )

    indicators.append(
        {
            "label": "Time to First Value",
            "value": round(time_to_value, 1),
            "unit": "dias",
            "status": ttfv_status,
            "note": {
                "good": "Usuários encontram valor rapidamente",
                "warn": "Tempo aceitável",
                "bad": "Demora para entregar valor ao usuário",
            }[ttfv_status],
            "category": "product",
        }
    )

    return indicators

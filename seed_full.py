import requests
from datetime import date
from dateutil.relativedelta import relativedelta


BASE = "http://localhost:8000"


# Cria empresa

company = requests.post(
    f"{BASE}/companies",
    json={
        "name": "HealthFlow",
        "sector": "saas",
        "stage": "pre_seed",
    },
).json()

company_id = company["id"]

print("Empresa criada:", company_id)


# Cria 33 meses de métricas para teste

month = date(2024, 1, 1)

for i in range(33):
    mrr = 3000 + (i * 1800)

    customers = 20 + (i * 8)

    response = requests.post(
        f"{BASE}/companies/{company_id}/metrics",
        json={
            "month": month.isoformat(),
            # financeiro
            "mrr": mrr,
            "mrr_churned": mrr * 0.02,
            "mrr_expansion": mrr * 0.05,
            "cash_balance": 150000 - (i * 2500),
            "monthly_burn": 12000 - (i * 100),
            "gross_margin": 78,
            "ebitda_margin": -40 + i,
            # clientes
            "new_customers": 5 + i,
            "total_customers": customers,
            # produto
            "daily_active_users": int(customers * 0.4),
            "monthly_active_users": int(customers * 0.75),
            "activated_users": int(customers * 0.6),
            "new_signups": customers + 10,
            "trial_users": 30 + i,
            "paid_conversions": 5 + i,
            "avg_time_to_value_days": max(2, 15 - i * 0.2),
            # vendas
            "leads": 100 + i * 20,
            "qualified_leads": 40 + i * 8,
            "opportunities": 20 + i * 5,
            "deals_won": 5 + i,
            "deals_lost": 3,
            "avg_sales_cycle_days": 45 - i * 0.5,
            # aquisição
            "google_ads_spend": 2000 + i * 100,
            "google_customers": 5 + i,
            "meta_ads_spend": 1000 + i * 80,
            "meta_customers": 3 + i,
            "outbound_spend": 800,
            "outbound_customers": 2 + i,
        },
    )

    print("Metric:", month)

    month += relativedelta(months=1)


# Cria clientes para heatmap

cohorts = {
    "2024-01-01": 8,
    "2024-04-01": 8,
    "2024-07-01": 7,
    "2024-10-01": 6,
    "2025-01-01": 6,
    "2025-04-01": 5,
    "2025-07-01": 4,
    "2025-10-01": 3,
    "2026-01-01": 2,
    "2026-04-01": 1,
}


customers = []

counter = 1


for signup_month, amount in cohorts.items():
    for _ in range(amount):
        customer = requests.post(
            f"{BASE}/companies/{company_id}/customers",
            json={
                "name": f"Customer {counter}",
                "signup_month": signup_month,
            },
        ).json()

        customers.append(
            {
                "id": customer["id"],
                "signup_month": date.fromisoformat(signup_month),
            }
        )

        counter += 1


print("Clientes:", len(customers))


# Snapshots para retenção

end = date(2026, 9, 1)


for customer in customers:
    signup = customer["signup_month"]

    month = signup

    while month <= end:
        age = (month.year - signup.year) * 12 + month.month - signup.month

        # retenção SaaS realista

        if age == 0:
            active = 1

        elif age <= 3:
            active = 1

        elif age <= 6:
            active = 1 if customer["id"] % 10 < 8 else 0

        elif age <= 12:
            active = 1 if customer["id"] % 10 < 7 else 0

        elif age <= 24:
            active = 1 if customer["id"] % 10 < 6 else 0

        else:
            active = 1 if customer["id"] % 10 < 5 else 0

        requests.post(
            f"{BASE}/customers/{customer['id']}/snapshots",
            json={
                "month": month.isoformat(),
                "active": active,
                "mrr": 250 if active else 0,
            },
        )

        month += relativedelta(months=1)


print("Heatmap criado")
print("Empresa pronta:", company_id)

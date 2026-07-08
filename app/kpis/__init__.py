from app.kpis.financial import compute_financial_kpis
from app.kpis.customers import compute_customer_kpis
from app.kpis.sales import compute_sales_kpis
from app.kpis.product import compute_product_kpis


def compute_kpis(current, previous, sector):
    indicators = []

    indicators.extend(compute_financial_kpis(current, previous, sector))

    indicators.extend(compute_customer_kpis(current, previous, sector))

    indicators.extend(compute_sales_kpis(current, previous, sector))

    indicators.extend(compute_product_kpis(current, previous, sector))

    return indicators

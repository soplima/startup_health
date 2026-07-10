from datetime import date
from typing import Optional, Literal

from pydantic import BaseModel, ConfigDict

Sector = Literal["saas", "marketplace", "hardware", "fintech", "ecommerce"]
Stage = Literal["pre_seed", "seed", "series_a", "series_b", "series_c_plus"]


class CompanyCreate(BaseModel):
    name: str
    sector: Sector
    stage: Stage
    founded_date: Optional[date] = None


class CompanyRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    sector: str
    stage: str
    founded_date: Optional[date] = None


class MetricCreate(BaseModel):
    month: date
    mrr: float
    mrr_churned: float = 0.0
    mrr_expansion: float = 0.0
    new_customers: int = 0
    customers_churned: int = 0
    total_customers: Optional[int] = None
    sales_spend: float = 0.0
    cash_balance: float
    monthly_burn: float
    gross_margin: float = 75.0
    ebitda_margin: Optional[float] = None

    daily_active_users: int = 0
    monthly_active_users: int = 0
    activated_users: int = 0
    new_signups: int = 0
    trial_users: int = 0
    paid_conversions: int = 0
    avg_time_to_value_days: float = 0.0

    leads: int = 0
    qualified_leads: int = 0
    opportunities: int = 0
    deals_won: int = 0
    deals_lost: int = 0
    avg_sales_cycle_days: float = 0.0

    google_ads_spend: float = 0.0
    google_customers: int = 0
    meta_ads_spend: float = 0.0
    meta_customers: int = 0
    outbound_spend: float = 0.0
    outbound_customers: int = 0


class MetricRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    month: date
    mrr: float
    mrr_churned: float
    mrr_expansion: float
    new_customers: int
    customers_churned: int
    total_customers: Optional[int] = None
    sales_spend: float
    cash_balance: float
    monthly_burn: float
    gross_margin: float
    ebitda_margin: Optional[float] = None

    daily_active_users: int
    monthly_active_users: int
    activated_users: int
    new_signups: int
    trial_users: int
    paid_conversions: int
    avg_time_to_value_days: float

    leads: int
    qualified_leads: int
    opportunities: int
    deals_won: int
    deals_lost: int
    avg_sales_cycle_days: float

    google_ads_spend: float
    google_customers: int
    meta_ads_spend: float
    meta_customers: int
    outbound_spend: float
    outbound_customers: int


class KPIIndicator(BaseModel):
    label: str
    value: float
    unit: str
    status: Literal["good", "warn", "bad", "neutral"]
    note: str
    category: str


class KPIResponse(BaseModel):
    company_id: int
    month: date
    sector: str
    indicators: list[KPIIndicator]


class CohortCell(BaseModel):
    month_offset: int
    retention: float


class CohortHeatmapRow(BaseModel):
    cohort_month: date
    cohort_size: int
    cells: list[CohortCell]


class CustomerCreate(BaseModel):
    name: str
    signup_month: date


class CustomerRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    name: str
    signup_month: date


class CustomerSnapshotCreate(BaseModel):
    month: date
    active: int = 1
    mrr: float = 0.0


class CustomerSnapshotRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    customer_id: int
    month: date
    active: int
    mrr: float

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
    total_customers: Optional[int] = None
    sales_spend: float = 0.0
    cash_balance: float
    monthly_burn: float
    gross_margin: float = 75.0


class MetricRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    company_id: int
    month: date
    mrr: float
    mrr_churned: float
    mrr_expansion: float
    new_customers: int
    total_customers: Optional[int] = None
    sales_spend: float
    cash_balance: float
    monthly_burn: float
    gross_margin: float


class KPIIndicator(BaseModel):
    label: str
    value: float
    unit: str
    status: Literal["good", "warn", "bad"]
    note: str


class KPIResponse(BaseModel):
    company_id: int
    month: date
    sector: str
    indicators: list[KPIIndicator]

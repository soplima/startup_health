from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Date,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from app.database import Base


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(
        String,
        nullable=False,
        index=True,
    )

    sector = Column(
        String,
        nullable=False,
        index=True,
    )

    stage = Column(
        String,
        nullable=False,
    )

    founded_date = Column(
        Date,
        nullable=True,
    )

    metrics = relationship(
        "Metric",
        back_populates="company",
        cascade="all, delete-orphan",
        order_by="Metric.month",
    )

    customers = relationship(
        "Customer",
        back_populates="company",
        cascade="all, delete-orphan",
    )


class Metric(Base):
    __tablename__ = "metrics"

    __table_args__ = (
        UniqueConstraint(
            "company_id",
            "month",
            name="uq_company_month",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    month = Column(
        Date,
        nullable=False,
    )

    mrr = Column(
        Float,
        nullable=False,
    )

    mrr_churned = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    mrr_expansion = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    sales_spend = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    cash_balance = Column(
        Float,
        nullable=False,
    )

    monthly_burn = Column(
        Float,
        nullable=False,
    )

    gross_margin = Column(
        Float,
        nullable=False,
        default=75.0,
    )

    ebitda_margin = Column(
        Float,
        nullable=True,
    )

    new_customers = Column(
        Integer,
        nullable=False,
        default=0,
    )

    customers_churned = Column(
        Integer,
        nullable=False,
        default=0,
    )

    total_customers = Column(
        Integer,
        nullable=True,
    )

    daily_active_users = Column(
        Integer,
        nullable=False,
        default=0,
    )

    monthly_active_users = Column(
        Integer,
        nullable=False,
        default=0,
    )

    activated_users = Column(
        Integer,
        nullable=False,
        default=0,
    )

    new_signups = Column(
        Integer,
        nullable=False,
        default=0,
    )

    trial_users = Column(
        Integer,
        nullable=False,
        default=0,
    )

    paid_conversions = Column(
        Integer,
        nullable=False,
        default=0,
    )

    avg_time_to_value_days = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    leads = Column(
        Integer,
        nullable=False,
        default=0,
    )

    qualified_leads = Column(
        Integer,
        nullable=False,
        default=0,
    )

    opportunities = Column(
        Integer,
        nullable=False,
        default=0,
    )

    deals_won = Column(
        Integer,
        nullable=False,
        default=0,
    )

    deals_lost = Column(
        Integer,
        nullable=False,
        default=0,
    )

    avg_sales_cycle_days = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    google_ads_spend = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    google_customers = Column(
        Integer,
        nullable=False,
        default=0,
    )

    meta_ads_spend = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    meta_customers = Column(
        Integer,
        nullable=False,
        default=0,
    )

    outbound_spend = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    outbound_customers = Column(
        Integer,
        nullable=False,
        default=0,
    )

    company = relationship(
        "Company",
        back_populates="metrics",
    )


class Customer(Base):
    __tablename__ = "customers"

    id = Column(
        Integer,
        primary_key=True,
        index=True,
    )

    company_id = Column(
        Integer,
        ForeignKey("companies.id"),
        nullable=False,
        index=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    signup_month = Column(
        Date,
        nullable=False,
    )

    company = relationship(
        "Company",
        back_populates="customers",
    )

    snapshots = relationship(
        "CustomerSnapshot",
        back_populates="customer",
        cascade="all, delete-orphan",
        order_by="CustomerSnapshot.month",
    )


class CustomerSnapshot(Base):
    __tablename__ = "customer_snapshots"

    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "month",
            name="uq_customer_snapshot",
        ),
    )

    id = Column(
        Integer,
        primary_key=True,
    )

    customer_id = Column(
        Integer,
        ForeignKey("customers.id"),
        nullable=False,
        index=True,
    )

    month = Column(
        Date,
        nullable=False,
    )

    active = Column(
        Integer,
        nullable=False,
        default=1,
    )

    mrr = Column(
        Float,
        nullable=False,
        default=0.0,
    )

    customer = relationship(
        "Customer",
        back_populates="snapshots",
    )

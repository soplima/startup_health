from datetime import date
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import asc, desc
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import Base, engine, get_db
from app.kpis import compute_kpis
from app.analysis.cohort_heatmap import build_heatmap

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Startup health tracker")


@app.post("/companies", response_model=schemas.CompanyRead)
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    db_company = models.Company(**company.model_dump())
    db.add(db_company)
    db.commit()
    db.refresh(db_company)
    return db_company


@app.get("/companies", response_model=list[schemas.CompanyRead])
def list_companies(sector: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Company)
    if sector:
        query = query.filter(models.Company.sector == sector)
    return query.all()


@app.get("/companies/{company_id}", response_model=schemas.CompanyRead)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@app.delete("/companies/{company_id}", status_code=204)
def delete_company(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    db.delete(company)  # cascades to its metrics, see models.py relationship
    db.commit()
    return None


@app.post("/companies/{company_id}/metrics", response_model=schemas.MetricRead)
def add_metric(
    company_id: int, metric: schemas.MetricCreate, db: Session = Depends(get_db)
):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    existing = (
        db.query(models.Metric)
        .filter(
            models.Metric.company_id == company_id, models.Metric.month == metric.month
        )
        .first()
    )
    if existing:
        raise HTTPException(
            status_code=400, detail="A metrics entry for this month already exists"
        )

    db_metric = models.Metric(company_id=company_id, **metric.model_dump())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@app.get("/companies/{company_id}/metrics", response_model=list[schemas.MetricRead])
def list_metrics(company_id: int, db: Session = Depends(get_db)):
    return (
        db.query(models.Metric)
        .filter(models.Metric.company_id == company_id)
        .order_by(asc(models.Metric.month))
        .all()
    )


@app.delete("/companies/{company_id}/metrics/{metric_id}", status_code=204)
def delete_metric(company_id: int, metric_id: int, db: Session = Depends(get_db)):
    metric = (
        db.query(models.Metric)
        .filter(models.Metric.id == metric_id, models.Metric.company_id == company_id)
        .first()
    )
    if not metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    db.delete(metric)
    db.commit()
    return None


@app.get("/companies/{company_id}/kpis/latest", response_model=schemas.KPIResponse)
def latest_kpis(company_id: int, db: Session = Depends(get_db)):
    company = db.query(models.Company).filter(models.Company.id == company_id).first()
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    recent = (
        db.query(models.Metric)
        .filter(models.Metric.company_id == company_id)
        .order_by(desc(models.Metric.month))
        .limit(2)
        .all()
    )
    if len(recent) < 2:
        raise HTTPException(
            status_code=400,
            detail="Need at least two months of metrics to compute growth-based KPIs",
        )

    current, previous = recent[0], recent[1]
    indicators = compute_kpis(current, previous, company.sector)

    return schemas.KPIResponse(
        company_id=company_id,
        month=current.month,
        sector=company.sector,
        indicators=indicators,
    )


@app.get(
    "/companies/{company_id}/analysis/cohorts",
    response_model=list[schemas.CohortHeatmapRow],
)
def cohort_analysis(company_id: int, db: Session = Depends(get_db)):

    company = db.query(models.Company).filter(models.Company.id == company_id).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    return build_heatmap(db, company_id)


@app.post(
    "/companies/{company_id}/customers",
    response_model=schemas.CustomerRead,
)
def add_customer(
    company_id: int,
    customer: schemas.CustomerCreate,
    db: Session = Depends(get_db),
):

    company = db.query(models.Company).filter(models.Company.id == company_id).first()

    if not company:
        raise HTTPException(
            status_code=404,
            detail="Company not found",
        )

    db_customer = models.Customer(
        company_id=company_id,
        **customer.model_dump(),
    )

    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)

    return db_customer


@app.post(
    "/customers/{customer_id}/snapshots",
    response_model=schemas.CustomerSnapshotRead,
)
def add_customer_snapshot(
    customer_id: int,
    snapshot: schemas.CustomerSnapshotCreate,
    db: Session = Depends(get_db),
):

    customer = (
        db.query(models.Customer).filter(models.Customer.id == customer_id).first()
    )

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found",
        )

    db_snapshot = models.CustomerSnapshot(
        customer_id=customer_id,
        **snapshot.model_dump(),
    )

    db.add(db_snapshot)
    db.commit()
    db.refresh(db_snapshot)

    return db_snapshot

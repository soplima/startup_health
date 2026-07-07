# Startup Health Tracker

> A full-stack Business Intelligence platform for monitoring the financial health of SaaS startups.

Startup Health Tracker is a full-stack web application that enables founders, investors, and analysts to monitor startup performance through industry-standard financial KPIs. Instead of relying on spreadsheets, the platform stores monthly operational metrics and automatically calculates key indicators that help assess growth, capital efficiency, customer profitability, and financial sustainability.

The project was built as an end-to-end Business Intelligence application, combining a REST API, business logic, persistent storage, and an interactive frontend.

---

## Features

- 📊 Company management
- 📅 Monthly financial metric tracking
- 📈 Automatic KPI calculation
- 🎯 Industry benchmark comparison
- 💰 Financial indicators displayed using localized formats (R$, %, and units)
- ⚡ FastAPI REST API with automatic OpenAPI documentation
- ⚛️ React frontend built with Vite
- 🐳 Dockerized development environment with hot reload
- 🗄️ Persistent database storage

---

## KPIs

The platform automatically computes the following SaaS metrics:

| KPI | Description |
|------|-------------|
| MRR Growth | Month-over-month Monthly Recurring Revenue growth |
| Net Revenue Retention (NRR) | Revenue retained after expansion and churn |
| CAC Payback | Time required to recover customer acquisition cost |
| LTV:CAC Ratio | Customer lifetime value relative to acquisition cost |
| Burn Multiple | Capital efficiency during growth |
| Runway | Estimated months before available cash is exhausted |

---

## Technology Stack

### Backend

- FastAPI
- SQLAlchemy
- Pydantic
- SQLite (default database)
- Uvicorn

### Frontend

- React
- Vite
- Axios

### DevOps

- Docker
- Docker Compose
- Hot Reload
- Persistent Docker Volumes

---

## Architecture

```text
                     React + Vite
                          │
                    Axios HTTP Client
                          │
                    FastAPI REST API
                          │
                  Business Logic Layer
                 (calculations.py)
                          │
                    SQLAlchemy ORM
                          │
                    SQLite Database
```

---

## Project Structure

```text
.
├── app/
│   ├── benchmarks.py
│   ├── calculations.py
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
│
├── frontend/
│   ├── src/
│   │   ├── api.js
│   │   ├── App.jsx
│   │   ├── App.css
│   │   └── components/
│   │       ├── CompanyPanel.jsx
│   │       ├── MetricForm.jsx
│   │       └── KpiDashboard.jsx
│
├── Dockerfile
├── compose.yaml
├── requirements.txt
└── README.md
```

---

## Running with Docker (Recommended)

Build and start the application:

```bash
docker compose up --build
```

The following services will become available:

| Service | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |

### Useful Docker Commands

```bash
docker compose up --build
docker compose up -d
docker compose down
docker compose down -v
docker compose logs -f
```

---

## Running Locally

### Backend

```bash
python -m venv .venv

source .venv/bin/activate

pip install -r requirements.txt

uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend

npm install

npm run dev
```

---

## How It Works

The workflow is straightforward:

```text
Create Company
      │
      ▼
Insert Month #1
      │
      ▼
Insert Month #2
      │
      ▼
Business KPIs are calculated
      │
      ▼
Dashboard compares results against benchmarks
```

### Important

Several KPIs depend on historical comparisons (such as growth rate and revenue retention).

Therefore, **at least two consecutive months of data are required** before KPI cards can be displayed.

---

## Business Logic

The mathematical calculations are isolated inside `calculations.py`, allowing the API layer to remain lightweight and making the formulas easier to test independently.

Current KPIs include:

- Monthly Recurring Revenue Growth
- Net Revenue Retention
- CAC Payback
- LTV:CAC
- Burn Multiple
- Runway

Benchmark thresholds are currently stored in `benchmarks.py`.

---

## Future Improvements

Planned features include:

- Dynamic benchmark calculation using historical database data
- PostgreSQL production support
- JWT authentication
- User accounts and permissions
- CSV import/export
- Interactive historical charts
- Financial forecasting
- AI-generated business insights
- Automatic monthly report generation

---

## Screenshots

### Dashboard

> Add a screenshot here.

```text
docs/dashboard.png
```

### Company Management

> Add a screenshot here.

```text
docs/company-panel.png
```

---

## Motivation

This project was developed to explore how Business Intelligence concepts can be applied to startup finance using modern software engineering practices.

Rather than focusing only on dashboards, the project demonstrates an end-to-end BI workflow:

- Data collection
- Persistent storage
- Business rule implementation
- KPI computation
- Benchmark comparison
- API development
- Interactive visualization

The goal is to simulate a simplified financial analytics platform similar to those used by venture capital firms and SaaS founders.

---

## License

This project is available under the MIT License.
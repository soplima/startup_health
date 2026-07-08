import FinancialKpis from "./FinancialKpis"

export default function KpiDashboard({ kpis }) {

  if (!kpis) return null

  return (
    <div className="panel">

      <div className="panel-header">
        <h2>Indicadores</h2>
        <span className="muted">
          até {kpis.month} · {kpis.sector}
        </span>
      </div>

      <FinancialKpis indicators={kpis.indicators} />

    </div>
  )
}
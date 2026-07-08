import FinancialKpis from "./FinancialKpis"
import CustomerKpis from "./CustomersKpis"

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

      <CustomerKpis indicators={kpis.indicators} />

    </div>
  )
}
export default function KpiDashboard({ kpis, loading, error, metricsCount }) {
  if (loading) return <div className="panel"><p className="muted">Loading KPIs...</p></div>

  if (error) {
    return (
      <div className="panel">
        <h2>Indicadores</h2>
        <p className="muted">
          {metricsCount < 2
            ? 'Adicione pelo menos dois meses de métricas para ver os KPIs baseados em crescimento.'
            : error}
        </p>
      </div>
    )
  }

  if (!kpis) return null

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Indicadores</h2>
        <span className="muted">ate {kpis.month} &middot; {kpis.sector}</span>
      </div>
      <div className="kpi-grid">
        {kpis.indicators.map((k) => (
          <div key={k.label} className={`kpi-card status-${k.status}`}>
            <p className="kpi-label">{k.label}</p>
            <p className="kpi-value">
              {k.value}{k.unit === 'percent' ? '%' : k.unit === 'x' ? 'x' : ` ${k.unit}`}
            </p>
            <p className="kpi-note">{k.note}</p>
          </div>
        ))}
      </div>
    </div>
  )
}

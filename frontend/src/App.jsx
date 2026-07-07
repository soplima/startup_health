import { useEffect, useState, useCallback } from 'react'
import { api } from './api'
import CompanyPanel from './components/CompanyPanel'
import MetricForm from './components/MetricForm'
import KpiDashboard from './components/KpiDashboard'
import MetricHistory from './components/MetricHistory'

export default function App() {
  const [companies, setCompanies] = useState([])
  const [selectedId, setSelectedId] = useState(null)
  const [metrics, setMetrics] = useState([])
  const [kpis, setKpis] = useState(null)
  const [kpiError, setKpiError] = useState(null)
  const [kpiLoading, setKpiLoading] = useState(false)
  const [loadError, setLoadError] = useState(null)

  const loadCompanies = useCallback(async () => {
    try {
      const data = await api.listCompanies()
      setCompanies(data)
      if (!selectedId && data.length > 0) setSelectedId(data[0].id)
    } catch (err) {
      setLoadError(err.message)
    }
  }, [selectedId])

  const loadCompanyData = useCallback(async (id) => {
    if (!id) return
    setKpiLoading(true)
    setKpiError(null)
    try {
      const metricsData = await api.listMetrics(id)
      setMetrics(metricsData)
      const kpiData = await api.getLatestKpis(id)
      setKpis(kpiData)
    } catch (err) {
      setKpis(null)
      setKpiError(err.message)
    } finally {
      setKpiLoading(false)
    }
  }, [])

  useEffect(() => { loadCompanies() }, [loadCompanies])
  useEffect(() => { loadCompanyData(selectedId) }, [selectedId, loadCompanyData])

  async function handleCreateCompany(data) {
    const company = await api.createCompany(data)
    await loadCompanies()
    setSelectedId(company.id)
  }

  async function handleAddMetric(companyId, payload) {
    await api.addMetric(companyId, payload)
    await loadCompanyData(companyId)
  }

    async function handleDeleteCompany(companyId) {
    if (!window.confirm("Deseja realmente excluir esta empresa?")) return

    await api.deleteCompany(companyId)

    const data = await api.listCompanies()
    setCompanies(data)

    if (data.length > 0) {
      setSelectedId(data[0].id)
    } else {
      setSelectedId(null)
      setMetrics([])
      setKpis(null)
    }
  }

  async function handleDeleteMetric(metricId) {
    if (!window.confirm("Deseja realmente excluir este mês?")) return

    await api.deleteMetric(selectedId, metricId)
    await loadCompanyData(selectedId)
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>Indicadores</h1>
        <p className="muted">Insira métricas mensais, receba KPIs comparados ao setor.</p>
      </header>

      {loadError && <p className="error-text">Could not reach the API: {loadError}</p>}

      <CompanyPanel
      companies={companies}
      selectedId={selectedId}
      onSelect={setSelectedId}
      onCreate={handleCreateCompany}
      onDelete={handleDeleteCompany}
    />

      {selectedId && (
        <>
          <KpiDashboard
            kpis={kpis}
            loading={kpiLoading}
            error={kpiError}
            metricsCount={metrics.length}
          />
          <MetricForm companyId={selectedId} onSubmitted={handleAddMetric} />
          <MetricHistory metrics={metrics} onDelete={handleDeleteMetric} />
        </>
      )}
    </div>
  )
}

import { useState } from 'react'

const SECTORS = ['saas', 'marketplace', 'hardware', 'fintech', 'ecommerce']
const STAGES = ['pre_seed', 'seed', 'series_a', 'series_b', 'series_c_plus']

export default function CompanyPanel({ companies, selectedId, onSelect, onCreate }) {
  const [showForm, setShowForm] = useState(companies.length === 0)
  const [name, setName] = useState('')
  const [sector, setSector] = useState('saas')
  const [stage, setStage] = useState('seed')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      await onCreate({ name, sector, stage })
      setName('')
      setShowForm(false)
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="panel">
      <div className="panel-header">
        <h2>Empresas</h2>
        <button type="button" className="btn-ghost" onClick={() => setShowForm((v) => !v)}>
          {showForm ? 'Cancelar' : 'Adicionar Empresa'}
        </button>
      </div>

      {companies.length > 0 && (
        <div className="company-list">
          {companies.map((c) => (
            <button
              key={c.id}
              type="button"
              className={`company-chip ${c.id === selectedId ? 'active' : ''}`}
              onClick={() => onSelect(c.id)}
            >
              {c.name}
              <span className="chip-meta">{c.sector.replace('_', ' ')}</span>
            </button>
          ))}
        </div>
      )}

      {showForm && (
        <form className="inline-form" onSubmit={handleSubmit}>
          <input
            placeholder="Nome da Empresa"
            value={name}
            onChange={(e) => setName(e.target.value)}
            required
          />
          <select value={sector} onChange={(e) => setSector(e.target.value)}>
            {SECTORS.map((s) => (
              <option key={s} value={s}>{s}</option>
            ))}
          </select>
          <select value={stage} onChange={(e) => setStage(e.target.value)}>
            {STAGES.map((s) => (
              <option key={s} value={s}>{s.replace('_', ' ')}</option>
            ))}
          </select>
          <button type="submit" disabled={submitting}>
            {submitting ? 'Salvando...' : 'Criar'}
          </button>
        </form>
      )}
      {error && <p className="error-text">{error}</p>}
    </div>
  )
}

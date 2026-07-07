import { useState, useEffect, useRef } from 'react'

const SECTORS = ['saas', 'marketplace', 'hardware', 'fintech', 'ecommerce']
const STAGES = ['pre_seed', 'seed', 'series_a', 'series_b', 'series_c_plus']

export default function CompanyPanel({
  companies,
  selectedId,
  onSelect,
  onCreate,
  onDelete,
}) {
  const [showForm, setShowForm] = useState(companies.length === 0)
  const [name, setName] = useState('')
  const [sector, setSector] = useState('saas')
  const [stage, setStage] = useState('seed')
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)
  const [openMenuId, setOpenMenuId] = useState(null)
  const listRef = useRef(null)

  // Close any open menu when clicking outside the company list
  useEffect(() => {
    function handleClickOutside(e) {
      if (listRef.current && !listRef.current.contains(e.target)) {
        setOpenMenuId(null)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

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

  async function handleDeleteClick(company) {
  setOpenMenuId(null)

  if (
    !window.confirm(
      `Excluir "${company.name}"? Isso também apaga todo o histórico de métricas.`
    )
  ) {
    return
  }

  try {
    await onDelete(company.id)
  } catch (err) {
    alert(err.message)
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
        <div className="company-list" ref={listRef}>
          {companies.map((c) => (
            <div
              key={c.id}
              className={`company-chip ${c.id === selectedId ? 'active' : ''}`}
            >
              <button
                type="button"
                className="company-select"
                onClick={() => onSelect(c.id)}
              >
                <strong>{c.name}</strong>
                <span className="chip-meta">{c.sector.replace('_', ' ')}</span>
              </button>

              <div className="company-menu">
                <button
                  type="button"
                  className="menu-trigger"
                  aria-label="Mais opções"
                  aria-expanded={openMenuId === c.id}
                  onClick={() => setOpenMenuId(openMenuId === c.id ? null : c.id)}
                >
                  ⋮
                </button>
                {openMenuId === c.id && (
                  <div className="company-menu-dropdown">
                    <button
                      type="button"
                      className="menu-delete"
                      onClick={() => handleDeleteClick(c)}
                    >
                      Excluir
                    </button>
                  </div>
                )}
              </div>
            </div>
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

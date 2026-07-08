import { useState } from 'react'

const empty = {
  month: '',
  mrr: '',
  mrr_churned: '',
  mrr_expansion: '',
  new_customers: '',
  total_customers: '',
  sales_spend: '',
  cash_balance: '',
  monthly_burn: '',
  gross_margin: '75',
  daily_active_users: '',
  monthly_active_users: '',
  activated_users: '',
  new_signups: '',
  trial_users: '',
  paid_conversions: '',
  avg_time_to_value_days: '',

}

// O quarto elemento da lista é o prefixo/sufixo visual do campo
const FIELDS = [
  ['month', 'Mês de referência', 'month', ''],
  ['mrr', 'MRR deste mês (Faturamento Recorrente)', 'number', 'R$'],
  ['mrr_churned', 'MRR perdido por cancelamentos (Churn)', 'number', 'R$'],
  ['mrr_expansion', 'MRR ganho com upsells/expansão', 'number', 'R$'],
  ['new_customers', 'Novos clientes conquistados no mês', 'number', 'qtd'],
  ['total_customers', 'Total de clientes ativos na base', 'number', 'qtd'],
  ['sales_spend', 'Gasto com vendas e marketing (CAC)', 'number', 'R$'],
  ['cash_balance', 'Saldo total em caixa', 'number', 'R$'],
  ['monthly_burn', 'Queima de caixa líquida (Net Burn)', 'number', 'R$'],
  ['gross_margin', 'Margem bruta', 'number', '%'],
  ['ebitda_margin','EBITDA Margin','number','%'],
  ['daily_active_users', 'Usuários ativos por dia (DAU)', 'number', ''],
  ['monthly_active_users', 'Usuários ativos por mês (MAU)', 'number', ''],
  ['activated_users', 'Usuários ativados', 'number', ''],
  ['new_signups', 'Novos cadastros', 'number', ''],
  ['trial_users', 'Usuários em trial', 'number', ''],
  ['paid_conversions', 'Conversões para pago', 'number', ''],
  ['avg_time_to_value_days', 'Tempo até primeira ação de valor', 'number', 'dias'],
]

export default function MetricForm({ companyId, onSubmitted }) {
  const [form, setForm] = useState(empty)
  const [submitting, setSubmitting] = useState(false)
  const [error, setError] = useState(null)

  function update(key, value) {
    setForm((f) => ({ ...f, [key]: value }))
  }

  async function handleSubmit(e) {
    e.preventDefault()
    setSubmitting(true)
    setError(null)
    try {
      const formattedMonth = form.month.length === 7 ? `${form.month}-01` : form.month;

      const payload = {
        month: formattedMonth,
        mrr: Number(form.mrr),
        mrr_churned: Number(form.mrr_churned || 0),
        mrr_expansion: Number(form.mrr_expansion || 0),
        new_customers: Number(form.new_customers || 0),
        total_customers: form.total_customers ? Number(form.total_customers) : null,
        sales_spend: Number(form.sales_spend || 0),
        cash_balance: Number(form.cash_balance),
        monthly_burn: Number(form.monthly_burn),
        gross_margin: Number(form.gross_margin || 75),
        ebitda_margin: form.ebitda_margin === '' ? null : Number(form.ebitda_margin),
        daily_active_users: Number(form.daily_active_users || 0),
        monthly_active_users: Number(form.monthly_active_users || 0),
        activated_users: Number(form.activated_users || 0),
        new_signups: Number(form.new_signups || 0),
        trial_users: Number(form.trial_users || 0),
        paid_conversions: Number(form.paid_conversions || 0),
        avg_time_to_value_days: Number(form.avg_time_to_value_days || 0),
      }
      await onSubmitted(companyId, payload)
      setForm(empty)
    } catch (err) {
      setError(err.message)
    } finally {
      setSubmitting(false)
    }
  }

  return (
    <div className="panel">
      <h2>Adicionar métricas mensais</h2>
      <form className="grid-form" onSubmit={handleSubmit}>
        {FIELDS.map(([key, label, type, unit]) => (
          <div className="field" key={key}>
            <label>{label}</label>
            <div className="input-wrapper">
              {unit && <span className="input-unit">{unit}</span>}
              <input
                type={type}
                value={form[key]}
                onChange={(e) => update(key, e.target.value)}
                required={key !== 'total_customers'}
              />
            </div>
          </div>
        ))}
        <button type="submit" disabled={submitting} className="submit-btn">
          {submitting ? 'Salvando...' : 'Salvar métricas'}
        </button>
      </form>
      {error && <p className="error-text">Erro ao salvar: {error}</p>}
    </div>
  )
}
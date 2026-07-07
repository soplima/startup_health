const BASE = '/api'

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: { 'Content-Type': 'application/json' },
    ...options,
  })
  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed: ${res.status}`)
  }
  return res.json()
}

export const api = {
  listCompanies: () => request('/companies'),
  createCompany: (data) =>
    request('/companies', { method: 'POST', body: JSON.stringify(data) }),
  getCompany: (id) => request(`/companies/${id}`),
  listMetrics: (id) => request(`/companies/${id}/metrics`),
  addMetric: (id, data) =>
    request(`/companies/${id}/metrics`, { method: 'POST', body: JSON.stringify(data) }),
  getLatestKpis: (id) => request(`/companies/${id}/kpis/latest`),
}

export async function deleteCompany(companyId) {
  const response = await fetch(
    `/companies/${companyId}`,
    {
      method: "DELETE",
    }
  )

  if (!response.ok) {
    throw new Error("Failed to delete company")
  }

  return response.json()
}


export async function deleteMetric(companyId, metricId) {
  const response = await fetch(
    `/companies/${companyId}/metrics/${metricId}`,
    {
      method: "DELETE",
    }
  )

  if (!response.ok) {
    throw new Error("Failed to delete metric")
  }

  return response.json()
}

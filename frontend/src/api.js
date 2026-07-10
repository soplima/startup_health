const BASE = '/api'


async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    headers: {
      'Content-Type': 'application/json',
    },
    ...options,
  })


  if (!res.ok) {
    const body = await res.json().catch(() => ({}))
    throw new Error(body.detail || `Request failed: ${res.status}`)
  }


  return res.json()
}



export const api = {


  listCompanies: () =>
    request('/companies'),


  createCompany: (data) =>
    request('/companies', {
      method: 'POST',
      body: JSON.stringify(data),
    }),


  getCompany: (id) =>
    request(`/companies/${id}`),



  deleteCompany: (id) =>
    request(`/companies/${id}`, {
      method: 'DELETE',
    }),




  listMetrics: (id) =>
    request(`/companies/${id}/metrics`),


  addMetric: (id, data) =>
    request(`/companies/${id}/metrics`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),


  deleteMetric: (companyId, metricId) =>
    request(`/companies/${companyId}/metrics/${metricId}`, {
      method: 'DELETE',
    }),




  getLatestKpis: (id) =>
    request(`/companies/${id}/kpis/latest`),



  listCohorts: (id) =>
    request(`/companies/${id}/cohorts`),


  addCohort: (id, data) =>
    request(`/companies/${id}/cohorts`, {
      method: 'POST',
      body: JSON.stringify(data),
    }),


  getCohortAnalysis: (id) =>
    request(`/companies/${id}/analysis/cohorts`),

}
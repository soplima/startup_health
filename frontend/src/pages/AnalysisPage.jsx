import { useEffect, useMemo, useState } from "react";
import { api } from "../api";

function heatColor(value) {
  if (value == null) return "#ffffff";

  if (value >= 90) return "#0B7A35";
  if (value >= 75) return "#4CAF50";
  if (value >= 60) return "#8BC34A";
  if (value >= 45) return "#FFC107";
  if (value >= 30) return "#FF9800";

  return "#D32F2F";
}

function formatMonth(dateString) {
  const date = new Date(dateString);

  return date.toLocaleDateString("pt-BR", {
    month: "short",
    year: "2-digit",
  });
}

export default function AnalysisPage({ companyId, onBack }) {
  const [cohorts, setCohorts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    async function loadAnalysis() {
      setLoading(true);
      setError(null);

      try {
        const data = await api.getCohortAnalysis(companyId);
        setCohorts(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    }

    loadAnalysis();
  }, [companyId]);

  const maxMonth = useMemo(() => {
    let max = 0;

    cohorts.forEach((row) => {
      row.cells.forEach((cell) => {
        if (cell.month_offset > max) {
          max = cell.month_offset;
        }
      });
    });

    return max;
  }, [cohorts]);

  return (
    <div className="panel">

      <button
        className="btn-ghost"
        onClick={onBack}
      >
        ← Voltar
      </button>

      <h1>Heatmap de Retenção por Coorte</h1>

        <p className="chart-description">
        Cada linha representa clientes que começaram no mesmo mês.
        As colunas mostram meses após a entrada desses clientes, não meses do calendário.
        <br /><br />
        Exemplo: uma coorte de janeiro/2024 terá M0 em janeiro/2024,
        M1 em fevereiro/2024, M2 em março/2024 e assim por diante.
        <br /><br />
        Coortes recentes possuem menos colunas porque ainda não existe histórico
        suficiente para acompanhar esses clientes por muitos meses.
        </p>

      {loading && <p>Carregando...</p>}

      {error && (
        <p className="error-text">{error}</p>
      )}

      {!loading && !error && cohorts.length === 0 && (
        <p>Nenhum dado encontrado.</p>
      )}

      {!loading && !error && cohorts.length > 0 && (
        <div className="heatmap-wrapper">

          <table className="cohort-heatmap">

            <thead>

              <tr>

                <th>Coorte</th>

                <th>Tamanho</th>

                {Array.from(
                  { length: maxMonth + 1 },
                  (_, i) => (
                    <th key={i}>
                    {i === 0 ? "Entrada" : `+${i} mês${i > 1 ? "es" : ""}`}
                    </th>
                  )
                )}

              </tr>

            </thead>

            <tbody>

              {cohorts.map((row) => (

                <tr key={row.cohort_month}>

                  <td>
                    {formatMonth(row.cohort_month)}
                  </td>

                  <td>
                    {row.cohort_size}
                  </td>

                  {Array.from(
                    { length: maxMonth + 1 },
                    (_, month) => {

                      const cell = row.cells.find(
                        (c) => c.month_offset === month
                      );

                      return (
                        <td
                          key={month}
                          style={{
                            backgroundColor: heatColor(
                              cell?.retention
                            ),
                            color:
                              cell?.retention == null
                                ? "#555"
                                : "white",
                          }}
                        >
                          {cell
                            ? `${cell.retention}%`
                            : "-"}
                        </td>
                      );
                    }
                  )}

                </tr>

              ))}

            </tbody>

          </table>

          <div className="heatmap-legend">

            <span>Retenção:</span>

            <div className="legend-box" style={{ background: "#0B7A35" }}>
              ≥90%
            </div>

            <div className="legend-box" style={{ background: "#4CAF50" }}>
              75%
            </div>

            <div className="legend-box" style={{ background: "#8BC34A" }}>
              60%
            </div>

            <div className="legend-box" style={{ background: "#FFC107", color: "#222" }}>
              45%
            </div>

            <div className="legend-box" style={{ background: "#FF9800" }}>
              30%
            </div>

            <div className="legend-box" style={{ background: "#D32F2F" }}>
              &lt;30%
            </div>

          </div>

        </div>
      )}
    </div>
  );
}
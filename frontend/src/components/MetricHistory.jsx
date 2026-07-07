import { useState } from "react";

export default function MetricHistory({ metrics, onDelete }) {
  const [openMenu, setOpenMenu] = useState(null);

  if (metrics.length === 0) {
    return (
      <div className="panel">
        <h2>Histórico de métricas</h2>
        <p className="muted">Nenhuma métrica cadastrada.</p>
      </div>
    );
  }

  return (
    <div className="panel">
      <h2>Histórico de métricas</h2>

      {metrics
        .slice()
        .reverse()
        .map((metric) => (
          <div key={metric.id} className="metric-row">
            <div>
              <strong>{metric.month}</strong>
              <div className="muted">
                MRR:{" "}
                {metric.mrr.toLocaleString("pt-BR", {
                  style: "currency",
                  currency: "BRL",
                  minimumFractionDigits: 0,
                })}
              </div>
            </div>

            <div className="metric-menu">
              <button
                className="menu-trigger"
                onClick={() =>
                  setOpenMenu(openMenu === metric.id ? null : metric.id)
                }
              >
                ⋮
              </button>

              {openMenu === metric.id && (
                <div className="company-menu-dropdown">
                  <button
                    className="menu-delete"
                    onClick={() => onDelete(metric.id)}
                  >
                    Excluir
                  </button>
                </div>
              )}
            </div>
          </div>
        ))}
    </div>
  );
}
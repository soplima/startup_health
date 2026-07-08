function formatValue(value, unit) {
  switch (unit) {
    case "R$":
    case "R$/mês":
      return value.toLocaleString("pt-BR", {
        style: "currency",
        currency: "BRL",
        minimumFractionDigits: 0,
      });

    case "%":
      return `${value}%`;

    case "x":
      return `${value}x`;

    case "meses":
      return `${value} meses`;

    default:
      return `${value} ${unit}`;
  }
}

export default function CustomerKpis({ indicators }) {
  const customers = indicators.filter(
    (k) => k.category === "customers"
  );

  if (customers.length === 0) return null;

  return (
    <>
      <h3>Indicadores de Clientes</h3>

      <div className="kpi-grid">
        {customers.map((k) => (
          <div
            key={k.label}
            className={`kpi-card status-${k.status}`}
          >
            <p className="kpi-label">{k.label}</p>

            <p className="kpi-value">
              {formatValue(k.value, k.unit)}
            </p>

            <p className="kpi-note">
              {k.note}
            </p>
          </div>
        ))}
      </div>
    </>
  );
}
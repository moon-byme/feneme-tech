import { useEffect, useState } from "react";
import { api, ApiError } from "../api";
import type { CargoType } from "../types";

type Props = { token: string; onSessionExpired: () => void };

function formatLimit(value: number) {
  return `${value.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 })} °C`;
}

/** Catálogo de tipos de carga com limite e fonte (US-15 / FT-114). Somente leitura. */
function CargoCatalog({ token, onSessionExpired }: Props) {
  const [cargoTypes, setCargoTypes] = useState<CargoType[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();
    setLoading(true);
    setError("");
    api.listCargoTypes(token, controller.signal)
      .then((items) => { if (!controller.signal.aborted) setCargoTypes(items); })
      .catch((failure) => {
        if (controller.signal.aborted) return;
        if (failure instanceof ApiError && failure.status === 401) {
          onSessionExpired();
          return;
        }
        setError(failure instanceof ApiError ? failure.message : "Erro ao consultar o catálogo de cargas.");
      })
      .finally(() => { if (!controller.signal.aborted) setLoading(false); });
    return () => controller.abort();
  }, [token, onSessionExpired]);

  return (
    <section className="panel catalog-panel" data-cy="cargo-catalog-panel">
      <div className="panel-heading">
        <div><p className="eyebrow">CATÁLOGO</p><h2>Tipos de carga</h2></div>
        <span className="count-badge">{cargoTypes.length}</span>
      </div>
      <p className="muted">
        O limite de cada carga é a temperatura contra a qual as rotas serão comparadas. O Feneme considera
        transporte sem refrigeração, por isso o catálogo só tem cargas com limite a partir de 20 °C e fonte verificável.
      </p>
      {loading && <p className="muted" role="status">Carregando catálogo...</p>}
      {error && <p className="message error" role="alert">Não foi possível consultar o catálogo: {error}</p>}
      {!loading && !error && (
        <div className="table-scroll">
          <table className="catalog-table" data-cy="cargo-catalog">
            <caption className="visually-hidden">Catálogo de tipos de carga</caption>
            <thead>
              <tr>
                <th scope="col">Carga</th>
                <th scope="col">Categoria</th>
                <th scope="col">Limite</th>
                <th scope="col">O que a fonte diz</th>
                <th scope="col">Fonte</th>
              </tr>
            </thead>
            <tbody>
              {cargoTypes.map((item) => (
                <tr key={item.id} data-cy="cargo-type-row">
                  <th scope="row">{item.name}</th>
                  <td>{item.category}</td>
                  <td className="nowrap">
                    <strong>{formatLimit(item.limit_c)}</strong>
                    {item.is_derived && <span className="tag" data-cy="derived-limit">limite derivado</span>}
                  </td>
                  <td>{item.reference}</td>
                  <td>
                    <a href={item.source_url} target="_blank" rel="noreferrer">
                      {item.source_name}<span className="visually-hidden"> (abre em nova aba)</span>
                    </a>
                    <span className="sub">{item.source_type}</span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
      <p className="muted small">
        "Limite derivado" quer dizer que o valor não aparece direto na fonte: foi deduzido de normas gerais.
        O catálogo é mantido pela equipe e não pode ser alterado por esta tela.
      </p>
    </section>
  );
}

export default CargoCatalog;

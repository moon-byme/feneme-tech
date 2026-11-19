import { useCallback, useEffect, useRef, useState } from "react";
import { api, ApiError } from "../api";
import type { AuthUser, Delivery } from "../types";
import { DELIVERY_STATUS_LABELS } from "../types";

type Props = { user: AuthUser; token: string; onLogout: (message?: string) => void };

function MotoristaHome({ user, token, onLogout }: Props) {
  const [deliveries, setDeliveries] = useState<Delivery[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [updates, setUpdates] = useState<Record<number, { loading: boolean; error?: string; notice?: string }>>({});
  const pending = useRef(new Set<number>());

  async function updateStatus(delivery: Delivery) {
    if (pending.current.has(delivery.id) || delivery.status === "ENTREGUE") return;
    const nextStatus = delivery.status === "PENDENTE" ? "EM_TRANSPORTE" : "ENTREGUE";
    pending.current.add(delivery.id);
    setUpdates((current) => ({ ...current, [delivery.id]: { loading: true } }));
    try {
      const updated = await api.updateDeliveryStatus(token, delivery.id, nextStatus);
      setDeliveries((current) => current.map((item) => item.id === updated.id ? updated : item));
      setUpdates((current) => ({ ...current, [delivery.id]: {
        loading: false, notice: `Status atualizado para ${DELIVERY_STATUS_LABELS[updated.status]}.`,
      } }));
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        onLogout("Sua sessão expirou. Entre novamente.");
        return;
      }
      setUpdates((current) => ({ ...current, [delivery.id]: {
        loading: false,
        error: e instanceof ApiError ? e.message : "Não foi possível atualizar o status. Tente novamente.",
      } }));
    } finally {
      pending.current.delete(delivery.id);
    }
  }

  const loadDeliveries = useCallback(async (signal?: AbortSignal) => {
    setLoading(true);
    setError("");
    setDeliveries([]);
    setUpdates({});
    try {
      const result = await api.listDeliveries(token, signal);
      if (!signal?.aborted) setDeliveries(result);
    } catch (e) {
      if (signal?.aborted) return;
      if (e instanceof ApiError && e.status === 401) {
        onLogout("Sua sessão expirou. Entre novamente.");
        return;
      }
      setError(e instanceof ApiError ? e.message : "Não foi possível consultar suas entregas.");
    } finally {
      if (!signal?.aborted) setLoading(false);
    }
  }, [token, onLogout]);

  useEffect(() => {
    const controller = new AbortController();
    void loadDeliveries(controller.signal);
    return () => controller.abort();
  }, [loadDeliveries]);

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark small" aria-hidden="true">F</div>
          <div><strong>Feneme</strong><span>Minhas entregas</span></div>
        </div>
        <div className="user-area">
          <span className="role-chip" data-cy="role-chip">Motorista</span>
          <span className="username">{user.username}</span>
          <button className="button-secondary" onClick={() => onLogout()} type="button">Sair</button>
        </div>
      </header>

      <section className="hero">
        <p className="eyebrow">ÁREA DO MOTORISTA</p>
        <h1 className="break-anywhere">Olá, {user.username}</h1>
        <p>Consulte suas entregas e atualize o status conforme o andamento do transporte.</p>
      </section>

      <section className="panel" aria-busy={loading}>
        <div className="panel-heading">
          <div><p className="eyebrow">SUAS ENTREGAS</p><h2>Entregas atribuídas</h2></div>
          <span className="count-badge">{deliveries.length}</span>
        </div>
        <div className="list-toolbar">
          <span className="muted">Apenas entregas sob sua responsabilidade</span>
          <button className="button-secondary" type="button" onClick={() => void loadDeliveries()} disabled={loading || Object.values(updates).some((update) => update.loading)}>Atualizar</button>
        </div>
        {error && <p className="message error" role="alert">{error}</p>}
        {loading ? (
          <p className="empty-state" role="status">Carregando entregas...</p>
        ) : !error && deliveries.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon" aria-hidden="true">↗</div>
            <strong>Nenhuma entrega atribuída</strong>
            <p>Quando o Gestor atribuir uma entrega a você, ela aparecerá aqui.</p>
          </div>
        ) : !error ? (
          <div className="delivery-list">
            {deliveries.map((delivery) => (
              <article className="delivery-card" key={delivery.id}>
                <div className="delivery-card-top">
                  <span className="delivery-id">ENTREGA #{delivery.id}</span>
                  <span className="status-chip" data-status={delivery.status}>{DELIVERY_STATUS_LABELS[delivery.status]}</span>
                </div>
                <div className="route">
                  <div><span className="route-dot origin-dot" /><div><small>ORIGEM</small><strong className="break-anywhere">{delivery.origin}</strong></div></div>
                  <div className="route-line" />
                  <div><span className="route-dot destination-dot" /><div><small>DESTINO</small><strong className="break-anywhere">{delivery.destination}</strong></div></div>
                </div>
                <div className="cargo"><small>CARGA</small><p className="break-anywhere">{delivery.cargo_description}</p></div>
                <div className="status-actions" aria-busy={updates[delivery.id]?.loading || false}>
                  <button
                    type="button"
                    data-cy="update-status"
                    disabled={delivery.status === "ENTREGUE" || updates[delivery.id]?.loading}
                    onClick={() => void updateStatus(delivery)}
                  >
                    {updates[delivery.id]?.loading ? "Salvando status..." : delivery.status === "PENDENTE"
                      ? "Iniciar transporte" : delivery.status === "EM_TRANSPORTE" ? "Confirmar entrega" : "Entrega finalizada"}
                  </button>
                  {updates[delivery.id]?.error && <p className="message error" role="alert">{updates[delivery.id].error}</p>}
                  {updates[delivery.id]?.notice && <p className="message success" role="status">{updates[delivery.id].notice}</p>}
                </div>
              </article>
            ))}
          </div>
        ) : null}
      </section>
      <footer>Feneme · Área do Motorista</footer>
    </main>
  );
}

export default MotoristaHome;

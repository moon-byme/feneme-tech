import { useEffect, useRef, useState } from "react";
import { api, ApiError } from "../api";
import type { DeliveryStatusHistoryResponse } from "../types";
import { DELIVERY_STATUS_LABELS } from "../types";

type Props = {
  deliveryId: number;
  token: string;
  onSessionExpired: () => void;
};

function DeliveryStatusHistory({ deliveryId, token, onSessionExpired }: Props) {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [history, setHistory] = useState<DeliveryStatusHistoryResponse | null>(null);
  const [error, setError] = useState("");
  const activeRequest = useRef(0);
  const panelId = "status-history-" + deliveryId;

  useEffect(() => {
    return () => { activeRequest.current += 1; };
  }, []);

  async function fetchHistory() {
    const request = ++activeRequest.current;
    setLoading(true);
    setError("");
    setHistory(null);
    try {
      const response = await api.getDeliveryStatusHistory(token, deliveryId);
      if (request === activeRequest.current) setHistory(response);
    } catch (failure) {
      if (request !== activeRequest.current) return;
      if (failure instanceof ApiError && failure.status === 401) {
        onSessionExpired();
        return;
      }
      setError(failure instanceof ApiError ? failure.message : "Erro ao consultar o histórico.");
    } finally {
      if (request === activeRequest.current) setLoading(false);
    }
  }

  function toggle() {
    if (open) {
      activeRequest.current += 1;
      setLoading(false);
      setOpen(false);
    } else {
      setOpen(true);
      void fetchHistory();
    }
  }

  return (
    <section className="status-history" data-cy="delivery-status-history">
      <button
        type="button"
        className="button-secondary"
        data-cy="history-toggle"
        aria-expanded={open}
        aria-controls={panelId}
        onClick={toggle}
      >
        {open ? "Ocultar histórico" : "Consultar histórico"}
      </button>
      {open && (
        <div id={panelId} className="history-panel" data-cy="history-panel" aria-busy={loading}>
          <div className="history-heading">
            <strong>Histórico de status</strong>
            <button
              type="button"
              className="button-secondary"
              data-cy="history-refresh"
              onClick={() => void fetchHistory()}
              disabled={loading}
            >
              Atualizar histórico
            </button>
          </div>
          {loading && <p className="muted" role="status">Carregando histórico...</p>}
          {error && <p role="alert" className="message error">Não foi possível consultar o histórico: {error}</p>}
          {!loading && history && (
            <>
              <p className="history-current-status" data-cy="history-current-status">
                Status atual: <strong>{DELIVERY_STATUS_LABELS[history.current_status]}</strong>
              </p>
              {history.history.length === 0 ? (
                <p className="history-empty" data-cy="history-empty">
                  Ainda não há mudanças de status registradas para esta entrega.
                </p>
              ) : (
                <ol className="history-list" data-cy="history-list">
                  {history.history.map((event) => (
                    <li key={event.id} data-cy="history-entry">
                      <strong>
                        {DELIVERY_STATUS_LABELS[event.previous_status]} → {DELIVERY_STATUS_LABELS[event.new_status]}
                      </strong>
                      <span className="muted">
                        {new Date(event.changed_at).toLocaleString("pt-BR", { dateStyle: "short", timeStyle: "short" })}
                        {" · "}{event.changed_by_username}
                      </span>
                    </li>
                  ))}
                </ol>
              )}
            </>
          )}
        </div>
      )}
    </section>
  );
}

export default DeliveryStatusHistory;

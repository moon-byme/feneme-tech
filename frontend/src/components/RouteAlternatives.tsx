import { useState } from "react";
import type { FormEvent } from "react";
import { api, ApiError } from "../api";
import type { Delivery } from "../types";

// US-06 (FT-46): o Gestor informa manualmente até duas alternativas de trajeto.
export const MAX_ROUTE_ALTERNATIVES = 2;

type Props = {
  delivery: Delivery;
  token: string;
  disabled: boolean;
  onSaved: () => Promise<void>;
  onSessionExpired: () => void;
};

export function formatDistance(km: number | string): string {
  return `${Number(km).toLocaleString("pt-BR", { maximumFractionDigits: 2 })} km`;
}

export function formatDuration(minutes: number): string {
  const hours = Math.floor(minutes / 60);
  const rest = minutes % 60;
  if (hours === 0) return `${rest} min`;
  return rest === 0 ? `${hours} h` : `${hours} h ${rest} min`;
}

function RouteAlternatives({ delivery, token, disabled, onSaved, onSessionExpired }: Props) {
  const [distance, setDistance] = useState("");
  const [duration, setDuration] = useState("");
  const [saving, setSaving] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [showComparison, setShowComparison] = useState(false);
  const [comparisonMessage, setComparisonMessage] = useState("");

  const alternatives = delivery.route_alternatives ?? [];
  const limitReached = alternatives.length >= MAX_ROUTE_ALTERNATIVES;

  function handleCompare() {
    setComparisonMessage("");
    if (alternatives.length < MAX_ROUTE_ALTERNATIVES) {
      setShowComparison(false);
      setComparisonMessage(
        `Cadastre duas alternativas para comparar. Atualmente há ${alternatives.length} de ${MAX_ROUTE_ALTERNATIVES}.`,
      );
      return;
    }
    setShowComparison((current) => !current);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setError("");
    setNotice("");
    setSaving(true);
    try {
      await api.createRouteAlternative(token, delivery.id, {
        // Aceita vírgula decimal digitada no padrão brasileiro.
        distance_km: distance.trim().replace(",", "."),
        duration_minutes: duration.trim(),
      });
      setDistance("");
      setDuration("");
      setShowComparison(false);
      setComparisonMessage("");
      setNotice("Alternativa de trajeto salva.");
      await onSaved();
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        onSessionExpired();
        return;
      }
      setError(e instanceof ApiError ? e.message : "Não foi possível salvar a alternativa de trajeto.");
    } finally {
      setSaving(false);
    }
  }

  return (
    <div className="route-alternatives" data-cy={`route-alternatives-${delivery.id}`}>
      <div className="route-alternatives-heading">
        <small>ALTERNATIVAS DE TRAJETO</small>
        <span className="muted" data-cy="route-alternatives-count">
          {alternatives.length}/{MAX_ROUTE_ALTERNATIVES}
        </span>
      </div>

      {alternatives.length === 0 ? (
        <p className="muted">Nenhuma alternativa informada.</p>
      ) : (
        <ol className="route-alternatives-list">
          {alternatives.map((alternative, index) => (
            <li key={alternative.id} data-cy="route-alternative-item">
              <strong>Alternativa {index + 1}</strong>
              <span>{formatDistance(alternative.distance_km)}</span>
              <span>{formatDuration(alternative.duration_minutes)}</span>
            </li>
          ))}
        </ol>
      )}

      <div className="route-comparison-actions">
        <button
          type="button"
          className="button-secondary"
          data-cy="route-compare-button"
          onClick={handleCompare}
        >
          {showComparison ? "Ocultar comparação" : "Comparar alternativas"}
        </button>
      </div>

      {comparisonMessage && (
        <p className="message error" role="status" data-cy="route-comparison-message">
          {comparisonMessage}
        </p>
      )}

      {showComparison && alternatives.length === MAX_ROUTE_ALTERNATIVES && (
        <section className="route-comparison" data-cy="route-comparison-panel" aria-label="Comparação de alternativas de trajeto">
          {alternatives.map((alternative, index) => (
            <article className="route-comparison-card" data-cy="route-comparison-item" key={alternative.id}>
              <strong>Alternativa {index + 1}</strong>
              <span><small>Distância</small>{formatDistance(alternative.distance_km)}</span>
              <span><small>Duração</small>{formatDuration(alternative.duration_minutes)}</span>
            </article>
          ))}
        </section>
      )}

      {limitReached ? (
        <p className="muted" data-cy="route-alternatives-limit">
          Limite de {MAX_ROUTE_ALTERNATIVES} alternativas atingido para esta entrega.
        </p>
      ) : (
        // noValidate: a validação fica a cargo da API, que identifica o campo a corrigir.
        <form className="assign-form" onSubmit={(event) => void handleSubmit(event)} noValidate>
          <div className="assign-controls">
            <label>
              Distância (km)
              <input
                data-cy="route-distance"
                inputMode="decimal"
                value={distance}
                onChange={(e) => setDistance(e.target.value)}
                placeholder="Ex.: 125,5"
              />
            </label>
            <label>
              Duração (min)
              <input
                data-cy="route-duration"
                inputMode="numeric"
                value={duration}
                onChange={(e) => setDuration(e.target.value)}
                placeholder="Ex.: 110"
              />
            </label>
            <button data-cy="route-submit" type="submit" disabled={disabled || saving}>
              {saving ? "Salvando..." : "Adicionar"}
            </button>
          </div>
        </form>
      )}

      {error && <p className="message error" role="alert" data-cy="route-error">{error}</p>}
      {notice && <p className="message success" role="status">{notice}</p>}
    </div>
  );
}

export default RouteAlternatives;

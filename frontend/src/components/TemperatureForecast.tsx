import { useState } from "react";
import { api, ApiError } from "../api";
import type { DailyForecast, ReferenceLocation } from "../types";

// US-08 (FT-47): previsão de temperatura ambiente da Open-Meteo para uma
// localidade de demonstração. A falha externa não bloqueia os demais fluxos.
type Props = {
  deliveryId: number;
  token: string;
  locations: ReferenceLocation[];
  onSessionExpired: () => void;
};

export function formatCelsius(value: number): string {
  return `${value.toLocaleString("pt-BR", { minimumFractionDigits: 1, maximumFractionDigits: 1 })} °C`;
}

export function formatForecastDate(isoDate: string): string {
  const [year, month, day] = isoDate.split("-");
  return `${day}/${month}/${year}`;
}

function TemperatureForecast({ deliveryId, token, locations, onSessionExpired }: Props) {
  const [location, setLocation] = useState("");
  const [forecast, setForecast] = useState<DailyForecast | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleConsult() {
    setError("");
    setForecast(null);
    if (!location) {
      setError("Selecione uma localidade de referência.");
      return;
    }
    setLoading(true);
    try {
      setForecast(await api.getForecast(token, location));
    } catch (e) {
      if (e instanceof ApiError && e.status === 401) {
        onSessionExpired();
        return;
      }
      setError(e instanceof ApiError ? e.message : "Previsão indisponível no momento.");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="forecast" data-cy={`forecast-${deliveryId}`}>
      <small className="section-label">PREVISÃO DE TEMPERATURA</small>
      <div className="assign-controls">
        <label>
          Localidade de referência
          <select
            data-cy="forecast-location"
            value={location}
            onChange={(e) => {
              setLocation(e.target.value);
              setForecast(null);
              setError("");
            }}
          >
            <option value="">Selecione...</option>
            {locations.map((item) => (
              <option key={item.slug} value={item.slug}>{item.name}</option>
            ))}
          </select>
        </label>
        <button
          className="button-secondary"
          data-cy="forecast-submit"
          type="button"
          disabled={loading || locations.length === 0}
          onClick={() => void handleConsult()}
        >
          {loading ? "Consultando..." : "Consultar previsão"}
        </button>
      </div>

      {forecast && (
        <div className="forecast-result" data-cy="forecast-result" role="status">
          <strong>
            Máx. {formatCelsius(forecast.temperature_max)} · Mín. {formatCelsius(forecast.temperature_min)}
          </strong>
          <span>
            {forecast.location.name} · hoje, {formatForecastDate(forecast.date)} · fonte: {forecast.source}
          </span>
          <small className="muted">{forecast.notice}</small>
        </div>
      )}
      {error && <p className="message error" role="alert" data-cy="forecast-error">{error}</p>}
    </div>
  );
}

export default TemperatureForecast;

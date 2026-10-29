import type { Delivery, DriverOption, LoginResponse } from "./types";

const API_BASE =
  import.meta.env.VITE_API_BASE_URL ||
  (import.meta.env.DEV ? "http://localhost:8000/api" : "/api");

export class ApiError extends Error {
  constructor(message: string, public status?: number) {
    super(message);
    this.name = "ApiError";
  }
}

function errorMessage(data: unknown): string {
  if (typeof data === "string") return data;
  if (data && typeof data === "object") {
    const record = data as Record<string, unknown>;
    if (typeof record.detail === "string") return record.detail;
    const first = Object.values(record)[0];
    if (Array.isArray(first) && typeof first[0] === "string") return first[0];
    if (typeof first === "string") return first;
  }
  return "Não foi possível concluir a operação. Tente novamente.";
}

async function request<T>(path: string, token?: string, init: RequestInit = {}): Promise<T> {
  let response: Response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...init,
      headers: {
        "Content-Type": "application/json",
        ...(token ? { Authorization: `Bearer ${token}` } : {}),
        ...init.headers,
      },
    });
  } catch {
    throw new ApiError("Não foi possível conectar à API. Confira se o back-end está em execução.");
  }
  const data = response.status === 204 ? null : await response.json().catch(() => null);
  if (!response.ok) throw new ApiError(errorMessage(data), response.status);
  return data as T;
}

export const api = {
  login(username: string, password: string) {
    return request<LoginResponse>("/auth/login/", undefined, {
      method: "POST",
      body: JSON.stringify({ username, password }),
    });
  },
  listDeliveries(token: string) {
    return request<Delivery[]>("/deliveries/", token);
  },
  listDrivers(token: string) {
    return request<DriverOption[]>("/drivers/", token);
  },
  createDelivery(token: string, input: { origin: string; destination: string; cargo_description: string }) {
    return request<Delivery>("/deliveries/", token, {
      method: "POST",
      body: JSON.stringify(input),
    });
  },
  assignDriver(token: string, deliveryId: number, driverId: number) {
    return request<Delivery>(`/deliveries/${deliveryId}/assign-driver/`, token, {
      method: "POST",
      body: JSON.stringify({ driver_id: driverId }),
    });
  },
};

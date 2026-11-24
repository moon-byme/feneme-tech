export type UserRole = "GESTOR" | "MOTORISTA";
export type DeliveryStatus = "PENDENTE" | "EM_TRANSPORTE" | "ENTREGUE";

export const DELIVERY_STATUS_LABELS: Record<DeliveryStatus, string> = {
  PENDENTE: "Pendente",
  EM_TRANSPORTE: "Em transporte",
  ENTREGUE: "Entregue",
};

export interface AuthUser {
  id: number;
  username: string;
  role: UserRole;
}

export interface LoginResponse {
  access: string;
  refresh: string;
  user: AuthUser;
}

export interface DriverOption {
  id: number;
  username: string;
}

export interface RouteAlternative {
  id: number;
  delivery: number;
  distance_km: number;
  duration_minutes: number;
  created_at: string;
}

export interface Delivery {
  id: number;
  /** Texto "Cidade - UF"; nas entregas anteriores à US-14 pode ser texto livre. */
  origin: string;
  destination: string;
  origin_city: number | null;
  destination_city: number | null;
  /** Entrega anterior à lista de cidades cuja origem ou destino não foi reconhecido. */
  needs_review: boolean;
  cargo_description: string;
  assigned_driver: number | null;
  assigned_driver_username: string | null;
  created_by_username: string;
  status: DeliveryStatus;
  route_alternatives?: RouteAlternative[];
  created_at: string;
  updated_at: string;
}

export interface DeliveryStatusChange {
  id: number;
  previous_status: DeliveryStatus;
  new_status: DeliveryStatus;
  changed_by_username: string;
  changed_at: string;
}

export interface DeliveryStatusHistoryResponse {
  delivery_id: number;
  current_status: DeliveryStatus;
  history: DeliveryStatusChange[];
}

export interface ReferenceLocation {
  slug: string;
  name: string;
}

export interface DailyForecast {
  location: ReferenceLocation;
  date: string;
  temperature_max: number;
  temperature_min: number;
  unit: string;
  source: string;
  notice: string;
}

/** US-15 / FT-114: tipo de carga com limite de temperatura de referência e fonte. */
export interface CargoType {
  id: number;
  name: string;
  category: string;
  limit_c: number;
  reference: string;
  source_name: string;
  source_url: string;
  source_type: string;
  is_derived: boolean;
}

/** US-14 / FT-113: cidade da lista fechada, a mesma do cadastro e do clima. */
export interface City {
  id: number;
  name: string;
  uf: string;
  label: string;
  slug: string;
  latitude: number;
  longitude: number;
}

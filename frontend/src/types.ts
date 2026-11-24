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
  origin: string;
  destination: string;
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

export type UserRole = "GESTOR" | "MOTORISTA";

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
  status: string;
  route_alternatives?: RouteAlternative[];
  created_at: string;
  updated_at: string;
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

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

export interface Delivery {
  id: number;
  origin: string;
  destination: string;
  cargo_description: string;
  assigned_driver: number | null;
  assigned_driver_username: string | null;
  created_by_username: string;
  status: string;
  created_at: string;
  updated_at: string;
}

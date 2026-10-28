import { useCallback, useEffect, useState } from "react";
import type { FormEvent } from "react";
import { api, ApiError } from "./api";
import MotoristaHome from "./components/MotoristaHome";
import type { AuthUser, Delivery, DriverOption, UserRole } from "./types";

type Session = { access: string; refresh: string; user: AuthUser };
const SESSION_KEY = "feneme-session";
const ROLES: UserRole[] = ["GESTOR", "MOTORISTA"];
const SESSION_EXPIRED = "Sua sessão expirou. Entre novamente.";

function isKnownRole(role: unknown): role is UserRole {
  return ROLES.includes(role as UserRole);
}

// Checagem apenas de interface: a assinatura do token é validada pelo back-end.
function tokenMatchesUser(access: string, user: AuthUser): boolean {
  try {
    const payload = access.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
    const claims = JSON.parse(atob(payload)) as { role?: unknown; exp?: unknown };
    return claims.role === user.role && typeof claims.exp === "number" && claims.exp * 1000 > Date.now();
  } catch {
    return false;
  }
}

function readSession(): Session | null {
  try {
    const raw = sessionStorage.getItem(SESSION_KEY);
    if (!raw) return null;
    const session = JSON.parse(raw) as Session;
    if (isKnownRole(session.user?.role) && tokenMatchesUser(session.access, session.user)) return session;
    sessionStorage.removeItem(SESSION_KEY);
    return null;
  } catch {
    return null;
  }
}

function App() {
  const [session, setSession] = useState<Session | null>(readSession);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [deliveries, setDeliveries] = useState<Delivery[]>([]);
  const [drivers, setDrivers] = useState<DriverOption[]>([]);
  const [origin, setOrigin] = useState("");
  const [destination, setDestination] = useState("");
  const [cargoDescription, setCargoDescription] = useState("");
  const [driverIds, setDriverIds] = useState<Record<number, string>>({});
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  const logout = useCallback((message = "") => {
    sessionStorage.removeItem(SESSION_KEY);
    setSession(null);
    setDeliveries([]);
    setDrivers([]);
    setError(message);
    setNotice("");
  }, []);

  // 401 com sessão ativa: token inválido ou expirado, volta ao login.
  const handleApiError = useCallback((e: unknown, fallback: string) => {
    if (e instanceof ApiError && e.status === 401) {
      logout(SESSION_EXPIRED);
      return;
    }
    setError(e instanceof ApiError ? e.message : fallback);
  }, [logout]);

  const loadDeliveries = useCallback(async (token: string) => {
    setLoading(true);
    try {
      setDeliveries(await api.listDeliveries(token));
      setError("");
    } catch (e) {
      handleApiError(e, "Erro ao consultar entregas.");
    } finally {
      setLoading(false);
    }
  }, [handleApiError]);

  const loadDrivers = useCallback(async (token: string) => {
    try {
      setDrivers(await api.listDrivers(token));
    } catch (e) {
      handleApiError(e, "Erro ao consultar motoristas.");
    }
  }, [handleApiError]);

  useEffect(() => {
    if (session?.user.role === "GESTOR") {
      void loadDeliveries(session.access);
      void loadDrivers(session.access);
    }
  }, [session, loadDeliveries, loadDrivers]);

  async function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setError("");
    setNotice("");
    try {
      const response = await api.login(username.trim(), password);
      if (!isKnownRole(response.user?.role)) {
        setError("Não foi possível realizar o login.");
        return;
      }
      sessionStorage.setItem(SESSION_KEY, JSON.stringify(response));
      setSession(response);
      setPassword("");
      setNotice("Login realizado com sucesso.");
    } catch (e) {
      // Mensagem genérica: não indica se o usuário existe (CT-14).
      setError(e instanceof ApiError && e.status !== 401 ? e.message : "Não foi possível realizar o login. Verifique usuário e senha.");
    } finally {
      setLoading(false);
    }
  }

  async function handleCreateDelivery(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    if (!session) return;
    setLoading(true);
    setError("");
    setNotice("");
    try {
      await api.createDelivery(session.access, {
        origin: origin.trim(),
        destination: destination.trim(),
        cargo_description: cargoDescription.trim(),
      });
      setOrigin("");
      setDestination("");
      setCargoDescription("");
      setNotice("Entrega cadastrada com sucesso.");
      await loadDeliveries(session.access);
    } catch (e) {
      handleApiError(e, "Não foi possível cadastrar a entrega.");
    } finally {
      setLoading(false);
    }
  }

  async function handleAssign(event: FormEvent<HTMLFormElement>, deliveryId: number) {
    event.preventDefault();
    if (!session) return;
    const driverId = Number(driverIds[deliveryId]);
    if (!Number.isInteger(driverId) || driverId <= 0) {
      setError("Selecione um motorista cadastrado.");
      return;
    }
    setLoading(true);
    setError("");
    setNotice("");
    try {
      await api.assignDriver(session.access, deliveryId, driverId);
      setNotice(`Motorista atribuído à entrega #${deliveryId}.`);
      await loadDeliveries(session.access);
    } catch (e) {
      handleApiError(e, "Não foi possível atribuir o motorista.");
    } finally {
      setLoading(false);
    }
  }

  if (!session) {
    return (
      <main className="login-shell">
        <section className="login-card">
          <div className="brand-mark" aria-hidden="true">F</div>
          <p className="eyebrow">GESTÃO LOGÍSTICA</p>
          <h1>Bem-vindo ao Feneme</h1>
          <p className="muted">Entre com sua conta Feneme.</p>
          <form onSubmit={handleLogin} className="stack">
            <label>
              Usuário
              <input autoComplete="username" value={username} onChange={(e) => setUsername(e.target.value)} required />
            </label>
            <label>
              Senha
              <input type="password" autoComplete="current-password" value={password} onChange={(e) => setPassword(e.target.value)} required />
            </label>
            {error && <p className="message error" role="alert">{error}</p>}
            {notice && <p className="message success" role="status">{notice}</p>}
            <button disabled={loading} type="submit">{loading ? "Entrando..." : "Entrar"}</button>
          </form>
          <p className="footnote">As contas são criadas pela administração do sistema. Não há cadastro público.</p>
        </section>
      </main>
    );
  }

  if (session.user.role === "MOTORISTA") {
    return <MotoristaHome user={session.user} onLogout={() => logout()} />;
  }

  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark small" aria-hidden="true">F</div>
          <div><strong>Feneme</strong><span>Gestão de entregas</span></div>
        </div>
        <div className="user-area">
          <span className="role-chip">Gestor</span>
          <span className="username">{session.user.username}</span>
          <button className="button-secondary" onClick={() => logout()} type="button">Sair</button>
        </div>
      </header>

      <section className="hero">
        <p className="eyebrow">PAINEL DE OPERAÇÕES</p>
        <h1>Gerencie suas entregas</h1>
        <p>Cadastre os dados essenciais da carga, consulte os registros e atribua um motorista responsável.</p>
      </section>

      {error && <p className="message error global-message" role="alert">{error}</p>}
      {notice && <p className="message success global-message" role="status">{notice}</p>}

      <div className="content-grid">
        <section className="panel">
          <div className="panel-heading">
            <div><p className="eyebrow">NOVA ENTREGA</p><h2>Cadastrar entrega</h2></div>
            <span className="step-number">01</span>
          </div>
          <form className="stack" onSubmit={handleCreateDelivery}>
            <label>
              Origem
              <input value={origin} onChange={(e) => setOrigin(e.target.value)} placeholder="Ex.: Campina Grande - PB" maxLength={180} required />
            </label>
            <label>
              Destino
              <input value={destination} onChange={(e) => setDestination(e.target.value)} placeholder="Ex.: João Pessoa - PB" maxLength={180} required />
            </label>
            <label>
              Descrição da carga
              <textarea value={cargoDescription} onChange={(e) => setCargoDescription(e.target.value)} placeholder="Descreva o tipo de alimento ou carga transportada" maxLength={500} rows={3} required />
            </label>
            <button disabled={loading} type="submit">{loading ? "Salvando..." : "Cadastrar entrega"}</button>
          </form>
        </section>

        <section className="panel delivery-panel">
          <div className="panel-heading">
            <div><p className="eyebrow">REGISTROS</p><h2>Entregas cadastradas</h2></div>
            <span className="count-badge">{deliveries.length}</span>
          </div>
          <div className="list-toolbar">
            <span className="muted">Dados persistidos no sistema</span>
            <button className="button-secondary" type="button" disabled={loading} onClick={() => void loadDeliveries(session.access)}>Atualizar</button>
          </div>
          {loading && deliveries.length === 0 ? (
            <p className="empty-state">Carregando entregas...</p>
          ) : deliveries.length === 0 ? (
            <div className="empty-state">
              <div className="empty-icon" aria-hidden="true">↗</div>
              <strong>Nenhuma entrega cadastrada</strong>
              <p>Quando uma entrega for criada, ela aparecerá aqui.</p>
            </div>
          ) : (
            <div className="delivery-list">
              {deliveries.map((delivery) => (
                <article className="delivery-card" key={delivery.id}>
                  <div className="delivery-card-top">
                    <span className="delivery-id">ENTREGA #{delivery.id}</span>
                    <span className="status-chip">{delivery.status === "PENDENTE" ? "Pendente" : delivery.status}</span>
                  </div>
                  <div className="route">
                    <div><span className="route-dot origin-dot" /><div><small>ORIGEM</small><strong>{delivery.origin}</strong></div></div>
                    <div className="route-line" />
                    <div><span className="route-dot destination-dot" /><div><small>DESTINO</small><strong>{delivery.destination}</strong></div></div>
                  </div>
                  <div className="cargo"><small>CARGA</small><p>{delivery.cargo_description}</p></div>
                  <div className="assignment">
                    {delivery.assigned_driver_username ? (
                      <p className="assigned-label">Motorista: <strong>{delivery.assigned_driver_username}</strong></p>
                    ) : (
                      <p className="muted">Ainda sem motorista atribuído.</p>
                    )}
                    <form onSubmit={(event) => void handleAssign(event, delivery.id)} className="assign-form">
                      <label htmlFor={`driver-${delivery.id}`}>Motorista cadastrado</label>
                      <div className="assign-controls">
                        <select
                          id={`driver-${delivery.id}`}
                          value={driverIds[delivery.id] ?? ""}
                          onChange={(e) => setDriverIds((current) => ({ ...current, [delivery.id]: e.target.value }))}
                          required
                        >
                          <option value="">Selecione um motorista...</option>
                          {drivers.map((driver) => (
                            <option value={driver.id} key={driver.id}>{driver.username} (ID {driver.id})</option>
                          ))}
                        </select>
                        <button type="submit" disabled={loading || drivers.length === 0}>Atribuir</button>
                      </div>
                      {drivers.length === 0 && <small className="muted">Cadastre um usuário com perfil Motorista no Admin para habilitar a atribuição.</small>}
                    </form>
                  </div>
                </article>
              ))}
            </div>
          )}
        </section>
      </div>
      <footer>Feneme · Sprint 1 · Gestão de entregas e cargas</footer>
    </main>
  );
}

export default App;

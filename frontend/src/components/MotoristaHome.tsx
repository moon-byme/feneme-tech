import type { AuthUser } from "../types";

type Props = { user: AuthUser; onLogout: () => void };

// Área mínima do Motorista (FT-54). Não consulta /deliveries/ nem /drivers/:
// a listagem das entregas atribuídas é a US-10 (FT-58, Release 2).
function MotoristaHome({ user, onLogout }: Props) {
  return (
    <main className="app-shell">
      <header className="topbar">
        <div className="brand">
          <div className="brand-mark small" aria-hidden="true">F</div>
          <div><strong>Feneme</strong><span>Minhas entregas</span></div>
        </div>
        <div className="user-area">
          <span className="role-chip">Motorista</span>
          <span className="username">{user.username}</span>
          <button className="button-secondary" onClick={onLogout} type="button">Sair</button>
        </div>
      </header>

      <section className="hero">
        <p className="eyebrow">ÁREA DO MOTORISTA</p>
        <h1 className="break-anywhere">Olá, {user.username}</h1>
        <p>Você está conectado ao Feneme com o perfil Motorista.</p>
      </section>

      <section className="panel">
        <div className="empty-state">
          <div className="empty-icon" aria-hidden="true">↗</div>
          <strong>Entregas atribuídas</strong>
          <p>A lista das entregas sob sua responsabilidade estará disponível em uma próxima entrega do sistema.</p>
        </div>
      </section>
      <footer>Feneme · Sprint 1 · Área do Motorista</footer>
    </main>
  );
}

export default MotoristaHome;

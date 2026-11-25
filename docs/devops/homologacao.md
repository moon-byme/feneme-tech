# Homologação — deploy automatizado (FT-110)

> Responsável: DevOps da R2 (João Paulo de Araujo). Tarefa: [FT-110](https://feneme.atlassian.net/browse/FT-110). Relatório da release: [FT-92](https://feneme.atlassian.net/browse/FT-92).

## Como funciona

```
PR integrado na main
  └─ GitHub Actions (ci.yml)
       ├─ Backend - Django checks and tests
       ├─ Frontend - build and tests
       ├─ E2E - Cucumber/Cypress (@smoke)
       ├─ Segurança - segredos fora do repositório
       └─ Deploy - homologação (Render)      ← só roda se TODOS acima passarem
            ├─ chama o Deploy Hook do Render com o commit da main
            └─ espera /api/health/ responder com o mesmo commit
```

- **Provedor:** [Render](https://render.com), plano gratuito: um *Web Service* Python e um PostgreSQL gratuito, descritos em [`render.yaml`](../../render.yaml).
- **Deploy automático do Render desligado** (`autoDeployTrigger: "off"`): quem dispara é o GitHub Actions, e só depois do CI verde. Se algum job falhar, o deploy é pulado e a versão anterior continua no ar.
- **Build:** compila o frontend (Vite), instala o backend e roda `collectstatic`. O Django serve a API e o frontend; o WhiteNoise serve os arquivos estáticos.
- **Partida:** `migrate`, `seed_homologacao` (contas de demonstração) e `gunicorn`. O plano gratuito não tem *pre-deploy command*, por isso a migração roda na partida.
- **Verificação:** `GET /api/health/` é público e devolve `{"status": "ok", "database": "ok", "commit": "<sha>"}`, sem dados de usuários nem segredos.

## Segredos

| Onde | Nome | Conteúdo |
| --- | --- | --- |
| Render (gerado pelo Blueprint) | `DJANGO_SECRET_KEY` | valor aleatório gerado pelo Render |
| Render (vinculado ao banco) | `DATABASE_URL` | string de conexão do PostgreSQL do Render |
| Render (informado no painel) | `HOMOLOG_GESTOR_PASSWORD`, `HOMOLOG_MOTORISTA_PASSWORD` | senhas de `gestor_demo` e `motorista_demo` |
| GitHub → Settings → Secrets and variables → Actions → **Secrets** | `RENDER_DEPLOY_HOOK_URL` | Deploy Hook do serviço no Render |
| GitHub → Settings → Secrets and variables → Actions → **Variables** | `HOMOLOGACAO_URL` | URL pública, ex.: `https://feneme-homologacao.onrender.com` |

Nenhum desses valores fica no repositório. O GitHub mascara os *secrets* nos logs, e o job `Segurança - segredos fora do repositório` falha se encontrar chave do Google, chave privada, `.env` versionado ou URL de banco com senha.

Em homologação, `DJANGO_DEBUG=False`: cookies só por HTTPS, `ALLOWED_HOSTS` e `CSRF_TRUSTED_ORIGINS` recebem o host do Render automaticamente, e o Django se recusa a subir sem `DJANGO_SECRET_KEY`. O redirecionamento de HTTP para HTTPS é feito pelo próprio Render.

## Configuração inicial (uma vez, ~15 minutos)

1. Entrar em <https://dashboard.render.com> com a conta GitHub e autorizar o repositório `moon-byme/feneme-tech`.
2. **New → Blueprint** → escolher o repositório, branch `main`. O Render lê o `render.yaml` e cria `feneme-homologacao` e `feneme-homologacao-db`.
3. Informar `HOMOLOG_GESTOR_PASSWORD` e `HOMOLOG_MOTORISTA_PASSWORD` quando o Render pedir (senhas fortes; compartilhar com a equipe só por mensagem privada).
4. Aguardar o primeiro deploy e abrir `https://<serviço>.onrender.com/api/health/`.
5. No serviço: **Settings → Deploy Hook → copiar** a URL.
6. No GitHub: criar o secret `RENDER_DEPLOY_HOOK_URL` (Deploy Hook) e a variável `HOMOLOGACAO_URL` (URL pública).
7. Rodar o workflow `CI` na `main` (**Actions → CI → Run workflow**) e conferir o job `Deploy - homologação (Render)` verde.

## Reproduzir localmente o ambiente de homologação

```bash
cd frontend && npm ci && npm run build
cd ../backend
export DJANGO_DEBUG=False DJANGO_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_urlsafe(50))')"
export DATABASE_URL=postgresql://feneme:<senha>@localhost:5432/feneme_homolog
export HOMOLOG_GESTOR_PASSWORD=<senha> HOMOLOG_MOTORISTA_PASSWORD=<senha>
export DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
python manage.py collectstatic --noinput && python manage.py migrate && python manage.py seed_homologacao
gunicorn config.wsgi:application --bind 127.0.0.1:8000
curl http://localhost:8000/api/health/
```

## Reverter (rollback)

- **Pelo Render:** no serviço, aba **Events/Deploys** → deploy anterior → **Rollback**. Volta o código; o banco não é revertido.
- **Pelo Git (preferível, deixa rastro):** abrir PR com `git revert <commit>` na `main`. Com o CI verde, o deploy leva a versão revertida.
- Migração que precise ser desfeita: `python manage.py migrate <app> <migração anterior>` pelo *Shell* do Render (plano pago) ou um novo PR com a migração reversa.

## Limitações do plano gratuito

- O serviço **hiberna após ~15 minutos sem acesso**; o primeiro acesso depois disso demora cerca de 1 minuto. Abrir a URL alguns minutos antes de uma demo.
- O PostgreSQL gratuito **expira 30 dias após a criação** e tem 1 GB. Para a R3/R4, recriar o banco (o deploy refaz migrações e contas) ou migrar de plano na FT-102.
- Sem domínio próprio, sem alta disponibilidade e sem *Shell*. Ambiente de produção e endurecimento ficam na FT-102 (R4).
- Dados de homologação são fictícios; não usar dados reais.

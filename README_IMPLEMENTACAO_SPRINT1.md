# Feneme — implementação dos requisitos da Sprint 1

Este pacote adiciona uma implementação inicial dos requisitos FT-43, FT-44, FT-55 e FT-45 ao repositório existente. Ele foi preparado para ser copiado para a raiz de `moon-byme/feneme-tech`, preservando os arquivos `.github/`, `CONTRIBUTING.md`, `JIRA_TAREFAS.md` e `README.md` já existentes.

## Requisitos incluídos

- **FT-43 / US-01:** login com credenciais e retorno do perfil do usuário.
- **FT-44 / US-03:** cadastro de entrega com origem, destino e descrição da carga.
- **FT-55 / US-04:** listagem das entregas persistidas, com estado vazio.
- **FT-45 / US-05:** atribuição de uma entrega existente a uma conta com perfil Motorista.

A API valida as permissões no servidor. A interface consulta a lista de Motoristas cadastrados para que o Gestor possa selecioná-los sem precisar memorizar IDs. Não existe endpoint de cadastro público. As contas são criadas por um administrador do Django ou pelo comando administrativo documentado abaixo.

## Estrutura

```text
backend/
  accounts/             # Perfil de acesso, login e permissões
  config/                # Configuração Django e rotas
  deliveries/             # Modelo, API, validações e testes
  manage.py
  requirements.txt
  Dockerfile
frontend/
  src/                   # Interface React + TypeScript
  index.html
  package.json
  tsconfig.json
  vite.config.ts
docker-compose.yml
.env.example
README_IMPLEMENTACAO_SPRINT1.md
```

## Executar com Docker (recomendado)

1. Instale Docker Desktop e inicie o Docker.
2. Na raiz do repositório, copie `.env.example` para `.env`.
3. Altere `DJANGO_SECRET_KEY` para um valor aleatório local. Não versione `.env`.
4. Execute:

   ```bash
   docker compose up --build
   ```

5. Crie contas de teste em outro terminal:

   ```bash
   docker compose exec backend python manage.py createsuperuser
   docker compose exec backend python manage.py create_feneme_user --username motorista_demo --role MOTORISTA
   ```

   O comando solicitará a senha. Para o gestor, crie um usuário normal no Django Admin e marque o perfil como `GESTOR`, ou use o mesmo comando com `--role GESTOR`.

6. Abra `http://localhost:5173`. A API estará em `http://localhost:8000/api/`.
7. Para administrar usuários, acesse `http://localhost:8000/admin/`.

A primeira execução aplica as migrações automaticamente. Para entrar no Admin, use uma conta criada com `createsuperuser`. No Admin, o perfil de cada usuário pode ser alterado entre `GESTOR` e `MOTORISTA`.

## Executar sem Docker

### Back-end

Requer Python 3.12+ e PostgreSQL (ou SQLite para desenvolvimento local).

```bash
cd backend
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# Linux/macOS:
# source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Sem variáveis de banco, o Django usa SQLite local para facilitar desenvolvimento e testes. Para usar PostgreSQL, defina `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST` e `DB_PORT`.

### Front-end

Em outro terminal:

```bash
cd frontend
npm install
npm run dev
```

O front-end usa `http://localhost:8000/api` por padrão. Para mudar, crie `frontend/.env` com `VITE_API_BASE_URL=http://localhost:8000/api`.

## API

Todas as respostas de erro seguem o formato JSON do Django REST Framework.

- `POST /api/auth/login/` — recebe `username` e `password`; retorna `access`, `refresh` e `user` (`id`, `username`, `role`).
- `POST /api/auth/refresh/` — renova o access token.
- `GET /api/drivers/` — lista contas ativas com perfil Motorista; somente Gestor autenticado.
- `GET /api/deliveries/` — lista entregas; somente Gestor autenticado.
- `POST /api/deliveries/` — cria entrega; somente Gestor autenticado. Campos obrigatórios: `origin`, `destination`, `cargo_description`.
- `GET /api/deliveries/{id}/` — consulta uma entrega específica; somente Gestor autenticado.
- `POST /api/deliveries/{id}/assign-driver/` — recebe `driver_id`; somente Gestor autenticado. O usuário precisa existir e ter perfil `MOTORISTA`.

Exemplo de cadastro:

```json
{
  "origin": "Campina Grande - PB",
  "destination": "João Pessoa - PB",
  "cargo_description": "Alimentos refrigerados"
}
```

Exemplo de atribuição:

```json
{
  "driver_id": 3
}
```

## Decisões de escopo

- A descrição do Jira indica origem, destino e descrição/tipo da carga como campos mínimos. Data prevista e localidade meteorológica foram explicitamente deixadas para validação do PO, então não foram impostas nesta implementação.
- O identificador é gerado pelo banco de dados.
- Não existe cadastro separado de carga nem de veículo.
- Não foram incluídos atualização de status pelo Motorista, recomendações de rota, Open-Meteo, histórico, edição ou exclusão, pois pertencem a outras histórias.
- O projeto existente menciona a integração Open-Meteo; ela não é necessária para estes quatro requisitos e foi deixada fora deste escopo.
- Os testes automatizados cobrem login, bloqueio de acesso sem autenticação/sem perfil Gestor, cadastro, listagem e atribuição válida/inválida.

## Segurança e limitações

- Configure `DJANGO_SECRET_KEY` e `DJANGO_DEBUG=False` antes de qualquer implantação pública.
- Não use senhas reais no repositório e não versione arquivos `.env`.
- O CORS está limitado por padrão a `localhost:5173`; ajuste `CORS_ALLOWED_ORIGINS` conforme o ambiente.
- O armazenamento de token no `sessionStorage` é uma simplificação para o MVP acadêmico; para produção, avalie uma arquitetura com cookies `HttpOnly`, `Secure` e proteção CSRF.
- O código precisa ser executado e revisado no ambiente da equipe. Um pacote gerado não substitui evidência de CI, revisão por PR ou aceite de QA.

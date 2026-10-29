# Feneme — implementação dos requisitos da Sprint 1

Este repositório contém a implementação dos requisitos FT-43, FT-44, FT-55, FT-45, FT-54 e FT-58 do Feneme, com interface React servida pelo Django e persistência em PostgreSQL local.

## Requisitos incluídos

- **FT-43 / US-01:** login com credenciais e retorno do perfil do usuário.
- **FT-54 / US-02:** login compartilhado com reconhecimento do perfil Motorista.
- **FT-44 / US-03:** cadastro de entrega com origem, destino e descrição da carga.
- **FT-55 / US-04:** listagem das entregas persistidas, com estado vazio.
- **FT-45 / US-05:** atribuição de uma entrega existente a uma conta com perfil Motorista.
- **FT-58 / US-10:** consulta das entregas atribuídas ao Motorista autenticado, com isolamento entre contas.

A API valida as permissões no servidor. A interface consulta a lista de Motoristas cadastrados para que o Gestor possa selecioná-los sem precisar memorizar IDs. Não existe endpoint de cadastro público. As contas são criadas por um administrador do Django ou pelo comando administrativo documentado abaixo.

## Estrutura e execução local

```text
backend/
  accounts/              # Perfil de acesso, login e permissões
  config/                # Configuração Django e rotas
  deliveries/            # Modelo, API, validações e testes
  manage.py
  requirements.txt
frontend/
  src/                   # Interface React + TypeScript
  dist/                  # Build gerado; não versionado
  index.html
  package.json
  tsconfig.json
  vite.config.ts
.env.example
iniciar.ps1
README_IMPLEMENTACAO_SPRINT1.md
```

O navegador acessa `http://localhost:8000`. O Django entrega a interface React compilada, seus arquivos em `/static/`, a API em `/api/` e o painel administrativo em `/admin/`. O PostgreSQL funciona como serviço local e não precisa de terminal aberto. Depois da preparação, basta manter um servidor Django em execução.

### Preparação no Windows (uma vez)

Requer Python 3.12+, Node.js 22+ com npm e PostgreSQL 14+ instalado e em execução. Execute os comandos PowerShell a partir da raiz do repositório.

1. No pgAdmin, abra o Query Tool conectado ao banco `postgres` como administrador. Execute cada instrução abaixo separadamente, com autocommit habilitado. Escolha uma senha local para o usuário da aplicação:

   ```sql
   CREATE ROLE feneme LOGIN PASSWORD 'substitua_por_uma_senha_local';
   CREATE DATABASE feneme OWNER feneme;
   ```

   Para executar os testes Django localmente, conceda também permissão de criar o banco temporário de testes:

   ```sql
   ALTER ROLE feneme CREATEDB;
   ```

2. Copie a configuração de exemplo:

   ```powershell
   Copy-Item .env.example .env
   ```

   Edite o `.env` da raiz: configure `DJANGO_SECRET_KEY` com um valor aleatório e ajuste `DB_NAME`, `DB_USER`, `DB_PASSWORD`, `DB_HOST=localhost` e `DB_PORT=5432` conforme seu PostgreSQL. Mantenha `DJANGO_DEBUG=True` para o servidor local entregar os arquivos estáticos. Não versione `.env`.

   O Django carrega esse arquivo automaticamente, mesmo quando iniciado pela pasta `backend`. Variáveis já definidas no ambiente têm prioridade. O banco é exclusivamente PostgreSQL.

3. Prepare o ambiente Python e instale as dependências:

   ```powershell
   python -m venv backend/.venv
   .\backend\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt
   ```

   Não é necessário ativar o ambiente virtual quando se usa o caminho completo do executável.

4. Instale e compile o frontend:

   ```powershell
   Push-Location frontend
   npm.cmd install
   npm.cmd run build
   Pop-Location
   ```

   O build usa `/api` no mesmo endereço do Django. O arquivo `frontend/.env` é opcional; `VITE_API_BASE_URL` só precisa ser preenchida para usar outra API. Valores antigos com `http://localhost:8000/api` devem ser removidos para usar o mesmo endereço do navegador. Variáveis `VITE_*` são incorporadas no build; recompile após alterá-las.

5. Aplique as migrações e crie as contas:

   ```powershell
   .\backend\.venv\Scripts\python.exe backend/manage.py migrate
   .\backend\.venv\Scripts\python.exe backend/manage.py createsuperuser
   .\backend\.venv\Scripts\python.exe backend/manage.py create_feneme_user --username gestor_demo --role GESTOR
   .\backend\.venv\Scripts\python.exe backend/manage.py create_feneme_user --username motorista_demo --role MOTORISTA
   ```

   Os comandos solicitam as senhas. Use o superusuário para administrar contas em `/admin/` e a conta Gestor para entrar na interface da Sprint 1. Os perfis também podem ser alterados no Django Admin.

### Iniciar com um comando

Na raiz do repositório:

```powershell
.\iniciar.ps1
```

O script usa o ambiente `backend/.venv`, recompila o React, aplica as migrações e inicia o Django no mesmo terminal. Ele interrompe a inicialização se o build ou as migrações falharem. Abra `http://localhost:8000` e use `Ctrl+C` para encerrar.

Se o PowerShell bloquear a execução do script, use uma liberação apenas para esse processo:

```powershell
powershell -ExecutionPolicy Bypass -File .\iniciar.ps1
```

Com o frontend já compilado e as migrações aplicadas, também é possível iniciar somente o Django:

```powershell
Set-Location backend
.\.venv\Scripts\python.exe manage.py runserver
```

Após alterar o React, execute novamente `npm.cmd run build` na pasta `frontend` ou reinicie com `iniciar.ps1`. Não é necessário manter o Vite aberto. A rota da interface é `/`; rotas inexistentes da API continuam retornando 404.

### Linux/macOS

Após preparar o mesmo banco PostgreSQL e o `.env` da raiz:

```bash
python3 -m venv backend/.venv
backend/.venv/bin/python -m pip install -r backend/requirements.txt
(cd frontend && npm install && npm run build)
backend/.venv/bin/python backend/manage.py migrate
backend/.venv/bin/python backend/manage.py createsuperuser
backend/.venv/bin/python backend/manage.py create_feneme_user --username gestor_demo --role GESTOR
backend/.venv/bin/python backend/manage.py runserver
```

### Verificação

Com PostgreSQL disponível e a permissão `CREATEDB` configurada para o usuário de testes:

```powershell
Push-Location backend
.\.venv\Scripts\python.exe manage.py check
.\.venv\Scripts\python.exe manage.py test --noinput
Pop-Location
Push-Location frontend
npm.cmd run build
Pop-Location
```

Os testes criam e removem um banco separado, `test_feneme` por padrão. No GitHub Actions, o workflow prepara um PostgreSQL local no runner Linux para verificar o backend; o job do frontend continua compilando a interface.

## API

Todas as respostas de erro seguem o formato JSON do Django REST Framework.

- `POST /api/auth/login/` — recebe `username` e `password`; retorna `access`, `refresh` e `user` (`id`, `username`, `role`).
- `POST /api/auth/refresh/` — renova o access token.
- `GET /api/drivers/` — lista contas ativas com perfil Motorista; somente Gestor autenticado.
- `GET /api/deliveries/` — Gestor consulta todas as entregas; Motorista consulta somente as atribuídas à própria conta. Requer autenticação e perfil válido.
- `POST /api/deliveries/` — cria entrega; somente Gestor autenticado. Campos obrigatórios: `origin`, `destination`, `cargo_description`.
- `GET /api/deliveries/{id}/` — Gestor consulta qualquer entrega; Motorista consulta somente uma entrega atribuída à própria conta. Para o Motorista, entregas de outro Motorista, sem atribuição ou inexistentes retornam o mesmo `404`.
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
- O projeto existente menciona a integração Open-Meteo; ela não é necessária para estes requisitos e foi deixada fora deste escopo.
- Os testes automatizados cobrem login, bloqueio de acesso sem autenticação, permissões por perfil, cadastro, isolamento da consulta por Motorista e atribuição válida/inválida.

## Segurança e limitações

- O `runserver` com arquivos estáticos e `DJANGO_DEBUG=True` atende à execução local. Uma implantação pública precisa de servidor apropriado e configuração de arquivos estáticos; apenas mudar `DJANGO_DEBUG=False` não basta. Consulte a [documentação do Django](https://docs.djangoproject.com/en/5.2/howto/static-files/).
- Não use senhas reais no repositório e não versione arquivos `.env`.
- O CORS está limitado por padrão a `localhost:5173`; ajuste `CORS_ALLOWED_ORIGINS` conforme o ambiente.
- O armazenamento de token no `sessionStorage` é uma simplificação para o MVP acadêmico; para produção, avalie uma arquitetura com cookies `HttpOnly`, `Secure` e proteção CSRF.
- O código precisa ser executado e revisado no ambiente da equipe. Um pacote gerado não substitui evidência de CI, revisão por PR ou aceite de QA.

## FT-54 / US-02 — Login como Motorista

**O que mudou**

- Back-end: sem alteração de lógica. O login (`POST /api/auth/login/`) já era compartilhado entre os perfis. Foram criados testes em `backend/accounts/tests.py` cobrindo CT-13 (login válido do Motorista e claim `role`), CT-14 (senha errada, usuário inexistente e conta inativa com a mesma mensagem e sem tokens), bloqueio das operações do Gestor para o Motorista (403, sem alterar dados), acesso cruzado entre dois Motoristas e sessão inválida (sem token, token malformado, expirado, adulterado e refresh usado como access).
- Front-end: o login aceita Gestor e Motorista, com textos neutros ("Entrar"). A área inicial do Motorista (`src/components/MotoristaHome.tsx`) foi ampliada pela FT-58 para consultar suas entregas, conforme a seção abaixo. Um 401 com sessão ativa encerra a sessão e mostra "Sua sessão expirou. Entre novamente.". Na leitura do `sessionStorage`, uma sessão cujo token esteja expirado ou com `role` diferente do usuário salvo é descartada.

**Como testar**

```powershell
cd backend
python manage.py test accounts
python manage.py create_feneme_user --username motorista_demo --role MOTORISTA
```

Depois, com back-end e front-end em execução, entre com a conta Motorista: a tela "Área do Motorista" deve aparecer. Com senha errada, a mensagem "Não foi possível realizar o login. Verifique usuário e senha." aparece e nenhuma sessão é criada.

## FT-58 / US-10 — Consultar entregas como Motorista

O filtro é aplicado no servidor usando a conta autenticada e seu perfil atual no banco. Parâmetros enviados pelo cliente não permitem consultar entregas de outro Motorista. A consulta individual usa o mesmo filtro da listagem: uma entrega fora da responsabilidade do Motorista retorna `404`, sem expor os dados da carga ou indicar se o registro existe. Contas sem perfil ou com perfil desconhecido recebem `403`.

O Gestor continua consultando todas as entregas e sendo o único perfil autorizado a cadastrar e atribuir. Ao reatribuir uma entrega, ela deixa de aparecer nas consultas do Motorista anterior e passa a aparecer nas do novo responsável.

A tela do Motorista mostra identificador, origem, destino, descrição da carga e status, além dos estados de carregamento, erro e lista vazia. O botão **Atualizar** refaz a consulta; não há atualização automática em segundo plano. A tela não consulta a lista de Motoristas e não oferece cadastro, atribuição ou alteração de status. Uma resposta `401` encerra a sessão e pede novo login.

Para validar automaticamente, execute a partir da raiz do projeto:

```powershell
.\backend\.venv\Scripts\python.exe backend/manage.py test --noinput
```

Os testes de `deliveries/test_ft58.py` cobrem isolamento da listagem e dos detalhes, entregas sem atribuição, tentativa de alterar o filtro por parâmetros, requisições HEAD, bloqueio de escrita, reatribuição, acesso do Gestor e contas com perfil ausente, desconhecido ou alterado após a emissão do token. Os testes de autenticação existentes foram atualizados para permitir a consulta própria e exigir `404` no acesso cruzado.

Para testar pela interface:

1. Recompile com `npm.cmd run build` na pasta `frontend`, ou reinicie usando `.\iniciar.ps1` na raiz.
2. Entre como Gestor, cadastre entregas e atribua uma delas a `motorista_demo`.
3. Saia e entre como `motorista_demo`: somente as entregas atribuídas a essa conta devem aparecer.
4. Para verificar o isolamento, crie outra conta Motorista e atribua outra entrega a ela. Essa entrega não deve aparecer para `motorista_demo`.
5. Reatribua uma entrega como Gestor e, ao voltar à conta do Motorista anterior, clique em **Atualizar**: a entrega deve desaparecer da lista.

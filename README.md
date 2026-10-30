# Feneme

Sistema web para gestão de entregas no transporte de alimentos, desenvolvido como projeto acadêmico. O Feneme busca apoiar a organização das operações logísticas, reunindo informações sobre entregas, responsáveis e, nas próximas etapas, dados climáticos e informações de trajetos.

> **Estado desta documentação:** Release 2 em desenvolvimento. Este README descreve o código encontrado no repositório analisado e distingue as funcionalidades já implementadas daquelas ainda previstas.

## Sumário

- [Visão geral](#visão-geral)
- [Estado atual do projeto](#estado-atual-do-projeto)
- [Funcionalidades implementadas](#funcionalidades-implementadas)
- [Funcionalidades previstas](#funcionalidades-previstas)
- [Arquitetura e funcionamento](#arquitetura-e-funcionamento)
- [Tecnologias utilizadas](#tecnologias-utilizadas)
- [Estrutura do repositório](#estrutura-do-repositório)
- [Executar localmente](#executar-localmente)
- [API disponível](#api-disponível)
- [Testes e qualidade](#testes-e-qualidade)
- [Processo de desenvolvimento](#processo-de-desenvolvimento)
- [Equipe e papéis da Release 2](#equipe-e-papéis-da-release-2)
- [Documentação complementar](#documentação-complementar)

## Visão geral

O transporte de alimentos envolve fatores como origem, destino, duração do deslocamento, características da carga e condições de temperatura. A falta de integração dessas informações pode dificultar o planejamento logístico e aumentar o risco de atrasos, perdas de qualidade e prejuízos.

O Feneme está sendo desenvolvido para apoiar a gestão dessas operações por meio de uma aplicação web. A proposta contempla dois perfis principais:

- **Gestor:** organiza as entregas, consulta os registros e atribui motoristas.
- **Motorista:** consulta as entregas que foram atribuídas à sua própria conta e, conforme a evolução do produto, poderá acompanhar e atualizar sua execução.

O sistema está sendo desenvolvido incrementalmente, em releases e sprints. Por isso, nem todas as funcionalidades previstas para o produto estão necessariamente disponíveis na versão atual.

## Estado atual do projeto

A Release 1 estabeleceu o fluxo básico de autenticação e gestão de entregas. O repositório já contém uma aplicação integrada, com frontend React, backend Django e persistência em PostgreSQL.

Na versão analisada, o fluxo funcional implementado permite:

1. autenticar usuários com perfil Gestor ou Motorista;
2. cadastrar entregas como Gestor;
3. consultar as entregas como Gestor;
4. consultar os motoristas cadastrados;
5. atribuir uma entrega a um Motorista;
6. permitir que cada Motorista consulte somente as entregas atribuídas à própria conta.

A equipe iniciou a **Release 2**, na qual os papéis Scrum são redistribuídos. As funcionalidades adicionais devem ser incorporadas conforme o backlog e os critérios de aceitação definidos para a release.

## Funcionalidades implementadas

As funcionalidades abaixo foram identificadas no código disponível no repositório analisado.

### Autenticação e contas

- Login por nome de usuário e senha.
- Autenticação baseada em tokens JWT.
- Identificação do perfil do usuário no retorno da autenticação.
- Perfis de acesso Gestor e Motorista.
- Encerramento da sessão pela interface.
- Tratamento de sessão expirada ou token inválido.
- Criação de contas por meio da administração do Django ou de comando administrativo.
- Não existe cadastro público de usuários na interface.

### Gestão de entregas — Gestor

- Cadastro de entrega com origem, destino e descrição da carga.
- Consulta das entregas cadastradas.
- Exibição dos dados da entrega e de seu status.
- Consulta de contas ativas com perfil Motorista.
- Atribuição e reatribuição de uma entrega a um Motorista válido.

### Consulta de entregas — Motorista

- Consulta das entregas atribuídas ao usuário autenticado.
- Exibição do identificador, origem, destino, descrição da carga e status.
- Atualização manual da listagem por meio do botão de atualização.
- Exibição de estado de carregamento, erro e lista vazia.
- Isolamento dos dados: o Motorista não consulta entregas atribuídas a outras contas.

### Segurança e autorização

- As permissões são verificadas no backend, não apenas na interface.
- Operações exclusivas do Gestor são bloqueadas para Motoristas.
- A listagem e a consulta individual de entregas aplicam o filtro de acordo com o usuário autenticado.
- Uma consulta individual de entrega não atribuída ao Motorista retorna `404`, evitando expor se o registro existe.
- A atribuição exige uma conta ativa com perfil Motorista.

## Funcionalidades previstas ou ainda não disponíveis

As funcionalidades a seguir fazem parte da proposta mais ampla do Feneme ou foram indicadas na documentação de planejamento, mas **não foram identificadas como implementadas no código analisado**. A inclusão e a prioridade de cada uma devem seguir o backlog aprovado da Release 2 e das releases seguintes.

- Integração com a API Open-Meteo para consulta de informações climáticas.
- Consulta e apresentação de temperatura associada às entregas ou aos trajetos.
- Cadastro, comparação ou recomendação de alternativas de rota.
- Cálculo ou apresentação de distância e tempo estimado de deslocamento.
- Atualização do status da entrega pelo Motorista.
- Histórico de entregas e de alterações.
- Funcionalidades adicionais de acompanhamento da operação.

**Limites da implementação atual:** o modelo de entrega possui apenas o status `PENDENTE`; não há fluxo de atualização de status. Também não foram identificados no frontend ou backend atuais recursos de integração climática, recomendação de rotas ou histórico de entregas. A presença dessas ideias na visão do produto não significa que estejam disponíveis.

## Arquitetura e funcionamento

O projeto utiliza uma arquitetura web com frontend separado do backend durante o desenvolvimento, mas com a interface compilada sendo servida pelo Django na execução integrada.

### Visão geral

```text
Navegador
   |
   v
Frontend React + TypeScript
   |
   | Requisições HTTP / JSON
   | Token JWT no cabeçalho Authorization
   v
Backend Django + Django REST Framework
   |
   +---- accounts
   |       - autenticação
   |       - perfis
   |       - permissões
   |
   +---- deliveries
   |       - cadastro e consulta
   |       - atribuição de motoristas
   |       - regras de acesso
   |
   v
PostgreSQL
   - usuários e perfis
   - entregas
```

### Backend

O backend é uma aplicação Django organizada em dois apps principais:

- `accounts`: complementa o usuário do Django com o perfil de acesso, implementa a autenticação customizada que inclui o papel no token e disponibiliza a listagem de motoristas.
- `deliveries`: contém o modelo de entrega, serializers, validações, endpoints e regras de autorização para consulta e atribuição.

O Django REST Framework disponibiliza a API em `/api/`. A autenticação da API utiliza JWT, com tokens de acesso e renovação.

### Frontend

O frontend utiliza React com TypeScript. O componente principal `App.tsx` controla o login, a sessão e a área do Gestor. A área do Motorista está separada em `components/MotoristaHome.tsx`. A comunicação HTTP com a API está centralizada em `api.ts`, enquanto os tipos compartilhados ficam em `types.ts`.

Durante o desenvolvimento, o Vite pode servir a interface separadamente. Na execução integrada documentada, o comando de build gera os arquivos estáticos em `frontend/dist/`, e o Django entrega a interface e os recursos estáticos.

### Banco de dados

O sistema utiliza PostgreSQL. Entre os dados persistidos estão:

- usuários do Django;
- perfil de cada usuário, relacionado ao usuário por uma relação um-para-um;
- entregas, incluindo origem, destino, descrição da carga, motorista atribuído, usuário criador, status e datas de criação/atualização.

O motorista atribuído pode ser nulo, permitindo que uma entrega permaneça sem responsável até que o Gestor faça a atribuição.

## Tecnologias utilizadas

| Camada | Tecnologia |
|---|---|
| Linguagem do backend | Python |
| Framework backend | Django |
| API | Django REST Framework |
| Autenticação | Simple JWT |
| Banco de dados | PostgreSQL |
| Linguagem do frontend | TypeScript |
| Biblioteca frontend | React |
| Ferramenta de desenvolvimento/build frontend | Vite |
| Versionamento | Git e GitHub |
| Integração contínua | GitHub Actions |

A Open-Meteo faz parte da proposta do produto, mas não deve ser considerada uma integração ativa na versão de código aqui documentada.

## Estrutura do repositório

```text
feneme-tech/
├── .github/
│   ├── ISSUE_TEMPLATE/          # Modelos de issues
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       └── ci.yml               # Pipeline de integração contínua
├── backend/
│   ├── accounts/                # Contas, perfis, autenticação e permissões
│   ├── config/                  # Configurações e rotas do Django
│   ├── deliveries/              # Entregas, API, validações e testes
│   ├── manage.py
│   └── requirements.txt
├── docs/
│   ├── modelos/                 # Modelos de documentação
│   └── sprints/                 # Atas, DoD, métricas e impedimentos
├── evidencias/                  # Evidências de validações e execuções
├── frontend/
│   ├── src/
│   │   ├── components/           # Componentes da interface
│   │   ├── App.tsx               # Fluxo principal e área do Gestor
│   │   ├── api.ts                # Comunicação com a API
│   │   ├── main.tsx              # Inicialização do React
│   │   ├── styles.css            # Estilos
│   │   └── types.ts              # Tipos TypeScript
│   ├── index.html
│   ├── package.json
│   ├── package-lock.json
│   └── vite.config.ts
├── .env.example                  # Exemplo de variáveis do backend
├── CONTRIBUTING.md               # Orientações de contribuição
├── iniciar.ps1                   # Inicialização integrada no Windows
├── README.md
└── README_IMPLEMENTACAO_SPRINT1.md # Guia detalhado de implementação da R1
```

Arquivos gerados, como `frontend/dist/`, e ambientes virtuais locais não precisam ser versionados. O arquivo `.env` contém configurações locais e não deve ser enviado ao repositório.

## Executar localmente

O procedimento detalhado de instalação e execução está no documento [`README_IMPLEMENTACAO_SPRINT1.md`](README_IMPLEMENTACAO_SPRINT1.md). Ele descreve a configuração do PostgreSQL, das variáveis de ambiente, do Python, do Node.js, a criação de usuários e a inicialização do servidor.

### Pré-requisitos

- Python 3.12 ou superior.
- Node.js 22 ou superior, com npm.
- PostgreSQL 14 ou superior.
- Git.

### Resumo da preparação

1. Clone o repositório e entre na pasta do projeto.
2. Crie um banco PostgreSQL e um usuário para a aplicação.
3. Copie `.env.example` para `.env` e configure as credenciais locais do banco e a chave secreta do Django.
4. Crie o ambiente virtual Python e instale `backend/requirements.txt`.
5. Instale as dependências do frontend e gere o build.
6. Aplique as migrações do Django.
7. Crie um superusuário e as contas de demonstração necessárias.

Exemplo dos comandos de instalação, a partir da raiz do repositório:

```powershell
python -m venv backend/.venv
.\backend\.venv\Scripts\python.exe -m pip install -r backend/requirements.txt

Push-Location frontend
npm.cmd install
npm.cmd run build
Pop-Location

.\backend\.venv\Scripts\python.exe backend/manage.py migrate
.\backend\.venv\Scripts\python.exe backend/manage.py createsuperuser
```

Depois de configurar o ambiente e criar as contas, no Windows é possível iniciar a aplicação integrada com:

```powershell
.\iniciar.ps1
```

A aplicação fica disponível em:

- Interface web: `http://localhost:8000/`
- API: `http://localhost:8000/api/`
- Administração Django: `http://localhost:8000/admin/`

O script `iniciar.ps1` recompila o frontend, aplica as migrações e inicia o servidor Django. O PostgreSQL precisa estar em execução e o arquivo `.env` precisa estar configurado.

Para instruções completas, incluindo a configuração do PostgreSQL, comandos para Linux/macOS e criação de usuários Gestor e Motorista, consulte o guia de implementação.

## API disponível

As rotas abaixo correspondem à implementação identificada no backend atual.

| Método | Endpoint | Acesso | Descrição |
|---|---|---|---|
| `POST` | `/api/auth/login/` | Público | Autentica usuário e retorna tokens e dados básicos do perfil. |
| `POST` | `/api/auth/refresh/` | Conforme configuração JWT | Renova o token de acesso a partir do refresh token. |
| `GET` | `/api/drivers/` | Gestor | Lista contas ativas com perfil Motorista. |
| `GET` | `/api/deliveries/` | Gestor e Motorista | Gestor consulta todas; Motorista consulta somente as próprias entregas atribuídas. |
| `POST` | `/api/deliveries/` | Gestor | Cadastra uma entrega. |
| `GET` | `/api/deliveries/{id}/` | Gestor e Motorista | Consulta uma entrega, respeitando o isolamento por Motorista. |
| `POST` | `/api/deliveries/{id}/assign-driver/` | Gestor | Atribui ou reatribui um Motorista à entrega. |

### Exemplo de cadastro de entrega

```json
{
  "origin": "Campina Grande - PB",
  "destination": "João Pessoa - PB",
  "cargo_description": "Alimentos refrigerados"
}
```

### Exemplo de atribuição de motorista

```json
{
  "driver_id": 3
}
```

A API utiliza JSON. Nas rotas protegidas, o cliente deve enviar o token de acesso no cabeçalho:

```text
Authorization: Bearer <access_token>
```

As operações de atualização e exclusão de entregas não estão habilitadas no `DeliveryViewSet` atual.

## Testes e qualidade

Os testes automatizados do backend estão distribuídos nos apps `accounts` e `deliveries`. Eles verificam aspectos como:

- autenticação e respostas para credenciais inválidas;
- autorização de operações conforme o perfil;
- cadastro e consulta de entregas;
- atribuição de motoristas;
- isolamento de dados entre motoristas;
- bloqueio de acesso a entregas não atribuídas ao usuário.

Para executar as verificações localmente, a partir da raiz:

```powershell
.\backend\.venv\Scripts\python.exe backend/manage.py check
.\backend\.venv\Scripts\python.exe backend/manage.py test --noinput

Push-Location frontend
npm.cmd run build
Pop-Location
```

Os testes do Django utilizam um banco de testes separado. O usuário PostgreSQL configurado para a execução local precisa ter permissão para criar o banco temporário de testes.

### Integração contínua

O workflow `.github/workflows/ci.yml` é executado em pushes para branches e em Pull Requests direcionados à `main`, além de permitir execução manual.

O pipeline possui verificações para:

- **Backend:** instalação das dependências, inicialização de PostgreSQL, `manage.py check` e testes do Django.
- **Frontend:** instalação das dependências e execução do build de produção.

O workflow detecta se os componentes existem antes de executar seus respectivos jobs. Atualmente, o frontend não possui script de testes automatizados configurado; portanto, a etapa de testes frontend é ignorada e o build é verificado.

### Critérios de qualidade

A equipe deve acompanhar os critérios definidos no Plano de Qualidade, Plano de Testes e Definition of Done (DoD). Uma issue não deve ser considerada concluída apenas porque o código foi implementado: os critérios de aceitação, evidências, testes e validação do responsável devem ser conferidos conforme o processo da equipe.

## Processo de desenvolvimento

O desenvolvimento é organizado em releases e sprints, com acompanhamento das atividades no Jira e versionamento no GitHub.

Fluxo recomendado:

1. Consultar a issue e os critérios de aceitação no Jira.
2. Criar uma branch a partir da `main`.
3. Implementar uma alteração relacionada à issue.
4. Executar os testes e verificações aplicáveis.
5. Abrir um Pull Request para a `main`, relacionando a issue.
6. Aguardar revisão e aprovação conforme as regras acordadas pela equipe.
7. Verificar a conclusão bem-sucedida da CI antes da integração.
8. Atualizar o Jira e registrar evidências e documentação pertinentes.

Convenções de branch, commits e Pull Requests estão descritas em [`CONTRIBUTING.md`](CONTRIBUTING.md).

## Equipe e papéis

###  Release 1

| Integrante | Papel |
|---|---|
| José Araújo Agra Neto | Product Owner / DevOps |
| João Paulo de Araujo | Scrum Master |
| Lethycia Zenaide Queiroz Melo | QA |

### Release 2

| Integrante | Papel |
|---|---|
| João Paulo de Araujo | Product Owner / DevOps |
| Lethycia Zenaide Queiroz Melo | Scrum Master |
| José Araújo Agra Neto | QA |

### Release 3

 Integrante | Papel |
|---|---|
| Lethycia Zenaide Queiroz Melo | Product Owner  / DevOps |
| José Araújo Agra Neto | Scrum Master |
| João Paulo de Araujo | QA |

### Release 4

| Integrante | Papel |
|---|---|
| José Araújo Agra Neto | Product Owner / DevOps |
| João Paulo de Araujo | Scrum Master |
| Lethycia Zenaide Queiroz Melo | QA |
### Responsabilidades

- **Product Owner (PO):** define e prioriza os requisitos do produto, mantém o Product Backlog, esclarece dúvidas sobre as necessidades dos usuários e valida o incremento conforme os critérios de aceitação.
- **Scrum Master (SM):** facilita os eventos Scrum, acompanha o andamento da sprint, promove a comunicação da equipe e auxilia na identificação e remoção de impedimentos.
- **Quality Assurance (QA):** planeja e executa verificações de qualidade, acompanha os critérios de aceitação, registra defeitos e evidências e verifica correções e regressões.
- **DevOps:** apoia a infraestrutura e os ambientes de desenvolvimento, o versionamento, a integração contínua, os processos de build e a confiabilidade do fluxo de entrega.

Todos os integrantes podem colaborar com o desenvolvimento, revisão e validação das funcionalidades. A atribuição de um papel define responsabilidades principais na release, não impede a colaboração dos demais.

## Documentação complementar

- [`README_IMPLEMENTACAO_SPRINT1.md`](README_IMPLEMENTACAO_SPRINT1.md): guia detalhado de instalação, configuração, execução, endpoints e implementação da Sprint 1.
- [`CONTRIBUTING.md`](CONTRIBUTING.md): fluxo de contribuição, convenções de branches, commits e Pull Requests.
- [`docs/modelos/`](docs/modelos/): modelos de histórias de usuário, bugs e documentação relacionada.
- [`docs/sprints/`](docs/sprints/): registros de planejamento, revisão, retrospectiva, Definition of Done, métricas e impedimentos das sprints.
- [`evidencias/`](evidencias/): registros e relatórios de evidências de validação.

---

**Feneme — Release 2 em desenvolvimento.**

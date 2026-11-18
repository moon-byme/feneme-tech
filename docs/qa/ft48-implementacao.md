# FT-48 / US-11 — atualização manual de status

Implementação preparada em 18/11/2026 para R2 / Sprint 3, baseada na `main` (`ab1bae3`). Branch: `feature/ft-48-atualizar-status-entrega`.

Referências: [FT-48](https://feneme.atlassian.net/browse/FT-48), incluindo a decisão do PO de 10/11/2026; [FT-34](https://feneme.atlassian.net/browse/FT-34), [FT-49](https://feneme.atlassian.net/browse/FT-49) e [FT-59](https://feneme.atlassian.net/browse/FT-59).

## Comportamento e contrato

`POST /api/deliveries/{id}/update-status/`, com JWT do Motorista atribuído e JSON `{"status":"EM_TRANSPORTE"}` ou `{"status":"ENTREGUE"}`.

- `200`: retorna a entrega completa com o status persistido.
- `400`: status ausente/inválido ou transição proibida, incluindo repetição, salto, retorno e qualquer mudança após `ENTREGUE`.
- `401`: autenticação ausente, inválida, expirada ou conta inativa.
- `403`: perfil Gestor, desconhecido ou ausente.
- `404`: entrega inexistente, sem atribuição ou atribuída a outro Motorista, sem divulgar seus dados.

Somente `PENDENTE → EM_TRANSPORTE → ENTREGUE` é permitido. O cadastro continua iniciando em `PENDENTE`. O serializer genérico mantém `status` somente leitura e PUT/PATCH continuam indisponíveis. O Django Admin também exibe o status como somente leitura.

O Motorista vê o status em português, a próxima ação, carregamento e mensagens de sucesso/erro. O botão fica desabilitado em entregas finalizadas e durante o envio; requisições duplicadas na mesma interface são bloqueadas. A interface só substitui os dados após confirmação da API. O botão de atualizar a lista fica desabilitado durante gravações. Um `401` encerra a sessão da interface. Em caso de estado desatualizado por outra sessão, a API rejeita a transição e o usuário pode atualizar a lista.

O Gestor consulta o último status pelos endpoints e pela listagem existentes, inclusive após recarregar; não recebe controles de alteração.

## Persistência, histórico e concorrência

`DeliveryStatusHistory` registra `delivery`, `previous_status`, `new_status`, `changed_by` e `changed_at`. A ordenação é `changed_at, id`, com índice por entrega e cronologia. As chaves estrangeiras usam `PROTECT` para preservar referências da auditoria. Há restrições no banco para os dois pares válidos e para impedir repetição da mesma transição por entrega.

A ação usa `transaction.atomic()` e `select_for_update()` diretamente sobre a entrega, sem joins anuláveis. O vínculo é revalidado sob bloqueio. Status, `updated_at` e evento só são confirmados juntos. Uma segunda requisição aguarda o commit e valida o estado atual; uma reatribuição concorrente revoga a autorização do Motorista anterior. Falhas de gravação propagam o erro e revertem a transação, sem mascarar sucesso.

A migração `0003_alter_delivery_status_deliverystatushistory` amplia as opções do status e cria a tabela de eventos. Não modifica entregas nem inventa histórico retroativo. A preservação é exercitada com `MigrationExecutor` em banco de teste e também foi conferida ao aplicar a migração local: as **3 entregas existentes permaneceram integralmente iguais**, comparando todos os campos antes/depois.

## Verificações executadas

Ambiente local: Windows, PostgreSQL, Python 3.14.5, Django 5.2.18, Node 24.22.1, Cypress 13.17.0 e Chrome 157. Não foram adicionados Docker, dependências ou mudanças de configuração local.

Na pasta `backend`, usando `.venv\Scripts\python.exe` como interpretador:

```powershell
.venv\Scripts\python.exe manage.py check
.venv\Scripts\python.exe manage.py migrate --noinput
.venv\Scripts\python.exe manage.py makemigrations --check --dry-run
.venv\Scripts\python.exe manage.py test --noinput
```

Resultados: system check sem problemas; migração aplicada; nenhuma migração pendente de geração; **166 testes aprovados em 171,914 s**, sem testes ignorados. A suíte completa abrange autenticação, cadastro, atribuição, FT-46, FT-58, acesso cruzado e clima, além da FT-48.

Cobertura específica em `deliveries.test_ft48` e `deliveries.test_ft48_migration`:

- Matriz dos nove pares de estado: duas transições aceitas e sete rejeitadas, com preservação dos dados em rejeições.
- Eventos com todos os campos obrigatórios e ordenação cronológica.
- Motorista de outra entrega, entrega sem atribuição/inexistente, Gestor, perfil desconhecido/ausente, conta inativa e tokens ausentes/inválidos/expirados.
- Papel atual no banco prevalece sobre token antigo; campos de usuário/data/estado anterior enviados pelo cliente não adulteram a auditoria.
- Edição genérica e alteração do estado inicial bloqueadas.
- Rollback de status e timestamp quando o histórico falha; nenhuma auditoria quando a entrega falha.
- **FT-34: 10 entregas × 2 transições = 20/20 atualizações válidas (100%)**, recuperadas por nova autenticação JWT, nova consulta HTTP e nova instância ORM, com 20 eventos persistidos.
- Listagem/detalhe do Gestor recuperam o estado atualizado; reatribuição revoga o acesso anterior e conserva a autoria de cada evento.
- Concorrência real com `TransactionTestCase`, conexões independentes, duas threads e transações sobrepostas: somente um sucesso por transição repetida, cadeia válida para destinos diferentes e bloqueio após reatribuição concorrente.
- Recuperação de status/histórico após fechar e reabrir a conexão com o PostgreSQL.
- Migração preserva entrega criada no schema anterior e não gera eventos artificiais.

Na pasta `frontend`:

```powershell
npm.cmd run build
npx.cmd tsc --noEmit -p cypress/tsconfig.json
```

Resultados: **build de produção aprovado** (TypeScript + Vite, 34 módulos); **tipagem dos cenários Cypress aprovada**. Não existe script de testes unitários `npm test` no projeto; os testes de interface usam Cucumber/Cypress.

Os cenários da FT-48 estão em `status.feature`, marcados `@US-11` e `@smoke`, integrando o job de smoke existente no CI. Exercitam as duas transições pela interface, estado final, nova autenticação/reload, consulta pelo Gestor sem controles, acesso cruzado, carregamento, erro/repetição, expiração da sessão e conflito com outra sessão. Histórico é verificado nos testes Django; não foi criado endpoint de consulta antecipando a FT-59.

Execução específica da FT-48, contra banco PostgreSQL descartável `feneme_ft48_e2e_20261118_001`, separado da base local:

```powershell
# Backend: DB_NAME aponta para a base descartável, já migrada e com seed_e2e_users.
# Frontend: CYPRESS_BASE_URL=http://127.0.0.1:8011 e CYPRESS_E2E_PASSWORD da base fictícia.
Remove-Item Env:ELECTRON_RUN_AS_NODE -ErrorAction SilentlyContinue
npm.cmd run e2e -- --browser chrome --env tags=@US-11 --config defaultCommandTimeout=30000
```

Resultado: **5/5 cenários aprovados em 56 s**, sem pendências ou ignorados. A primeira tentativa de inicialização herdava `ELECTRON_RUN_AS_NODE=1`, incompatível com o aplicativo Cypress; a execução no sandbox também encontrou restrições do Electron. Após remover a variável apenas no processo de teste e usar Chrome fora do sandbox, houve uma execução com 3/5 sucessos e dois timeouts de login (prazo padrão de 8 s). Com prazo de 30 s passado exclusivamente pela CLI, os cinco cenários passaram, sem mudança na configuração do projeto.

Regressão dos grupos de cenários usados no CI:

```powershell
npm.cmd run e2e -- --browser chrome --env 'tags=@smoke or @R1 or @US-07 or @US-08' --config defaultCommandTimeout=30000
```

Resultado: **25/25 cenários aprovados em 3 min 6 s**, sem falhas, pendências ou ignorados: atribuição (2), autenticação (4), cadastro/consulta (4), previsão (2), status/isolamento FT-58/FT-48 (10) e comparação de trajetos (3). O relatório HTML local é gerado em `frontend/cypress/reports/cucumber-report.html` (artefato ignorado pelo Git; o CI publica seu próprio relatório). Cenários futuros de US-12/US-13/recomendação não integram esses grupos e não foram declarados aprovados.

Verificação adicional, na pasta `backend`:

```powershell
.venv\Scripts\python.exe verify_ft48_restart.py --database feneme_ft48_e2e_20261118_001
```

Resultado: **PASS**. O script cria dados fictícios em base com prefixo obrigatório `feneme_ft48_e2e_`, inicia um processo Django independente, cadastra/atribui a entrega pela API, executa a primeira transição e encerra o servidor. Após iniciar outro processo, autentica novamente Gestor e Motorista e confirma `EM_TRANSPORTE` via HTTP; uma conexão ORM nova recupera o evento com entrega, estados, autoria e data/hora. No Windows, encerra a árvore do PID que criou, confirma que a porta fechou e exige um novo PID. A execução requer permissão para encerrar os próprios subprocessos; neste ambiente foi feita fora do sandbox. A sondagem de inicialização repete erros de conexão transitórios.

## Arquivos alterados

| Área | Arquivos | Finalidade |
| --- | --- | --- |
| Permissões | `backend/accounts/permissions.py` | Perfil Motorista na ação específica |
| Dados | `backend/deliveries/models.py`, `migrations/0003_alter_delivery_status_deliverystatushistory.py` | Estados e histórico persistente |
| API | `backend/deliveries/serializers.py`, `views.py` | Entrada validada, transições, bloqueio e transação |
| Administração | `backend/deliveries/admin.py` | Status somente leitura |
| Testes de backend | `backend/deliveries/test_ft48.py`, `test_ft48_migration.py` | Regras, segurança, atomicidade, concorrência, FT-34 e migração |
| Verificação adicional | `backend/verify_ft48_restart.py` | Reinício real do servidor em banco descartável |
| Cliente HTTP e tipos | `frontend/src/api.ts`, `types.ts` | Operação específica e rótulos compartilhados |
| Interface | `frontend/src/components/MotoristaHome.tsx`, `App.tsx`, `styles.css` | Ações do Motorista e status legível para ambos os perfis |
| Aceitação | `frontend/cypress/e2e/status.feature`, `support/step_definitions/status.steps.ts` | Cenários reais da US-11 e tipagem dos aliases existentes |
| Documentação | `README.md`, `docs/qa/ft48-implementacao.md` | Contrato, decisões, evidências e pendências |

## Integrações e pendências de aceite

- **FT-34:** medição automatizada de 20/20 atualizações recuperadas; a conferência independente do driver continua com QA.
- **FT-49:** o status atualizado já integra listagem e detalhe existentes do Gestor; nenhuma tela independente de acompanhamento foi antecipada.
- **FT-59:** modelo único de eventos persistentes, indexados e cronológicos; endpoint e interface de consulta completa pertencem àquela história.
- Revisão do código e testes pelo QA, demonstração/aceite do PO, conferência docente da DoD e integração por PR permanecem pendentes. A execução automatizada não substitui esses aceites.
- A FT-48 não foi marcada como concluída no Jira e não houve merge automático.

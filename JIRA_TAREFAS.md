# Textos para cadastro manual no Jira — Feneme

Crie uma tarefa principal e subtarefas conforme o tipo de issue disponível no projeto. Os identificadores abaixo são nomes sugeridos, não chaves Jira reais.

## Tarefa principal
**Resumo:** Configurar estrutura do repositório e integração contínua do Feneme

**Descrição:**
Organizar o fluxo de contribuição do repositório GitHub do Feneme e preparar uma pipeline inicial de integração contínua. A configuração deve padronizar branches, Issues e Pull Requests, além de executar verificações automáticas compatíveis com os componentes e comandos existentes no projeto.

**Critérios de aceitação:**
- [ ] Convenções de branches documentadas.
- [ ] Template de Pull Request disponível.
- [ ] Templates de Issue para bug, funcionalidade e tarefa técnica disponíveis.
- [ ] Workflow de CI versionado em `.github/workflows/ci.yml`.
- [ ] Workflow executado em push e em Pull Requests para `main`.
- [ ] Jobs executam as verificações de back-end/front-end quando esses componentes estiverem presentes e configurados.
- [ ] Resultado da execução validado e evidências registradas.
- [ ] Limitações por ausência de código ou testes documentadas, quando aplicável.

## Subtarefa 1 — Definir fluxo de branches e contribuição
**Descrição:** Documentar o fluxo de trabalho baseado em `main` e branches curtas por atividade, incluindo convenções de nomes, commits e Pull Requests.

**Critérios de aceitação:**
- [ ] Convenções para `feature/*`, `fix/*`, `docs/*`, `test/*`, `ci/*` e `refactor/*` documentadas.
- [ ] Fluxo de abertura, revisão e integração de PR documentado.

## Subtarefa 2 — Criar templates de Issues e Pull Requests
**Descrição:** Criar formulários para bugs, funcionalidades e tarefas técnicas, além de um template de PR com resumo, Issue relacionada, validação e checklist.

**Critérios de aceitação:**
- [ ] Formulário de bug criado.
- [ ] Formulário de funcionalidade criado.
- [ ] Formulário de tarefa técnica criado.
- [ ] Template de PR criado e conferido no GitHub.

## Subtarefa 3 — Configurar pipeline de integração contínua
**Descrição:** Criar workflow do GitHub Actions para executar verificações de back-end Django e front-end React/TypeScript quando os arquivos e scripts necessários estiverem presentes.

**Critérios de aceitação:**
- [ ] Workflow executado a cada push.
- [ ] Workflow executado em PR direcionado à `main`.
- [ ] Back-end executa `python manage.py check` e `python manage.py test` quando configurado.
- [ ] Front-end executa o build quando configurado e os testes quando houver script de teste.
- [ ] Nenhum segredo ou credencial é armazenado no repositório.
- [ ] Limitações por ausência de componentes ou scripts são visíveis nos logs.

## Subtarefa 4 — Validar CI e registrar evidências
**Descrição:** Fazer push da configuração, conferir a aba Actions e registrar o resultado da execução. Quando o código da aplicação estiver disponível, validar também a execução real de build e testes.

**Critérios de aceitação:**
- [ ] Execução do workflow consultada na aba Actions.
- [ ] Evidência do resultado anexada ou vinculada à tarefa.
- [ ] Jobs ignorados e motivos documentados, se aplicável.
- [ ] Pendências identificadas registradas como novas tarefas.

## Evidências a adicionar depois da implementação
- Link para o commit que adicionou os arquivos.
- Link para a execução do GitHub Actions.
- Link para o Pull Request, se a mudança for integrada por PR.
- Captura de tela dos jobs e respectivos resultados.

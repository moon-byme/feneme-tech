# Como contribuir com o Feneme

## Fluxo de trabalho
1. Confira ou crie uma Issue para a atividade.
2. Crie uma branch a partir da `main`.
3. Faça alterações pequenas e relacionadas à Issue.
4. Execute localmente os testes e o build aplicáveis.
5. Abra um Pull Request para `main`, preenchendo o template.
6. Aguarde a revisão e a conclusão bem-sucedida das verificações de CI antes de integrar.

## Convenção de branches
- `feature/<descricao-curta>`: nova funcionalidade.
- `fix/<descricao-curta>`: correção de bug.
- `docs/<descricao-curta>`: documentação.
- `test/<descricao-curta>`: testes.
- `ci/<descricao-curta>`: integração contínua e infraestrutura de desenvolvimento.
- `refactor/<descricao-curta>`: refatoração sem mudança intencional de comportamento.

Use nomes curtos, em minúsculas, com palavras separadas por hífen. Exemplo: `ci/github-actions`.

## Commits
Prefira mensagens curtas e descritivas. Exemplos:
- `feat: adicionar cadastro de entregas`
- `fix: validar status da entrega`
- `docs: atualizar instruções de execução`
- `ci: configurar pipeline inicial`

## Pull Requests
- Relacione a Issue correspondente quando existir.
- Explique o motivo e o impacto da mudança.
- Informe quais testes e verificações foram executados.
- Não inclua credenciais, tokens, arquivos `.env` ou dados pessoais reais.

## Integração contínua
O workflow em `.github/workflows/ci.yml` é acionado em pushes e em Pull Requests direcionados à `main`. Os jobs de back-end e front-end são ativados quando os arquivos de entrada correspondentes existem no repositório. Se um componente ainda não foi criado, seu job é ignorado; isso não significa que esse componente foi testado.

## Testes de aceitação (Cucumber + Cypress)
Os cenários ficam em `frontend/cypress/e2e/*.feature` (Gherkin em português) e os passos em `frontend/cypress/support/step_definitions/`. O job `E2E - Cucumber/Cypress (@smoke)` do CI executa os cenários marcados com `@smoke` a cada push e PR, e publica o relatório HTML como artefato `e2e-smoke-report`.

Para rodar localmente, com o PostgreSQL configurado no `.env`:

```bash
# back-end (pasta backend/)
python manage.py migrate
E2E_PASSWORD=<senha-de-teste> python manage.py seed_e2e_users   # cria gestor_e2e e motorista_e2e
cd ../frontend && npm run build && cd ../backend
python manage.py runserver

# em outro terminal (pasta frontend/)
CYPRESS_E2E_PASSWORD=<senha-de-teste> npm run e2e:smoke   # só @smoke
CYPRESS_E2E_PASSWORD=<senha-de-teste> npm run e2e         # todos os cenários
```

No Windows (PowerShell), defina as variáveis com `$env:E2E_PASSWORD="..."` e `$env:CYPRESS_E2E_PASSWORD="..."`. O relatório fica em `frontend/cypress/reports/cucumber-report.html`. Use somente contas fictícias.

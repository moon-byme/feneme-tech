# FT-49 / US-12 — Evidências e pendências

## Escopo implementado

A listagem e o detalhe existentes (`GET /api/deliveries/` e `GET /api/deliveries/{id}/`) consultam `Delivery.status` persistido, respeitam os perfis e o escopo do Motorista, e retornam 404 para um identificador inexistente. Nenhuma rota ou regra de transição da FT-48 foi alterada.

Na área do Gestor, a listagem existente foi identificada como acompanhamento, os dados essenciais e o status atual foram destacados, e a falha de consulta passou a ser distinta do estado vazio. **Atualizar** realiza nova consulta à API; o Gestor não recebe controles para alterar status.

## Testes locais

| Comando | Resultado real |
| --- | --- |
| `cypress run --browser chrome --env tags=@US-12 --config defaultCommandTimeout=30000` | **3 aprovados, 0 falhas, 0 pendentes, 0 ignorados**, duração 20 s. Inclui CT-24, CT-25 e o cenário de falha de consulta. Cypress 13.17.0, Chrome 157 headless, Node 24.22.1. |
| `npm.cmd run e2e -- --browser chrome --env 'tags=@US-11 or @US-10' --config defaultCommandTimeout=30000` | **10 aprovados, 0 falhas, 0 pendentes, 0 ignorados**, duração 50 s. Regressão FT-48/FT-58. |
| `.\.venv\Scripts\python.exe manage.py check` (`backend`) | **PASS** — nenhum problema de configuração. |
| `.\.venv\Scripts\python.exe manage.py makemigrations --check --dry-run` (`backend`) | **PASS** — nenhuma migração pendente. |
| `.\.venv\Scripts\python.exe manage.py test deliveries.test_delivery_status deliveries.test_ft58 deliveries.test_acesso_cruzado --noinput -v 2` (`backend`) | **PASS** — 62 testes. |
| `.\.venv\Scripts\python.exe manage.py test --noinput -v 2` (`backend`) | **PASS** — 167 testes, 0 falhas, 0 skips. |
| `npm.cmd run build` (`frontend`) | **PASS** — build TypeScript/Vite. |
| `npx.cmd --no-install tsc --noEmit -p cypress/tsconfig.json` (`frontend`) | **PASS** — tipagem Cypress. |

Os resultados Cypress 3/3 e 10/10 acima foram fornecidos na saída de terminal da execução local. A saída reporta zero capturas e vídeo desativado. O arquivo HTML local [`cucumber-report.html`](../../frontend/cypress/reports/cucumber-report.html), atualizado em 19/11/2026, contém os 10 cenários de regressão FT-48/FT-58; ele não contém CT-24/CT-25. Portanto, os resultados US-12 estão documentados pela saída fornecida, não por um relatório HTML salvo no repositório.

O Cypress exibiu avisos de depreciação/loader do Node, mas os dois comandos terminaram com todos os cenários aprovados.

## Pipeline CI e Pull Requests

- **Não há execução CI para FT-49**: a busca de Actions para `feature/ft-49-consultar-andamento-entregas` retornou zero execuções.
- **Não há PR FT-49 no GitHub** e `git ls-remote` não encontrou a branch remota. A branch e as alterações continuam locais.
- O CI mais recente da predecessora FT-48, [run #260](https://github.com/moon-byme/feneme-tech/actions/runs/44357992089), terminou com sucesso no commit `1b68903` de `feature/ft-48-atualizar-status-entrega`. Backend, build frontend e E2E estão verdes. O job E2E desse run cobriu smoke, US-07, R1 e US-08; **não valida CT-24/CT-25 nem as alterações locais da FT-49**.
- O [PR #41](https://github.com/moon-byme/feneme-tech/pull/41) permanece aberto, sem merge. As verificações do CI nele estão verdes, mas não há review registrada. A FT-49 deve ser publicada em branch própria e ter PR com base em `feature/ft-48-atualizar-status-entrega` enquanto o #41 não for integrado.

## Pendências para revisão e aceite

1. Publicar a branch FT-49 e abrir o PR com o template oficial, evidências acima e dependência explícita do PR #41.
2. Executar/aguardar CI no commit da FT-49; o CI verde da FT-48 não cobre estas mudanças.
3. QA independente revisar o código e validar CT-24/CT-25 e as regressões, incluindo status persistido após atualização/nova sessão, isolamento do Motorista, 404 sem vazamento e estado de erro distinto de lista vazia.
4. PO validar os critérios de aceite e registrar o aceite formal.
5. Conferir a DoD do Jira após QA e PO. Não marcar a FT-49 como concluída nem integrar antes dessas aprovações.

Nenhum merge foi realizado e a história não foi marcada como concluída.

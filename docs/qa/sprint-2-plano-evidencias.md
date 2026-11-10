# QA — Sprint 2: plano de execução, evidências e pendências

**Projeto:** Feneme — Release 2  
**Sprint:** FT Sprint 2 (03/11/2026 a 12/11/2026)  
**Responsável QA:** José Araújo Agra Neto  
**Issues:** FT-32, FT-33, FT-74, FT-75 e FT-88

> Este documento separa implementação de testes, execução comprovada e atividades que dependem de pessoas ou funcionalidades ainda não disponíveis. Os resultados abaixo são atualizados com base nas execuções efetivamente concluídas no CI.

## 1. Estado do repositório na auditoria

- Existem oito arquivos Gherkin para fluxos de autenticação, entregas, trajetos, previsão, recomendação, status e histórico.
- A branch principal já contém definições de etapas Cypress para autenticação, entregas e atribuição, incluindo `frontend/cypress/support/step_definitions/autenticacao.steps.ts`, `entregas.steps.ts` e `atribuicao.steps.ts`. Essas etapas foram incorporadas pela PR #15, já integrada à `main`.
- O workflow `.github/workflows/ci.yml` executa `npm run e2e:smoke` e `npm run e2e:r1`. Após a PR #18, o smoke também seleciona CT-22 e CT-23 da US-10; a regressão `@R1` contém 10 cenários da Sprint 1.
- O código da branch principal ainda não apresenta cliente/serviço/endpoint Open-Meteo nem recursos persistidos de alternativas de trajeto e recomendação. O modelo de entrega expõe apenas o status inicial PENDENTE; não há fluxo de atualização/histórico de status implementado nessa branch.
- Há testes backend para autenticação, cadastro, consulta, atribuição e isolamento de entregas. A PR #18 acrescentou cenários Cypress/Cucumber para CT-22 e CT-23, exercitando a API com dois motoristas de teste. Isso não equivale a validar a interface visual do Motorista nem cobre todas as histórias R2.

## 2. FT-33 / FT-74 — Segurança de erros e logs (Q-06)

### Instrumentação adicionada

Arquivo: `backend/accounts/test_q06_tratamento_erros.py`

O arquivo contém 20 testes negativos identificados individualmente (`test_q06_01` a `test_q06_20`). Eles cobrem credenciais inválidas, ausência e adulteração de token, permissões negadas, dados obrigatórios ausentes e atribuição inválida.

Cada caso verifica:
- status HTTP esperado;
- ausência de traceback na resposta;
- ausência de senha e marcadores fictícios sensíveis na resposta;
- ausência desses mesmos valores nos logs capturados durante a requisição.

### Execução e evidência no CI

**Resultado confirmado:** 20/20 cenários Q-06 aprovados, com **0 exposições** de senha ou marcadores sensíveis nas respostas e nos logs, e sem traceback nas respostas/logs verificados. A suíte completa do backend executou 123 testes com resultado `OK`.

A execução ocorreu no CI da PR #17, commit `a40004bd92ffab404705b3d3fdf2b50d26338460`. Todos os jobs do workflow terminaram com sucesso.

**Evidência:** [GitHub Actions — CI da PR #17 (run 42732366544)](https://github.com/moon-byme/feneme-tech/actions/runs/42732366544)

### Como executar localmente

Na pasta `backend`:

```bash
python manage.py test accounts.test_q06_tratamento_erros -v 2
```

**Limitação da medição:** a instrumentação cobre os endpoints e fluxos existentes e exercitados. Ela não comprova o tratamento de exceções de serviços ainda inexistentes, incluindo Open-Meteo.

## 3. FT-32 — Resiliência à indisponibilidade da Open-Meteo

**Critério do driver:** 10 de 10 falhas simuladas (timeout, HTTP 5xx e previsão ausente) devem preservar cadastro e comparação manuais, exibir indisponibilidade e não confirmar recomendação climática sem dados.

**Bloqueio encontrado:** não foi localizado cliente Open-Meteo, serviço meteorológico ou endpoint de previsão na branch principal. Sem a implementação e seu contrato, não é possível escrever testes de integração válidos sem inventar interfaces ou produzir testes que passam sem testar o sistema real.

**Ação necessária da equipe de desenvolvimento:** disponibilizar o cliente/serviço e o ponto de integração de previsão, mantendo a dependência externa isolada e injetável/mockável. Quando disponível, QA deverá simular pelo menos:
1. timeout;
2. HTTP 500;
3. HTTP 502;
4. HTTP 503;
5. resposta sem corpo;
6. JSON inválido;
7. campo de temperatura ausente;
8. lista de previsões vazia;
9. latência acima do limite;
10. erro de conexão/DNS.

Para cada caso, verificar que o cadastro e a comparação manuais continuam acessíveis, que a interface informa indisponibilidade e que nenhuma recomendação climática é marcada como confirmada.

**Resultado:** não medido — bloqueado por ausência da integração no código auditado.

## 4. FT-75 — Facilidade de cadastro (Q-07)

**Meta original:** pelo menos 4 de 5 avaliadores concluem o cadastro corretamente, sem ajuda, em até 3 minutos.

Essa métrica exige participantes humanos. Não é válido substituir os cinco avaliadores por testes automatizados, nem declarar um resultado sem observação real.

### Protocolo de execução

1. Selecionar cinco avaliadores representativos, sem participação na implementação.
2. Usar o mesmo ambiente e a mesma versão do sistema para todos.
3. Apresentar o roteiro uma única vez, sem orientar durante a execução.
4. Iniciar o cronômetro quando o participante começar a tarefa.
5. Encerrar quando a entrega estiver salva corretamente ou quando atingir 3 minutos.
6. Registrar conclusão correta, tempo, pedido de ajuda e observações.
7. Considerar sucesso apenas quando a conclusão for correta, sem ajuda e em até 3 minutos.

### Planilha de coleta

| Avaliador | Concluiu corretamente? | Sem ajuda? | Tempo (mm:ss) | Sucesso (≤ 3 min)? | Observações |
|---|---|---|---|---|---|
| P1 | Pendente | Pendente | Pendente | Pendente | |
| P2 | Pendente | Pendente | Pendente | Pendente | |
| P3 | Pendente | Pendente | Pendente | Pendente | |
| P4 | Pendente | Pendente | Pendente | Pendente | |
| P5 | Pendente | Pendente | Pendente | Pendente | |

**Cálculo:** avaliadores com sucesso / 5. A meta é ≥ 4/5 (80%).

**Resultado:** não medido — depende de cinco participantes e da versão funcional do formulário de cadastro. **Responsabilidade pela medição Q-07: confirmada pelo PO**; a divergência anterior entre o texto da issue e a atribuição no Jira não é mais uma pendência de confirmação.

## 5. FT-88 — Execução e rastreabilidade de QA na Sprint 2

### Estado das especificações

Os cenários R2 existentes estão em:
- `frontend/cypress/e2e/trajetos.feature`
- `frontend/cypress/e2e/previsao.feature`
- `frontend/cypress/e2e/recomendacao.feature`
- `frontend/cypress/e2e/status.feature`
- `frontend/cypress/e2e/historico.feature`

Os cenários R1 estão em `autenticacao.feature` e `entregas.feature`, além dos cenários de atribuição. A PR #15 já foi integrada à `main` e adicionou as etapas Cypress de entregas e atribuição, complementando as etapas de autenticação.

### Execução no CI

O workflow `.github/workflows/ci.yml` executa:
- `npm run e2e:smoke`, para os cenários selecionados pela tag `@smoke`;
- `npm run e2e:r1`, para a regressão da Sprint 1, selecionando 10 cenários marcados com `@R1`.

Na execução do CI da PR #18 (run `42736986570`), o job Cypress E2E smoke e o job de regressão `@R1` concluíram com sucesso. O log confirmou CT-22 e CT-23 aprovados (2/2) e 10 cenários `@R1` aprovados (10/10). Build do frontend e verificações/testes backend também concluíram com sucesso.

### Execução e evidências da PR #18

A PR [#18 — automatiza visibilidade das entregas do Motorista](https://github.com/moon-byme/feneme-tech/pull/18) foi aprovada e integrada à `main` em 09/11/2026 (horário local). O commit de merge é `9e23b4596cab31da9e454d8d6048a6b2ade2c6b4`.

- [Workflow CI da PR #18 — run 42736986570](https://github.com/moon-byme/feneme-tech/actions/runs/42736986570)
- [Artefato de evidências do Cypress](https://github.com/moon-byme/feneme-tech/actions/runs/42736986570/artifacts/13728016161)
- CT-22: motorista consulta suas entregas e não recebe a entrega atribuída ao outro motorista — aprovado.
- CT-23: acesso direto à entrega alheia retorna HTTP 404 e a resposta não contém origem, destino ou descrição — aprovado.
- Regressão `@R1`: 10/10 cenários aprovados.
- Build frontend, verificações Django e testes backend: jobs aprovados.

**Limite da evidência:** CT-22/CT-23 foram verificados por requisições à API (`cy.request`), não por interação com a tela do Motorista. A revisão da PR recomendou registrar essa limitação e, quando a interface estiver estável, acrescentar validação visual. Também foi sugerida a criação futura de um comando `e2e:r2`, separando a suíte R2 do smoke; isso ainda não foi implementado nesta atualização.

### Pendências de execução

- Criar definições de etapas para os demais cenários R2 somente depois que as interfaces e endpoints correspondentes estiverem disponíveis.
- Executar os cenários de sucesso e exceção, anexando relatórios e screenshots quando houver falha.
- Criar, em alteração futura, um comando `e2e:r2` para executar a suíte R2 separadamente, quando houver conjunto suficiente de cenários executáveis; manter `@smoke` restrito ao caminho crítico.
- Registrar um Bug por defeito reproduzível, com passos, esperado/observado, severidade, evidência e vínculo à US/PR.
- Conferir a DoD de cada história candidata à conclusão. Status Done isolado não é evidência de teste nem aceite de QA.
- Verificar a correção da branch `fix/corrigir-temperatura` quando ela estiver acessível e integrada; não presumir que a correção está presente na branch principal.

### Evidências atuais

- Os arquivos `.feature` existem e têm rastreabilidade por US/CT.
- As etapas Cypress de autenticação, entregas e atribuição estão na `main`; a PR #18 adicionou os passos de API para CT-22/CT-23.
- O CI executou smoke (incluindo CT-22/CT-23) e regressão R1 (10 cenários), todos aprovados no run 42736986570.
- Nenhum Bug novo deve ser criado sem defeito confirmado.

**Resultado:** regressão R1 (10/10) e CT-22/CT-23 (2/2) executados com sucesso no CI. A cobertura R2 continua parcial: os demais cenários dependem das funcionalidades correspondentes; CT-22/CT-23 ainda precisam de validação pela interface quando ela estiver estável.

## 6. Critérios de encerramento por issue

| Issue | Entrega de QA | Situação honesta |
|---|---|---|
| FT-32 | 10 cenários de falha Open-Meteo com continuidade manual | Bloqueado: integração não localizada |
| FT-33 | Verificação de segurança das respostas e logs | Q-06 executado no CI: 20/20 aprovados, 0 exposições; evidência no [workflow da PR #17](https://github.com/moon-byme/feneme-tech/actions/runs/42732366544) |
| FT-74 | Q-06: 0 exposição em 20 cenários | Atingido: 20/20 aprovados, 0 exposições na resposta e nos logs; suíte backend com 123 testes `OK` |
| FT-75 | Q-07: ≥ 4/5 em até 3 min | Protocolo pronto; aguarda cinco avaliadores humanos; responsável pela medição confirmado pelo PO |
| FT-88 | Cenários, smoke, bugs, indicadores e DoD de R2 | R1: 10/10 aprovados; CT-22/CT-23: 2/2 aprovados por API na PR #18; demais cenários R2 dependem das funcionalidades correspondentes; validação visual da US-10 pendente |

## 7. Próximas dependências

1. Desenvolvedores: disponibilizar a integração Open-Meteo e as funcionalidades R2 ausentes.
2. Equipe: disponibilizar ambiente funcional e cinco avaliadores para a medição Q-07.
3. QA: completar etapas Cypress dos demais fluxos R2 quando houver funcionalidades e contratos; acrescentar validação visual de CT-22/CT-23 quando a tela estiver estável; avaliar a separação da suíte em `e2e:r2`.

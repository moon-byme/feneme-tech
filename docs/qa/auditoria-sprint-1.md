# Auditoria de QA — Sprint 1 / Release 1

**Projeto:** Feneme  
**Escopo:** US-01 a US-05 (FT-43, FT-54, FT-44, FT-55 e FT-45)  
**Data da auditoria:** 04/11/2026  
**Responsável pela verificação na R2:** QA

## Objetivo

Consolidar o estado verificável dos testes, da rastreabilidade e das pendências de qualidade da Sprint 1, sem reescrever o histórico nem declarar como executado aquilo que não possui evidência.

## 1. Evidências encontradas no repositório

| História | Evidência encontrada | Situação desta auditoria |
|---|---|---|
| US-01 — FT-43: login do Gestor | Testes de autenticação no backend e cenários Gherkin de login válido/inválido em `frontend/cypress/e2e/autenticacao.feature`. Etapas correspondentes em `autenticacao.steps.ts`. | Implementação de teste e integração smoke de login presentes. |
| US-02 — FT-54: login do Motorista | Testes de autenticação/perfil no backend e cenários Gherkin de login válido/inválido no mesmo arquivo de autenticação. | Implementação de teste e integração smoke de login presentes. |
| US-03 — FT-44: cadastro de entrega | Testes de API para cadastro válido, campos obrigatórios ausentes e bloqueio de cadastro pelo Motorista em `backend/deliveries/tests.py`. | Testes backend presentes; cenário Gherkin ainda sem etapas Cypress correspondentes. |
| US-04 — FT-55: consulta de entregas | Teste `test_gestor_sees_empty_delivery_list` em `backend/deliveries/tests.py`, além dos testes de listagem. | A lacuna descrita anteriormente no Jira existe no registro, mas o teste de estado vazio já está no código atual. Falta vincular evidência de execução específica à US e completar o E2E Gherkin. |
| US-05 — FT-45: atribuição de Motorista | Teste `test_gestor_can_assign_existing_driver` e teste `test_cannot_assign_user_with_manager_profile` em `backend/deliveries/tests.py`. | Testes backend para atribuição válida e perfil incompatível presentes; cenário Gherkin ainda sem etapas Cypress correspondentes. |

## 2. Evidência de CI consultada

Workflow run: [GitHub Actions — run 41761676035](https://github.com/moon-byme/feneme-tech/actions/runs/41761676035)  
Commit: `f2c6e770f5f88d1f2910c9d8ab6092ce6a7a3f78`

Os quatro jobs reportaram sucesso:
- Detect application components;
- Backend — Django checks and tests;
- Frontend — build and tests;
- E2E — Cucumber/Cypress (@smoke).

O job E2E executa `npm run e2e:smoke`, que seleciona apenas cenários com a tag `@smoke`. No arquivo atual, essa tag está nos cenários de login válido do Gestor e do Motorista. Assim, o sucesso desse job comprova o smoke de autenticação, não a execução de todos os cenários dos arquivos `.feature`.

Artefato publicado: [e2e-smoke-report](https://github.com/moon-byme/feneme-tech/actions/runs/41761676035).

## 3. Lacunas e ações necessárias

1. Implementar definições de etapas Cypress para os cenários de cadastro, consulta e atribuição, ou documentar claramente quais verificações serão realizadas por API/backend e quais serão E2E de interface.
2. Executar os cenários Gherkin da Sprint 1 que ainda não fazem parte do smoke e anexar os resultados às respectivas histórias.
3. Vincular a evidência específica de `test_gestor_sees_empty_delivery_list` à FT-55 e de `test_cannot_assign_user_with_manager_profile` à FT-45, após confirmar a execução no relatório de testes.
4. Conferir e registrar a DoD individual das cinco histórias. O status Concluído no Jira, isoladamente, não comprova o preenchimento da DoD nem o aceite de QA/PO.
5. Preservar o resultado da Q-04: 0 de 7 PRs com aprovação formal de outra pessoa antes do merge (0%, meta de 100%). A ação de exigir PR, uma aprovação e CI verde depende da configuração de proteção da branch principal; essa proteção ainda precisa ser verificada no GitHub.
6. Manter a Q-15 separada da cobertura funcional: o Jira registra 5/5 histórias com vínculo US ↔ teste ↔ PR (100% após a inclusão dos links), mas isso não significa que todos os critérios de aceite ou a DoD estejam satisfeitos.
7. Não declarar Q-08 (cobertura de linhas) ou Q-09 (taxa histórica de sucesso do pipeline) como medidas sem os relatórios e universos de cálculo correspondentes.

## 4. Métricas e interpretação

### Q-04 — Revisão obrigatória de código
Resultado registrado para a R1: **0/7 = 0%**, meta **100%**. O resultado deve permanecer como desvio histórico; não deve ser reescrito após mudanças posteriores no fluxo.

### Q-15 — Documentação e rastreabilidade
Resultado registrado após a correção dos vínculos: **5/5 = 100%**. O indicador mede presença de rastreabilidade entre US, testes e PR. Não mede cobertura completa, aprovação de testes nem DoD.

### Q-08 e Q-09
A existência de testes e de uma execução de CI bem-sucedida não basta, por si só, para calcular cobertura de linhas ou taxa histórica de sucesso. Essas métricas permanecem sem resultado numérico até que sejam coletados os relatórios adequados.

## 5. Critério para encerrar esta auditoria

A auditoria da Sprint 1 poderá ser considerada documentalmente fechada quando:
- os cenários faltantes tiverem etapas implementadas e execução comprovada, ou tiverem sua estratégia alternativa de teste registrada;
- as evidências dos casos de estado vazio e perfil incompatível estiverem ligadas às FT-55 e FT-45;
- a DoD das cinco US tiver sido conferida por QA e PO, sem marcar itens sem evidência;
- as métricas tiverem resultado ou justificativa explícita de não medição;
- as pendências de proteção de branch e revisão de PR estiverem encaminhadas ao responsável pelo repositório.

**Nota:** esta auditoria registra o que foi localizado no código e no histórico consultado. Não substitui a execução local dos testes, a revisão humana do código nem o aceite formal do Product Owner.

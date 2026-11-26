# FENEME — Plano de Teste Funcional
**Versão 2.4 | Release 2 — fechamento da Sprint 3 | 26/11/2026**  
**QA R2:** José Araújo Agra Neto | **QA R1:** Lethycia Zenaide Queiroz Melo  
**Jira:** [FT-10](https://feneme.atlassian.net/browse/FT-10) | **Repositório:** [moon-byme/feneme-tech](https://github.com/moon-byme/feneme-tech)

> Atualiza a v2.3 (16/11/2026) com resultados comprovados da Sprint 3, CT-07/CT-18 verificados, homologação, regressão completa da R2, indicadores, evidências e histórico de revisão. Resultados não executados ou replanejados permanecem explicitamente identificados.

## Histórico de revisão

| Data | Versão | Release/Sprint | Descrição | Autor |
|---|---:|---|---|---|
| 19/10/2026 | 1.0 | R1/S0 | Plano original: 7 US e CT-01 a CT-12 | Lethycia Zenaide Queiroz Melo |
| 20/10/2026 | 2.0 | R1–R4/S0 | Ampliação para 13 US e CT-01 a CT-26; Q-01 a Q-15 e rastreabilidade Jira | Revisão documental |
| 20/10/2026 | 2.1 | R1–R4/S0 | Ajustes de qualidade, escopo, cobertura e rastreabilidade | Revisão documental |
| 12/11/2026 | 2.2 | R2/S2 | Resultados parciais S2, BDD, GitHub Actions e limitações | Lethycia Zenaide Queiroz Melo |
| 16/11/2026 | 2.3 | R2/Planning S3 | Mudança FT-112; US-14 a US-20; CT-27 a CT-48; reescrita US-09 | João Paulo de Araujo |
| 26/11/2026 | **2.4** | **R2/fechamento S3** | Resultados S3; CT-07/18 verificados; homologação; regressão R2; indicadores e evidências | **José Araújo Agra Neto** |

## 1. Objetivo e escopo

Planejar e registrar testes funcionais rastreáveis, contemplando sucesso e exceção. A matriz mantém CT-01 a CT-48. O escopo da R2 abrange login, entregas, trajetos manuais, previsão Open-Meteo, atualização de status, andamento, histórico, lista única de cidades e catálogo de cargas.

Fora do escopo: rastreamento GPS em tempo real, sensores/temperatura real do alimento, trânsito em tempo real, veículos refrigerados e aplicativo nativo. A temperatura consultada é previsão de temperatura ambiente.

| US | Jira | Funcionalidade | Release/Sprint |
|---|---|---|---|
| US-01 | FT-43 | Login do Gestor | R1/S1 |
| US-02 | FT-54 | Login do Motorista | R1/S1 |
| US-03 | FT-44 | Cadastro de entrega e carga | R1/S1 |
| US-04 | FT-55 | Consulta de entregas | R1/S1 |
| US-05 | FT-45 | Atribuição de Motorista | R1/S1 |
| US-06 | FT-46 | Cadastro de trajetos manuais (substituído na R3) | R2/S2 |
| US-07 | FT-56 | Comparação de trajetos manuais (substituída na R3) | R2/S2 |
| US-08 | FT-47 | Previsão de temperatura ambiente | R2/S2 |
| US-09 | FT-57 | Comparação térmica e menor exposição | R3/S5 |
| US-10 | FT-58 | Entregas atribuídas ao Motorista | R2/S2 |
| US-11 | FT-48 | Atualização de status | R2/S3 |
| US-12 | FT-49 | Consulta de andamento | R2/S3 |
| US-13 | FT-59 | Histórico de entregas | R2/S3 |
| US-14 | FT-113 | Lista única de cidades | R2/S3 |
| US-15 | FT-114 | Catálogo de tipos de carga, limite e fonte | R2/S3 |
| US-16 | FT-117 | Tipo de carga e data/hora de saída | R3/S4 |
| US-17 | FT-118 | Geração automática de até três rotas | R3/S4 |
| US-18 | FT-120 | Visualização de rotas no mapa | R3/S4 |
| US-19 | FT-122 | Registro da rota escolhida | R3/S5 |
| US-20 | FT-123 | Comparação de horários de saída | R4/S6 |

## 2. Estratégia e ambiente

- Backend/integração: Django/DRF, `TestCase`/`APIClient`, PostgreSQL, mocks e fixtures.
- Funcional/BDD: Cypress + Cucumber, cenários `.feature` em português e tags por release/história.
- CI: GitHub Actions executa checks Django, build frontend, E2E (`@smoke`, `@US-07`, `@R1`, `@US-08`, `@R2`), varredura de segredos e deploy em push na `main`.
- Testes exploratórios/manuais: homologação, formulários, permissões e apresentação do catálogo.
- Regra: só marcar CT aprovado com execução observada ou evidência rastreável. Mocks não comprovam disponibilidade real de provedor externo.

| Componente | Situação no fechamento R2 |
|---|---|
| Homologação | Render: https://feneme-homologacao.onrender.com |
| Backend / banco | Django/DRF e PostgreSQL |
| Frontend | React/TypeScript |
| E2E | Cypress + Cucumber |
| CI | GitHub Actions, `.github/workflows/ci.yml` |
| APIs | Open-Meteo; chamadas externas simuladas no CI. Google Routes/Maps ficam para R3. |
| Dados | Contas, entregas, cidades e cargas fictícias |

A primeira implantação em homologação foi validada no CI #351, com health check documentado (`status: ok`, `database: ok`). Em 26/11, o QA confirmou manualmente a FT-114 em homologação: sete tipos de carga, campos e limites corretos, “limite derivado” para cosméticos e links das fontes funcionando. Não é necessário repetir esse teste.

## 3. Matriz de casos CT-01 a CT-48

| CT | US/Jira | Cenário | Tipo | Situação no fechamento |
|---|---|---|---|---|
| 01 | US-01/FT-43 | Login válido do Gestor | Sucesso | Aprovado R1 |
| 02 | US-01/FT-43 | Senha inválida do Gestor | Exceção | Aprovado R1 |
| 03 | US-03/FT-44 | Cadastro válido | Sucesso | Aprovado R1 |
| 04 | US-03/FT-44 | Campos obrigatórios ausentes | Exceção | Aprovado R1 |
| 05 | US-05/FT-45 | Vincular Motorista válido | Sucesso | Aprovado R1 |
| 06 | US-07/FT-56 | Comparar duas alternativas manuais | Sucesso | Aprovado; @US-07 3/3 |
| 07 | US-06/FT-46 | Terceira alternativa ou entrada inválida | Exceção | **Aprovado; verificado em @R2** |
| 08 | US-09/FT-57 | Comparação térmica e menor exposição | Sucesso | Replanejado S5/R3 |
| 09 | US-08/FT-47 | Open-Meteo indisponível | Exceção | Aprovado; @US-08 2/2 |
| 10 | US-11/FT-48 | Motorista atualiza entrega atribuída | Sucesso | Aprovado; regressão @R2 |
| 11 | US-11/FT-48 | Motorista altera entrega alheia | Exceção | Aprovado; regressão @R2 e Q-05 20/20 |
| 12 | US-13/FT-59 | Histórico existente | Sucesso | Aprovado; histórico @R2 |
| 13 | US-02/FT-54 | Login válido do Motorista | Sucesso | Aprovado R1 |
| 14 | US-02/FT-54 | Senha inválida do Motorista | Exceção | Aprovado R1 |
| 15 | US-04/FT-55 | Consultar entregas existentes | Sucesso | Aprovado R1 |
| 16 | US-04/FT-55 | Consulta sem entregas | Exceção | Aprovado R1 |
| 17 | US-05/FT-45 | Atribuir não-Motorista | Exceção | Aprovado R1 |
| 18 | US-06/FT-46 | Cadastrar até duas alternativas válidas | Sucesso | **Aprovado; verificado em @R2** |
| 19 | US-07/FT-56 | Comparar com menos de duas opções | Exceção | Aprovado; @US-07 3/3 |
| 20 | US-08/FT-47 | Temperatura prevista disponível | Sucesso | Aprovado; @US-08 2/2 |
| 21 | US-09/FT-57 | Comparação sem previsão disponível | Exceção | Replanejado S5/R3 |
| 22 | US-10/FT-58 | Motorista consulta próprias entregas | Sucesso | Aprovado; API 2/2 |
| 23 | US-10/FT-58 | Motorista consulta entrega alheia | Exceção | Aprovado; API 2/2 |
| 24 | US-12/FT-49 | Gestor consulta situação atual | Sucesso | Aprovado; regressão @R2 |
| 25 | US-12/FT-49 | Consultar entrega inexistente | Exceção | Aprovado; regressão @R2 |
| 26 | US-13/FT-59 | Histórico sem alterações | Exceção | Aprovado; histórico @R2 |
| 27 | US-14/FT-113 | Cadastro com cidades da lista | Sucesso | Aprovado; PR #47 / E2E @US-14 |
| 28 | US-14/FT-113 | Origem igual ao destino | Exceção | Aprovado; PR #47 / E2E @US-14 |
| 29 | US-14/FT-113 | Cidade inexistente via API | Exceção | Aprovado; backend PR #47 |
| 30 | US-14/FT-113 | Mesma lista no clima | Sucesso | Aprovado; backend PR #47 |
| 31 | US-15/FT-114 | Consultar catálogo de cargas | Sucesso | Aprovado; E2E, CI e homologação manual |
| 32 | US-15/FT-114 | Motorista altera catálogo via API | Exceção | Aprovado; backend PR #44 |
| 33 | US-16/FT-117 | Cadastro com carga e saída em 2 dias | Sucesso | Planejado S4/R3 |
| 34 | US-16/FT-117 | Saída em 30 min ou em 6 dias | Exceção | Planejado S4/R3 |
| 35 | US-16/FT-117 | Tipo de carga ausente | Exceção | Planejado S4/R3 |
| 36 | US-17/FT-118 | Três rotas distintas (CG→Recife) | Sucesso | Planejado S4/R3 |
| 37 | US-17/FT-118 | Trajeto curto (49/51 km) | Exceção | Planejado S4/R3 |
| 38 | US-17/FT-118 | Alternativas insuficientes | Exceção | Planejado S4/R3 |
| 39 | US-17/FT-118 | Repetir consulta em menos de 24 h | Sucesso | Planejado S4/R3 |
| 40 | US-17/FT-118 | Routes API timeout/5xx/429/403 | Exceção | Planejado S4/R3 |
| 41 | US-18/FT-120 | Três rotas no mapa | Sucesso | Planejado S4/R3 |
| 42 | US-18/FT-120 | Mapa indisponível | Exceção | Planejado S4/R3 |
| 43 | US-09/FT-57 | Empate térmico e repetição | Exceção | Planejado S5/R3 |
| 44 | US-19/FT-122 | Escolher rota destacada ou outra | Sucesso | Planejado S5/R3 |
| 45 | US-19/FT-122 | Motorista tenta alterar rota | Exceção | Planejado S5/R3 |
| 46 | US-19/FT-122 | Previsão muda após escolha | Sucesso | Planejado S5/R3 |
| 47 | US-20/FT-123 | Comparar horários de saída | Sucesso | Planejado S6/R4 |
| 48 | US-20/FT-123 | Chegada fora do horizonte | Exceção | Planejado S6/R4 |

### 3.1 Observações da matriz

- CT-07 e CT-18 deixaram de ser parciais: `trajetos.feature` contém os cenários de cadastro válido, terceira alternativa e entradas inválidas. Os três cenários `@US-06` passaram dentro da execução `@R2` 29/29.
- CT-08 e CT-21 foram reescritos pela FT-112 e passaram para FT-57, Sprint 5/R3.
- CT-06, CT-07, CT-18 e CT-19 são da funcionalidade de trajetos manuais e serão aposentados na R3 (FT-119).
- CT-27/28 têm cenários E2E; CT-29/30 têm cobertura backend na PR #47.
- CT-31/32 têm cobertura backend na PR #44; CT-31 também tem cenário E2E e verificação manual em homologação.
- CT-32 é coberto pelo backend e não deve ser somado como cenário Cypress.

## 4. Resultados da Sprint 3 e regressão completa da R2

CI da PR #51: [run 45731598047](https://github.com/moon-byme/feneme-tech/actions/runs/45731598047). Todos os jobs passaram.

| Suíte | Resultado |
|---|---:|
| Backend Django | 196/196 |
| Cypress `@smoke` | 18/18 |
| Cypress `@US-07` | 3/3 |
| Regressão `@R1` | 10/10 |
| Cypress `@US-08` | 2/2 |
| Regressão completa `@R2` | **29/29** |
| Q-05 — tentativas de alteração cruzada | **20/20 rejeitadas** |

Q-01 considera **30 CT únicos aplicáveis**: 10 CT da regressão R1 + 20 CT específicos R2. Resultado: **30/30 (100%)**. A suíte Cypress `@R2` possui 29 cenários; CT-32 é coberto pelo backend.

Resultados por história da Sprint 3:
- FT-48/US-11: CT-10 e CT-11 aprovados; atualização persistida e acesso cruzado negado.
- FT-49/US-12: CT-24 e CT-25 aprovados; consulta de andamento e tratamento de entrega inexistente.
- FT-59/US-13: CT-12 e CT-26 aprovados; 2 cenários em `historico.feature`.
- FT-113/US-14: CT-27 a CT-30 cobertos por E2E/backend na PR #47.
- FT-114/US-15: CT-31/32 cobertos por Cypress/backend na PR #44; catálogo confirmado manualmente em homologação.
- CT-07/18 completados na regressão R2.

Resultados de regressão:
- R1 10/10; @US-07 3/3; @US-08 2/2; @R2 29/29; backend 196/196; smoke 18/18.
- Os resultados pertencem a seleções parcialmente sobrepostas; não somar as contagens como casos únicos.

## 5. Indicadores e evidências

Valores conforme o Plano de Qualidade atualizado em 26/11/2026.

| Indicador | Resultado R2 | Evidência / ressalva |
|---|---|---|
| Q-01 — Execução de CT | 30/30 = 100% | 10 CT R1 + 20 específicos R2; CI #45731598047 |
| Q-02 — Bugs críticos/altos sem plano | 0 Bugs registrados na consulta de 26/11 | Snapshot Jira; não prova ausência de defeitos não reportados |
| Q-03 — Critérios Gherkin verificáveis | 8/8 = 100% | Critérios aplicáveis |
| Q-04 — Revisão de PR | 19/19 = 100% na Sprint 3 | PRs #39–#57; recorte estrito `main`: 18/18; SM FT-72/10319 |
| Q-05 — Acesso cruzado | 20/20 rejeitadas = 100% | Zero alterações indevidas; PR #51 / CI #45731598047 |
| Q-06 — Erros/logs sem exposição | 0 exposições em 20 cenários | FT-74 / evidências de segurança |
| Q-07 — Facilidade de cadastro | 5/5 participantes = 100% na medição registrada | Repetição após mudanças do formulário não comprovada aqui |
| Q-08 — Cobertura backend | 88% conforme Plano de Qualidade v2.6 | Valor reproduzido da planilha; não recalculado nesta atualização |
| Q-09 — Estabilidade CI na `main` | 45/47 = 95,7% | Pushes na `main` da R2; `workflow_dispatch` excluído |
| Q-10 — Credenciais/sessões inválidas | 20/20 = 100% | Evidência de autenticação |
| Q-11 — Consistência térmica | Planejado R3 | FT-57/S5; não medido na R2 |
| Q-12 — Persistência de status | 20/20 = 100% | PR #41 e CI #260; conferência PO FT-80 |
| Q-13 — Continuidade sem Open-Meteo | 10/10 = 100% | Falhas simuladas; não mede disponibilidade real; FT-81 |
| Q-14 — Usabilidade em 360 px | Planejado R3 | Não medido na R2 |
| Q-15 — Rastreabilidade funcional | 9/9 = 100% R2; Sprint 3: 5/5 | SM FT-83/10320 e FT-83/10338 |
| Q-16 — Indicador adicional | Proposta não aprovada | Sem medição |

**Ressalvas:** Q-07 representa a sessão registrada de 5/5, não prova repetição após mudanças posteriores no formulário. Q-08 foi reproduzido da planilha v2.6. Q-09 mede sucesso de execuções na `main`, não cobertura de código.

## 6. Gestão de defeitos

O relatório de achados está em `docs/qa/relatorio-de-defeitos-r2.md`. Três candidatos foram documentados na Sprint 2: estado vazio após falha na consulta (FT-55), apresentação de apenas um erro de campo (FT-44) e resposta de previsão associada à localidade anterior (FT-47). A situação atual de cada achado e as ressalvas de reteste estão no relatório.

Consulta Jira `project = FT AND issuetype = Bug` em 26/11: nenhum resultado. Busca de issues `bug` no GitHub: nenhum resultado. Isso significa zero tickets formais localizados, não ausência absoluta de defeitos.

## 7. Cronograma

| Sprint | Foco | Entregável / situação |
|---|---|---|
| S0/R1 | Plano e matriz CT-01 a CT-26 | Concluído |
| S1/R1 | CT-01 a CT-05 e CT-13 a CT-17 | Concluído; regressão 10/10 |
| S2/R2 | Trajetos, clima, entregas Motorista e R1 | Concluído; histórico preservado |
| S3/R2 | CT-10 a CT-12, CT-24 a CT-32, CT-07/18 e regressão | **Concluído; v2.4** |
| S4/R3 | CT-33 a CT-42 | Planejado |
| S5/R3 | CT-08, CT-21 e CT-43 a CT-46 | Planejado |
| S6/R4 | CT-47 e CT-48; regressão geral | Planejado |

## 8. Critérios de entrada e saída

**Entrada:** DoR conferida, Gherkin compreendido, código integrado, ambiente e massa fictícia disponíveis; serviços externos substituídos por mocks/fixtures no CI.

**Saída:** CT aplicáveis às histórias concluídas executados; resultados e evidências registrados; achados descritos e vinculados; regressão pertinente executada; limitações e itens replanejados comunicados ao PO. A publicação da tag/release é responsabilidade de PO/DevOps (FT-92).

## 9. Referências

- [PR #37 — achados de QA da Sprint 2](https://github.com/moon-byme/feneme-tech/pull/37)
- [PR #41 — atualização de status / Q-12](https://github.com/moon-byme/feneme-tech/pull/41)
- [PR #44 — catálogo de cargas / FT-114](https://github.com/moon-byme/feneme-tech/pull/44)
- [PR #47 — lista única de cidades / FT-113](https://github.com/moon-byme/feneme-tech/pull/47)
- [PR #51 — regressão R2, CT e Q-05](https://github.com/moon-byme/feneme-tech/pull/51)
- [CI #45731598047 — backend e regressão R2](https://github.com/moon-byme/feneme-tech/actions/runs/45731598047)
- [CI #45738722270 — homologação/deploy](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270)
- [FT-112 — mudança de escopo](https://feneme.atlassian.net/browse/FT-112)
- [FT-91 — fechamento QA R2](https://feneme.atlassian.net/browse/FT-91)
- [Plano de Qualidade](https://docs.google.com/spreadsheets/d/1iRGEGUlcYLnbFpMCBW8yy89v-VHCkdEi-gPcPEhxdv8/edit?usp=sharing)

**Estado:** atualizado até o fechamento da Sprint 3/R2 em 26/11/2026. Casos R3/R4 permanecem planejados.
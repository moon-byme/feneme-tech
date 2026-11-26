# Relatório do Pipeline — Release 2

**Projeto:** Feneme · **Release:** R2 (Sprints 2 e 3, 03/11/2026 a 26/11/2026) · **Responsável:** DevOps — João Paulo de Araujo
**Rastreabilidade:** [FT-92](https://feneme.atlassian.net/browse/FT-92) (publicação da R2), [FT-110](https://feneme.atlassian.net/browse/FT-110) (homologação), [FT-89](https://feneme.atlassian.net/browse/FT-89) (pendências de PO/DevOps da R1), FT-77 (Q-09) e FT-72 (Q-04)
**Workflow:** `.github/workflows/ci.yml` (nome `CI`) · **Fonte dos dados:** API do GitHub Actions e de Pull Requests, consultada em 25/11/2026
**Período coberto:** execuções nº 52 (03/11, 22h08) a nº 310 (25/11, 18h20), horário de Brasília

## 1. Configuração do pipeline ao fim da R2

| Job | O que verifica | Desde |
| --- | --- | --- |
| `Detect application components` | Detecta `backend/` e `frontend/` para ativar os demais jobs | R1 |
| `Backend - Django checks and tests` | `manage.py check` e `manage.py test` com PostgreSQL | R1 |
| `Frontend - build and tests` | `npm ci` e `npm run build` (TypeScript + Vite) | R1 |
| `E2E - Cucumber/Cypress (@smoke)` | Sobe PostgreSQL e Django com o build do React e executa `@smoke`, `@US-07`, `@R1` e `@US-08`; publica relatório e capturas de falha | R2 (PR #11, ampliado nas PRs #15, #18, #24, #25) |
| `Segurança - segredos fora do repositório` | Falha se houver chave do Google, chave privada, `.env` versionado ou URL de banco com senha | R2 (FT-110) |
| `Deploy - homologação (Render)` | Só em push na `main`, depois de todos os jobs acima: dispara o deploy e espera `/api/health/` com o commit implantado | R2 (FT-110) |

**Gatilhos:** push em qualquer branch, Pull Request para a `main` e execução manual.
**Proteção da `main`:** desde 04/11/2026, só por Pull Request, com 1 aprovação de outro integrante e os jobs de backend, frontend e E2E obrigatórios ([`docs/devops/protecao-main.md`](../../devops/protecao-main.md)).

> Os dois últimos jobs entram com o PR da FT-110. Os números abaixo são das execuções anteriores a ele.

## 2. Indicadores da R2

| Indicador | R2 (total) | Sprint 2 (03–16/11) | Sprint 3 (17–25/11) |
| --- | ---: | ---: | ---: |
| Execuções do workflow | 259 | 196 | 63 |
| Sucesso | 236 (**91,1%**) | 182 (92,9%) | 54 (85,7%) |
| Falhas | 23 | 14 | 9 |
| Execuções na `main` (push) | 34 | 27 | 7 |
| Sucesso na `main` | **34/34 (100%)** | 27/27 | 7/7 |
| Duração mediana (execuções com sucesso) | 3 min 27 s | 3 min 18 s | 3 min 52 s |
| Duração máxima | 6 min 12 s | 6 min 12 s | 5 min 18 s |

- **Nenhuma falha chegou à `main`.** Todas as 23 falhas ocorreram em branches de trabalho e foram corrigidas antes do merge; a proteção da `main` impediu a integração com checagens vermelhas.
- A duração mediana subiu frente à R1 (51 s) porque o job E2E passou a executar quatro seleções de cenários com Cypress.
- A taxa menor da Sprint 3 vem de ajustes em testes E2E durante o desenvolvimento das FT-49, FT-113 e FT-114 (seção 3), não de instabilidade do runner.

## 3. Falhas, causas e correções

Execuções do mesmo commit (push e pull_request) contam separadamente no total, mas aparecem agrupadas por episódio.

| Execuções | Data (BRT) | Branch | Job que falhou | Causa identificada | Correção | Tempo até o verde |
| --- | --- | --- | --- | --- | --- | --- |
| [#74](https://github.com/moon-byme/feneme-tech/actions/runs/42111106366), [#77](https://github.com/moon-byme/feneme-tech/actions/runs/42111205236) | 05/11 | `qa/sprint1-cypress-regression` | E2E | Etapas de atribuição duplicadas e preparação da entrega ausente nos cenários novos | `701675b`, `13da418` | minutos |
| [#87](https://github.com/moon-byme/feneme-tech/actions/runs/42700405554)–#90 | 09/11 | `qa/sprint2-quality-assurance` | Backend | Teste FT-74 esperava status HTTP diferente do retornado para exclusão proibida | `a40004b` | 3,8 h |
| [#101](https://github.com/moon-byme/feneme-tech/actions/runs/42736745437) | 09/11 | `qa/r2-status-visibility-e2e` | E2E | Cenários CT-22/CT-23 marcados como `@smoke` antes de as etapas existirem | `14cb07c` | minutos |
| [#124](https://github.com/moon-byme/feneme-tech/actions/runs/42838062498) | 10/11 | `qa/ft58-validacao-interface-motorista` | E2E | Cenário da interface do Motorista incompleto | `32c505c` | minutos |
| [#134](https://github.com/moon-byme/feneme-tech/actions/runs/42841691033)–#138 | 10/11 | `test/ft32-q13-falhas-preservam-fluxos` | Backend | Erro de continuação de linha no teste Q-13 | `e3f98d6` | 12 min |
| [#152](https://github.com/moon-byme/feneme-tech/actions/runs/42845484376) | 10/11 | `feature/FT-56-comparacao-trajetos` | E2E | Cenário de comparação sem alternativas cadastradas ainda sem etapa | `ce25b53` | minutos |
| [#188](https://github.com/moon-byme/feneme-tech/actions/runs/43103753587) | 11/11 | `docs/FT-33-evidencias-seguranca-r2` | E2E | Falha isolada; a execução seguinte do mesmo conteúdo passou | `eb93768` | minutos |
| [#261](https://github.com/moon-byme/feneme-tech/actions/runs/44530428057)–#264 | 19/11 e 24/11 | `feature/ft-49-consultar-andamento-entregas` | E2E | Textos da tela mudaram ("Acompanhamento das entregas", "Motorista responsável") e as etapas antigas não foram atualizadas | `0007284`, `73c830d` | 5 dias (branch parada de 19 a 24/11) |
| [#275](https://github.com/moon-byme/feneme-tech/actions/runs/45456611113) | 24/11 | `feature/ft-59-consultar-historico-entrega` | Frontend | Build quebrado entre commits intermediários do histórico | `c08908c` | minutos |
| [#286](https://github.com/moon-byme/feneme-tech/actions/runs/45493153805), [#288](https://github.com/moon-byme/feneme-tech/actions/runs/45494003629) | 24/11 | `feature/FT-114-catalogo-tipos-carga` | E2E | O contador do catálogo reutilizou a classe `.count-badge`, lida pelo teste de lista vazia ("07" em vez de "0") | `49bfdb9` | 2,5 h |
| [#287](https://github.com/moon-byme/feneme-tech/actions/runs/45493178330), [#291](https://github.com/moon-byme/feneme-tech/actions/runs/45516781060) | 24/11 | `feature/FT-113-lista-unica-cidades` | E2E | Mesma causa da FT-114 e, depois, cenário novo procurando o seletor do clima sem entrega cadastrada | `49bfdb9`, `b1d70f3` | 20,9 h |

**Tempo de correção:** mediana de minutos nos episódios corrigidos no mesmo dia; os dois casos longos (FT-49 e FT-113) foram branches paradas, não quebras da `main`.

**Medidas tomadas:** o E2E roda em toda branch antes do PR, as falhas publicam capturas como artefato, e a regra combinada na R2 é não abrir PR com CI vermelho. Para a R3: atualizar as etapas E2E no mesmo commit que muda textos da tela e não reutilizar classes CSS usadas como seletor de teste (preferir `data-cy`).

## 4. Governança da integração (revisão de PRs)

| Indicador | Valor |
| --- | --- |
| PRs integrados na R2 (#11 a #46) | 35 |
| Com aprovação de outro integrante **antes** do merge | 33 (94,3%) |
| Sem aprovação prévia | #11 (aprovado 16 s depois do merge, 03/11) e #12 (03/11), ambos antes da proteção da `main` |
| PRs da Sprint 3 (#38 a #46) com aprovação prévia | 9/9 (100%) |

**Ocorrência na Sprint 3:** a PR #42 (FT-49) foi integrada com a base ainda apontando para a branch da FT-48, porque essa branch não foi apagada no merge da #41. O código chegou à `main` pela PR #43, com a base corrigida e o conflito do README resolvido. **Medida:** apagar a branch no merge e conferir a base antes de integrar PRs empilhados.

## 5. Homologação (FT-110)

O deploy automatizado no Render foi implementado no PR da FT-110 (seções 1 e [`docs/devops/homologacao.md`](../../devops/homologacao.md)): o job de deploy depende de todos os testes, só roda em push na `main` e espera o `/api/health/` responder com o commit implantado. A implantação automática foi confirmada em 25/11/2026 no [CI #351](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270), após a correção do Deploy Hook pela [PR #53](https://github.com/moon-byme/feneme-tech/pull/53).

### Evidências complementares da FT-110 (25/11/2026)

- URL: https://feneme-homologacao.onrender.com; Render Live, disparo via Deploy Hook (HTTP 200).
- Health check: https://feneme-homologacao.onrender.com/api/health/ — `status: ok`, `database: ok`; commit `b017151287a6b9325c690037651c92412aff8a1f`, igual ao SHA da execução.
- Backend, frontend (build), E2E e segurança aprovados; as duas etapas do deploy concluídas. Não havia script de teste unitário do frontend configurado.
- [CI #331](https://github.com/moon-byme/feneme-tech/actions/runs/45730929872): falha E2E e deploy ignorado em branch de QA. A condição de branch também impede o deploy; não comprova isoladamente o bloqueio por falha na main. A regra `needs` confirma a dependência dos jobs por inspeção da configuração, sem ensaio de falha na main.
- [CI #345](https://github.com/moon-byme/feneme-tech/actions/runs/45734971703) e [#348](https://github.com/moon-byme/feneme-tech/actions/runs/45735867289): jobs de teste aprovados, deploy falhou; #348 retornou HTTP 404. A PR #53 corrigiu o parâmetro do hook, com recuperação comprovada pelo #351.
- Fonte editável do registro: [validacao-homologacao-r2.typ](validacao-homologacao-r2.typ).

Os indicadores das seções 2–4 e 6 mantêm o recorte original indicado no relatório; não representam as execuções posteriores nem o fechamento completo da R2.

## 6. Comparação com a Release 1

| Indicador | R1 (06–29/10) | R2 (03–25/11) |
| --- | --- | --- |
| Execuções | 51 | 259 |
| Sucesso | 100% (51/51), com jobs pulados no início | 91,1% (236/259) com todos os jobs ativos |
| Sucesso na `main` | 100% | 100% (34/34) |
| Commits diretos na `main` | 10 | 0 |
| Testes E2E/BDD no CI | nenhum | Cucumber/Cypress em quatro seleções |
| PRs com revisão antes do merge | 0 de 7 avaliados | 33 de 35 |
| Deploy de homologação | não havia | implementado (FT-110) |

## 7. Pendências e registro final

- [x] Proteção da `main` aplicada (04/11/2026).
- [x] Indicadores consolidados da R2 (este relatório).
- [x] Primeira implantação automatizada bem-sucedida: [CI #351](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270), [homologação](https://feneme-homologacao.onrender.com), [health check](https://feneme-homologacao.onrender.com/api/health/).
- [ ] CI da `main` no commit escolhido para a tag `v2.0.0`.
- [ ] Tag `v2.0.0` e GitHub Release publicadas; link deste relatório na FT-92 e na versão Release 2 do Jira.

## 8. Complemento de fechamento — recorte até o CI #375 (26/11/2026)

Os números das seções 2–4 e 6 são o recorte histórico até #310. A consulta adicional ao histórico de CI recuperou **todas as 65 execuções #311–#375**, sem lacunas, até o [run #375](https://github.com/moon-byme/feneme-tech/actions/runs/45832088850) na main (commit `5894f6251b08c46f4caf2fa3888758f53110890e`). O recorte ainda deve ser atualizado caso haja novos merges antes da tag.

| Indicador | #52–#310 (recorte original) | #311–#375 (complemento) | #52–#375 (acumulado) |
| --- | ---: | ---: | ---: |
| Execuções | 259 | 65 | **324** |
| Sucesso | 236 | 60 | **296 (91,4%)** |
| Falhas | 23 | 5 | **28** |
| Pushes na main | 34 | 11 | **45** |
| Sucesso na main (Q-09) | 34/34 | 9/11 | **43/45 (95,6%)** |

A meta proposta da Q-09 (≥90%) permanece atingida no recorte da R2; não se deve usar 100% como taxa final. Não foram recalculadas as durações medianas e máximas do período completo; as do quadro original permanecem restritas a #52–#310.

| Novas falhas | Local | Causa / encaminhamento |
| --- | --- | --- |
| [#331](https://github.com/moon-byme/feneme-tech/actions/runs/45730929872), [#332](https://github.com/moon-byme/feneme-tech/actions/runs/45730935425), [#333](https://github.com/moon-byme/feneme-tech/actions/runs/45731594912) | branch QA | Ajuste de cenários/etiquetas CT e seleção da regressão integral; QA documentou 27/31 inicialmente e 29/29 após revisão do universo aplicável e correção das etapas (PR #51; [CI aprovado](https://github.com/moon-byme/feneme-tech/actions/runs/45731598047)). |
| [#345](https://github.com/moon-byme/feneme-tech/actions/runs/45734971703), [#348](https://github.com/moon-byme/feneme-tech/actions/runs/45735867289) | main | Testes passaram; deploy falhou. #348 retornou HTTP 404; PR #53 corrigiu o parâmetro do hook e #351 confirmou recuperação. |

As duas falhas na main foram de implantação, não regressão funcional do backend/E2E. A regra de deploy continua restrita à main com dependências verdes. A última execução consultada (#375) teve sucesso em todos os seis jobs: detecção, backend, frontend (build), E2E (inclui @R2), segurança e deploy. Não é ainda um commit ratificado para a tag.

**Governança — Sprint 3:** conferência dos registros de aprovação e horários de merge das PRs #39–#57: **19/19 (100%)** com aprovação externa prévia. Excluindo #42, cuja base era uma feature, o recorte estrito da main é **18/18 (100%)**. A #42 teve aprovação antes de ser integrada na feature e seu conteúdo entrou na main pela #43. A PR #58 ainda aberta não integra o denominador. [Q-04 / FT-72](https://feneme.atlassian.net/browse/FT-72?focusedCommentId=10319). As contagens históricas da seção 4 não foram sobrescritas.

**Pendente para o lançamento:** ratificação da Review, fechamento da QA, verificação do CI e da implantação do commit final escolhido, tag, publicação e versão Jira.

## Histórico do documento

| Data | Versão | Descrição | Autor |
| --- | --- | --- | --- |
| 03/11/2026 | 0.1 | Relatório parcial da R2 com linha de base da R1 (rascunho local) | João Paulo de Araujo |
| 25/11/2026 | 1.0 | Consolidação da R2: 259 execuções, falhas e causas, governança de PRs e homologação | João Paulo de Araujo |
| 25/11/2026 | 1.1 | Complemento de homologação e evidências dos runs #331, #345, #348 e #351; indicadores originais preservados | Lethycia (SM R2), conferência documental |

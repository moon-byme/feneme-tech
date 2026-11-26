# Aceite do PO — Sprint 3 e Release 2

**PO:** João Paulo de Araujo · **Sprint:** FT Sprint 3 (17 a 26/11/2026) · **Rastreabilidade:** [FT-92](https://feneme.atlassian.net/browse/FT-92)
**Situação em 25/11/2026:** decisões preparadas a partir das evidências do GitHub e do Jira; confirmar na Sprint Review de 26/11 e registrar ali qualquer mudança.

## Sprint Goal

> Concluir a Release 2 com a atualização manual de status das entregas pelo Motorista, a consulta de andamento pelo Gestor e o histórico persistente, integrados na sequência FT-48 → FT-49 → FT-59. Preparar a evolução do Feneme com uma lista única de 26 cidades, catálogo de 7 tipos de carga com fontes, configuração segura do Google Cloud e registro do risco R10, além de executar testes, regressão, validação da DoD e procedimentos de homologação e publicação da R2.

Ratificado na Planning 3 ([ata](../../sprints/sprint-3/feneme_sprint_planning_3.typ)). **Avaliação:** atingido na parte de produto (status, andamento, histórico, cidades e catálogo); parcialmente atingido na preparação do Google Cloud, que depende de evidência no console (FT-115).

## Decisões sobre as histórias da Sprint 3

| Item | Decisão | Fundamento |
| --- | --- | --- |
| FT-48 — US-11 Atualizar status | **Aceita** | PR #41 integrada com aprovação prévia; 20/20 atualizações persistidas (Q-12); CI verde |
| FT-49 — US-12 Consultar andamento | **Aceita** | Código revisado na PR #42 e integrado na `main` pela PR #43; CI verde (run do commit `f80e290`) |
| FT-59 — US-13 Histórico | **Aceita** | PR #43 com aprovação prévia; E2E CT-26 a CT-28; CI verde |
| FT-114 — US-15 Catálogo de cargas | **Aceita** | PR #44 com aprovação prévia; CI pós-merge verde; 7 cargas com fonte conferidas com a FT-112 (D4). Validação manual do QA registrada como pendência na FT-91 |
| FT-113 — US-14 Lista de cidades | **Aceita condicionada ao merge da PR #47** | CI verde em todos os jobs, inclusive E2E `@US-14`; aguarda aprovação do QA para integrar |
| FT-110 — Homologação | **Aceita condicionada à primeira execução do deploy** | Workflow, Blueprint e guia prontos; falta criar o serviço no Render e registrar o primeiro run verde e a URL |
| FT-115 — Google Cloud | **Não aceita na Sprint 3** | Procedimento documentado, `.env.example` sem chaves e varredura de segredos no CI; faltam as evidências do console. Vai para a Sprint 4, antes da US-17 |
| FT-116 — R10 | **Não aceita na Sprint 3** | Depende da FT-115; tratamento no código (cache e falha simulada) é da Sprint 4 |
| FT-57 — US-09 Comparação térmica | **Fora da R2** | Transferida para a Sprint 5 (R3) por decisão de 16/11 (FT-112) |

## Riscos tratados na sprint

| Risco | Situação | Encaminhamento |
| --- | --- | --- |
| R05 (FT-64) | Tratamento comprovado: 20/20 | Registrar o risco residual na planilha (ver [riscos-residuais.md](riscos-residuais.md)) |
| R06 (FT-65) | 10/10 cenários com aviso e sem bloqueio | Parte da recomendação climática fica com a FT-57 (Sprint 5) |
| R08 (FT-67) | Cidades em lista fechada (FT-113); tipo de carga e saída na Sprint 4 | Teste de usabilidade cronometrado junto com a FT-117 |
| R10 (FT-116) | Preparado, não comprovado | Sprint 4, junto com a FT-115 |

## Repriorização para a Sprint 4

1. **FT-115 e FT-116** sobem para o início da Sprint 4: são pré-requisito da US-17 (rotas automáticas).
2. **FT-67** segue com a FT-117 (tipo de carga e saída no formulário) e o teste de usabilidade.
3. **FT-119** (remover o cadastro manual de trajetos) entra junto com a FT-118, para o Gestor não ficar sem comparação entre uma e outra.
4. A ordem planejada da R3 se mantém: FT-117 → FT-118 → FT-120 (Sprint 4); FT-57 → FT-122 (Sprint 5).

## Itens da DoD sob responsabilidade do PO

- [x] Sprint Goal registrado e avaliado.
- [x] Aceites e rejeições fundamentados por história.
- [x] Repriorização do que não foi concluído, com destino e motivo.
- [x] Release notes com somente o que tem evidência ([release-notes.md](release-notes.md)).
- [ ] Confirmação das decisões na Sprint Review de 26/11.

## Complemento de evidências — 26/11/2026 (pré-Review)

O quadro de decisões de 25/11 foi preservado. A documentação posterior permite atualizar o estado das condições técnicas, **sem substituir a ratificação do PO na Review**.

| Item | Conferência atual | Evidência |
| --- | --- | --- |
| FT-48, FT-49, FT-59 | DoDs técnicas conferidas no Jira; aceites já constam na decisão de 25/11 | PRs #41, #42 (feature), #43 (main), #51; QA nos comentários 10268–10270 |
| FT-113 | Condição de merge satisfeita; PO confirmou aceite em 25/11 | [PR #47](https://github.com/moon-byme/feneme-tech/pull/47), [FT-113](https://feneme.atlassian.net/browse/FT-113?focusedCommentId=10252) |
| FT-110 | Condição de deploy satisfeita; CI #351 e documentação #55 integrados; CI #375 também verde | [CI #351](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270), [#375](https://github.com/moon-byme/feneme-tech/actions/runs/45832088850), [homologação](https://feneme-homologacao.onrender.com) |
| FT-114 | Aceite do PO e testes automatizados comprovados; verificação manual do catálogo/fontes em homologação pendente | [PR #44](https://github.com/moon-byme/feneme-tech/pull/44), [FT-114](https://feneme.atlassian.net/browse/FT-114?focusedCommentId=10318) |
| FT-115/116 | Carryover para Sprint 4 conforme decisão do PO; cota de 100/dia comprovada, orçamento/validação local e tratamento do risco ainda pendentes | [FT-115](https://feneme.atlassian.net/browse/FT-115?focusedCommentId=10284), [FT-116](https://feneme.atlassian.net/browse/FT-116?focusedCommentId=10315) |

A [FT-72](https://feneme.atlassian.net/browse/FT-72?focusedCommentId=10319) confirma Q-04 de Sprint 3 em 19/19 PRs aprovadas antes do merge (18/18 no recorte estrito main); a [FT-83](https://feneme.atlassian.net/browse/FT-83?focusedCommentId=10320) confirma Q-15 em 5/5 US da Sprint 3 com vínculo teste/PR. Rastreabilidade não equivale ao aceite integral da DoD. A [FT-91](https://feneme.atlassian.net/browse/FT-91?focusedCommentId=10321) acompanha o relatório de qualidade e a verificação restante.

**Não registrar a Review como ocorrida antes da confirmação efetiva de data, participantes, demonstração e decisões.** A tag e a publicação dependem da conclusão acordada pelo time.

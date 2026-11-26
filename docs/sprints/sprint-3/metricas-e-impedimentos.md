# Métricas e impedimentos — Sprint 3 / R2

**Recorte:** conferência documental de 26/11/2026, antes do fechamento formal da Sprint 3. Não é ata de Review/Retrospectiva nem cálculo definitivo de velocity. Fonte: Jira, [Planning 3](feneme_sprint_planning_3.typ), GitHub Actions e PRs.

## 1. Escopo e fotografia do board

Na Planning de 17/11, 19 issues/58 SP foram ratificados conforme [FT-90](https://feneme.atlassian.net/browse/FT-90?focusedCommentId=10217). Na consulta de 26/11 anterior à correção da FT-115, a Sprint 3 tinha 16 issues/50 SP:

| Situação | Issues | SP |
| --- | --- | ---: |
| Concluído por status | FT-115, FT-114, FT-113, FT-112, FT-110, FT-81, FT-80, FT-65, FT-64, FT-59, FT-49, FT-48 | 35 |
| Em andamento | FT-92, FT-91, FT-90 | 10 |
| Em análise | FT-34 | 5 |
| Total | 16 | 50 |

FT-115 (2 SP) foi corrigida para Sprint 4/R3 e Em andamento conforme decisão do PO de 25/11: não integra a entrega aceita da R2. Após essa correção, mantidos os demais estados, o escopo fica em 15 issues/48 SP, sendo 33 SP em Done por status. A FT-114 ainda exige validação manual de QA. As cinco US funcionais da S3 somam 19 SP e possuem evidências e decisão de aceite do PO, sujeitas à ratificação da Review; não confundir esse subtotal com velocity aceita.

Após a conferência QA/PO já registrada na FT-80, o driver FT-34 (5 SP) foi atualizado para Concluído. Mantidos os demais estados, a fotografia subsequente é de 12 issues/38 SP em Done e 3 issues/10 SP em andamento, dentro de 15 issues/48 SP. Não equivale à velocity final.

A diferença entre 58 SP da Planning e a fotografia de 48 SP corresponde à alteração líquida de escopo (-10 SP); a trajetória diária e cada mudança devem ser confirmadas no relatório do Jira, sem inventar pontos de burndown. Ao término, registrar a velocity apenas com itens que cumpram a DoD acordada, discriminando as ressalvas e carryovers.

## 2. Impedimentos e qualidade

- I-03: acompanhamento preventivo do fluxo de PR. [FT-72](https://feneme.atlassian.net/browse/FT-72?focusedCommentId=10319): 19/19 PRs #39–#57 aprovadas por outro integrante antes do merge, 18/18 no recorte estrito de main. A #42 foi integrada na feature e chegou à main pela #43; conferir base antes de integrar PRs dependentes.
- Q-15: [FT-83](https://feneme.atlassian.net/browse/FT-83?focusedCommentId=10320): 5/5 US da S3 com vínculo teste/PR/Jira; não implica fechamento da DoD de FT-114.
- Regressão integral @R2: [29/29](https://github.com/moon-byme/feneme-tech/actions/runs/45731598047), PR #51 integrada. FT-57 fora da R2; manter o escopo aprovado.
- Homologação: falhas #345 e #348 corrigidas pela PR #53; [#351](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270) confirmou recuperação; [#375](https://github.com/moon-byme/feneme-tech/actions/runs/45832088850) verde inclusive deploy. Consultar [relatório de pipeline](../../releases/release-2/relatorio-pipeline.md).
- QA: validar manualmente catálogo e links de fontes da FT-114 e consolidar relatório da FT-91. Não pressupor que QA já executou essa verificação.
- Riscos: [riscos residuais R2](../../releases/release-2/riscos-residuais.md), FT-8. R05/R06 com residual 8 documentado; R08 e R10 seguem em tratamento, R01 aguarda aprovação residual. O registro de riscos deve manter decisões e evidências reais.

## 3. Fechamento a registrar

- [ ] Burndown e velocity oficiais exportados do Jira/GitHub após o fim da Sprint, com interpretação e ressalvas.
- [ ] Review com demonstração, aceites/rejeições e repriorização ratificada.
- [ ] Retrospectiva e plano de ação, responsáveis e prazos; rotação para a R3.
- [ ] Revisão final do registro de riscos e links da DoD; publicação formal da versão pelo PO/DevOps.

**Acompanhamento:** [FT-90](https://feneme.atlassian.net/browse/FT-90) · [FT-91](https://feneme.atlassian.net/browse/FT-91) · [FT-92](https://feneme.atlassian.net/browse/FT-92).

# Feneme — Relatório consolidado de métricas e impedimentos da Release 2

**Período:** 03–26/11/2026 · **Sprints:** 2 e 3 · **Responsável:** Scrum Master da R2 · **Data de consolidação:** 26/11/2026  
**Rastreabilidade:** [FT-87](https://feneme.atlassian.net/browse/FT-87), [FT-90](https://feneme.atlassian.net/browse/FT-90), [FT-124](https://feneme.atlassian.net/browse/FT-124), [FT-38 — DoD](https://feneme.atlassian.net/browse/FT-38), critério 8 da DoD Release.

## 1. Resultados consolidados

| Indicador | Sprint 2 | Sprint 3 | Release 2 |
| --- | ---: | ---: | ---: |
| Escopo inicialmente selecionado (SP) | 40 | 58 | 98 |
| Entradas de escopo (SP) | 4 | 0 | 4 |
| Saídas de escopo (SP) | 8 | 10 | 18 |
| Escopo final (SP) | 36 | 48 | 84 |
| Issues concluídas por status / escopo final | 11/11 | 15/15 | 26/26 |
| Pontos concluídos por status | 36 | 48 | 84 |
| Pontos restantes por status | 0 | 0 | 0 |
| Conclusão do escopo final por status | 100% | 100% | 100% |
| Histórias funcionais com aceite do PO | 4 | 5 | 9 |
| SP funcionais com aceite do PO | 12 | 19 | 31 |

**Método:** consulta JQL `project = FT AND sprint in ('FT Sprint 2','FT Sprint 3')` em 26/11: 26 issues em Concluído, somando 84 SP. O agregado é a soma dos recortes de sprint, não o compromisso inicial líquido da release: as movimentações entre sprints da própria R2 aparecem no histórico. Os 40 SP iniciais da S2 são uma reconstrução pelas issues, não o valor inicial confirmado do gráfico nativo. A FT-58 (2 SP) preserva a ressalva histórica de revisão do PR original. Os 84 SP são velocity operacional por status, não uma certificação automática da DoD de cada item. Os 31 SP funcionais são um recorte distinto, incluído no total operacional.

## 2. Burndown e alterações de escopo

- **S2:** 40 + 4 − 8 = 36 SP. Entraram FT-56 e FT-58 (2 SP cada); saíram FT-32 (5 SP) e FT-33 (3 SP), para S3. A captura de 12/11 mostra zero pontos restantes. Ver [relatório S2](../../sprints/sprint-2/metricas-e-impedimentos.pdf) e [burndown S2](../../sprints/sprint-2/burndown-sprint-2.png).
- **S3:** 58 − 10 = 48 SP. FT-32 (5 SP) foi para S5; FT-67 (2 SP), FT-115 (2 SP) e FT-116 (1 SP) foram para S4. A primeira fotografia de 26/11 registrava 38/48 SP e 10 restantes; a segunda registra 48/48 SP e zero restantes. Ver [relatório S3](../../sprints/sprint-3/metricas-e-impedimentos.md), [burndown S3](../../sprints/sprint-3/burndown-sprint-3.svg) e [aceite do PO](aceite-po-sprint-3.md).

A conclusão se concentrou nos últimos dias das duas sprints. Mudanças de escopo também alteraram o burndown; não interpretar toda redução como entrega. O gráfico S3 é reprodução visual da captura oficial, com pontos intermediários aproximados.

## 3. Velocity

A S2 concluiu 36 SP e a S3, 48 SP por status: aumento de 12 SP (33,3%). A média operacional da R2 foi 42 SP/sprint. Para manter a comparação homogênea, o [gráfico de velocity operacional](../../sprints/sprint-3/velocity-operacional.svg) usa o escopo final e os pontos concluídos por status; a [captura de velocity S2](../../sprints/sprint-2/velocity-sprint-2.png) preserva a evidência do Jira. O indicador não substitui a avaliação de capacidade nem o aceite formal.

## 4. Impedimentos recorrentes e ações

| Registro | Resultado na R2 | Encaminhamento R3 |
| --- | --- | --- |
| I-03 — revisão de PR | Melhoria do processo; Q-04 S3: 19/19 PRs #39–57 com aprovação externa pré-merge (18/18 no recorte estrito da main). FT-58 mantém ressalva histórica. | Manter revisão externa e CI obrigatório; conferir destino de PRs dependentes. [FT-72/10319](https://feneme.atlassian.net/browse/FT-72?focusedCommentId=10319). |
| Concentração de entregas e documentação no fechamento | Burndowns atingiram zero SP por status, mas com baixas concentradas no final. | Acompanhar métricas e ações intermediárias em [FT-126](https://feneme.atlassian.net/browse/FT-126). |
| Mudança de escopo e dependências | FT-112 reorganizou o produto; 10 SP da S3 transferidos com justificativa. | Acompanhar sequência FT-115/116, FT-117/118/120; revisar capacidade antes do compromisso da S4. |
| Falhas de homologação | Execuções #345/#348 recuperadas pela PR #53; CI #351 confirmou recuperação. | Antecipar validação de infraestrutura e preservar evidências. [Relatório do pipeline](relatorio-pipeline.md). |
| Medição de usabilidade | Q-07: 5/5 participantes, sem cronometragem; preservar limitação. | Reavaliar com roteiro/cronômetro conforme FT-67 e critérios da equipe. |

A revisão dos riscos está documentada na [FT-8/10355](https://feneme.atlassian.net/browse/FT-8?focusedCommentId=10355) e no [registro de riscos residuais](riscos-residuais.md). Tratamentos transferidos à R3 são continuidade do produto, não pendências de elaboração deste relatório.

## 5. Conclusão

O escopo final das duas sprints soma 84 SP concluídos por status, 26/26 issues e zero SP restantes; nove histórias funcionais somam 31 SP com aceite registrado. A Release 2 apresenta melhoria no processo de integração e rastreabilidade, com oportunidade de distribuir entregas e evidências ao longo das sprints. O relatório consolida velocity, burndown, alterações de escopo e impedimentos recorrentes para o critério 8 da DoD Release, sem declarar publicação da tag nem substituir outros critérios.

**Fontes:** [S2 — fonte editável](../../sprints/sprint-2/fontes/metricas-e-impedimentos.typ) · [S3 — relatório](../../sprints/sprint-3/metricas-e-impedimentos.md) · [PR #60](https://github.com/moon-byme/feneme-tech/pull/60) · [retrospectiva R2](ata-retrospectiva-release-2-feneme.md) · [relatório de qualidade](../../qa/sprint-3-relatorio-parcial-r2.md).

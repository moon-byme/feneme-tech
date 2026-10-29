# Métricas e impedimentos — Sprint 1 (FT Sprint 1)

**Período:** 21/10/2026 a 29/10/2026 | **Fonte:** Jira (projeto FT, board 1), consulta de 29/10/2026 às 18h45. Valores a reconfirmar no fechamento da sprint.

## Velocity

| Indicador | Valor |
|---|---|
| Itens na sprint | 23 issues / 64 SP |
| US funcionais comprometidas | 5 US / 15 SP (FT-43 3, FT-54 2, FT-44 5, FT-55 2, FT-45 3) |
| US concluídas (Done) | 5 US / **15 SP** |
| **Velocity (US)** | **15 SP** |
| Demais itens Done (drivers, tasks Q, planos) | 0 de 18 até o momento da consulta |

O compromisso funcional da R1 (5 US / 15 SP) foi entregue. Os drivers (FT-29, FT-30), as ações de risco (FT-60, FT-61) e as tasks do Plano de Qualidade seguem em andamento. A maioria depende de verificação do QA ou de aceite do PO.

## Burndown

Anexar a captura do relatório **Jira → Reports → Burndown chart (FT Sprint 1)** no fechamento da sprint.

## Impedimentos

| ID | Data | Descrição | Impacto | Status | Resolução |
|---|---|---|---|---|---|
| I-01 | 26/10/2026 | Desvio do fluxo de PR: o código das US-01, 03, 04 e 05 foi commitado direto na main (de2b3d9) e removido em seguida (c48007d). | A main ficou sem o código entre 26/10 19h22 e 27/10 14h38, cerca de 19 horas. | Resolvido | Código reintegrado pelo PR #1 (revert 86d9eba, merge 8496e3a em 27/10/2026). Equipe deve confirmar o motivo na retro. Ação sugerida: proteger a main (exigir PR e aprovação). |
| I-02 | 29/10/2026 | Ambiente Docker substituído por execução local (PR #3). | Mudança de setup no fim da sprint. | Resolvido | Instruções atualizadas em README_IMPLEMENTACAO_SPRINT1.md. |

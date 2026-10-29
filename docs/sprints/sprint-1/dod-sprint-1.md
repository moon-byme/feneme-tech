# Conferência da DoD da Sprint — Sprint 1 (FT Sprint 1)

**Período:** 21/10/2026 a 29/10/2026 | **Release:** R1 | **Instrumento oficial:** planilha `Feneme_Definition_of_Done_Preenchida`, aba "DoD da Sprint" (FT-38).
**Sprint Goal:** Implementar o fluxo básico de gestão de entregas do Feneme, permitindo que Gestor e Motorista realizem login com segurança e que o Gestor cadastre, consulte e atribua entregas a motoristas.
**Papéis R1:** PO/DevOps — José Araújo Agra Neto | SM — João Paulo de Araujo | QA — Lethycia Zenaide Queiroz Melo
**Conferência dos critérios do SM:** João Paulo de Araujo, 29/10/2026. Critérios de outros papéis ficam "A verificar", com as observações levantadas pelo SM.

Legenda: Sim / Não / N/A / A verificar (pelo papel indicado).

## A. Meta e entregas da sprint

| # | Critério | Quem verifica | Resposta | Evidência / observação |
|---|---|---|---|---|
| 1 | Sprint Goal atingido (ou desvio justificado) | PO | A verificar | As 5 US do goal (FT-43, FT-54, FT-44, FT-55, FT-45) estão Done, com testes de API passando (38/38 em 29/10/2026). |
| 2 | US concluídas atendem à DoD de US | QA | A verificar | FT-43, FT-44, FT-45 e FT-55 estão Done com a DoD da US desmarcada; FT-54 está parcialmente marcada. Ver Q-15 (FT-83). |
| 3 | Itens não concluídos voltaram ao backlog com pendência registrada | PO | A verificar | Fazer no encerramento da sprint (drivers e tasks Q ainda In Progress). |
| 4 | Incremento demonstrado ao PO na Sprint Review | SM | Não (pendente) | Review ainda não registrada. Ata em `ata-review.md`, a preencher na reunião. |
| 5 | Aceite ou rejeição de cada US registrado | PO | A verificar | Nenhuma das 5 US tem aceite do PO registrado na issue. |

## B. Qualidade e integração

| # | Critério | Quem verifica | Resposta | Evidência / observação |
|---|---|---|---|---|
| 6 | CI verde na main ao fim da sprint | DevOps | A verificar | Todos os runs do GitHub Actions da sprint terminaram com sucesso. Último run na main (b962926, PR #5): https://github.com/moon-byme/feneme-tech/actions/runs/40959484596 |
| 7 | Bugs da sprint registrados com evidência e severidade | QA | A verificar | Nenhuma issue do tipo Bug no projeto. |
| 8 | Nenhum bug crítico/alto sem plano | QA | A verificar | Sem bugs registrados. |
| 9 | Regressão dos itens afetados executada | QA | A verificar | Suíte completa do backend executada em 29/10/2026 na main b962926 (após o PR #5): 52/52 OK. |

## C. Gestão e cerimônias

| # | Critério | Quem verifica | Resposta | Evidência / observação |
|---|---|---|---|---|
| 10 | Board do Jira atualizado (status, responsável, SP, sprint, vínculos) | SM | Sim | Todas as 23 issues da FT Sprint 1 têm responsável, story points e sprint. Links de PR e evidências foram adicionados às 5 US, FT-30 e FT-61 em 29/10/2026. |
| 11 | Sprint Planning realizada, com plano e Sprint Goal | SM | Sim, parcial | O Sprint Goal e o escopo estão registrados na FT Sprint 1 (início em 21/10/2026). Não há ata da Planning no repositório. |
| 12 | Ata da Review em docs/sprints/ | SM | Não (pendente) | Modelo criado em `docs/sprints/sprint-1/ata-review.md`; preencher na Review. |
| 13 | Ata da Retrospectiva em docs/sprints/, com ações, responsáveis e prazos | SM | Não (pendente) | Modelo criado em `docs/sprints/sprint-1/ata-retrospectiva.md`; preencher na Retro. |
| 14 | Ações da retrospectiva anterior acompanhadas | SM | Não | Não há ata da retrospectiva da Sprint 0 no repositório nem no Jira. |
| 15 | Impedimentos registrados com status e resolução | SM | Sim (registrado agora) | I-01 e I-02 registrados em `metricas-e-impedimentos.md`. I-01: código commitado direto na main e removido em 26/10 (de2b3d9, c48007d), reintegrado pelo PR #1 em 27/10. |

## D. Métricas e planejamento

| # | Critério | Quem verifica | Resposta | Evidência / observação |
|---|---|---|---|---|
| 16 | Métricas da sprint registradas (burndown e velocity) | SM | Sim, parcial | Velocity calculada em `metricas-e-impedimentos.md` (15 SP de US). Falta anexar a captura do burndown do Jira (Reports → Burndown) no fechamento. |
| 17 | Backlog repriorizado pelo PO | PO | A verificar | FT-53 (validar priorização das 13 US) ainda In Progress. |
| 18 | Planilha de riscos atualizada | SM | Sim, parcial | R02 (FT-61) reavaliado no Jira: índice 15 → 10. Falta copiar o valor para a planilha de riscos. |
| 19 | Itens da próxima sprint com critérios de aceite e estimativa (DoR) | PO | A verificar | — |

## Critérios adicionais da equipe

| # | Critério | Quem verifica | Resposta | Evidência / observação |
|---|---|---|---|---|
| 20 | Permissões Gestor/Motorista respeitadas | QA | A verificar | accounts.tests: Motorista recebe 403 em 5 operações do Gestor; acesso cruzado bloqueado. |
| 21 | Funcionalidades verificadas, sem falhas críticas conhecidas | QA | A verificar | 52/52 testes OK na main b962926; nenhum bug registrado. |
| 22 | Falhas da Open-Meteo tratadas | QA | N/A | Integração com a Open-Meteo prevista para a R2. |
| 23 | Status e histórico persistidos | QA | N/A | Atualização de status de entrega prevista para a R2. |

**Indicador parcial (somente critérios do SM: 4, 10, 11, 12, 13, 14, 15, 16, 18):** Sim = 5 (10, 11, 15, 16, 18; três deles parciais) | Não = 4 (4, 12, 13, 14) → 5 ÷ 9 = **56%** antes da Review e da Retrospectiva. Se as duas reuniões acontecerem e as atas 12 e 13 forem preenchidas, os critérios 4, 12 e 13 passam a Sim e o resultado sobe para 8 ÷ 9 = **89%**.

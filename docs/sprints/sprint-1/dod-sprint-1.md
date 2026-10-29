# Conferência da Definition of Done — Sprint 1

**Sprint:** FT Sprint 1  
**Período:** 21/10/2026 a 29/10/2026 | **Release:** R1  
**Instrumento:** planilha `Feneme_Definition_of_Done_Preenchida`, aba "DoD da Sprint" (FT-38).  
**Sprint Goal:** Implementar o fluxo básico de gestão de entregas do Feneme, permitindo que Gestor e Motorista realizem login com segurança e que o Gestor cadastre, consulte e atribua entregas a motoristas.  
**Papéis:** PO/DevOps — José Araújo Agra Neto | SM — João Paulo de Araujo | QA — Lethycia Zenaide Queiroz Melo  
**Registro da conferência:** 29/10/2026, conduzida pelo SM, com consolidação das evidências disponíveis no Jira e no GitHub.

**Resultado da conferência:** os critérios foram analisados considerando as evidências disponíveis no encerramento da Sprint 1. Quando a verificação dependia de confirmação específica do PO, QA ou DevOps e não havia evidência registrada, o item permaneceu como "A verificar".

Legenda: **Sim** = atendido com evidência; **Não** = não atendido; **N/A** = não aplicável à sprint; **A verificar** = depende de validação do papel responsável.

## A. Meta e entregas da sprint

| # | Critério | Quem verifica | Resultado | Evidência / registro da reunião |
|---|---|---|---|---|
| 1 | Sprint Goal atingido (ou desvio justificado) | PO | A verificar | As cinco US relacionadas ao objetivo (FT-43, FT-54, FT-44, FT-55 e FT-45) estavam em Done e a suíte de testes de API apresentou 38/38 testes aprovados na verificação registrada. O PO deve formalizar o aceite do objetivo. |
| 2 | US concluídas atendem à DoD de US | QA | A verificar | FT-43, FT-44, FT-45 e FT-55 estavam em Done com itens da DoD da US desmarcados; FT-54 estava parcialmente preenchida. A QA ficou responsável pela conferência final. Ver Q-15 (FT-83). |
| 3 | Itens não concluídos voltaram ao backlog com pendência registrada | PO | N/A | No estado final do Jira, as 23 issues (64 SP) estavam em Done. Não houve itens não concluídos a retornar ao Product Backlog. |
| 4 | Incremento demonstrado ao PO na Sprint Review | SM | Sim | O incremento da versão `7960995` foi apresentado na Sprint Review de 29/10/2026, contemplando os cinco fluxos previstos no Sprint Goal. |
| 5 | Aceite ou rejeição de cada US registrado | PO | A verificar | Na Review, as cinco US foram avaliadas funcionalmente. O aceite formal individual deve constar nos comentários das respectivas issues; a evidência disponível não comprova esses registros. |

## B. Qualidade e integração

| # | Critério | Quem verifica | Resultado | Evidência / registro da reunião |
|---|---|---|---|---|
| 6 | CI verde na main ao fim da sprint | DevOps | A verificar | As execuções do GitHub Actions consultadas terminaram com sucesso. Último run identificado na main `7960995`, PR #7: [GitHub Actions — run 40965591244](https://github.com/moon-byme/feneme-tech/actions/runs/40965591244). |
| 7 | Bugs da sprint registrados com evidência e severidade | QA | Sim | Não havia issues classificadas como Bug no projeto na consulta de encerramento. |
| 8 | Nenhum bug crítico/alto sem plano | QA | Sim | Não foram identificados bugs críticos ou altos registrados sem tratamento. A conclusão considera os bugs cadastrados no Jira. |
| 9 | Regressão dos itens afetados executada | QA | A verificar | A suíte completa do backend foi executada em 29/10/2026 na main `7960995`, após o PR #7, com 102/102 testes aprovados. A QA deve confirmar se a execução cobre todos os itens afetados. |

## C. Gestão e cerimônias

| # | Critério | Quem verifica | Resultado | Evidência / registro da reunião |
|---|---|---|---|---|
| 10 | Board do Jira atualizado (status, responsável, SP, sprint e vínculos) | SM | Sim | As 23 issues da FT Sprint 1 possuíam responsável, story points e sprint. Links de PR e evidências foram adicionados às cinco US, FT-30 e FT-61 em 29/10/2026. |
| 11 | Sprint Planning realizada, com plano e Sprint Goal | SM | Sim, parcialmente documentado | O Sprint Goal e o escopo estão registrados na FT Sprint 1, iniciada em 21/10/2026. Não foi localizada ata específica da Planning no repositório. |
| 12 | Ata da Review em `docs/sprints/` | SM | Sim | A Review foi registrada em `ata-review.md`, com incremento apresentado, métricas, avaliação do Sprint Goal e pendências identificadas. |
| 13 | Ata da Retrospectiva em `docs/sprints/`, com ações, responsáveis e prazos | SM | Sim | A retrospectiva foi registrada em `ata-retrospectiva.md`, contendo pontos positivos, oportunidades de melhoria e sete ações com responsáveis, prazos e formas de verificação. |
| 14 | Ações da retrospectiva anterior acompanhadas | SM | Não | Não foi localizada ata da retrospectiva da Sprint 0 no repositório ou no Jira; portanto, não havia ações anteriores documentadas para acompanhamento. |
| 15 | Impedimentos registrados com status e resolução | SM | Sim | I-01, I-02 e I-03 estão registrados em `metricas-e-impedimentos.md`. I-01 foi resolvido com a reintegração do código pelo PR #1 em 27/10; I-02 foi resolvido com a atualização das instruções de execução; I-03 permanece aberto. |

## D. Métricas e planejamento

| # | Critério | Quem verifica | Resultado | Evidência / registro da reunião |
|---|---|---|---|---|
| 16 | Métricas da sprint registradas (burndown e velocity) | SM | Sim | `metricas-e-impedimentos.md` apresenta burndown diário e velocity final de 64 SP (100% dos 64 SP comprometidos; 23/23 issues concluídas). |
| 17 | Backlog repriorizado pelo PO | PO | A verificar | A FT-53 consta como Done no estado final do Jira; a priorização registrada deverá ser considerada pelo PO na preparação da Sprint 2. |
| 18 | Planilha de riscos atualizada | SM | Sim | O risco R02 (FT-61) foi reavaliado de 15 para 10 e registrado no Jira e na planilha, aba Riscos, linha 9, em 29/10/2026. |
| 19 | Itens da próxima sprint com critérios de aceite e estimativa (DoR) | PO | A verificar | A velocity final foi de 64 SP, mas o compromisso da Sprint 2 deverá ser definido conforme a disponibilidade real da equipe e a prontidão dos itens, sem assumir repetição automática desse volume. A validação individual dos itens permanece com o PO. |

## Critérios adicionais da equipe

| # | Critério | Quem verifica | Resultado | Evidência / registro da reunião |
|---|---|---|---|---|
| 20 | Permissões Gestor/Motorista respeitadas | QA | A verificar | Os testes em `accounts.tests` indicam respostas 403 para o Motorista em cinco operações exclusivas do Gestor e bloqueio de acesso cruzado. A QA deve confirmar a validação final. |
| 21 | Funcionalidades verificadas, sem falhas críticas conhecidas | QA | A verificar | A suíte executada na main `7960995` apresentou 102/102 testes aprovados e não havia bugs registrados. A aprovação final da QA ainda precisa ser formalizada. |
| 22 | Falhas da Open-Meteo tratadas | QA | N/A | A integração com a Open-Meteo está prevista para a Release 2. |
| 23 | Status e histórico persistidos | QA | N/A | A atualização de status e o histórico de entregas estão previstos para a Release 2. |

## Conclusão da conferência

A equipe identificou que o objetivo funcional da Sprint 1 foi implementado, mas que a conclusão das histórias não deve ser confundida com o atendimento integral da DoD. Permaneceram pontos de atenção relacionados à revisão de código, à conferência dos critérios de qualidade e ao registro formal do aceite do PO.

Entre os critérios sob responsabilidade direta do SM (4, 10, 11, 12, 13, 14, 15, 16 e 18), oito foram considerados atendidos e um não atendido (critério 14), resultando em **8/9 = 89%**. O critério 11 foi considerado parcialmente documentado, mas registrado como atendido quanto à realização e ao planejamento identificável da sprint.

**Encaminhamento:** o SM manterá o acompanhamento das pendências no Jira; QA e PO deverão concluir as verificações atribuídas aos seus papéis antes de considerar as histórias integralmente conformes à DoD.

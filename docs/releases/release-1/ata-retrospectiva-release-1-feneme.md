# FENEME — Ata da Retrospectiva da Release 1

**Projeto:** Feneme — Gestão Inteligente de Transporte de Alimentos  
**Cerimônia:** Retrospectiva da Release 1 (R1)  
**Data da reunião:** 03 de novembro de 2026 (terça-feira)  
**Horário de início:** aproximadamente 17h (horário de Brasília)  
**Horário de término:** 18h (horário de Brasília)  
**Modalidade:** reunião remota por mensagens em chat 
**Participantes:** 
- José Araújo Agra Neto — Product Owner (PO) / DevOps na Release 1;
- João Paulo de Araujo — Scrum Master (SM) na Release 1;
- Lethycia Zenaide Queiroz Melo — Quality Assurance (QA) na Release 1.

> **Sobre a origem deste registro.** Conforme relato da equipe, ocorreu uma retrospectiva da Release 1 em 03/11/2026, com início por volta das 17h, por chat. Esta ata foi escrita **em 10/11/2026**, com base nesse relato, no documento *Feedback da Release 1 — G06 — Feneme* e nas tarefas de melhoria depois registradas no Jira. **Não é transcrição do chat.** 

## 1. Objetivo da retrospectiva

Analisar o feedback recebido sobre a Release 1, identificar problemas no processo de desenvolvimento e de gestão da equipe, levantar lições aprendidas e organizar ações de melhoria para a Release 2, distribuindo o acompanhamento conforme os papéis assumidos na nova release.

Este encontro de retrospectiva, relatado como iniciado **às 17h de 03/11**, é **distinto da Sprint Planning 2**, registrada posteriormente no mesmo dia, das **19h às 22h**, via WhatsApp.

## 2. Pauta reconstruída a partir do feedback e do encaminhamento das tarefas

1. Leitura e discussão das observações sobre a Release 1.
2. Identificação de pendências de Scrum, documentação, critérios de aceite, testes e riscos.
3. Discussão do processo de revisão de Pull Requests e integração contínua.
4. Definição de medidas corretivas e de responsáveis por papel na Release 2.
5. Organização das atividades no Jira para as Sprints 2 e 3.

## 3. Avaliação da Release 1

### 3.1. Lições identificadas

- Atualizar o Jira durante a sprint e registrar impedimentos assim que surgirem.
- Exigir revisão por outro integrante antes de integrar alterações à `main`.
- Distinguir implementação funcional de conclusão comprovada pela Definition of Done (DoD).
- Registrar testes executados, resultados de CI e decisões de aceite com evidências.
- Revisar os nove riscos e apresentar métricas verificáveis ao final de cada sprint.
- Documentar cerimônias e decisões com datas reais, sem reconstruir registros como se tivessem sido escritos anteriormente.

## 4. Ações corretivas encaminhadas para a Release 2

O feedback foi utilizado como referência para distribuir as ações entre os papéis **da Release 2**, diferentes dos da R1. Os vínculos abaixo refletem o planejamento registrado posteriormente no Jira e não afirmam que os números das issues tenham sido definidos literalmente durante a conversa das 17h.

| Papel na R2 | Responsável | Ações de melhoria e acompanhamento | Rastreabilidade no Jira |
| --- | --- | --- | --- |
| **Scrum Master** | Lethycia Zenaide Queiroz Melo | Organizar calendário e acordos, documentar Planning/Review/Retrospectiva, acompanhar impedimentos (inclusive I-03), burndown/velocity e revisão dos riscos R01–R09. | [FT-87](https://feneme.atlassian.net/browse/FT-87) — Sprint 2; [FT-90](https://feneme.atlassian.net/browse/FT-90) — Sprint 3 |
| **QA** | José Araújo Agra Neto | Preparar e executar `.feature` com Cucumber/Cypress, definir cenários `@smoke`, registrar defeitos e medições, conferir DoD das histórias e elaborar relatório de qualidade. | [FT-88](https://feneme.atlassian.net/browse/FT-88) — Sprint 2; [FT-91](https://feneme.atlassian.net/browse/FT-91) — Sprint 3 |
| **PO / DevOps** | João Paulo de Araujo | Validar prioridades, Sprint Goals e critérios de aceite; registrar decisões nas issues; proteger a `main`, exigir aprovação de PRs, integrar CI e publicar relatório de pipeline, tag e release notes. | [FT-89](https://feneme.atlassian.net/browse/FT-89) — Sprint 2; [FT-92](https://feneme.atlassian.net/browse/FT-92) — Sprint 3 |

**Nota sobre os papéis:** na Release 1, conforme o feedback, José Araújo foi PO/DevOps, João Paulo foi Scrum Master e Lethycia foi QA. A distribuição na tabela é a da **Release 2**.

## 5. Encaminhamentos e critérios para acompanhar a melhoria

| Encaminhamento | Como verificar nas próximas sprints |
| --- | --- |
| Documentar cerimônias e acordos de trabalho | Atas com data, horário, pauta, participantes, decisões e responsáveis; documentos versionados e vinculados ao Jira. |
| Revisar o processo de integração | PRs com aprovação de outro integrante antes do merge e checagens obrigatórias de CI. |
| Acompanhar riscos e impedimentos | Situação explícita de I-03 e de cada risco R01–R09, com evidências e ações pendentes. |
| Fortalecer a DoD e o aceite | Histórias com testes, revisão e aceite do PO/QA comprovados ou ressalvas documentadas. |
| Melhorar transparência dos resultados | Burndown, velocity, relatório de qualidade e relatório do pipeline com dados reais e limitações declaradas. |

## 6. Evidências produzidas depois da retrospectiva

Os itens a seguir demonstram **desdobramentos posteriores**; não significam que os documentos ou PRs já existiam durante a reunião de 03/11:

- [PR #14 — Documentação inicial da Sprint 2](https://github.com/moon-byme/feneme-tech/pull/14): ata da Planning, calendário e acordos de trabalho; integrado à `main` após aprovação.
- [PR #21 — Organização documental das Sprints 0 e 1](https://github.com/moon-byme/feneme-tech/pull/21): organização de atas e registros retrospectivos, integrado à `main` em 10/11.
- [FT-87](https://feneme.atlassian.net/browse/FT-87), [FT-88](https://feneme.atlassian.net/browse/FT-88) e [FT-89](https://feneme.atlassian.net/browse/FT-89): acompanhamento das ações da Sprint 2.
- [FT-90](https://feneme.atlassian.net/browse/FT-90), [FT-91](https://feneme.atlassian.net/browse/FT-91) e [FT-92](https://feneme.atlassian.net/browse/FT-92): continuidade e fechamento da Release 2 na Sprint 3.

## 7. Conclusão da retrospectiva

A retrospectiva relatada de 03/11/2026 permitiu à equipe discutir os problemas encontrados na Release 1 e orientar um plano de melhoria para a Release 2. O resultado documentável é o **encaminhamento de ações por papel**, com tarefas de acompanhamento e critérios de verificação posteriores. A efetividade dessas ações será avaliada com as evidências produzidas durante as Sprints 2 e 3.
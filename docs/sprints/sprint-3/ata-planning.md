# Feneme — Registro de preparação e encaminhamentos da Sprint Planning 3

**Release:** R2 (término previsto em 26/11/2026)  
**Sprint:** FT Sprint 3 (17 a 26/11/2026)  
**Referência principal:** [FT-90](https://feneme.atlassian.net/browse/FT-90)  
**Data dos registros de conversa:** 16/11/2026, das 18h32 às 21h04 (trechos fornecidos pela Scrum Master)  
**Modalidade:** mensagens de WhatsApp, acompanhadas de decisões já registradas no Jira  
**Natureza:** consolidação documental posterior dos registros disponíveis; **não é transcrição de uma Planning integral nem comprovação de aprovação coletiva de todos os itens**.

## 1. Participantes e papéis

- Lethycia Zenaide Queiroz Melo — Scrum Master (SM).
- João Paulo de Araujo — Product Owner (PO) e DevOps.
- José Araújo Agra Neto — QA.

Os papéis constam da [FT-50](https://feneme.atlassian.net/browse/FT-50). As mensagens fornecidas mencionam a participação da SM e a consulta ao QA, mas **não permitem comprovar presença simultânea dos três em toda uma cerimônia de Planning**.

## 2. Assuntos comprovadamente tratados por mensagens em 16/11

- **18h32–18h35:** a SM solicita que as tarefas estejam com a DoR marcada antes do início da Sprint 3; outro participante pergunta se a DoR corresponde aos critérios que tornam a tarefa apta à sprint e a SM confirma.
- **20h38–20h41:** a SM compartilha planilhas de Análise de Riscos, DoD e Plano de Qualidade; solicita a José que confira Análise de Riscos e Plano de Qualidade.
- **21h04:** outro participante responde “até onde eu vi, td ok” à solicitação de conferência. Isso representa conferência informal, **não aceite completo da DoD, nem homologação de todos os riscos**.
- No Jira, o PO registra decisões de escopo em [FT-112](https://feneme.atlassian.net/browse/FT-112), incluindo lista fechada de 26 cidades, catálogo de 7 tipos de carga, configuração Google Cloud e transferência da FT-57 para Sprint 5/R3.

**Links compartilhados no chat de 16/11:**
- Análise de Riscos: https://docs.google.com/spreadsheets/d/1YE0_OJXr4QK-6S5Y6GqY0jBbmzPjwD2eB5sVUnEKKWk/edit
- DoD: https://docs.google.com/spreadsheets/d/1uvuHzqeCdq3KdlqwBdhIC62qk0n0oM2h/edit
- Plano de Qualidade: https://docs.google.com/spreadsheets/d/14Vl3nNDkXJ5_kTD8gVmLfH-a_s3OqKUxTF6WQS5CrQ4/edit

**Atenção à versão:** em [FT-90](https://feneme.atlassian.net/browse/FT-90) e [FT-50](https://feneme.atlassian.net/browse/FT-50) existem URLs diferentes, indicadas como documentos atuais em 17/11. Confirmar qual versão é oficial antes de substituir qualquer referência; não presumir equivalência de conteúdo.

## 3. Backlog, estimativas e avaliação da capacidade

Conferência do Jira em 17/11: **19 issues / 58 SP**, todas vinculadas à Sprint 3 e à R2, com responsável atribuído e status **Pronto para a sprint**. DoR assinalada nas histórias FT-48, FT-49, FT-59, FT-90, FT-91, FT-92, FT-110, FT-113 e FT-114. Checklists prévios não provam, por si, validação coletiva na Planning.

| Responsável no Jira | SP atribuídos |
| --- | ---: |
| João Paulo | 31 |
| Lethycia | 15 |
| José | 12 |
| **Total** | **58** |

Velocidade operacional de referência da Sprint 2: **36 SP em status Concluído** (11 issues), com ressalvas de DoD e aceite registradas em `docs/sprints/sprint-2/fontes/metricas-e-impedimentos.typ`. Os 58 SP da Sprint 3 representam **22 SP a mais (aproximadamente 61%)** do que esse indicador. **Capacidade efetiva não confirmada:** falta registrar disponibilidade, carga remanescente, viabilidade e eventual despriorização de itens com os três participantes; estimativas em pontos não equivalem a horas.

**Estimativas das novas US:**
- [FT-113](https://feneme.atlassian.net/browse/FT-113): **5 SP**, cadastrados e identificados como confirmados *para o planejamento* na descrição atual da história.
- [FT-114](https://feneme.atlassian.net/browse/FT-114): **3 SP**, cadastrados e identificados como confirmados *para o planejamento*.
- Ambas as descrições exigem que a ata registre a validação da equipe; **não foi fornecida evidência da votação coletiva**, portanto nenhuma votação está presumida ou fabricada.

## 4. Sequência de dependências — encaminhamento técnico registrado

**FT-48 → FT-49 → FT-59**, conforme dependências e planejamento das histórias no Jira:

1. **FT-48 — US-11 (5 SP, Lethycia):** atualizar status pelo Motorista, validar autorização e transições permitidas, persistência e eventos de histórico.
2. **FT-49 — US-12 (3 SP, João Paulo):** consultar status atual pelo Gestor. Preparação de interface/testes isolados pode ocorrer em paralelo, mas integração e aceite dependem de status persistido na FT-48.
3. **FT-59 — US-13 (3 SP, Lethycia):** consultar histórico cronológico e persistente. Preparação isolada possível; integração e aceite dependem de FT-48 e FT-49.

**Decisão de registro:** adotar essa ordem como encadeamento técnico de referência da Sprint 3. É coerente com dependências já descritas e a repriorização do PO. A ata **não atribui votação coletiva adicional não documentada**.

## 5. Sprint Goal — decisão de encaminhamento / proposta atualizada

> Concluir a Release 2 com a atualização manual de status das entregas pelo Motorista, a consulta de andamento pelo Gestor e o histórico persistente, integrados na sequência FT-48 → FT-49 → FT-59. Preparar a evolução do Feneme com uma lista única de 26 cidades, catálogo de 7 tipos de carga com fontes, configuração segura do Google Cloud e registro do risco R10, além de executar testes, regressão, validação da DoD e procedimentos de homologação e publicação da R2.

**Origem e escopo:** texto derivado do objetivo registrado para a FT Sprint 3 no Jira, atualizado conforme decisão do PO em FT-112 de 16/11. A FT-57 fica na Sprint 5/R3 e não faz parte do objetivo desta sprint.

**Status da decisão:** esta é a **redação final proposta/registrada pela SM para a ata**; a ratificação formal coletiva do compromisso permanece condicionada à conferência da capacidade. Não afirmar concordância individual dos outros integrantes sem sua manifestação.

## 6. DoD e riscos

A DoD foi enviada por link à conversa em 16/11. **Compartilhar o link é evidência de disponibilização, não comprovação suficiente da apresentação/revisão de cada critério com a equipe.** Registrar eventuais ressalvas e a versão aprovada quando confirmadas.

Análise de Riscos e Plano de Qualidade foram compartilhados; houve retorno informal favorável após solicitação ao QA. A mudança de escopo introduz **R10 — FT-116**, que precisa constar na matriz da versão oficial a ser conferida.

## 7. Situação das pendências originais da FT-90

| Pendência | Estado documental em 17/11 | Evidência |
| --- | --- | --- |
| Estimativas FT-113/FT-114 | Valores cadastrados para planejamento: 5/3 SP; **validação coletiva não demonstrada** | Histórias e observações atuais no Jira |
| Capacidade e escopo 58 SP | **Pendente de validação coletiva** | 58 SP cadastrados; 36 SP de velocity operacional anterior; distribuição desigual |
| Sequência FT-48 → FT-49 → FT-59 | **Encadeamento técnico registrado**; validação da implementação ocorrerá durante a sprint | Dependências nas três histórias e prioridade do PO |
| Sprint Goal atualizado | **Redação final de encaminhamento registrada**, dependente de ratificação do compromisso | Meta cadastrada para FT Sprint 3 e FT-112 |
| Apresentação formal da DoD | **Link compartilhado; revisão/ciência formal não comprovada** | Conversa de 16/11 |
| Ata no Jira/GitHub | **Registro documental produzido**, sujeito a revisão e aceite do time | Este arquivo e comentário de FT-90 |

## 8. Encaminhamentos para concluir a Planning sem lacunas

1. PO, SM e QA: confirmar capacidade e compromisso da Sprint 3 diante dos **58 SP** e da distribuição 31/15/12; registrar se haverá manutenção integral ou retirada de itens.
2. Equipe: registrar ciência/validação das estimativas da FT-113 (5 SP) e FT-114 (3 SP), sem atribuir votação retroativa.
3. Equipe: confirmar ciência da **versão oficial atual** da DoD e eventuais ressalvas.
4. Equipe: ratificar o objetivo já redigido e a ordem de integração FT-48 → FT-49 → FT-59.
5. SM: atualizar a FT-90 após essas confirmações; preservar este registro como evidência de preparação e não como comprovação de decisões que ainda não tenham sido tomadas.

**Rastreabilidade:** [FT-90](https://feneme.atlassian.net/browse/FT-90) · [FT-50](https://feneme.atlassian.net/browse/FT-50) · [FT-112](https://feneme.atlassian.net/browse/FT-112) · [FT-113](https://feneme.atlassian.net/browse/FT-113) · [FT-114](https://feneme.atlassian.net/browse/FT-114).

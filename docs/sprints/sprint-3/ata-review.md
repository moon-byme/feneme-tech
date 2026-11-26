# Feneme — Ata da Sprint Review 3

**Release:** R2 · **Sprint:** FT Sprint 3 (17–26/11/2026)  
**Data da reunião:** 26/11/2026, período da tarde  
**Modalidade:** Google Meet e complementação por WhatsApp  
**Participantes da equipe:** Lethycia Zenaide Queiroz Melo (SM), João Paulo de Araujo (PO/DevOps) e José Araújo Agra Neto (QA).  
**Facilitação:** Scrum Master da R2  
**Natureza do registro:** síntese elaborada em 26/11 a partir do relato da SM sobre a reunião realizada e dos registros do Jira/GitHub. Horários exatos, sequência dos canais e falas individuais não foram informados.

## 1. Pauta e objetivo

Revisar o incremento da Sprint 3 e o Sprint Goal, conferir os aceites e evidências de qualidade, discutir os resultados operacionais, as mudanças de escopo e os encaminhamentos para a R3.

O objetivo definido na [Planning 3](feneme_sprint_planning_3.typ) era concluir o fluxo de atualização, consulta e histórico de status, preparar as rotas automáticas por meio da lista de cidades e catálogo de cargas e concluir testes, homologação e publicação da R2.

## 2. Incremento e decisões de aceite

A SM confirmou a realização dos pontos da pauta de Review e alinhamento, exceto a revisão dos riscos. A tabela consolida as decisões já registradas pelo PO em [aceite-po-sprint-3.md](../../releases/release-2/aceite-po-sprint-3.md), as condições técnicas posteriormente satisfeitas e o encaminhamento informado pela SM. Não constitui transcrição de demonstração, votação ou novo teste.

| Item | Resultado / encaminhamento | Evidência |
| --- | --- | --- |
| FT-48 — atualização de status | Aceite registrado pelo PO; concluída | PR #41; Q-12 20/20 |
| FT-49 — consulta de andamento | Aceite registrado pelo PO; concluída | PR #42 integrada à feature, conteúdo na main pela #43 |
| FT-59 — histórico de entregas | Aceite registrado pelo PO; concluída | PR #43 e regressão #51 |
| FT-113 — lista de 26 cidades | Condição de merge atendida; aceite PO registrado | PR #47, FT-113/10252 |
| FT-114 — catálogo de 7 cargas | Aceite PO e validação manual QA concluídos | PR #44, [QA FT-114/10325](https://feneme.atlassian.net/browse/FT-114?focusedCommentId=10325), PR #58 |
| FT-110 — homologação | Condição de deploy satisfeita; Concluído no Jira | CI #351, #375 e #394; PR #55; [ambiente](https://feneme-homologacao.onrender.com) |
| FT-115/FT-116 — Google Cloud e R10 | Trabalho remanescente na Sprint 4/R3 | Decisão PO de 25/11, issues atualizadas |
| FT-57 — comparação térmica | Fora da R2; Sprint 5/R3 | FT-112 |

**Avaliação do Sprint Goal:** parte funcional atingida (status, consulta, histórico, cidades e catálogo); preparação Google Cloud parcialmente atendida, com carryover acordado. Publicação formal da versão depende do fechamento de QA/DevOps e da escolha do commit final. O aceite funcional não significa que todos os critérios de processo estejam encerrados.

## 3. Métricas e qualidade discutidas

| Indicador | Recorte verificável |
| --- | --- |
| Compromisso inicial S3 | 19 issues / 58 SP |
| Escopo atual S3 | 15 issues / 48 SP |
| Concluído por status em 26/11 | 12 issues / 38 SP (79,2%) |
| Em andamento | FT-90/91/92, 3 issues / 10 SP |
| Cinco histórias funcionais S3 | 19 SP |
| S2 | 11 issues / 36 SP por status; 12 SP funcionais |
| Regressão R1 | 10/10 cenários |
| Regressão R2 | 29/29 cenários; relatório QA registra 30 CT únicos acumulados, incluindo CT-32 por backend |
| Q-04 | 19/19 aprovações externas anteriores ao merge nas PRs #39–#57; recorte S3, não agregado final R2 |
| Q-05 / Q-12 / Q-13 | 20/20 bloqueios de acesso cruzado; 20/20 alterações persistidas; 10/10 falhas simuladas tratadas |
| Q-15 | 9/9 US rastreáveis na R2 |
| Q-09 | 43/45 (95,6%) na main até CI #375; atualizar após novas execuções |

O [CI #394](https://github.com/moon-byme/feneme-tech/actions/runs/45849612416) foi consultado após o recorte e está concluído com sucesso. Não é prova de seleção da tag final. As métricas por status devem ser reconciliadas com a DoD e os gráficos nativos antes de publicar a velocity final. A variação líquida de escopo foi de -10 SP; o compromisso inicial era superior à referência de 36 SP da S2.

## 4. Decisões e continuidade

- Manter a sequência FT-115/116 antes de FT-118; FT-117 → FT-118 → FT-120, com FT-119 coordenada com a substituição dos trajetos manuais.
- Manter FT-57 e FT-122 na Sprint 5.
- Confirmar as estimativas e a capacidade na Planning 4; preservar as prioridades e dependências documentadas na FT-112.
- A equipe tratou os tópicos de retrospectiva e avaliação individual, registrados na [ata da retrospectiva R2](../../releases/release-2/ata-retrospectiva-release-2-feneme.md).
- A revisão coletiva dos riscos R01–R10 não foi realizada durante a reunião: foi delegada a José Neto e João Paulo, que deverão registrar o resultado na FT-8 e na planilha oficial. Não declarar riscos revistos sem a evidência correspondente.

## 5. Fechamento

A Review foi realizada conforme relato da SM. O horário exato e eventuais ressalvas individuais adicionais ficam a conferir pelos participantes na revisão do documento. Permanecem abertas as ações de fechamento FT-90 (SM), FT-91 (QA) e FT-92 (PO/DevOps), bem como a atualização das planilhas e publicação da R2.

**Referências:** [FT-90](https://feneme.atlassian.net/browse/FT-90) · [FT-91](https://feneme.atlassian.net/browse/FT-91) · [FT-92](https://feneme.atlassian.net/browse/FT-92) · [FT-112](https://feneme.atlassian.net/browse/FT-112) · [relatório QA R2](../../qa/sprint-3-relatorio-parcial-r2.md) · [métricas S3](metricas-e-impedimentos.md).

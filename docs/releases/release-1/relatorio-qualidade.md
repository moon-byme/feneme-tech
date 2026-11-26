# Relatório de qualidade — Release 1

**Projeto:** Feneme — Gestão Inteligente de Transporte de Alimentos  
**Período avaliado:** 06/10 a 29/10/2026 (Sprints 0 e 1)  
**Versão:** v1.0.0 (tag de 29/10; GitHub Release publicada em 03/11)  
**Elaboração:** 26/11/2026 — consolidação documental retrospectiva  
**QA da R1:** Lethycia Zenaide Queiroz Melo; **PO/DevOps da R1:** José Araújo Agra Neto; **SM da R1:** João Paulo de Araujo.  
**Rastreabilidade:** [FT-124](https://feneme.atlassian.net/browse/FT-124), [FT-9](https://feneme.atlassian.net/browse/FT-9), [FT-10](https://feneme.atlassian.net/browse/FT-10), [FT-38](https://feneme.atlassian.net/browse/FT-38).

## 1. Escopo e fontes

A R1 entregou os fluxos básicos de autenticação de Gestor e Motorista, cadastro, consulta e atribuição de entregas. O relatório atende à necessidade de consolidação de qualidade da R1 (critério 7 da DoD da Release). Utiliza o Plano de Teste Funcional v2.3 de 16/11, especialmente a matriz e o cronograma da Sprint 1, o relatório funcional da FT-69, logs de CI, métricas, comentários e aceites do Jira. A versão v2.3 inclui alterações posteriores ao período avaliado; não são atribuídas à R1.

Não foi realizada uma nova execução de testes para elaborar este documento. Medições e complementações posteriores são identificadas pela data e não substituem os registros históricos.

## 2. Testes funcionais planejados e resultados

| História | Casos previstos na matriz | Resultado histórico informado em 29/10 | Evidência |
|---|---|---|---|
| US-01 / FT-43 — Login Gestor | CT-01, CT-02 | Aprovados | [FT-43](https://feneme.atlassian.net/browse/FT-43) |
| US-02 / FT-54 — Login Motorista | CT-13, CT-14 | Aprovados | [FT-54](https://feneme.atlassian.net/browse/FT-54) |
| US-03 / FT-44 — Cadastro | CT-03, CT-04 | Aprovados | [FT-44](https://feneme.atlassian.net/browse/FT-44) |
| US-04 / FT-55 — Consulta | CT-15, CT-16 | Aprovados no relatório funcional; ressalva original sobre estado vazio | [FT-55](https://feneme.atlassian.net/browse/FT-55) |
| US-05 / FT-45 — Atribuição | CT-05, CT-17 | Aprovados no relatório funcional; ressalva original sobre motorista inexistente | [FT-45](https://feneme.atlassian.net/browse/FT-45) |

| Recorte | Planejados | Executados | Aprovados | Reprovados | Bloqueados |
|---|---:|---:|---:|---:|---|
| Q-01 original R1 (CT-01 a CT-05) | 5 | 5 | 5 | 0 | Nenhum relatado |
| Controle ampliado (CT-01 a CT-05 e CT-13 a CT-17) | 10 | 10 | 10 | 0 | Nenhum relatado |

Os dois recortes se sobrepõem; não devem ser somados. O controle ampliado é provisório para fins da métrica Q-01 enquanto não houver ratificação do universo pelo PO/QA. O relatório da FT-69 registra 33 métodos de API aprovados, 11 verificações de interface automatizadas e build aprovado; são unidades de verificação diferentes da quantidade de CT.

**Evidências:** [relatório funcional FT-69 (PDF)](../../../evidencias/FT69/relatorio-consolidado.pdf), [resultados por CT](../../../evidencias/FT69/resultados-consolidados.json), [manifesto de procedência](../../../evidencias/FT69/manifesto-evidencias.json), [FT-69](https://feneme.atlassian.net/browse/FT-69). As transcrições preservam resultados relatados, mas os logs locais integrais e capturas originais não foram recuperados. O CI constitui evidência independente da execução automatizada.

## 3. Regressão e integração contínua

- Em 29/10, o [CI da versão demonstrada na Review](https://github.com/moon-byme/feneme-tech/actions/runs/40965591244), commit `7960995`, registrou **102 testes de backend aprovados**. O [log do job](https://github.com/moon-byme/feneme-tech/actions/runs/40965591244/job/123769190731) registra `Ran 102 tests` e `OK` às 19h25min16s (UTC−3). A execução terminou às 19h25min20s, anterior ao aceite do PO na [FT-43](https://feneme.atlassian.net/browse/FT-43?focusedCommentId=10035), registrado às 20h19. A [ata da Review](../../sprints/sprint-1/ata-review.md) identifica essa versão e o resultado como evidência apresentada. Não registra o horário exato de início da demonstração; portanto, a anterioridade ao início não é comprovada por relógio.
- O [CI final da R1](https://github.com/moon-byme/feneme-tech/actions/runs/40990301407) registra **103 testes de backend aprovados**, com build do frontend aprovado. Não havia script de testes frontend configurado nem regressão E2E no CI da R1.
- A regressão de 10/10 cenários R1 em Cypress consta do Plano de Teste v2.3 como resultado da **Sprint 2**, não como execução anterior à apresentação da R1.
- [Relatório do pipeline R1](relatorio-pipeline.md): 51/51 execuções bem-sucedidas, das quais 21 na main (duas execuções iniciais sem jobs de backend/frontend por ausência de componentes).

## 4. Indicadores de qualidade aplicáveis à R1

| Indicador | Resultado | Meta / avaliação | Evidência e recorte |
|---|---|---|---|
| Q-01 — Execução dos CT | 5/5 = 100%; controle ampliado 10/10 provisório | Meta 100%; resultado relatado, formalização do universo pendente | [FT-69](https://feneme.atlassian.net/browse/FT-69) |
| Q-02 — Bugs críticos/altos sem tratamento | 0 registrados | Meta 0, atendida no universo cadastrado | [FT-70](https://feneme.atlassian.net/browse/FT-70) |
| Q-03 — Gherkin verificável | 5/5 = 100% | Meta 100%; conferência documental de 25/11 | [FT-71](https://feneme.atlassian.net/browse/FT-71), [conferência PO/DevOps](conferencia-po-devops-r1.md) |
| Q-04 — Revisão de código | 10/10 = 100% pela métrica vigente na FT-72, em 25/11 | Meta 100% na conferência atual; histórico de outubro sob critério original preservado | [FT-72](https://feneme.atlassian.net/browse/FT-72) |
| Q-05 — Bloqueio de acesso cruzado | 20/20 rejeitadas; 0 alterações indevidas | Meta 100% e 0 alterações | [FT-73](https://feneme.atlassian.net/browse/FT-73), [FT-29](https://feneme.atlassian.net/browse/FT-29), [PR #7](https://github.com/moon-byme/feneme-tech/pull/7) |
| Q-08 — Cobertura de linhas do backend | 84% | Meta proposta ≥70%; medição retrospectiva na tag v1.0.0 em 25/11, não medida originalmente | [FT-76](https://feneme.atlassian.net/browse/FT-76), [conferência PO/DevOps](conferencia-po-devops-r1.md) |
| Q-09 — Estabilidade da main | 21/21 = 100% | Meta proposta ≥90%; sucesso do workflow não equivale a todos os jobs executados | [FT-77](https://feneme.atlassian.net/browse/FT-77), [relatório pipeline](relatorio-pipeline.md) |
| Q-10 — Rejeição de credenciais/sessões inválidas | 20/20 = 100%; 0 acessos indevidos | Meta 100% nos 20 casos previstos | [FT-78](https://feneme.atlassian.net/browse/FT-78), [FT-30](https://feneme.atlassian.net/browse/FT-30), [PR #4](https://github.com/moon-byme/feneme-tech/pull/4) |
| Q-15 — Rastreabilidade | 5/5 = 100% após organização dos vínculos em 29/10 | Meta 100%; mede vínculos, não cobertura integral | [FT-83](https://feneme.atlassian.net/browse/FT-83) |

Os indicadores Q-06, Q-07 e Q-11 a Q-14 têm verificações previstas em ciclos posteriores no planejamento; este relatório não atribui resultados posteriores à R1. Q-16 foi proposto em 16/11. A métrica Q-04 atual da FT-72 deve ser reconciliada com os documentos oficiais que ainda reproduzam sua redação anterior. Os resultados retrospectivos devem constar na planilha com data, universo e fonte.

## 5. Defeitos, desvios e tratamento

A [FT-70](https://feneme.atlassian.net/browse/FT-70) registra zero issues do tipo Bug no período histórico da R1; consequentemente, zero bugs críticos/altos cadastrados em aberto sem tratamento. Isso não significa ausência absoluta de defeitos nem comprova zero defeitos informais.

| Achado | Tratamento / situação |
|---|---|
| I-01 — integração e recuperação da main | Reintegração do código pelo PR #1; resolvido conforme métricas da S1. |
| I-02 — mudança de ambiente local | PR #3 e instruções de execução atualizadas; resolvido conforme métricas. |
| I-03 — não conformidade histórica do fluxo de revisão | Encaminhado à R2; consultar FT-72 e retrospectiva da S1. |
| FT-55 — estado vazio | Teste de API presente na tag; cobertura de interface complementada posteriormente. Aceite vigente sem ressalvas em 25/11 ([PO](https://feneme.atlassian.net/browse/FT-55?focusedCommentId=10293)). |
| FT-45 — motorista inexistente | Teste complementar de rejeição e preservação do vínculo integrado na [PR #50](https://github.com/moon-byme/feneme-tech/pull/50); [CI](https://github.com/moon-byme/feneme-tech/actions/runs/45722858113) aprovado. Aceite vigente sem ressalvas em 25/11 ([PO](https://feneme.atlassian.net/browse/FT-45?focusedCommentId=10294)). |
| R01 — acesso cruzado | Tratamento técnico evidenciado; índice residual proposto 10, aguardando decisão da equipe ([FT-60](https://feneme.atlassian.net/browse/FT-60?focusedCommentId=10263)). |
| R02 — autenticação inválida | Residual 10 registrado em 29/10 ([FT-61](https://feneme.atlassian.net/browse/FT-61)). |

## 6. Conclusão e encaminhamentos

As cinco histórias funcionais foram demonstradas e têm aceites individuais registrados. A documentação atual das DoDs individuais foi consolidada em 25/11; as ressalvas funcionais da FT-45 e FT-55 receberam novos aceites. A R1 apresenta evidências positivas de regressão de backend, execução funcional reportada e rastreabilidade. O resultado não implica que todos os critérios da DoD estivessem atendidos no encerramento original.

Este relatório reúne o registro de casos, bugs/desvios, indicadores, regressão e limitações requerido pelo critério 7 da DoD da Release. Para finalizar a conferência, vincular o relatório à planilha após revisão e integração, confirmar o universo Q-01 e os lançamentos das métricas, ratificar as justificativas de N/A e a decisão residual de R01. A conferência técnica independente da R2 e a avaliação docente continuam distintas.

**Referências complementares:** [auditoria de QA S1](../../qa/auditoria-sprint-1.md), [DoD S1](../../sprints/sprint-1/dod-sprint-1.md), [métricas S1](../../sprints/sprint-1/metricas-e-impedimentos.md), [retrospectiva da release](ata-retrospectiva-release-1-feneme.md), [GitHub Release v1.0.0](https://github.com/moon-byme/feneme-tech/releases/tag/v1.0.0).

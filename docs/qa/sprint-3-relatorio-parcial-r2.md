# QA — Relatório de Qualidade da Sprint 3 e Release 2

**Projeto:** Feneme — Gestão Inteligente de Transporte de Alimentos  
**Sprint:** FT Sprint 3 (17/11/2026 a 26/11/2026)  
**Responsável QA:** José Araújo Agra Neto  
**Data de consolidação:** 26/11/2026  
**Issues acompanhadas:** FT-32, FT-80, FT-81 e FT-91

> **Estado deste documento: PARECER FINAL DE QA (26/11/2026), preparado para publicação.** Consolida evidências do Jira, PRs, GitHub Actions e Plano de Testes. A Scrum Master confirmou Q-04 em 19/19 PRs da Sprint 3 (#39–#57) e Q-15 em 5/5 US da Sprint 3 e 9/9 US funcionais no agregado da R2. O QA concluiu a verificação manual da FT-114 em homologação (sete tipos, campos e links das fontes corretos). A planilha foi atualizada pelo QA; conferir nela os recortes finais de Q-04 e Q-15 indicados neste relatório. O CI #394 passou em todos os jobs, incluindo regressão e deploy. Nenhuma medição foi estimada; ressalvas e itens replanejados permanecem explicitados.

## 1. Resumo executivo

| Issue | Verificação | Resultado comprovado | Situação de QA |
|---|---|---|---|
| FT-32 | Resiliência à indisponibilidade da Open-Meteo | 10/10 falhas simuladas preservaram cadastro e comparação manual | Replanejada para FT Sprint 5/R3, junto da FT-57; critério restante será validado após sua implementação |
| FT-80 | Q-12 — Persistência de alterações de status | 20/20 alterações válidas persistidas e recuperadas (100%); Resultado R2 registrado como 1,0 na planilha | Concluída; conferência formal do PO registrada em 26/11 |
| FT-81 | Q-13 — Continuidade sem resposta da Open-Meteo | 10/10 falhas simuladas preservaram os fluxos manuais (100%); Q-13 consta na planilha | Concluída; conferência formal do PO registrada; R06 residual P4/S4 = 8 lançado na planilha e FT-65 concluída |
| FT-91 | Regressão, métricas, DoD e relatório da R2 | Q-01 30/30; Q-02 zero Bugs registrados em aberto; Q-04 19/19 na Sprint 3; Q-05 20/20; Q-15 5/5 na Sprint 3 e 9/9 na R2; regressão @R2 29/29 | Concluída no Jira; PR #58 integrada; validação manual da FT-114 aprovada; métricas confirmadas pela SM; parecer final consolidado nesta atualização |

## 2. FT-80 — Q-12: persistência de alterações de status

**Meta:** 100% de 20 mudanças válidas recuperadas com histórico correto.

**Resultado comprovado:** 20/20 (100%).

A PR [#41 — atualização manual de status (FT-48)](https://github.com/moon-byme/feneme-tech/pull/41) documenta a execução de 20 atualizações válidas em 10 entregas, recuperadas após nova autenticação JWT e consulta posterior, com 20 eventos correspondentes no histórico.

Evidências registradas na PR:
- Backend: 166/166 testes aprovados na execução local descrita na PR.
- Q-12/FT-34: 20/20 alterações persistidas e recuperadas.
- Reinício real do servidor: status e histórico recuperados após encerramento e inicialização de outro processo.
- Cypress: 5/5 cenários da US-11 e 25/25 cenários de regressão na execução local descrita.
- CI: [execução #260](https://github.com/moon-byme/feneme-tech/actions/runs/44357992089), indicada na PR como aprovada.

A PR #41 foi integrada à `main`. A implementação foi posteriormente reutilizada pela FT-59, sem nova migração.

**Atualização de fechamento (26/11):** a conferência formal do PO foi confirmada e registrada em comentário na FT-80. Q-12 está preenchida em Resultado R2 com o valor numérico `1,0` (100%); as evidências da PR #41 e do CI #260 estão vinculadas na planilha. A FT-80 foi movida para Concluído no Jira.

## 3. FT-81 — Q-13: continuidade sem resposta da Open-Meteo

**Meta:** 100% de 10 casos de falha com comparação manual preservada.

**Resultado comprovado:** 10/10 (100%) para a continuidade dos fluxos manuais.

A [PR #24 — dez falhas sem bloquear fluxos manuais](https://github.com/moon-byme/feneme-tech/pull/24) foi integrada à `main`. O teste `test_ten_external_failure_scenarios_preserve_manual_flows`, em `backend/weather/tests.py`, cobre timeout, conexão recusada, HTTP 500, 503, 429, 204, JSON inválido, previsão ausente, listas vazias e temperatura nula.

Em cada caso, verifica a resposta genérica de indisponibilidade e a continuidade do cadastro e do registro de alternativas manuais. A execução documentada confirma 10 entregas e 20 alternativas persistidas.

Evidência: [GitHub Actions — PR #24 (run 42844947365)](https://github.com/moon-byme/feneme-tech/actions/runs/42844947365). A execução documentada registrou 142 testes backend aprovados, Cypress `@R1` 10/10 e `@US-08` 2/2.

**Limitação:** os testes usam mocks. Não medem a disponibilidade real da Open-Meteo nem uma chamada externa bem-sucedida.

**Atualização de fechamento (26/11):** Q-13 está registrada em Resultado R2 com `100% de 10`. O PO confirmou a conferência formal da FT-81 e a reavaliação do risco residual R06 para P4/S4 = 8, já lançada na planilha de riscos e registrada na FT-65. A FT-81 foi movida para Concluído no Jira. Q-13 não comprova disponibilidade real do provedor.

## 4. FT-32 — DA-CON-JA-01: isolar falhas da Open-Meteo

A parte do driver relativa à continuidade dos fluxos manuais está coberta pela mesma evidência da Q-13: 10/10 falhas simuladas preservaram o cadastro e a comparação manual.

Entretanto, o critério original também menciona não confirmar recomendação climática sem dados. Essa parte não pode ser testada nesta release: a FT-57 (US-09 — comparação térmica e recomendação) foi retirada da R2 e replanejada para a Sprint 5/R3, conforme decisão registrada na FT-112.

**Resultado de QA:** atendimento parcial, restrito ao isolamento das falhas e à continuidade manual. Não declarar o driver integralmente concluído com base apenas nos 10/10 casos.

**Decisão do PO (26/11):** a FT-32 foi replanejada para a FT Sprint 5 (R3), junto da dependência FT-57. A parte já verificada (continuidade manual, Q-13 10/10) permanece registrada; a validação do critério restante — não confirmar recomendação climática sem dados — será feita após a implementação da FT-57. A justificativa foi registrada no Jira e a descrição do driver atualizada. A FT-32 não é bloqueadora do fechamento da Sprint 3/R2.

## 5. Regressão e evidências da Sprint 3

### 5.1 FT-48 — atualização manual de status

A [PR #41](https://github.com/moon-byme/feneme-tech/pull/41) foi integrada à `main`. O PO registrou aceite dos critérios da US-11. A evidência descrita inclui 5/5 cenários Cypress da US-11 e 25/25 cenários de regressão na execução local, além do CI indicado na PR.

### 5.2 FT-49 e FT-59 — acompanhamento e histórico

A [PR #43](https://github.com/moon-byme/feneme-tech/pull/43) foi integrada à `main` em 24/11/2026 (merge commit `62e52568105b68801c601d09378eac0338dd1c29`).

A descrição e a revisão aprovada registram:
- Backend: 173/173 testes aprovados.
- Build do frontend aprovado.
- Cypress smoke: 15/15 aprovados na execução descrita na PR. A auditoria posterior identificou que `status.feature` reutilizava CT-27/CT-28 para cenários de histórico, em conflito com a matriz v2.3; a correção está na PR #51. Após a correção, a regressão completa executou `historico.feature` com CT-12 e CT-26: 2/2 aprovados no CI #45731598047.
- Regressão `@US-07`: 3/3; `@R1`: 10/10; `@US-08`: 2/2.
- Cobertura do histórico cronológico, estado vazio, nova autenticação, autorização e respostas 401/403/404.

A revisão aprovada disponível é do PO (`jpauloaraujo`). O aceite do PO está registrado, mas a revisão independente de QA deve ser registrada separadamente; a aprovação do PO não substitui a validação do QA.

**Limitação de evidência:** os resultados acima são os informados na PR e no CI associado ao commit `f80e290`; não foi realizada uma execução local independente pelo QA nesta consolidação.


### 5.3 FT-114 — US-15: catálogo de tipos de carga

A [PR #44](https://github.com/moon-byme/feneme-tech/pull/44) foi integrada à `main` em 25/11/2026 às 14:58 UTC (merge commit `04f3b8e9ba992e1cb522d987706c6fd5c81b28ed`).

A entrega inclui:
- Catálogo somente leitura com sete tipos de carga, categoria, limite em °C, referência e fonte.
- Endpoint autenticado `GET /api/tipos-carga/`; tentativas de criação, edição e exclusão retornam 405; acesso anônimo retorna 401.
- Painel do catálogo no frontend.
- Testes de backend para os sete registros, limites/fontes, autenticação e permissões; cenário Cypress CT-31 para apresentação dos sete itens e identificação do limite derivado.

**Evidência de CI:** [execução da PR #44](https://github.com/moon-byme/feneme-tech/actions/runs/45637482487) e [execução pós-merge na main](https://github.com/moon-byme/feneme-tech/actions/runs/45639919854). Na execução pós-merge, os quatro jobs — detecção de componentes, testes Django, build/testes do frontend e E2E Cypress (@smoke) — terminaram com sucesso. A descrição da PR registra 178/178 testes backend aprovados na execução local; esse número é evidência informada na PR, não uma contagem extraída do log do CI.

**Aceite e limitação:** o documento do PO `docs/releases/release-2/aceite-po-sprint-3.md` marca a FT-114 como Aceita, e a issue está como Concluída no Jira. A revisão estática dos arquivos de model, seed, serializer, viewset, testes backend, componente `CargoCatalog.tsx` e `cargas.feature` não identificou bloqueador evidente. A primeira implantação em homologação foi validada em 25/11/2026 no [CI #351](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270), com todos os jobs, inclusive deploy, concluídos com sucesso; o health check documentado retornou `status: ok` e `database: ok` para o commit implantado. **Validação manual de QA (26/11/2026): aprovada conforme confirmação do QA.** O QA acessou https://feneme-homologacao.onrender.com e confirmou que os sete tipos aparecem, os campos do catálogo estão corretos (incluindo “limite derivado” para cosméticos) e os links das fontes abrem corretamente.

### 5.4 FT-113 — US-14: lista de cidades

A [PR #47](https://github.com/moon-byme/feneme-tech/pull/47) foi integrada à `main`. A condição de aceite do PO (merge da PR) foi satisfeita e o Jira registra a história como Concluída. A entrega contém a lista única de 26 cidades, compartilhada entre cadastro e clima, e cenários de rejeição de origem igual ao destino. O CI da PR passou, incluindo E2E `@US-14`; o vínculo PR/testes/CI foi acrescentado à issue FT-113. Q-15 inclui FT-113 entre as cinco histórias formalmente concluídas na Sprint 3.

### 5.5 PRs de preparação de release e risco

As PRs [#48](https://github.com/moon-byme/feneme-tech/pull/48) e [#49](https://github.com/moon-byme/feneme-tech/pull/49) foram integradas. A primeira implantação automatizada em homologação foi validada no CI #351 e a FT-110 está Concluída no Jira; a documentação complementar foi integrada pela [PR #55](https://github.com/moon-byme/feneme-tech/pull/55). FT-115 (Google Cloud) e FT-116 (R10) não foram aceitas na Sprint 3: faltam evidências de console e a FT-116 depende da FT-115; ambas foram replanejadas para Sprint 4. R06/FT-65 foi reavaliado e está tratado para os fluxos atuais, com índice residual 8.

### 5.6 Regressão integrada e Q-01/Q-05

A PR [#51](https://github.com/moon-byme/feneme-tech/pull/51) foi aprovada pelos dois revisores e integrada à `main` em 26/11/2026 (merge commit `7acb133c5a9a6302ef876252dd9e68b13328d16d`). Ela acrescentou 20 tentativas R2 de atualização de status de entregas alheias para Q-05, corrigiu a rastreabilidade de CT-12/CT-26 em `historico.feature`, removeu a tag `@R2` de `recomendacao.feature` (CT-08/CT-21 foram movidos para Sprint 5/R3 pela FT-112) e incluiu a execução integral de `@R2` no CI.

No [CI run #45731598047](https://github.com/moon-byme/feneme-tech/actions/runs/45731598047), todos os jobs passaram: backend 196/196; `@smoke` 18/18; comparação de trajetos 3/3; `@R1` 10/10; `@US-08` 2/2; regressão `@R2` 29/29. A matriz aplicável à R2 contém 30 CT únicos (10 da regressão R1 e 20 específicos da R2, incluindo CT-32 coberto pelo backend): **Q-01 = 30/30 (100%)**. Para Q-05, as 20 tentativas de acesso cruzado ao endpoint de status foram rejeitadas (404), sem vazamento, alteração de entrega ou evento de histórico: **20/20 (100%), zero alterações indevidas**. O resultado técnico e a integração da PR #51 estão confirmados; o CI completo da PR passou no run #45731598047.

## 6. Pendências para concluir a FT-91

### 6.1 Pré-conferência da DoD sob responsabilidade de QA (FT-38)

A avaliação abaixo é técnica e preliminar; não substitui o preenchimento oficial da planilha DoD nem o aceite do PO/SM.

| Critério DoD da Sprint | Avaliação QA | Evidência / ressalva |
|---|---|---|
| 2 — US concluídas atendem à DoD individual | Parcial | FT-48, FT-49, FT-59 e FT-113 têm PR, testes e CI; FT-114 foi aceita pelo PO, está Concluída no Jira e tem PR/CI verde; validação manual independente do catálogo e das fontes em homologação aprovada pelo QA em 26/11 (sete tipos, campos e links conferidos). |
| 7 — Bugs encontrados registrados com evidência/severidade | Sem ocorrência registrada no Jira | Consulta `project = FT AND issuetype = Bug` retornou zero issues. Confirmar com a equipe se houve defeito relatado fora do Jira; não inferir ausência de defeitos não reportados. |
| 8 — Nenhum bug crítico/alto aberto sem plano | Atendido no Jira | Zero issues do tipo Bug; portanto, zero bugs críticos/altos em aberto no rastreador. |
| 9 — Regressão dos itens afetados executada | Atendido | CI na `main` [run 45738722270](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270) passou em backend, frontend, segurança, E2E e deploy; o E2E executou @R1, @R2, @smoke, @US-07 e @US-08. |
| 20 — Permissões Gestor/Motorista verificadas | Atendido nos fluxos cobertos | Q-05 20/20 tentativas de atualização cruzada rejeitadas; catálogo somente leitura e acesso anônimo 401 verificados na FT-114. |
| 21 — Funcionalidades concluídas verificadas, sem falhas críticas conhecidas | Parcial | CI verde nas histórias integradas; a homologação está disponível, e o QA confirmou a verificação manual da FT-114 em 26/11, sem divergências relatadas. |
| 22 — Falhas Open-Meteo não bloqueiam fluxos manuais | Atendido | Q-13 10/10 falhas simuladas preservaram cadastro e comparação manual. |
| 23 — Status e histórico persistem | Atendido | Q-12 20/20; CT-12 e CT-26 do histórico passaram 2/2 na regressão @R2. |

**DoD da Release sob QA:**
- Critério 4 (ciclo de regressão antes da apresentação): atendido pela execução CI acima.
- Critério 7 (relatório de qualidade da release): parecer final consolidado nesta atualização; a publicação formal depende da integração desta versão do relatório no repositório.
- Critério 2 (implantação em homologação e demonstração): implantação automatizada e health check concluídos no CI #351; a verificação manual da FT-114 foi concluída pelo QA; a demonstração formal na Review ainda não está documentada.

1. **Indicadores de qualidade da R2:** Q-01 = 30/30 CT únicos aplicáveis executados (100%); Q-02 = zero Bugs registrados em aberto na consulta Jira de 25/11 (snapshot do rastreador, não prova ausência de defeitos não reportados); Q-03 = 8/8 (100%); Q-04 = 19/19 PRs (#39–#57) com aprovação externa anterior ao merge na Sprint 3 (100%; recorte estrito da main: 18/18, pois #42 entrou pela feature e chegou à main via #43); Q-05 = 20/20 tentativas indevidas de alteração de status rejeitadas, sem alterações/eventos indevidos (100%); Q-06 = 0 exposições em 20 cenários; Q-07 = 5/5 participantes; Q-08 = 84% (142 testes OK, conforme planilha); Q-09 = 22/22 (100%, conforme planilha; não confundir com a taxa de sucesso do pipeline na main); Q-10 = 20/20 (100%); Q-12 = 20/20 (100%); Q-13 = 10/10 (100%); Q-15 = 9/9 histórias funcionais concluídas com vínculo de teste/PR no agregado da R2 (100%), sendo 5/5 na Sprint 3. A Scrum Master confirmou os recortes em [FT-72/10319](https://feneme.atlassian.net/browse/FT-72?focusedCommentId=10319), [FT-83/10320](https://feneme.atlassian.net/browse/FT-83?focusedCommentId=10320) e [FT-83/10338](https://feneme.atlassian.net/browse/FT-83?focusedCommentId=10338). Q-11 e Q-14 estão programadas para R3; Q-16 permanece proposta, sem aprovação e sem medição. **Planilha:** considerar Q-04 19/19 para a Sprint 3 e Q-15 9/9 para a R2, mantendo 5/5 como recorte da Sprint 3; registrar data, universo e links das confirmações.
2. **Q-12 e Q-13:** resultados registrados na planilha (20/20 e 10/10). Manter vinculadas as evidências das seções 2 e 3.
3. **FT-32:** decisão do PO registrada; issue movida para a FT Sprint 5/R3 junto da FT-57. Validar o critério restante após a implementação da dependência.
4. **Revisão independente e aceite:** a Scrum Master confirmou Q-04 em 19/19 PRs (#39–#57) na Sprint 3, com aprovação externa antes do merge; o recorte estrito da main é 18/18. Q-15 foi confirmado em 5/5 na Sprint 3 e 9/9 no agregado da R2. Q-12/FT-80 e Q-13/FT-81 foram formalmente conferidas pelo PO e concluídas no Jira. A FT-114 está Concluída no Jira; a homologação foi implantada e o QA aprovou manualmente o catálogo e os links/fontes em 26/11. A observação de duplicidade de cenários de histórico em `historico.feature` e `status.feature` (sem CT na segunda) permanece como melhoria a avaliar na R3. O recorte Q-04 19/19 da Sprint 3 não deve ser confundido com o relatório do pipeline da R2 (#11–#46, 33/35), que mede universo e período diferentes.
5. **Sprint 3 — demais entregas:** FT-113 foi integrada e aceita após merge da PR #47. FT-114 foi aceita pelo PO, integrada pela PR #44 e está Concluída no Jira. O primeiro deploy em homologação foi validado no CI #351 e documentado pela PR #55; a verificação manual de QA do catálogo e das fontes foi aprovada em 26/11. FT-115 e FT-116 foram explicitamente não aceitas na Sprint 3 e replanejadas para Sprint 4; não tratá-las como pendências de implementação da FT-91/R2.
6. **Smoke e regressão final:** a execução integral do CI na `main`, após integração da PR #51, passou em segurança, backend, frontend, E2E e deploy no [CI #351](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270). O job E2E executou `@smoke`, `@US-07`, `@R1`, `@US-08` e a regressão completa `@R2`; todos os jobs terminaram com sucesso. A evidência anterior detalha 18/18 `@smoke`, 10/10 `@R1`, 3/3 `@US-07`, 2/2 `@US-08` e 29/29 `@R2` no run 45731598047. A implantação em homologação também foi concluída no CI #351.
7. **Defeitos:** registrar bugs apenas quando houver reprodução confirmada, com severidade, passos, resultado esperado/observado, evidência e vínculo à US/PR. Não duplicar defeitos já registrados.
8. **DoD:** revisar os critérios das histórias candidatas ao aceite, documentar cada item não comprovado e comunicar impedimentos ao PO.
9. **Relatório final:** parecer consolidado nesta versão, com resultados, métricas, defeitos registrados, regressão, limitações e recomendações. A integração da PR que contém este arquivo é a etapa de publicação documental.

## 7. Referências

- [FT-32 — Driver de confiabilidade](https://feneme.atlassian.net/browse/FT-32)
- [FT-80 — Q-12](https://feneme.atlassian.net/browse/FT-80)
- [FT-81 — Q-13](https://feneme.atlassian.net/browse/FT-81)
- [FT-91 — QA da Sprint 3 e relatório R2](https://feneme.atlassian.net/browse/FT-91)
- [PR #51 — regressão R2, Q-05 e rastreabilidade CT](https://github.com/moon-byme/feneme-tech/pull/51)
- [CI completo na main com deploy — run 45738722270](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270)
- [FT-112 — mudança de escopo da R2](https://feneme.atlassian.net/browse/FT-112)
- [Plano de Qualidade Q-01 a Q-15](https://docs.google.com/spreadsheets/d/1iRGEGUlcYLnbFpMCBW8yy89v-VHCkdEi-gPcPEhxdv8/edit?usp=sharing)
- [Plano de Testes CT/US e regressão](https://docs.google.com/document/d/1UuZl4kbzAqqMAKdMW1UT53nRWxehrRowU-_2-xOkfOI/edit?usp=sharing)
- [Planilha DoD — Sprints e Releases](https://docs.google.com/spreadsheets/d/1taP4dEHKtgOcq0IizKQGb_t1NhWtNU2sLdFVvvCQw84/edit?usp=sharing)


## 8. Parecer final de QA — 26/11/2026

**Conclusão:** as evidências disponíveis sustentam o encerramento das atividades de QA previstas para a Sprint 3 e a consolidação de qualidade da R2, observadas as limitações e os itens formalmente replanejados abaixo. A FT-91 consta como Concluída no Jira; a PR #58 foi integrada. Esta atualização substitui o caráter parcial do relatório após sua integração à `main`.

### Resultados finais e ressalvas

- **Regressão:** @R2 29/29; @R1 10/10; @smoke 18/18; @US-07 3/3; @US-08 2/2 no CI #45731598047. O CI #394 (run [45849612416](https://github.com/moon-byme/feneme-tech/actions/runs/45849612416)) também concluiu com sucesso os seis jobs: segurança, detecção de componentes, backend, frontend, E2E e deploy em homologação.
- **Homologação / FT-114:** verificação manual do QA aprovada em 26/11: sete tipos de carga exibidos, campos e limites corretos (incluindo “limite derivado” para cosméticos) e links das fontes funcionando. Não é necessário repetir o teste manual.
- **Defeitos:** a consulta Jira de 25/11 não encontrou issues do tipo Bug em aberto. Isso significa zero Bugs registrados no universo consultado; não permite afirmar que não houve relatos informais ou defeitos não reportados. Não foram criados Bugs sem reprodução confirmada.
- **Q-04 e Q-15:** usar os universos confirmados pela SM: Q-04 19/19 na Sprint 3 (#39–#57); Q-15 5/5 na Sprint 3 e 9/9 no agregado da R2. A PR #58 não integra o universo formal confirmado no comentário 10319, que explicitamente encerra o recorte em #57.
- **Escopo não concluído nesta release:** FT-115/FT-116 foram replanejadas para Sprint 4; FT-57 e o critério restante da FT-32 foram replanejados para Sprint 5/R3. Esses itens não devem ser tratados como bugs nem como bloqueadores de QA da Sprint 3, conforme decisões do PO.
- **Limitações de evidência:** Q-13 usa falhas simuladas e não mede disponibilidade real da Open-Meteo; Q-02 reflete apenas o rastreador Jira; Q-08 e Q-09 mantêm os universos e valores da planilha, sem equiparar cobertura de testes à estabilidade do pipeline.

**Parecer QA:** aprovado para fechamento das atividades de QA da Sprint 3 / R2, com as ressalvas documentadas. A publicação da versão/tag `v2.0.0`, a GitHub Release e a marcação da versão como lançada no Jira permanecem sob responsabilidade de PO/DevOps, na FT-92; não são declaradas como concluídas por este parecer.


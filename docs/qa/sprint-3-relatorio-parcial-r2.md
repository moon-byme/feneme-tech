# QA — Sprint 3: relatório parcial de qualidade da Release 2

**Projeto:** Feneme — Gestão Inteligente de Transporte de Alimentos  
**Sprint:** FT Sprint 3 (17/11/2026 a 26/11/2026)  
**Responsável QA:** José Araújo Agra Neto  
**Data de consolidação:** 26/11/2026  
**Issues acompanhadas:** FT-32, FT-80, FT-81 e FT-91

> **Estado deste documento: PARCIAL (atualizado em 26/11/2026).** Registra resultados sustentados por evidências do Jira, PRs, GitHub Actions e plano de testes. As medições Q-01, Q-02, Q-04, Q-05, Q-12, Q-13 e Q-15 foram apuradas nesta consolidação. A planilha deve refletir a reauditoria de Q-04 (12/12, não mais 7/7) e receber/conferir os resultados de Q-01, Q-02, Q-05 e Q-15. Ainda faltam revisão independente, validação manual no ambiente publicado, conferência formal do PO/SM e fechamento da DoD. Nenhuma medição foi estimada.

## 1. Resumo executivo

| Issue | Verificação | Resultado comprovado | Situação de QA |
|---|---|---|---|
| FT-32 | Resiliência à indisponibilidade da Open-Meteo | 10/10 falhas simuladas preservaram cadastro e comparação manual | Parcial: requisito de não recomendar sem dados depende da FT-57, replanejada para Sprint 5/R3 |
| FT-80 | Q-12 — Persistência de alterações de status | 20/20 alterações válidas persistidas e recuperadas (100%); Resultado R2 registrado como 1,0 na planilha | Medição e lançamento documental confirmados; falta conferência formal/revisão independente |
| FT-81 | Q-13 — Continuidade sem resposta da Open-Meteo | 10/10 falhas simuladas preservaram os fluxos manuais (100%); Q-13 consta na planilha | Medição comprovada; R06/FT-65 reavaliado e concluído; falta conferência formal e revisão independente |
| FT-91 | Regressão, métricas, DoD e relatório da R2 | Q-01 30/30; Q-02 0 Bugs abertos no Jira; Q-04 12/12; Q-05 20/20; Q-15 4/4; regressão @R2 29/29 | Em andamento; PR #51 aberta, validação manual da FT-114, conferência formal e DoD ainda pendentes |

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

**Atualização de fechamento (25/11):** na versão mais recente da planilha anexada pelo responsável, Q-12 está preenchida em Resultado R2 com o valor numérico `1,0` (100%), e a aba Revisões registra a inclusão do resultado em 25/11. As evidências da PR #41 e do CI #260 estão vinculadas na planilha. O lançamento documental está confirmado; permanece a conferência formal pela equipe/PO e a revisão independente de QA.

## 3. FT-81 — Q-13: continuidade sem resposta da Open-Meteo

**Meta:** 100% de 10 casos de falha com comparação manual preservada.

**Resultado comprovado:** 10/10 (100%) para a continuidade dos fluxos manuais.

A [PR #24 — dez falhas sem bloquear fluxos manuais](https://github.com/moon-byme/feneme-tech/pull/24) foi integrada à `main`. O teste `test_ten_external_failure_scenarios_preserve_manual_flows`, em `backend/weather/tests.py`, cobre timeout, conexão recusada, HTTP 500, 503, 429, 204, JSON inválido, previsão ausente, listas vazias e temperatura nula.

Em cada caso, verifica a resposta genérica de indisponibilidade e a continuidade do cadastro e do registro de alternativas manuais. A execução documentada confirma 10 entregas e 20 alternativas persistidas.

Evidência: [GitHub Actions — PR #24 (run 42844947365)](https://github.com/moon-byme/feneme-tech/actions/runs/42844947365). A execução documentada registrou 142 testes backend aprovados, Cypress `@R1` 10/10 e `@US-08` 2/2.

**Limitação:** os testes usam mocks. Não medem a disponibilidade real da Open-Meteo nem uma chamada externa bem-sucedida.

**Atualização de fechamento (26/11):** Q-13 está registrada em Resultado R2 com `100% de 10`. O risco residual R06 foi reavaliado em `docs/releases/release-2/riscos-residuais.md`: índice residual 8 (P=4, S=4), tratado para os fluxos atuais; a recomendação climática permanece vinculada à FT-57 (Sprint 5/R3). A FT-65 aparece como Concluída no Jira. Falta a conferência formal/revisão independente. Q-13 não comprova disponibilidade real do provedor.

## 4. FT-32 — DA-CON-JA-01: isolar falhas da Open-Meteo

A parte do driver relativa à continuidade dos fluxos manuais está coberta pela mesma evidência da Q-13: 10/10 falhas simuladas preservaram o cadastro e a comparação manual.

Entretanto, o critério original também menciona não confirmar recomendação climática sem dados. Essa parte não pode ser testada nesta release: a FT-57 (US-09 — comparação térmica e recomendação) foi retirada da R2 e replanejada para a Sprint 5/R3, conforme decisão registrada na FT-112.

**Resultado de QA:** atendimento parcial, restrito ao isolamento das falhas e à continuidade manual. Não declarar o driver integralmente concluído com base apenas nos 10/10 casos.

**Ação necessária:** PO/equipe devem confirmar se a FT-32 será mantida como carryover com a parte de recomendação explicitamente pendente, ou se o critério/escopo do driver será formalmente revisado. Não alterar o critério de aceite unilateralmente.

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

**Aceite e limitação:** o documento do PO `docs/releases/release-2/aceite-po-sprint-3.md` marca a FT-114 como Aceita, mas registra a validação manual do QA como pendência na FT-91. A revisão estática dos arquivos de model, seed, serializer, viewset, testes backend, componente `CargoCatalog.tsx` e `cargas.feature` não identificou bloqueador evidente. Ainda não foi realizada sessão manual no ambiente publicado nem conferência manual dos links/fontes; a FT-110 aguarda a primeira execução do deploy no Render.

### 5.4 FT-113 — US-14: lista de cidades

A [PR #47](https://github.com/moon-byme/feneme-tech/pull/47) foi integrada à `main`. A condição de aceite do PO (merge da PR) foi satisfeita e o Jira registra a história como Concluída. A entrega contém a lista única de 26 cidades, compartilhada entre cadastro e clima, e cenários de rejeição de origem igual ao destino. O CI da PR passou, incluindo E2E `@US-14`; o vínculo PR/testes/CI foi acrescentado à issue FT-113. Q-15 inclui FT-113 entre as quatro histórias formalmente concluídas.

### 5.5 PRs de preparação de release e risco

As PRs [#48](https://github.com/moon-byme/feneme-tech/pull/48) e [#49](https://github.com/moon-byme/feneme-tech/pull/49) foram integradas. O aceite do PO registra a preparação do workflow/Blueprint e guia de deploy, mas a FT-110 só será concluída após criar o serviço no Render e registrar o primeiro deploy verde e a URL. FT-115 (Google Cloud) e FT-116 (R10) não foram aceitas na Sprint 3: faltam evidências de console e a FT-116 depende da FT-115; ambas foram replanejadas para Sprint 4. R06/FT-65 foi reavaliado e está tratado para os fluxos atuais, com índice residual 8.

### 5.6 Regressão integrada e Q-01/Q-05

A PR [#51](https://github.com/moon-byme/feneme-tech/pull/51) acrescentou 20 tentativas R2 de atualização de status de entregas alheias para Q-05, corrigiu a rastreabilidade de CT-12/CT-26 em `historico.feature`, removeu a tag `@R2` de `recomendacao.feature` (CT-08/CT-21 foram movidos para Sprint 5/R3 pela FT-112) e incluiu a execução integral de `@R2` no CI.

No [CI run #45731598047](https://github.com/moon-byme/feneme-tech/actions/runs/45731598047), todos os jobs passaram: backend 196/196; `@smoke` 18/18; comparação de trajetos 3/3; `@R1` 10/10; `@US-08` 2/2; regressão `@R2` 29/29. A matriz aplicável à R2 contém 30 CT únicos (10 da regressão R1 e 20 específicos da R2, incluindo CT-32 coberto pelo backend): **Q-01 = 30/30 (100%)**. Para Q-05, as 20 tentativas de acesso cruzado ao endpoint de status foram rejeitadas (404), sem vazamento, alteração de entrega ou evento de histórico: **20/20 (100%), zero alterações indevidas**. A PR #51 ainda aguarda revisão/merge; o resultado técnico está comprovado no CI, mas a integração da PR não deve ser presumida.

## 6. Pendências para concluir a FT-91

### 6.1 Pré-conferência da DoD sob responsabilidade de QA (FT-38)

A avaliação abaixo é técnica e preliminar; não substitui o preenchimento oficial da planilha DoD nem o aceite do PO/SM.

| Critério DoD da Sprint | Avaliação QA | Evidência / ressalva |
|---|---|---|
| 2 — US concluídas atendem à DoD individual | Parcial | FT-48, FT-49, FT-59 e FT-113 têm PR, testes e CI; FT-114 foi aceita pelo PO, mas a validação manual independente continua pendente (FT-110/homologação). |
| 7 — Bugs encontrados registrados com evidência/severidade | Sem ocorrência registrada no Jira | Consulta `project = FT AND issuetype = Bug` retornou zero issues. Confirmar com a equipe se houve defeito relatado fora do Jira; não inferir ausência de defeitos não reportados. |
| 8 — Nenhum bug crítico/alto aberto sem plano | Atendido no Jira | Zero issues do tipo Bug; portanto, zero bugs críticos/altos em aberto no rastreador. |
| 9 — Regressão dos itens afetados executada | Atendido | CI [run 45731598047](https://github.com/moon-byme/feneme-tech/actions/runs/45731598047): @R1 10/10, @R2 29/29, @smoke 18/18, @US-07 3/3 e @US-08 2/2. |
| 20 — Permissões Gestor/Motorista verificadas | Atendido nos fluxos cobertos | Q-05 20/20 tentativas de atualização cruzada rejeitadas; catálogo somente leitura e acesso anônimo 401 verificados na FT-114. |
| 21 — Funcionalidades concluídas verificadas, sem falhas críticas conhecidas | Parcial | CI verde nas histórias integradas; FT-114 ainda aguarda validação manual no ambiente publicado. |
| 22 — Falhas Open-Meteo não bloqueiam fluxos manuais | Atendido | Q-13 10/10 falhas simuladas preservaram cadastro e comparação manual. |
| 23 — Status e histórico persistem | Atendido | Q-12 20/20; CT-12 e CT-26 do histórico passaram 2/2 na regressão @R2. |

**DoD da Release sob QA:**
- Critério 4 (ciclo de regressão antes da apresentação): atendido pela execução CI acima.
- Critério 7 (relatório de qualidade da release): parcial; o relatório foi atualizado, mas permanece parcial até a validação manual da FT-114, conferência formal e fechamento das pendências.
- Critério 2 (implantação em homologação e demonstração): depende da FT-110; primeiro deploy no Render e URL ainda pendentes.

1. **Indicadores de qualidade R2:** Q-01 = 30/30 CT únicos executados (100%); Q-02 = zero Bugs registrados em aberto no Jira na consulta de 25/11 (snapshot do rastreador, não prova ausência de defeitos não reportados); Q-03 = 100% (8/8 US); Q-04 = 12/12 PRs (#39–#50) com aprovação de pessoa diferente do autor antes do merge (100%); Q-05 = 20/20 tentativas indevidas de alteração de status rejeitadas, zero alterações/eventos indevidos (100%); Q-06 = 0 exposições em 20 cenários; Q-07 = 5/5 participantes; Q-08 = 84% (142 testes OK, conforme registro da planilha); Q-09 = 100% (22/22 execuções); Q-10 = 100% (20/20); Q-12 = 20/20 (100%); Q-13 = 10/10 (100%); Q-15 = 4/4 histórias formalmente concluídas com vínculo de evidência teste/PR no Jira (100%, apuração preliminar aguardando conferência do SM). Q-11 e Q-14 estão programadas para R3; Q-16 permanece proposta, sem aprovação e sem medição. **Atualização necessária na planilha:** substituir o denominador de Q-04 de 7/7 para 12/12; inserir/conferir Q-01, Q-02, Q-05 e Q-15 com as evidências descritas aqui.
2. **Q-12 e Q-13:** resultados registrados na planilha (20/20 e 10/10). Manter vinculadas as evidências das seções 2 e 3.
3. **FT-32:** obter decisão do PO sobre o carryover da parte dependente da FT-57, que está fora da R2.
4. **Revisão independente e aceite:** a Q-04 foi reauditada em 12/12 PRs com aprovação independente. A revisão estática da FT-114 foi registrada, mas falta validação manual no ambiente publicado. A PR #51 aguarda revisão/merge. A aprovação do PO não substitui a validação manual do QA.
5. **Sprint 3 — demais entregas:** FT-113 foi integrada e aceita após merge da PR #47. FT-114 foi aceita pelo PO e integrada pela PR #44, mas a validação manual de QA permanece pendente até a primeira homologação/deploy (FT-110). FT-115 e FT-116 foram explicitamente não aceitas na Sprint 3 e replanejadas para Sprint 4; não tratá-las como pendências de implementação da FT-91/R2.
6. **Smoke e regressão final:** a execução integral do CI na PR #51 passou em `@smoke` (18/18), `@R1` (10/10), `@US-07` (3/3), `@US-08` (2/2) e `@R2` (29/29), run 45731598047. A PR #51 ainda aguarda revisão/merge; repetir a conferência após a integração na `main`.
7. **Defeitos:** registrar bugs apenas quando houver reprodução confirmada, com severidade, passos, resultado esperado/observado, evidência e vínculo à US/PR. Não duplicar defeitos já registrados.
8. **DoD:** revisar os critérios das histórias candidatas ao aceite, documentar cada item não comprovado e comunicar impedimentos ao PO.
9. **Relatório final:** substituir este documento parcial por uma versão final somente após concluir as verificações acima, consolidando resultados, métricas, defeitos, regressão, limitações e recomendações.

## 7. Referências

- [FT-32 — Driver de confiabilidade](https://feneme.atlassian.net/browse/FT-32)
- [FT-80 — Q-12](https://feneme.atlassian.net/browse/FT-80)
- [FT-81 — Q-13](https://feneme.atlassian.net/browse/FT-81)
- [FT-91 — QA da Sprint 3 e relatório R2](https://feneme.atlassian.net/browse/FT-91)
- [PR #51 — regressão R2, Q-05 e rastreabilidade CT](https://github.com/moon-byme/feneme-tech/pull/51)
- [CI completo — run 45731598047](https://github.com/moon-byme/feneme-tech/actions/runs/45731598047)
- [FT-112 — mudança de escopo da R2](https://feneme.atlassian.net/browse/FT-112)
- [Plano de Qualidade Q-01 a Q-15](https://docs.google.com/spreadsheets/d/1iRGEGUlcYLnbFpMCBW8yy89v-VHCkdEi-gPcPEhxdv8/edit?usp=sharing)
- [Plano de Testes CT/US e regressão](https://docs.google.com/document/d/1UuZl4kbzAqqMAKdMW1UT53nRWxehrRowU-_2-xOkfOI/edit?usp=sharing)
- [Planilha DoD — Sprints e Releases](https://docs.google.com/spreadsheets/d/1taP4dEHKtgOcq0IizKQGb_t1NhWtNU2sLdFVvvCQw84/edit?usp=sharing)

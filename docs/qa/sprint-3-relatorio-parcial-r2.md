# QA — Sprint 3: relatório parcial de qualidade da Release 2

**Projeto:** Feneme — Gestão Inteligente de Transporte de Alimentos  
**Sprint:** FT Sprint 3 (17/11/2026 a 26/11/2026)  
**Responsável QA:** José Araújo Agra Neto  
**Data de consolidação:** 26/11/2026  
**Issues acompanhadas:** FT-32, FT-80, FT-81 e FT-91

> **Estado deste documento: PARCIAL (atualizado em 26/11/2026).** Registra resultados sustentados por evidências do Jira, PRs, GitHub Actions e plano de testes. As medições Q-01, Q-02, Q-04, Q-05, Q-12, Q-13 e Q-15 foram apuradas nesta consolidação. A reauditoria de Q-04 (12/12) foi registrada; a conferência formal do PO para Q-12 e Q-13 foi confirmada em 26/11. A homologação foi implantada e validada no CI #351; a validação manual independente da FT-114 está liberada, mas ainda precisa ser executada pelo QA. Também faltam confirmação do SM sobre Q-04/Q-15 e fechamento oficial da DoD. Nenhuma medição foi estimada.

## 1. Resumo executivo

| Issue | Verificação | Resultado comprovado | Situação de QA |
|---|---|---|---|
| FT-32 | Resiliência à indisponibilidade da Open-Meteo | 10/10 falhas simuladas preservaram cadastro e comparação manual | Replanejada para FT Sprint 5/R3, junto da FT-57; critério restante será validado após sua implementação |
| FT-80 | Q-12 — Persistência de alterações de status | 20/20 alterações válidas persistidas e recuperadas (100%); Resultado R2 registrado como 1,0 na planilha | Concluída; conferência formal do PO registrada em 26/11 |
| FT-81 | Q-13 — Continuidade sem resposta da Open-Meteo | 10/10 falhas simuladas preservaram os fluxos manuais (100%); Q-13 consta na planilha | Concluída; conferência formal do PO registrada; R06 residual P4/S4 = 8 lançado na planilha e FT-65 concluída |
| FT-91 | Regressão, métricas, DoD e relatório da R2 | Q-01 30/30; Q-02 0 Bugs abertos no Jira; Q-04 12/12; Q-05 20/20; Q-15 5/5 (preliminar); regressão @R2 29/29 | Em andamento; PR #51 integrada; deploy de homologação validado; falta QA manual da FT-114, confirmação do SM para Q-04/Q-15 e fechamento oficial da DoD |

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

**Aceite e limitação:** o documento do PO `docs/releases/release-2/aceite-po-sprint-3.md` marca a FT-114 como Aceita, e a issue está como Concluída no Jira. A revisão estática dos arquivos de model, seed, serializer, viewset, testes backend, componente `CargoCatalog.tsx` e `cargas.feature` não identificou bloqueador evidente. A primeira implantação em homologação foi validada em 25/11/2026 no [CI #351](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270), com todos os jobs, inclusive deploy, concluídos com sucesso; o health check documentado retornou `status: ok` e `database: ok` para o commit implantado. A validação manual independente do catálogo e dos links/fontes pelo QA ainda não foi executada e agora pode ser feita em https://feneme-homologacao.onrender.com.

### 5.4 FT-113 — US-14: lista de cidades

A [PR #47](https://github.com/moon-byme/feneme-tech/pull/47) foi integrada à `main`. A condição de aceite do PO (merge da PR) foi satisfeita e o Jira registra a história como Concluída. A entrega contém a lista única de 26 cidades, compartilhada entre cadastro e clima, e cenários de rejeição de origem igual ao destino. O CI da PR passou, incluindo E2E `@US-14`; o vínculo PR/testes/CI foi acrescentado à issue FT-113. Q-15 inclui FT-113 entre as quatro histórias formalmente concluídas.

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
| 2 — US concluídas atendem à DoD individual | Parcial | FT-48, FT-49, FT-59 e FT-113 têm PR, testes e CI; FT-114 foi aceita pelo PO, está Concluída no Jira e tem PR/CI verde; falta a validação manual independente do catálogo e das fontes em homologação. |
| 7 — Bugs encontrados registrados com evidência/severidade | Sem ocorrência registrada no Jira | Consulta `project = FT AND issuetype = Bug` retornou zero issues. Confirmar com a equipe se houve defeito relatado fora do Jira; não inferir ausência de defeitos não reportados. |
| 8 — Nenhum bug crítico/alto aberto sem plano | Atendido no Jira | Zero issues do tipo Bug; portanto, zero bugs críticos/altos em aberto no rastreador. |
| 9 — Regressão dos itens afetados executada | Atendido | CI na `main` [run 45738722270](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270) passou em backend, frontend, segurança, E2E e deploy; o E2E executou @R1, @R2, @smoke, @US-07 e @US-08. |
| 20 — Permissões Gestor/Motorista verificadas | Atendido nos fluxos cobertos | Q-05 20/20 tentativas de atualização cruzada rejeitadas; catálogo somente leitura e acesso anônimo 401 verificados na FT-114. |
| 21 — Funcionalidades concluídas verificadas, sem falhas críticas conhecidas | Parcial | CI verde nas histórias integradas; a homologação está disponível, mas o QA ainda precisa executar a verificação manual da FT-114. |
| 22 — Falhas Open-Meteo não bloqueiam fluxos manuais | Atendido | Q-13 10/10 falhas simuladas preservaram cadastro e comparação manual. |
| 23 — Status e histórico persistem | Atendido | Q-12 20/20; CT-12 e CT-26 do histórico passaram 2/2 na regressão @R2. |

**DoD da Release sob QA:**
- Critério 4 (ciclo de regressão antes da apresentação): atendido pela execução CI acima.
- Critério 7 (relatório de qualidade da release): parcial; o relatório foi atualizado, mas permanece parcial até a validação manual da FT-114, confirmação do SM sobre Q-04/Q-15 e fechamento das pendências.
- Critério 2 (implantação em homologação e demonstração): implantação automatizada e health check concluídos no CI #351; falta a demonstração/validação manual do incremento.

1. **Indicadores de qualidade R2:** Q-01 = 30/30 CT únicos executados (100%); Q-02 = zero Bugs registrados em aberto no Jira na consulta de 25/11 (snapshot do rastreador, não prova ausência de defeitos não reportados); Q-03 = 100% (8/8 US); Q-04 = 12/12 PRs (#39–#50) com aprovação de pessoa diferente do autor antes do merge (100%); Q-05 = 20/20 tentativas indevidas de alteração de status rejeitadas, zero alterações/eventos indevidos (100%); Q-06 = 0 exposições em 20 cenários; Q-07 = 5/5 participantes; Q-08 = 84% (142 testes OK, conforme registro da planilha); Q-09 = 100% (22/22 execuções); Q-10 = 100% (20/20); Q-12 = 20/20 (100%); Q-13 = 10/10 (100%); Q-15 = 5/5 histórias formalmente concluídas com vínculo de evidência teste/PR no Jira (100%, apuração preliminar após a FT-114 passar a Concluída; aguarda conferência do SM). Q-11 e Q-14 estão programadas para R3; Q-16 permanece proposta, sem aprovação e sem medição. **Conferência da planilha:** Q-04 foi reauditada como 12/12 (PRs #39–#50); o registro oficial deve ser confirmado pelo SM. Conferir/inserir Q-01, Q-02 e Q-05; atualizar Q-15 para 5/5, incluindo a FT-114 já Concluída, com as evidências descritas aqui.
2. **Q-12 e Q-13:** resultados registrados na planilha (20/20 e 10/10). Manter vinculadas as evidências das seções 2 e 3.
3. **FT-32:** decisão do PO registrada; issue movida para a FT Sprint 5/R3 junto da FT-57. Validar o critério restante após a implementação da dependência.
4. **Revisão independente e aceite:** a Q-04 foi reauditada em 12/12 PRs com aprovação independente. O PO confirmou a conferência formal de Q-12/FT-80 e Q-13/FT-81, ambas concluídas no Jira. A FT-114 está Concluída no Jira, e a homologação está disponível após o CI #351; falta o QA manual verificar a tela do catálogo e os links/fontes. Q-15 passa preliminarmente a 5/5 histórias concluídas com evidência teste/PR (FT-48, FT-49, FT-59, FT-113 e FT-114), aguardando confirmação do SM. O revisor da PR #51 observou duplicidade de cenários de histórico em `historico.feature` e `status.feature` (sem CT na segunda); avaliar a remoção na R3. Também recomendou explicitar que Q-04 12/12 cobre PRs #39–#50, enquanto o relatório do pipeline da release considera #11–#46 (33/35), universos/períodos diferentes.
5. **Sprint 3 — demais entregas:** FT-113 foi integrada e aceita após merge da PR #47. FT-114 foi aceita pelo PO, integrada pela PR #44 e está Concluída no Jira. O primeiro deploy em homologação foi validado no CI #351 e documentado pela PR #55; falta apenas a verificação manual de QA do catálogo e das fontes. FT-115 e FT-116 foram explicitamente não aceitas na Sprint 3 e replanejadas para Sprint 4; não tratá-las como pendências de implementação da FT-91/R2.
6. **Smoke e regressão final:** a execução integral do CI na `main`, após integração da PR #51, passou em segurança, backend, frontend, E2E e deploy no [CI #351](https://github.com/moon-byme/feneme-tech/actions/runs/45738722270). O job E2E executou `@smoke`, `@US-07`, `@R1`, `@US-08` e a regressão completa `@R2`; todos os jobs terminaram com sucesso. A evidência anterior detalha 18/18 `@smoke`, 10/10 `@R1`, 3/3 `@US-07`, 2/2 `@US-08` e 29/29 `@R2` no run 45731598047. A implantação em homologação também foi concluída no CI #351.
7. **Defeitos:** registrar bugs apenas quando houver reprodução confirmada, com severidade, passos, resultado esperado/observado, evidência e vínculo à US/PR. Não duplicar defeitos já registrados.
8. **DoD:** revisar os critérios das histórias candidatas ao aceite, documentar cada item não comprovado e comunicar impedimentos ao PO.
9. **Relatório final:** substituir este documento parcial por uma versão final somente após concluir as verificações acima, consolidando resultados, métricas, defeitos, regressão, limitações e recomendações.

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

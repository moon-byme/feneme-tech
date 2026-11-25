# QA — Sprint 3: relatório parcial de qualidade da Release 2

**Projeto:** Feneme — Gestão Inteligente de Transporte de Alimentos  
**Sprint:** FT Sprint 3 (17/11/2026 a 26/11/2026)  
**Responsável QA:** José Araújo Agra Neto  
**Data de consolidação:** 25/11/2026  
**Issues acompanhadas:** FT-32, FT-80, FT-81 e FT-91

> **Estado deste documento: PARCIAL.** Registra somente resultados sustentados por evidências disponíveis no Jira, nas PRs e no GitHub Actions. Não substitui a execução dos testes que ainda dependem de integração, a conferência do Plano de Qualidade nem o aceite formal das histórias. Nenhuma medição pendente foi estimada ou preenchida como resultado.

## 1. Resumo executivo

| Issue | Verificação | Resultado comprovado | Situação de QA |
|---|---|---|---|
| FT-32 | Resiliência à indisponibilidade da Open-Meteo | 10/10 falhas simuladas preservaram cadastro e comparação manual | Parcial: requisito de não recomendar sem dados depende da FT-57, replanejada para Sprint 5/R3 |
| FT-80 | Q-12 — Persistência de alterações de status | 20/20 alterações válidas persistidas e recuperadas (100%) | Evidência automatizada existente; falta conferência do lançamento na planilha e revisão independente nesta sprint |
| FT-81 | Q-13 — Continuidade sem resposta da Open-Meteo | 10/10 falhas simuladas preservaram os fluxos manuais | Medição aprovada; falta conferência do resultado registrado e reavaliação do risco residual |
| FT-91 | Regressão, métricas, DoD e relatório da R2 | Evidências de FT-48, FT-49 e FT-59 disponíveis; regressões documentadas | Em andamento; fechamento depende das validações e entregas listadas na seção 6 |

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

**Pendência de fechamento:** conferir se o resultado 20/20 está lançado na coluna R2 do Plano de Qualidade e se a equipe/PO conferiu a evidência. A existência dos testes e do CI não comprova, por si só, a atualização da planilha.

## 3. FT-81 — Q-13: continuidade sem resposta da Open-Meteo

**Meta:** 100% de 10 casos de falha com comparação manual preservada.

**Resultado comprovado:** 10/10 (100%) para a continuidade dos fluxos manuais.

A [PR #24 — dez falhas sem bloquear fluxos manuais](https://github.com/moon-byme/feneme-tech/pull/24) foi integrada à `main`. O teste `test_ten_external_failure_scenarios_preserve_manual_flows`, em `backend/weather/tests.py`, cobre timeout, conexão recusada, HTTP 500, 503, 429, 204, JSON inválido, previsão ausente, listas vazias e temperatura nula.

Em cada caso, verifica a resposta genérica de indisponibilidade e a continuidade do cadastro e do registro de alternativas manuais. A execução documentada confirma 10 entregas e 20 alternativas persistidas.

Evidência: [GitHub Actions — PR #24 (run 42844947365)](https://github.com/moon-byme/feneme-tech/actions/runs/42844947365). A execução documentada registrou 142 testes backend aprovados, Cypress `@R1` 10/10 e `@US-08` 2/2.

**Limitação:** os testes usam mocks. Não medem a disponibilidade real da Open-Meteo nem uma chamada externa bem-sucedida.

**Pendência de fechamento:** conferir o lançamento do resultado R2 no Plano de Qualidade e registrar a reavaliação do risco residual. A FT-81 não deve ser interpretada como comprovação de disponibilidade do provedor.

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
- Cypress smoke: 15/15 aprovados, incluindo CT-26, CT-27 e CT-28 da FT-59 (3/3).
- Regressão `@US-07`: 3/3; `@R1`: 10/10; `@US-08`: 2/2.
- Cobertura do histórico cronológico, estado vazio, nova autenticação, autorização e respostas 401/403/404.

A revisão aprovada disponível é do PO (`jpauloaraujo`). O aceite do PO está registrado, mas a revisão independente de QA deve ser registrada separadamente; a aprovação do PO não substitui a validação do QA.

**Limitação de evidência:** os resultados acima são os informados na PR e no CI associado ao commit `f80e290`; não foi realizada uma execução local independente pelo QA nesta consolidação.

## 6. Pendências para concluir a FT-91

1. **Plano de Qualidade (Q-01 a Q-15):** conferir o universo de cada indicador aplicável à R2, meta, resultado, evidência, estado de atendimento e justificativa para itens não medidos/não aplicáveis. Não preencher valores sem evidência.
2. **Q-12 e Q-13:** conferir os resultados já registrados na planilha e vincular as evidências citadas nas seções 2 e 3.
3. **FT-32:** obter decisão do PO sobre o carryover da parte dependente da FT-57, que está fora da R2.
4. **Revisão independente:** registrar a revisão de QA das PRs/funcionalidades entregues, em especial FT-48, FT-49 e FT-59. A aprovação do PO não deve ser contada como aprovação de QA.
5. **Sprint 3 — novas entregas:** a PR #44 da FT-114 (catálogo de tipos de carga) ainda aparece aberta e sem revisão aprovada no momento desta consulta. A validação de QA dessa entrega deve ocorrer depois de CI verde e integração. A lista de cidades (FT-113), a configuração Google Cloud (FT-115) e o risco R10 (FT-116) também precisam ser conferidos quando suas entregas/evidências estiverem disponíveis.
6. **Smoke e regressão final:** conferir com DevOps a execução atual do `@smoke` após a integração das entregas restantes e registrar o resultado do pipeline da R2. Os resultados históricos de PRs anteriores não substituem a verificação final da versão candidata.
7. **Defeitos:** registrar bugs apenas quando houver reprodução confirmada, com severidade, passos, resultado esperado/observado, evidência e vínculo à US/PR. Não duplicar defeitos já registrados.
8. **DoD:** revisar os critérios das histórias candidatas ao aceite, documentar cada item não comprovado e comunicar impedimentos ao PO.
9. **Relatório final:** substituir este documento parcial por uma versão final somente após concluir as verificações acima, consolidando resultados, métricas, defeitos, regressão, limitações e recomendações.

## 7. Referências

- [FT-32 — Driver de confiabilidade](https://feneme.atlassian.net/browse/FT-32)
- [FT-80 — Q-12](https://feneme.atlassian.net/browse/FT-80)
- [FT-81 — Q-13](https://feneme.atlassian.net/browse/FT-81)
- [FT-91 — QA da Sprint 3 e relatório R2](https://feneme.atlassian.net/browse/FT-91)
- [FT-112 — mudança de escopo da R2](https://feneme.atlassian.net/browse/FT-112)
- [Plano de Qualidade Q-01 a Q-15](https://docs.google.com/spreadsheets/d/1iRGEGUlcYLnbFpMCBW8yy89v-VHCkdEi-gPcPEhxdv8/edit?usp=sharing)
- [Plano de Testes CT/US e regressão](https://docs.google.com/document/d/1UuZl4kbzAqqMAKdMW1UT53nRWxehrRowU-_2-xOkfOI/edit?usp=sharing)
- [Planilha DoD — Sprints e Releases](https://docs.google.com/spreadsheets/d/1taP4dEHKtgOcq0IizKQGb_t1NhWtNU2sLdFVvvCQw84/edit?usp=sharing)

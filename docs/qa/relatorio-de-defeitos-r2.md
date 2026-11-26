# Feneme — Relatório de defeitos e achados de QA
**Versão 1.0 | Sprint 2 e fechamento da Release 2 | 26/11/2026**
**QA:** José Araújo Agra Neto

## 1. Objetivo e critério de classificação

Consolida os achados de QA documentados na Sprint 2 e informa o que foi possível verificar no código até 26/11/2026. Os três itens foram originalmente descritos como **candidatos a defeito** no relatório da Sprint 2, integrado pela [PR #37](https://github.com/moon-byme/feneme-tech/pull/37), nos arquivos `docs/sprints/sprint-2/bugs-qa.pdf` e `docs/sprints/sprint-2/fontes/bugs-qa.typ`.

As prioridades (duas médias e uma baixa) são sugestões do relatório original; não são severidades formalmente atribuídas no Jira.

## 2. Resumo executivo

| ID | Achado | História | Prioridade sugerida | Estado observado em 26/11 |
|---|---|---|---|---|
| QA-R2-01 | Estado vazio após falha na consulta de entregas | FT-55 | Média | Lógica atual aparenta corrigir; reteste específico não localizado |
| QA-R2-02 | Apenas o primeiro erro de campo é apresentado | FT-44 | Baixa | Lógica atual ainda seleciona a primeira mensagem; requer correção/reteste |
| QA-R2-03 | Resposta da previsão pode corresponder à localidade anterior | FT-47 | Média | Condição assíncrona ainda é possível; requer correção/reteste |

## 3. Achados detalhados

### QA-R2-01 — Estado vazio exibido após falha na consulta de entregas

- **História:** FT-55 — Consultar entregas cadastradas.
- **Prioridade sugerida:** Média (não é severidade formal).
- **Descrição:** quando `GET /api/deliveries/` falha, o painel podia mostrar uma mensagem de erro e também “Nenhuma entrega cadastrada”, embora a consulta não tenha sido concluída.
- **Reprodução documentada:** entrar como Gestor; simular HTTP 500 na consulta; observar se o estado vazio aparece junto do erro.
- **Esperado:** mostrar a falha e oferecer nova tentativa, sem afirmar que a lista está vazia.
- **Causa original:** estado vazio decidido pelo array `deliveries`, sem distinguir lista vazia de erro de carregamento.
- **Código atual:** `frontend/src/App.tsx` mantém `deliveryError` separado. Quando a consulta falha sem dados, exibe “Tente atualizar a consulta para carregar as entregas”; “Nenhuma entrega cadastrada” só aparece sem erro.
- **Estado:** **aparentemente corrigido no código atual**. Não foi localizada execução de regressão especificamente dedicada a HTTP 500 nesse componente; não declarar reteste específico aprovado sem evidência.
- **Evidência:** `frontend/src/App.tsx`; relatório original / PR #37.

### QA-R2-02 — Apenas o primeiro erro de campo é apresentado no cadastro

- **História:** FT-44 — Cadastrar entrega e dados da carga.
- **Prioridade sugerida:** Baixa (não é severidade formal).
- **Descrição:** quando o backend retorna erros para vários campos, o frontend seleciona apenas a primeira mensagem.
- **Reprodução documentada:** entrar como Gestor; preencher mais de um campo com valor inválido; tentar cadastrar; verificar se todos os campos são identificados.
- **Esperado:** informar todos os campos inválidos ou destacar cada campo correspondente.
- **Causa original:** `errorMessage()` em `frontend/src/api.ts` seleciona apenas o primeiro valor do objeto de erros.
- **Código atual:** a função ainda utiliza `Object.values(record)[0]` e retorna a primeira mensagem do primeiro campo. Não foi localizada correção posterior.
- **Estado:** **pendente de triagem/correção e reteste**. Não há issue formal Bug localizada no Jira.
- **Evidência:** `frontend/src/api.ts`, função `errorMessage()`; relatório original / PR #37.

### QA-R2-03 — Resultado de previsão pode corresponder à localidade anteriormente selecionada

- **História:** FT-47 — Consultar previsão de temperatura.
- **Prioridade sugerida:** Média (não é severidade formal).
- **Descrição:** durante uma consulta, a localidade pode ser alterada; a resposta assíncrona anterior pode chegar depois e ser exibida como se pertencesse à seleção atual.
- **Reprodução documentada:** selecionar localidade A e iniciar consulta; antes da resposta, selecionar localidade B; aguardar e conferir se o resultado corresponde à seleção atual.
- **Esperado:** descartar/cancelar resposta obsoleta ou impedir troca de localidade durante o carregamento.
- **Causa original:** a resposta assíncrona é aplicada sem confirmar se ainda corresponde à seleção atual.
- **Código atual:** em `frontend/src/components/TemperatureForecast.tsx`, `handleConsult()` aplica `setForecast(await api.getForecast(token, location))`; o seletor continua habilitado durante `loading` e não há verificação de que a localidade não mudou.
- **Estado:** **ainda plausível no código atual; requer triagem/correção e reteste**. Não foi realizada nova reprodução manual em homologação nesta consolidação.
- **Evidência:** `frontend/src/components/TemperatureForecast.tsx`; relatório original / PR #37.

## 4. Achado de rastreabilidade corrigido na Sprint 3

A revisão da suíte identificou cenários de histórico em `status.feature` reutilizando CT-27/CT-28, que pertencem à matriz de cidades/catálogo. A [PR #51](https://github.com/moon-byme/feneme-tech/pull/51) corrigiu a rastreabilidade: CT-12 e CT-26 ficaram em `historico.feature`, e a execução integral `@R2` foi adicionada ao CI.

**Estado:** corrigido e integrado. **Evidência:** CI [45731598047](https://github.com/moon-byme/feneme-tech/actions/runs/45731598047), regressão `@R2` 29/29 aprovada. Classificação: defeito de rastreabilidade/automação, não defeito funcional do produto.

## 5. Situação dos registros formais

Consultas realizadas em 26/11/2026:
- Jira: `project = FT AND issuetype = Bug` — nenhum resultado.
- GitHub: busca de issues no repositório com termo/label `bug` — nenhum resultado.

Isso não invalida os três achados históricos. Significa que não foram encontrados tickets formais de Bug nas consultas. Não é correto afirmar “zero defeitos encontrados”; o correto é “zero tickets formais de Bug encontrados”, mantendo os três achados históricos documentados.

## 6. Recomendações

1. PO/equipe devem confirmar a triagem e a severidade formal dos três achados.
2. Criar issues Jira do tipo Bug para os achados confirmados, vinculando FT-44, FT-47 ou FT-55, CT aplicável, passos, resultado esperado/observado e evidência.
3. Para QA-R2-01, adicionar/localizar teste automatizado de falha HTTP 500 e confirmar a correção já presente.
4. Para QA-R2-02, apresentar todos os erros de validação e testar vários campos inválidos simultaneamente.
5. Para QA-R2-03, impedir a troca de localidade durante carregamento ou invalidar respostas obsoletas; testar respostas fora de ordem.
6. Reexecutar testes afetados após correção e registrar resultados no Jira.

## 7. Evidências e referências

- [PR #37 — relatório original de achados da Sprint 2](https://github.com/moon-byme/feneme-tech/pull/37)
- Fonte original: `docs/sprints/sprint-2/fontes/bugs-qa.typ`
- PDF original: `docs/sprints/sprint-2/bugs-qa.pdf`
- [PR #51 — correção de rastreabilidade CT e regressão R2](https://github.com/moon-byme/feneme-tech/pull/51)
- [CI #45731598047 — regressão R2 29/29 e backend 196/196](https://github.com/moon-byme/feneme-tech/actions/runs/45731598047)
- [FT-44 — Cadastro de entrega](https://feneme.atlassian.net/browse/FT-44)
- [FT-47 — Previsão de temperatura](https://feneme.atlassian.net/browse/FT-47)
- [FT-55 — Consulta de entregas](https://feneme.atlassian.net/browse/FT-55)

**Conclusão:** três achados candidatos foram documentados desde a Sprint 2. Um aparenta estar corrigido no código, sem reteste específico localizado; dois ainda merecem triagem/correção e reteste. Nenhum foi encontrado como ticket formal Bug na consulta de 26/11/2026.

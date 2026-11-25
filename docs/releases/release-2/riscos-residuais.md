# Reavaliação dos riscos tratados na Release 2

**Responsável:** PO/DevOps (João Paulo de Araujo) · **Data:** 25/11/2026 · **Referência:** FT-8 e [planilha de Análise de Riscos](https://docs.google.com/spreadsheets/d/1BW27HTpsCLZND5vjA2dcW1B9HR7OFktL1d9YUuZPoQg/edit?usp=sharing)

Escala da disciplina: Probabilidade (P) invertida, 1 = muito provável e 5 = muito improvável; Severidade (S) de 1 a 5; Índice = (6 − P) × S. A severidade não muda com o tratamento: o que cai é a probabilidade.

| Risco | Jira | Índice inicial | Evidência do tratamento | P residual | S | Índice residual | Situação |
| --- | --- | ---: | --- | ---: | ---: | ---: | --- |
| R05 — status não persistir | FT-64 | (6−3)×4 = **12** | Transação atômica com trava da entrega e restrições no banco (PR #41); 20/20 atualizações e eventos recuperados após novo login; CI verde | 4 | 4 | **8** | Tratado; monitorar em regressão |
| R06 — falha da Open-Meteo bloquear fluxos | FT-65 | (6−2)×4 = **16** | Timeout e erros tratados com aviso (PR #23); 10/10 falhas simuladas sem bloquear cadastro e comparação manual (PR #24, #30) | 4 | 4 | **8** | Tratado para os fluxos atuais; recomendação climática reavaliada na FT-57 (Sprint 5) |
| R08 — erro ou demora no cadastro | FT-67 | (6−3)×3 = **9** | Origem e destino só pela lista de 26 cidades; origem igual ao destino e cidade inexistente rejeitadas (FT-113, PR #47) | 3 | 3 | **9** | Parcial: mantém P até o teste de usabilidade e a FT-117 (Sprint 4) |
| R10 — APIs do Google (cota, custo, chave) | FT-116 | (6−3)×4 = **12** | Procedimento documentado; CI sem chaves e com varredura de segredos (FT-110) | 3 | 4 | **12** | Não reavaliado: depende das evidências da FT-115 |

**Como registrar na planilha:** preencher as colunas de risco residual com P, S e índice acima, a data de 25/11/2026 e o link da evidência (PR ou issue). R08 e R10 continuam abertos.

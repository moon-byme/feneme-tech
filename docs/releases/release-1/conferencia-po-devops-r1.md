# Conferência de PO/DevOps da Release 1 — regularização documental

**Elaborado em:** 25/11/2026, de forma **retrospectiva**, pelo PO/DevOps da R2 (João Paulo de Araujo), a pedido da SM no checklist da [FT-124](https://feneme.atlassian.net/browse/FT-124).
**Escopo:** Sprint 0 e Sprint 1 da R1 (06/10 a 29/10/2026), histórias US-01 a US-05 (FT-43, FT-54, FT-44, FT-55, FT-45). PO/DevOps da R1 na época: José Araújo Agra Neto.
**Fontes:** Jira (issues e comentários originais), API do GitHub (PRs, reviews, Actions, tags e releases) e o repositório na tag `v1.0.0`.

**Regra de integridade:** nada aqui altera o que foi registrado em 29/10. Aceites, ressalvas e não conformidades originais ficam como estão. Medições e testes feitos depois são identificados com a data real em que ocorreram.

## 1. Aceites das cinco histórias

| US | Issue | Aceite original do PO (29/10) | PR de integração | Review antes do merge | CI da `main` | Conferência de 25/11 |
| --- | --- | --- | --- | --- | --- | --- |
| US-01 Login do Gestor | FT-43 | Aceito (20h19) | #1 (27/10) | **Não** (0 reviews) | Sim | Aceite preservado. Gherkin coberto por testes de API (comentário de 29/10, 18h49) |
| US-02 Login do Motorista | FT-54 | Aceito (20h20) | #2 (29/10) | **Não** (0 reviews) | Sim ([run](https://github.com/moon-byme/feneme-tech/actions/runs/40903583088)) | Aceite preservado. DoD da issue já marca a review como não atendida |
| US-03 Cadastrar entrega | FT-44 | Aceito (20h20) | #1 (27/10) | **Não** (0 reviews) | Sim | Aceite preservado |
| US-04 Consultar entregas | FT-55 | **Aceito com ressalva** (20h21): sem teste do estado vazio | #1 (27/10) | **Não** (0 reviews) | Sim | Ressalva preservada; tratamento na seção 4 |
| US-05 Atribuir motorista | FT-45 | **Aceito com ressalva** (20h21): sem teste de Motorista inexistente | #1 (27/10) | **Não** (0 reviews) | Sim | Ressalva preservada; tratamento na seção 4 |

O critério da DoD "Código revisado e integrado por Pull Request" fica **Não atendido** nas cinco US. Isso não muda com testes ou revisões posteriores (impedimento I-03).

## 2. Q-03 — Critérios de aceite verificáveis (FT-71)

**Universo:** as cinco US funcionais planejadas para a Sprint 1. **Critério:** a US tem cenário Gherkin de sucesso **e** pelo menos um de exceção, e a DoR marca esse item.

| US | Cenários de sucesso | Cenários de exceção | Completo |
| --- | --- | --- | --- |
| FT-43 | Login válido do Gestor | Senha inválida | Sim |
| FT-54 | Login válido do Motorista | Ação exclusiva do Gestor; credenciais incorretas | Sim |
| FT-44 | Cadastro válido | Campos obrigatórios ausentes; cadastro não autorizado | Sim |
| FT-55 | Listar entregas | Nenhuma entrega cadastrada | Sim |
| FT-45 | Atribuição válida | Motorista inválido; atribuição não autorizada | Sim |

**Resultado R1:** 5 de 5 = **100%** (meta: 100%). Conferido no texto atual das issues em 25/11/2026. Os cenários estavam na DoR, assinalada antes da Sprint 1.

## 3. Q-08 — Cobertura de linhas do backend (FT-76)

**Relatório original da R1:** não existe. O CI da R1 não tinha `pytest-cov` nem `coverage`, e não há relatório no repositório, na pasta `evidencias/` nem no Jira. A [auditoria da Sprint 1](../../qa/auditoria-sprint-1.md) já registrava que Q-08 não fora medida. **Qualquer valor lançado para a R1 antes de 25/11 não tem comprovação.**

**Nova medição na versão da R1, feita em 25/11/2026:**

| Item | Valor |
| --- | --- |
| Versão medida | tag `v1.0.0` → commit `929d907` |
| Ferramenta | Coverage.py 7.17 (`coverage run manage.py test`), Python 3.13, Django 5.2.19, DRF 3.16.1, PostgreSQL 16 |
| Universo (módulos testáveis) | `backend/accounts`, `backend/deliveries`, `backend/config` |
| Excluídos | migrações, arquivos de teste, `manage.py`, `wsgi.py`/`asgi.py` e scripts `verify_*.py` |
| Testes executados | 103, todos aprovados |
| Linhas elegíveis / não cobertas | 267 / 43 |
| **Cobertura** | **84%** (meta proposta: ≥ 70%) |

O único módulo sem cobertura relevante era o comando interativo `create_feneme_user` (0%).

**Comparação, na mesma configuração:** `main` em `1ecb4b3` (25/11/2026, fim da R2) → 194 testes, 655 linhas, **88%**.

## 4. Testes posteriores das ressalvas (FT-45 e FT-55)

**FT-55 — estado vazio**
- O teste de API `deliveries/tests.py::test_gestor_sees_empty_delivery_list` (CT-16, lista vazia) entrou na `main` pela **PR #8, às 19h46 de 29/10**, 35 minutos **antes** do aceite (20h21). A ressalva não considerou esse teste, que verifica a API, e não a mensagem da tela.
- A parte de interface ("informa que não há entregas" e "não apresenta registros fictícios") foi automatizada no cenário E2E `@CT-16` de `frontend/cypress/e2e/entregas.feature`, integrado pela **PR #12 em 03/11/2026**. Ele roda no CI a cada push.
- **Conclusão de 25/11:** a ressalva está **tratada integralmente**, com cobertura posterior ao aceite.

**FT-45 — Motorista inexistente**
- `accounts/test_q06_tratamento_erros.py::test_q06_19_motorista_inexistente_na_atribuicao` (**PR #17, 09/11/2026**) confirma o 400 sem vazamento de dados, mas **não** confere o motivo nem a preservação do vínculo anterior.
- Em **25/11/2026** foi criado `deliveries/tests.py::test_nonexistent_driver_is_rejected_and_keeps_previous_assignment`: com um Motorista já atribuído, o envio de `driver_id` inexistente retorna 400 com o motivo "O usuário informado não existe ou está inativo", e a atribuição anterior permanece.
- **Conclusão de 25/11:** a ressalva fica **tratada integralmente** quando esse teste for integrado com CI verde.

## 5. Q-09 — Estabilidade do pipeline (FT-77)

**Universo definido:** workflow `CI`, eventos de push na branch `main`, de 22/10/2026 21h12 (criação do workflow) a 29/10/2026 23h12 (commit da tag `v1.0.0`), horário de Brasília. Antes de 22/10 não havia CI.

**Resultado R1:** 21 de 21 execuções concluídas com sucesso = **100%** (meta: ≥ 90%).

Execuções: [#1](https://github.com/moon-byme/feneme-tech/actions/runs/39876721757), [#2](https://github.com/moon-byme/feneme-tech/actions/runs/40407702577), [#5](https://github.com/moon-byme/feneme-tech/actions/runs/40411912590), [#9](https://github.com/moon-byme/feneme-tech/actions/runs/40552576742), [#16](https://github.com/moon-byme/feneme-tech/actions/runs/40904717652), [#20](https://github.com/moon-byme/feneme-tech/actions/runs/40923195980), [#21](https://github.com/moon-byme/feneme-tech/actions/runs/40926450769), [#24](https://github.com/moon-byme/feneme-tech/actions/runs/40946472419), [#27](https://github.com/moon-byme/feneme-tech/actions/runs/40959484596), [#30](https://github.com/moon-byme/feneme-tech/actions/runs/40963771703), [#34](https://github.com/moon-byme/feneme-tech/actions/runs/40965591244), [#37](https://github.com/moon-byme/feneme-tech/actions/runs/40968402490), [#42](https://github.com/moon-byme/feneme-tech/actions/runs/40970019321), [#43](https://github.com/moon-byme/feneme-tech/actions/runs/40970818209), [#45](https://github.com/moon-byme/feneme-tech/actions/runs/40986454546), [#46](https://github.com/moon-byme/feneme-tech/actions/runs/40989441878), [#47](https://github.com/moon-byme/feneme-tech/actions/runs/40989458116), [#48](https://github.com/moon-byme/feneme-tech/actions/runs/40989472188), [#49](https://github.com/moon-byme/feneme-tech/actions/runs/40989490051), [#50](https://github.com/moon-byme/feneme-tech/actions/runs/40989562323), [#51](https://github.com/moon-byme/feneme-tech/actions/runs/40990301407).

**Limitações:**
- Em #1 e #5, os jobs de backend e frontend foram **pulados** (ainda não havia código): a execução terminou como sucesso sem testar nada. Nas outras 19, os dois jobs rodaram e passaram.
- O CI não bloqueava merge (a proteção da `main` só veio em 04/11), não tinha E2E e o frontend era só compilado.
- A medição preliminar de 9/9 (29/10, 18h53) foi substituída por este recorte.

## 6. Relatório histórico do pipeline da R1

[`relatorio-pipeline.md`](relatorio-pipeline.md) conferido contra a API do GitHub em 25/11: **51 execuções** (39 push, 12 pull_request), 51 com sucesso, **21 na `main`**, mediana de **51 s** e máximo de 1 min 55 s, e **103 testes** de backend na tag. Os números conferem. Os pontos de I-03 (PRs sem review e commits diretos na `main`), a ausência de E2E e a ausência de bloqueio de merge estão descritos no relatório; as correções aparecem no [relatório da R2](../release-2/relatorio-pipeline.md).

## 7. Tag e GitHub Release `v1.0.0`

| Item | Valor conferido |
| --- | --- |
| Tag | `v1.0.0` (tag leve) → commit `929d907`, de 29/10/2026 23h12, com o CI da `main` verde ([#51](https://github.com/moon-byme/feneme-tech/actions/runs/40990301407)) |
| GitHub Release | "Release 1 — Fundação e fluxo básico de gestão", rascunho criado em 29/10 23h12 e **publicado em 03/11/2026 20h45** por `moon-byme` |
| Notas | Listam FT-43/FT-54, FT-44, FT-55, FT-45, a execução 5/5 da FT-69 e as limitações da R1 (DoD incompleta e PRs sem revisão — FT-72) |
| Homologação (DoD Release) | **N/A justificado:** a R1 não tinha ambiente de homologação; o deploy automatizado passou a existir na R2 (FT-110) |

## 8. Riscos R01 e R02

| Risco | Inicial | Evidência | Residual | Situação |
| --- | --- | --- | --- | --- |
| R02 (FT-61) | P 3, S 5 → 15 | PR #4 (29/10), 20/20 casos não autorizados rejeitados, CI [#24](https://github.com/moon-byme/feneme-tech/actions/runs/40946472419) | P 4, S 5 → **10** (registrado em 29/10) | Decisão e evidência conferidas |
| R01 (FT-60) | P 2, S 5 → 20 | PR #7 (29/10, 19h24), 20/20 tentativas de acesso cruzado rejeitadas e 0 alterações indevidas (FT-29/FT-73), CI [#33](https://github.com/moon-byme/feneme-tech/actions/runs/40965460479); na R2, testes de acesso cruzado para a atualização de status (FT-48) | **Proposta:** P 4, S 5 → **10** | **Aguarda aprovação da equipe**; a FT-60 ainda tem o campo do residual vazio |

Justificativa da proposta para R01: a autorização por perfil e por Motorista responsável é aplicada no backend e verificada por regressão automática a cada push; a severidade de um acesso indevido continua máxima.

## 9. Itens que não cabem ao PO/DevOps

- **Revisão técnica independente** de FT-29, FT-69, FT-70 e FT-78: cabe ao QA da R2 (José), com a data atual.
- **Q-02 e lançamentos no Plano de Qualidade:** conferência na planilha oficial (seção 10).

## 10. Classificação preliminar para o fechamento da R1

Sujeita aos pareceres do QA e da SM:
- **Conformes:** Gherkin das cinco US (Q-03 100%), CI da `main` (Q-09 21/21), aceites individuais registrados, tag e GitHub Release, relatório do pipeline, R02 com residual.
- **Conformes com ressalva:** Q-08 (medida só em 25/11, retrospectivamente), FT-45/FT-55 (cobertura posterior ao aceite), R01 (residual proposto, ainda sem aprovação).
- **Não conformes:** revisão de PR antes do merge nas cinco US (I-03) e commits diretos na `main`.
- **Não aplicáveis à R1:** homologação/deploy e testes E2E no CI.


## 11. Complemento documental de 26/11/2026

A conferência de 25/11 e os fatos históricos foram preservados. Os registros posteriores permitem localizar os seguintes desdobramentos:

- As cinco US têm conferências documentais na FT-124 e evidências de testes e integração. O PO da R2 formalizou os aceites vigentes sem ressalva da [FT-55](https://feneme.atlassian.net/browse/FT-55?focusedCommentId=10293) e da [FT-45](https://feneme.atlassian.net/browse/FT-45?focusedCommentId=10294), após a integração dos testes complementares (PR #50 para FT-45). Os registros originais permanecem preservados.
- A [PR #57](https://github.com/moon-byme/feneme-tech/pull/57) foi aprovada e integrada: [relatório de qualidade R1](relatorio-qualidade.md). A [PR #56](https://github.com/moon-byme/feneme-tech/pull/56) consolidou o acompanhamento da retrospectiva da Sprint 0.
- A [FT-71](https://feneme.atlassian.net/browse/FT-71), [FT-76](https://feneme.atlassian.net/browse/FT-76) e [FT-77](https://feneme.atlassian.net/browse/FT-77) incorporaram os resultados e os links desta conferência. A Q-08 foi medida retrospectivamente (84%); a Q-09 da R1 é 21/21 (100%), incluindo duas execuções sem os jobs de código.
- A [FT-124](https://feneme.atlassian.net/browse/FT-124?focusedCommentId=10311) consolida a repriorização decorrente do feedback da R1, e a [avaliação interna por papel](https://feneme.atlassian.net/browse/FT-124?focusedCommentId=10312) está documentada como formato coletivo proposto para o critério 14.
- A revisão técnica adicional pelo QA da release seguinte é uma possibilidade de regularização interna, não uma nova exigência da disciplina: a verificação de QA já exercida na R1 e a conferência documental posterior pelo PO/DevOps são registros distintos. Caso se mantenha uma exigência específica de parecer independente, não atribuir esse parecer a quem não o emitiu.
- R01: evidências e proposta residual P4/S5=10 estão na [FT-60](https://feneme.atlassian.net/browse/FT-60?focusedCommentId=10263); falta decisão coletiva e lançamento. R02 permanece registrado com residual 10.

Pendências documentais devem ficar registradas como tal na DoD; a conferência administrativa não apaga fatos históricos. A homologação na R1 não era obrigatória segundo a orientação da disciplina. 

# QA — Sprint 2: plano de execução, evidências e pendências

**Projeto:** Feneme — Release 2  
**Sprint:** FT Sprint 2 (03/11/2026 a 12/11/2026)  
**Responsável QA:** José Araújo Agra Neto  
**Issues:** FT-32, FT-33, FT-47, FT-56, FT-74, FT-75, FT-81 e FT-88

> Este documento separa implementação de testes, execução comprovada e atividades que dependem de pessoas ou funcionalidades ainda não disponíveis. Os resultados abaixo são atualizados com base nas execuções efetivamente concluídas no CI.

> **Atualização de referências — 10/11/2026:** as PRs #25 e #27 foram integradas à `main`. Este documento registra os resultados Q-13/US-08, a comparação de trajetos da US-07 e a cobertura ampliada da consulta do Motorista, distinguindo evidências automatizadas de validações humanas pendentes.

## 1. Estado atual do repositório

- A branch principal contém o cadastro manual de até duas alternativas de trajeto (US-06 / FT-46), integrado pela PR #20, a integração Open-Meteo (US-08 / FT-47), integrada pela PR #23, e a medição Q-13, integrada pela PR #24.
- A PR #25 da FT-56 foi integrada à `main` em 10/11/2026 (merge commit `862507f83fab4917dd862bf7a03fce65df3cb649`). A comparação explícita apresenta duas alternativas lado a lado e informa quando há zero ou uma alternativa.
- O workflow executa `npm run e2e:smoke`, `npm run e2e:routes`, `npm run e2e:r1` e `npm run e2e:weather`. Na execução da `main` após a PR #25, os cenários `@US-07`, `@US-08`, `@R1` e smoke passaram.
- O arquivo `trajetos.feature` também contém cenários `@US-06` com etapas implementadas, mas eles não são selecionados por nenhum script do CI atual: `e2e:routes` seleciona somente `@US-07`, enquanto os demais scripts selecionam `@smoke`, `@R1` e `@US-08`. A lacuna está registrada nas FT-46 e FT-89 como ação de DevOps.
- A PR #22 integrou a validação visual da consulta de entregas do Motorista. A PR #27 também foi integrada à `main` em 10/11/2026 (merge commit `c76f97e9ab9a04e59aeaa4c9b4e94c48ab79c7f9`), acrescentando cobertura visual de lista vazia, atualização após reatribuição e conferência do status.
- Permanecem pendentes as funcionalidades de recomendação (US-09), atualização de status/histórico persistente (US-11/US-13) e acompanhamento do Gestor (US-12), conforme os respectivos itens do backlog.

## 2. FT-33 / FT-74 — Segurança de erros e logs (Q-06)

### Instrumentação adicionada

Arquivo: `backend/accounts/test_q06_tratamento_erros.py`

O arquivo contém 20 testes negativos identificados individualmente (`test_q06_01` a `test_q06_20`). Eles cobrem credenciais inválidas, ausência e adulteração de token, permissões negadas, dados obrigatórios ausentes e atribuição inválida.

Cada caso verifica:
- status HTTP esperado;
- ausência de traceback na resposta;
- ausência de senha e marcadores fictícios sensíveis na resposta;
- ausência desses mesmos valores nos logs capturados durante a requisição.

### Execução e evidência no CI

**Resultado confirmado:** 20/20 cenários Q-06 aprovados, com **0 exposições** de senha ou marcadores sensíveis nas respostas e nos logs, e sem traceback nas respostas/logs verificados. A suíte completa do backend executou 123 testes com resultado `OK`.

A execução ocorreu no CI da PR #17, commit `a40004bd92ffab404705b3d3fdf2b50d26338460`. Todos os jobs do workflow terminaram com sucesso.

**Evidência:** [GitHub Actions — CI da PR #17 (run 42732366544)](https://github.com/moon-byme/feneme-tech/actions/runs/42732366544)

### Como executar localmente

Na pasta `backend`:

```bash
python manage.py test accounts.test_q06_tratamento_erros -v 2
```

**Limitação da medição:** a instrumentação Q-06 cobre os endpoints e fluxos exercitados na época da PR #17. O tratamento de falhas da Open-Meteo é coberto separadamente pela medição Q-13, integrada pela PR #24.

**Verificação complementar do driver DA-SEG-JA-01 (FT-33):** além dos 20 cenários Q-06, `backend/weather/tests.py` contém `test_external_failures_return_503_with_generic_message`, que exercita 18 categorias de falha da dependência externa (timeout, conexão/DNS, HTTP 4xx/5xx, resposta vazia/inválida, dados ausentes ou inconsistentes e resposta excessiva). Em cada caso, verifica a resposta HTTP 503 genérica e inspeciona resposta e logs para impedir a exposição de URL, traceback e marcadores/detalhes da exceção externa. Essa cobertura complementar não é somada aos 20 cenários Q-06; são evidências distintas para fluxos distintos.

## 3. FT-32 — Resiliência à indisponibilidade da Open-Meteo

**Critério do driver:** 10 de 10 falhas simuladas (timeout, HTTP 5xx e previsão ausente) devem preservar cadastro e comparação manuais, exibir indisponibilidade e não confirmar recomendação climática sem dados.

**Resultado da medição:** 10/10 cenários comprovaram a continuidade dos fluxos manuais e o aviso de indisponibilidade. A parte de recomendação climática não foi medida: depende da US-09 (FT-57), ainda não implementada, e será verificada na Sprint 3. Essa separação também está registrada no risco R06 (FT-65).

### Implementação e medição

A integração Open-Meteo está na `main` pela PR #23:
- `GET /api/weather/locations/` lista as localidades de referência.
- `GET /api/weather/forecast/?location=<slug>` consulta a previsão diária de temperatura ambiente.
- O cliente trata timeout, falha de conexão/DNS, HTTP diferente de 200, JSON inválido, previsão ausente e valores inconsistentes.
- A API retorna uma mensagem genérica de indisponibilidade; a integração externa é simulada nos testes.

A PR [#24 — comprova dez falhas sem bloquear fluxos manuais](https://github.com/moon-byme/feneme-tech/pull/24) foi aprovada e integrada à `main` em 10/11/2026. Merge commit: `024f13492689b450a281278663d44a673d576d6b`.

O teste `test_ten_external_failure_scenarios_preserve_manual_flows`, em `backend/weather/tests.py`, executa dez cenários:
1. timeout;
2. conexão recusada;
3. HTTP 500;
4. HTTP 503;
5. HTTP 429;
6. HTTP 204;
7. JSON inválido;
8. estrutura sem previsão diária;
9. listas vazias;
10. temperatura nula.

Em cada cenário, verifica HTTP 503 com mensagem genérica, cadastra uma entrega, registra duas alternativas manuais e consulta a lista para confirmar que ambas continuam disponíveis para comparação. Ao final, confirma **10 entregas e 20 alternativas persistidas**, com distâncias e durações recuperadas corretamente.

### Execução e evidência no CI

**Resultado confirmado:** 10/10 cenários de falha com continuidade dos fluxos manuais. No workflow da PR #24:
- backend: 142 testes aprovados;
- frontend: build aprovado;
- regressão `@R1`: 10/10;
- cenários `@US-08`: 2/2;
- job E2E smoke: aprovado.

**Evidência:** [GitHub Actions — PR #24 (run 42844947365)](https://github.com/moon-byme/feneme-tech/actions/runs/42844947365).

**Limitação:** os cenários usam mocks. Comprovam o tratamento das falhas simuladas e a continuidade do cadastro/alternativas manuais; não medem disponibilidade real do provedor nem comprovam uma chamada externa real bem-sucedida. O risco residual de indisponibilidade do provedor deve continuar registrado e ser reavaliado pela equipe.

## 4. FT-75 — Facilidade de cadastro (Q-07)

**Meta original:** pelo menos 4 de 5 avaliadores concluem o cadastro corretamente, sem ajuda, em até 3 minutos.

Essa métrica exige participantes humanos. Não é válido substituir os cinco avaliadores por testes automatizados, nem declarar um resultado sem observação real.

### Protocolo de execução

1. Selecionar cinco avaliadores representativos, sem participação na implementação.
2. Usar o mesmo ambiente e a mesma versão do sistema para todos.
3. Apresentar o roteiro uma única vez, sem orientar durante a execução.
4. Iniciar o cronômetro quando o participante começar a tarefa.
5. Encerrar quando a entrega estiver salva corretamente ou quando atingir 3 minutos.
6. Registrar conclusão correta, tempo, pedido de ajuda e observações.
7. Considerar sucesso apenas quando a conclusão for correta, sem ajuda e em até 3 minutos.

### Planilha de coleta

| Avaliador | Concluiu corretamente? | Sem ajuda? | Tempo (mm:ss) | Sucesso (≤ 3 min)? | Observações |
|---|---|---|---|---|---|
| P1 | Sim (relato consolidado) | Sim (relato consolidado) | Não cronometrado | Não verificável | Teste remoto conduzido por José Araújo Agra Neto; conclusão descrita como rápida, sem tempo medido |
| P2 | Sim (relato consolidado) | Sim (relato consolidado) | Não cronometrado | Não verificável | Teste remoto conduzido por José Araújo Agra Neto; conclusão descrita como rápida, sem tempo medido |
| P3 | Sim (relato consolidado) | Sim (relato consolidado) | Não cronometrado | Não verificável | Teste remoto conduzido por José Araújo Agra Neto; conclusão descrita como rápida, sem tempo medido |
| P4 | Sim (relato consolidado) | Sim (relato consolidado) | Não cronometrado | Não verificável | Teste remoto conduzido por José Araújo Agra Neto; conclusão descrita como rápida, sem tempo medido |
| P5 | Sim (relato consolidado) | Sim (relato consolidado) | Não cronometrado | Não verificável | Teste remoto conduzido por José Araújo Agra Neto; conclusão descrita como rápida, sem tempo medido |

**Cálculo:** avaliadores com sucesso / 5. A meta é ≥ 4/5 (80%).

**Resultado da execução (11/11/2026):** os cinco participantes concluíram corretamente o cadastro e não solicitaram ajuda, conforme relato consolidado do QA. Os testes foram realizados **remotamente e conduzidos por José Araújo Agra Neto (QA)**.

**Limitação importante:** o cronômetro não foi utilizado e os tempos individuais não foram anotados. O responsável relata que as conclusões pareceram rápidas, mas essa impressão não comprova que cada participante concluiu em até 3 minutos. Por isso, o critério temporal permanece **não verificado** e não se declara que a meta quantitativa completa foi atingida.

| Resultado observado | Valor |
|---|---:|
| Participantes avaliados | 5 |
| Cadastros concluídos corretamente (relato do QA) | 5/5 |
| Participantes que não solicitaram ajuda (relato do QA) | 5/5 |
| Tempos individuais medidos | 0/5 |
| Conclusões comprovadas em até 3 minutos | Não verificável |
| Meta completa (≥ 4/5 corretos, sem ajuda e ≤ 3 min) | Ainda não comprovada |

**Rastreabilidade:** cinco avaliações remotas com a mesma versão do formulário, conduzidas por José Araújo Agra Neto. Os identificadores P1–P5 são anônimos e representam apenas a organização da coleta; os resultados de conclusão correta e ausência de ajuda foram informados pelo QA de forma consolidada, sem fichas individuais contemporâneas. Não foram criados tempos fictícios. Para comprovar a métrica original, será necessário repetir a medição com cronômetro e registrar o tempo real de cada participante, ou obter registros contemporâneos confiáveis.

**Responsabilidade pela medição Q-07:** QA — José Araújo Agra Neto. O resultado observado é favorável, mas a verificação da meta de três minutos permanece pendente.
## 5. FT-88 — Execução e rastreabilidade de QA na Sprint 2

### Estado das especificações

Os cenários R2 existentes estão em:
- `frontend/cypress/e2e/trajetos.feature`
- `frontend/cypress/e2e/previsao.feature`
- `frontend/cypress/e2e/recomendacao.feature`
- `frontend/cypress/e2e/status.feature`
- `frontend/cypress/e2e/historico.feature`

Os cenários R1 estão em `autenticacao.feature` e `entregas.feature`, além dos cenários de atribuição. A PR #15 já foi integrada à `main` e adicionou as etapas Cypress de entregas e atribuição, complementando as etapas de autenticação.

### Execução no CI

O workflow `.github/workflows/ci.yml` executa:
- `npm run e2e:smoke`, para os cenários selecionados pela tag `@smoke`;
- `npm run e2e:r1`, para a regressão da Sprint 1, selecionando 10 cenários marcados com `@R1`.

Na execução do CI da PR #18 (run `42736986570`), o job Cypress E2E smoke e o job de regressão `@R1` concluíram com sucesso. O log confirmou CT-22 e CT-23 aprovados (2/2) e 10 cenários `@R1` aprovados (10/10). Build do frontend e verificações/testes backend também concluíram com sucesso.

### Execução e evidências da PR #18

A PR [#18 — automatiza visibilidade das entregas do Motorista](https://github.com/moon-byme/feneme-tech/pull/18) foi aprovada e integrada à `main` em 09/11/2026 (horário local). O commit de merge é `9e23b4596cab31da9e454d8d6048a6b2ade2c6b4`.

- [Workflow CI da PR #18 — run 42736986570](https://github.com/moon-byme/feneme-tech/actions/runs/42736986570)
- [Artefato de evidências do Cypress](https://github.com/moon-byme/feneme-tech/actions/runs/42736986570/artifacts/13728016161)
- CT-22: motorista consulta suas entregas e não recebe a entrega atribuída ao outro motorista — aprovado.
- CT-23: acesso direto à entrega alheia retorna HTTP 404 e a resposta não contém origem, destino ou descrição — aprovado.
- Regressão `@R1`: 10/10 cenários aprovados.
- Build frontend, verificações Django e testes backend: jobs aprovados.

**Limite da evidência:** CT-22/CT-23 foram verificados por requisições à API (`cy.request`), não por interação com a tela do Motorista. A revisão da PR recomendou registrar essa limitação e, quando a interface estiver estável, acrescentar validação visual. Também foi sugerida a criação futura de um comando `e2e:r2`, separando a suíte R2 do smoke; isso ainda não foi implementado nesta atualização.

### Complementação visual da US-10 — PRs #22 e #27

O [PR #22 — valida consulta de entregas na interface do Motorista](https://github.com/moon-byme/feneme-tech/pull/22) foi integrado à `main` em **10/11/2026**, pelo commit `b1e48947332b6c4865c084651a35f739459b8688`. Seu cenário realiza login pela interface, verifica identificação, origem, destino e carga da entrega própria e confirma que a entrega do outro Motorista não aparece na lista.

- [CI do PR #22 — run 42838232088](https://github.com/moon-byme/feneme-tech/actions/runs/42838232088): workflow concluído com sucesso; smoke **5/5**, incluindo três cenários da US-10, e regressão R1 **10/10**.
- O acesso direto à entrega alheia continua verificado pelo CT-23 de API; a cobertura visual complementa essa evidência, sem substituí-la.

O [PR #27 — consulta de entregas revisada](https://github.com/moon-byme/feneme-tech/pull/27) acrescenta os cenários visuais de lista vazia e atualização após reatribuição, além da conferência explícita do status. **A PR #27 foi aprovada e integrada à `main` em 10/11/2026**, pelo merge commit `c76f97e9ab9a04e59aeaa4c9b4e94c48ab79c7f9`.

- [CI do PR #27 — run 42857524540](https://github.com/moon-byme/feneme-tech/actions/runs/42857524540), head `64c4506562e8cacac0de464bb7a8b1afcbbabc97`: quatro jobs aprovados; os logs confirmam smoke **7/7**, sendo dois cenários de autenticação e cinco da US-10, e regressão R1 **10/10**.
- O cenário visual de lista vazia intercepta uma resposta `200 []`. A resposta real da API sem atribuições possui cobertura em `backend/deliveries/test_ft58.py`.
- O cenário de reatribuição usa a API real como Gestor e verifica a remoção do cartão ao clicar em **Atualizar** na sessão do Motorista. Não comprova atualização automática de uma tela já aberta.
- A CI e a revisão da PR #27 foram concluídas e os testes estão integrados à `main`; isso não substitui o aceite formal do PO da FT-58.

### US-07 / FT-56 — comparação de alternativas

A PR [#25 — Comparar alternativas de trajeto](https://github.com/moon-byme/feneme-tech/pull/25) foi aprovada pelo PO e integrada à `main` em 10/11/2026 (merge commit `862507f83fab4917dd862bf7a03fce65df3cb649`). A implementação apresenta os dois valores cadastrados lado a lado quando existem duas alternativas e informa quando há zero ou uma, sem exibir comparação fictícia.

- Os cenários Cypress CT-06 e CT-19 cobrem duas, uma e zero alternativas.
- O CI após integração aprovou smoke, `@US-07` (3/3), regressão `@R1` (10/10) e `@US-08` (2/2), além dos jobs backend e frontend.
- Evidência: [GitHub Actions — main após PR #25 (run 42848223672)](https://github.com/moon-byme/feneme-tech/actions/runs/42848223672).
- A DoD da FT-56 ainda exige registro de verificação técnica independente por integrante diferente do autor/QA e aceite final do PO, conforme decisão registrada no Jira.

### Pendências de execução

- Criar definições de etapas para os demais cenários R2 somente depois que as interfaces e endpoints correspondentes estiverem disponíveis.
- Executar os cenários de sucesso e exceção, anexando relatórios e screenshots quando houver falha.
- Criar, em alteração futura, um comando `e2e:r2` para executar a suíte R2 separadamente, quando houver conjunto suficiente de cenários executáveis; manter `@smoke` restrito ao caminho crítico.
- Registrar um Bug por defeito reproduzível, com passos, esperado/observado, severidade, evidência e vínculo à US/PR.
- Conferir a DoD de cada história candidata à conclusão. Status Done isolado não é evidência de teste nem aceite de QA.
- Preservar a distinção entre a cobertura visual integrada pelas PRs #22 e #27 e o aceite formal ainda pendente da FT-58.
- Verificar a correção da branch `fix/corrigir-temperatura` quando ela estiver acessível e integrada; não presumir que a correção está presente na branch principal.

### Evidências atuais

- Os arquivos `.feature` existem e têm rastreabilidade por US/CT.
- As etapas Cypress de autenticação, entregas e atribuição estão na `main`; a PR #18 adicionou os passos de API para CT-22/CT-23.
- O CI executou smoke (incluindo CT-22/CT-23) e regressão R1 (10 cenários), todos aprovados no run 42736986570.
- A validação visual de consulta própria foi integrada pelo PR #22, com CI aprovado no run 42838232088.
- Os complementos de lista vazia, reatribuição e status passaram no CI do PR #27 (run 42857524540); sua integração foi concluída pelo commit `c76f97e`.
- Nenhum Bug novo deve ser criado sem defeito confirmado.

**Resultado:** preservam-se os resultados históricos de regressão R1 (10/10) e CT-22/CT-23 por API (2/2) da PR #18. A consulta própria também possui validação visual integrada pelo PR #22. A PR #27 foi integrada após smoke 7/7 e regressão R1 10/10 aprovados. A cobertura R2 continua parcial; esses resultados não comprovam a execução de todas as histórias nem o aceite formal da FT-58.

## 6. Critérios de encerramento por issue

| Issue | Entrega de QA | Situação honesta |
|---|---|---|
| FT-32 | 10 cenários de falha Open-Meteo com continuidade manual | Q-13 aprovada 10/10 para continuidade dos fluxos manuais e aviso de indisponibilidade; recomendação climática depende da US-09 (FT-57), prevista para Sprint 3; risco residual do provedor externo permanece |
| FT-33 | Verificação de segurança das respostas e logs | Q-06: 20/20 aprovados e 0 exposições; cobertura complementar de 18 categorias de falha Open-Meteo verifica resposta genérica e ausência de detalhes externos nos logs/respostas. Evidências: [CI PR #17](https://github.com/moon-byme/feneme-tech/actions/runs/42732366544) e [CI PR #24](https://github.com/moon-byme/feneme-tech/actions/runs/42844947365). Mantém-se a ressalva de que US-09/FT-57 ainda não foi implementada. |
| FT-74 | Q-06: 0 exposição em 20 cenários | Atingido: 20/20 aprovados, 0 exposições na resposta e nos logs; suíte backend com 123 testes `OK` |
| FT-75 | Q-07: ≥ 4/5 em até 3 min | Cinco participantes concluíram corretamente e sem ajuda, conforme relato consolidado do QA. Teste remoto conduzido por José Araújo Agra Neto. Tempos não foram cronometrados; limite de 3 min e meta completa permanecem não verificados. Repetir medição cronometrada e registrar tempos reais antes de declarar a meta atingida. |
| FT-47 | US-08: previsão e tratamento de indisponibilidade | PR #23 integrada; E2E `@US-08` 2/2; demonstração real registrada na FT-47 em 10/11/2026 (João Pessoa: máx. 30,3 °C / mín. 25,0 °C, conferida com o JSON da Open-Meteo); aceite do PO registrado em 10/11/2026 |
| FT-56 | US-07: comparação de alternativas | PR #25 integrada; CT-06/CT-19 e CI aprovados; aguarda verificação técnica independente e aceite final do PO |
| FT-81 | Q-13: continuidade dos fluxos manuais | 10/10 falhas simuladas; 10 entregas e 10 alternativas persistidas; Resultado R2 registrado na planilha, pendente de conferência da equipe |
| FT-58 | US-10: consulta de entregas do Motorista | PRs #22 e #27 integradas; API e interface cobertas, incluindo lista vazia e reatribuição; revisão pós-integração e aceite formal do PO ainda pendentes |
| FT-88 | Cenários, smoke, bugs, indicadores e DoD de R2 | R1: 10/10 e CT-22/CT-23 por API: 2/2 na PR #18; consulta visual integrada pela PR #22; complementos da PR #27 integrados (`c76f97e`), com smoke 7/7 e R1 10/10 aprovados. Cobertura R2 e aceite das histórias permanecem parciais. |

## 7. Próximas dependências

1. Equipe: manter o risco residual de indisponibilidade real da Open-Meteo registrado; a Q-13 mede falhas simuladas, não disponibilidade externa.
2. QA/equipe: repetir a medição Q-07 com cronômetro, registrar os cinco tempos reais e obter conferência/aceite formal antes de declarar a meta atingida.
3. QA: completar etapas Cypress dos demais fluxos R2 quando houver funcionalidades e contratos; manter a cobertura visual da US-10 e avaliar a separação da suíte em `e2e:r2`.

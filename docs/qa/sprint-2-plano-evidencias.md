# QA — Sprint 2: plano de execução, evidências e pendências

**Projeto:** Feneme — Release 2  
**Sprint:** FT Sprint 2 (03/11/2026 a 12/11/2026)  
**Responsável QA:** José Araújo Agra Neto  
**Issues:** FT-32, FT-33, FT-74, FT-75 e FT-88

> Este documento separa implementação de testes, execução comprovada e atividades que dependem de pessoas ou funcionalidades ainda não disponíveis. Não registrar como aprovado nenhum cenário que não tenha sido executado.

## 1. Estado do repositório na auditoria

- Existem oito arquivos Gherkin para fluxos de autenticação, entregas, trajetos, previsão, recomendação, status e histórico.
- A única definição de etapas Cypress encontrada na branch principal é `frontend/cypress/support/step_definitions/autenticacao.steps.ts`.
- O workflow `.github/workflows/ci.yml` executa `npm run e2e:smoke`, filtrando `@smoke`. No arquivo de autenticação, as tags `@smoke` estão nos dois logins válidos da R1. Portanto, CI verde nesse job não comprova execução dos cenários R2.
- O código da branch principal ainda não apresenta cliente/serviço/endpoint Open-Meteo nem recursos persistidos de alternativas de trajeto e recomendação. O modelo de entrega expõe apenas o status inicial PENDENTE; não há fluxo de atualização/histórico de status implementado nessa branch.
- Há testes backend existentes para autenticação, cadastro, consulta, atribuição e isolamento de entregas. Eles não substituem a execução E2E de todos os critérios das histórias R2.

## 2. FT-33 / FT-74 — Segurança de erros e logs (Q-06)

### Instrumentação adicionada

Arquivo: `backend/accounts/test_q06_tratamento_erros.py`

O arquivo contém 20 testes negativos identificados individualmente (`test_q06_01` a `test_q06_20`). Eles cobrem credenciais inválidas, ausência e adulteração de token, permissões negadas, dados obrigatórios ausentes e atribuição inválida.

Cada caso verifica:
- status HTTP esperado;
- ausência de traceback na resposta;
- ausência de senha e marcadores fictícios sensíveis na resposta;
- ausência desses mesmos valores nos logs capturados durante a requisição.

### Como executar

Na pasta `backend`:

```bash
python manage.py test accounts.test_q06_tratamento_erros -v 2
```

**Resultado:** pendente de execução no ambiente com dependências e PostgreSQL configurados. O número de testes escritos (20) não deve ser confundido com 20 testes aprovados. Após executar, registrar o resultado real do runner e o link do workflow/artefato.

**Limitação da medição:** a instrumentação cobre os endpoints e fluxos que existem atualmente na branch principal. Ela não comprova o tratamento de exceções de serviços ainda inexistentes, incluindo Open-Meteo.

## 3. FT-32 — Resiliência à indisponibilidade da Open-Meteo

**Critério do driver:** 10 de 10 falhas simuladas (timeout, HTTP 5xx e previsão ausente) devem preservar cadastro e comparação manuais, exibir indisponibilidade e não confirmar recomendação climática sem dados.

**Bloqueio encontrado:** não foi localizado cliente Open-Meteo, serviço meteorológico ou endpoint de previsão na branch principal. Sem a implementação e seu contrato, não é possível escrever testes de integração válidos sem inventar interfaces ou produzir testes que passam sem testar o sistema real.

**Ação necessária da equipe de desenvolvimento:** disponibilizar o cliente/serviço e o ponto de integração de previsão, mantendo a dependência externa isolada e injetável/mockável. Quando disponível, QA deverá simular pelo menos:
1. timeout;
2. HTTP 500;
3. HTTP 502;
4. HTTP 503;
5. resposta sem corpo;
6. JSON inválido;
7. campo de temperatura ausente;
8. lista de previsões vazia;
9. latência acima do limite;
10. erro de conexão/DNS.

Para cada caso, verificar que o cadastro e a comparação manuais continuam acessíveis, que a interface informa indisponibilidade e que nenhuma recomendação climática é marcada como confirmada.

**Resultado:** não medido — bloqueado por ausência da integração no código auditado.

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
| P1 | Pendente | Pendente | Pendente | Pendente | |
| P2 | Pendente | Pendente | Pendente | Pendente | |
| P3 | Pendente | Pendente | Pendente | Pendente | |
| P4 | Pendente | Pendente | Pendente | Pendente | |
| P5 | Pendente | Pendente | Pendente | Pendente | |

**Cálculo:** avaliadores com sucesso / 5. A meta é ≥ 4/5 (80%).

**Resultado:** não medido — depende de cinco participantes e da versão funcional do formulário de cadastro. O responsável descrito no texto da FT-75 é Lethycia, embora a atribuição atual do Jira esteja em José; confirmar a responsabilidade com o PO antes do encerramento.

## 5. FT-88 — Execução e rastreabilidade de QA na Sprint 2

### Estado das especificações

Os cenários R2 existentes estão em:
- `frontend/cypress/e2e/trajetos.feature`
- `frontend/cypress/e2e/previsao.feature`
- `frontend/cypress/e2e/recomendacao.feature`
- `frontend/cypress/e2e/status.feature`
- `frontend/cypress/e2e/historico.feature`

Também há cenários R1 em `autenticacao.feature` e `entregas.feature`, além de atribuição.

### Pendências de execução

- Criar definições de etapas para os cenários R2 somente depois que as interfaces e endpoints correspondentes estiverem disponíveis.
- Executar os cenários de sucesso e exceção, anexando relatórios e screenshots quando houver falha.
- Definir com DevOps o conjunto smoke. O pipeline atual seleciona apenas `@smoke`; não marcar cenários não executáveis ou não validados como smoke.
- Registrar um Bug por defeito reproduzível, com passos, esperado/observado, severidade, evidência e vínculo à US/PR.
- Conferir a DoD de cada história candidata à conclusão. Status Done isolado não é evidência de teste nem aceite de QA.
- Verificar a correção da branch `fix/corrigir-temperatura` quando ela estiver acessível e integrada; não presumir que a correção está presente na branch principal.

### Evidências atuais

- Os arquivos `.feature` existem e têm rastreabilidade por US/CT.
- A implementação Cypress de etapas observada na branch principal cobre apenas autenticação.
- O workflow smoke existente comprova apenas os cenários que de fato carregam `@smoke` e são selecionados pelo comando. Não comprova os cenários R2 ainda sem etapas.
- Nenhum Bug novo deve ser criado sem defeito confirmado.

**Resultado:** parcialmente preparado; execução funcional R2 pendente da disponibilização das funcionalidades e dos contratos de integração.

## 6. Critérios de encerramento por issue

| Issue | Entrega de QA | Situação honesta |
|---|---|---|
| FT-32 | 10 cenários de falha Open-Meteo com continuidade manual | Bloqueado: integração não localizada |
| FT-33 | Verificação de segurança das respostas e logs | Instrumentação adicionada via FT-74; aguarda execução |
| FT-74 | Q-06: 0 exposição em 20 cenários | 20 testes escritos; resultado ainda não medido |
| FT-75 | Q-07: ≥ 4/5 em até 3 min | Protocolo pronto; aguarda avaliadores humanos |
| FT-88 | Cenários, smoke, bugs, indicadores e DoD de R2 | Parcial; cenários R2 ainda não executáveis na branch auditada |

## 7. Próximas dependências

1. Desenvolvedores: disponibilizar a integração Open-Meteo e as funcionalidades R2 ausentes.
2. DevOps: executar a suíte Q-06 no CI e publicar artefatos; alinhar a seleção smoke com QA.
3. PO: confirmar o responsável final pela FT-75 e aprovar os critérios de usabilidade.
4. Equipe: disponibilizar ambiente funcional e cinco avaliadores para a medição Q-07.
5. QA: completar etapas Cypress, executar cenários, registrar bugs confirmados e atualizar resultados com evidências reais.


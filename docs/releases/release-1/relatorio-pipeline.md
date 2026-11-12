# Relatório do Pipeline — Release 1

**Projeto:** Feneme — Gestão Inteligente de Transporte de Alimentos
**Release:** R1 (06/10/2026 a 29/10/2026) · **Tag:** `v1.0.0` (commit `929d907`, 29/10/2026 23:12)
**Responsável pelo relatório:** João Paulo de Araujo (DevOps na R2)
**Rastreabilidade:** FT-89 (pendências de PO/DevOps do feedback da R1). O relatório do pipeline da R2 pertence à FT-92 e não substitui este documento.

> Este relatório é **histórico**. Ele descreve o pipeline como existia na R1 e não aplica aprovações nem correções retroativas. Horários em America/Sao_Paulo (UTC−3).

## 1. Fontes consultadas

| Fonte | Como foi obtida |
| --- | --- |
| Execuções do GitHub Actions | `gh run list --created "2026-10-06..2026-10-29"` e, para os commits de 29/10 à noite (30/10 em UTC), `gh run list --branch main --created "2026-10-30"` (workflow `CI`) |
| Revisões dos PRs #1 a #10 | `gh pr view <n> --json reviews,mergedAt,mergedBy,...` |
| Workflow e evolução | Histórico de `.github/workflows/ci.yml` no Git |
| Commits na `main` | `git log --first-parent main` de 22/10 a 29/10 |
| Proteção da `main` e R2 | `docs/devops/protecao-main.md` e comentários da FT-89 |

## 2. O que o pipeline verificava na R1

O workflow `CI` foi criado em **22/10/2026** (commit `e7caa58`). Antes dessa data, **não havia integração contínua**. Por isso, não existem execuções entre 06/10 e 21/10.

**Gatilhos:** `push` em qualquer branch, `pull_request` para a `main` e execução manual (`workflow_dispatch`).

| Job | Etapas | Observação na R1 |
| --- | --- | --- |
| `Detect application components` | Detecta `backend/manage.py` e `frontend/package.json` | Se o componente não existe, o job correspondente é **pulado**, e a execução termina como sucesso |
| `Backend - Django checks and tests` | Instala dependências, roda `manage.py check` e `manage.py test` | Até 29/10, os testes rodavam em **SQLite** porque o CI não definia `DB_NAME`. A partir do PR #3 (29/10), passaram a usar **PostgreSQL** instalado no runner |
| `Frontend - build and tests` | `npm ci`/`npm install` e `npm run build` (`tsc -b && vite build`) | O `package.json` **não tinha script `test`**, então a etapa de testes do frontend era pulada com aviso. Na prática, o frontend era verificado só por compilação TypeScript e build |

**Evolução do workflow na R1:**

| Data | Commit | Mudança |
| --- | --- | --- |
| 22/10 | `e7caa58` | Criação do workflow com os três jobs acima |
| 29/10 | `cfddfc4` (PR #3) | Remoção do Docker e inclusão do PostgreSQL local no job de backend |

Na tag `v1.0.0`, o backend tinha **103 métodos de teste** em 6 arquivos (`accounts/` e `deliveries/`), executados pelo job de backend. Testes de interface ou E2E **não existiam** no CI.

## 3. Execuções na R1

**Total: 51 execuções, 51 com sucesso e 0 com falha.**

| Recorte | Execuções |
| --- | --- |
| Evento `push` | 39 |
| Evento `pull_request` | 12 |
| Branch `main` | 21 (todas com sucesso) |
| Outras branches | 30 (todas com sucesso) |

### 3.1 Execuções na `main`

| Data/hora | Origem | Run |
| --- | --- | --- |
| 22/10 21:12 | Commit direto: "configurando estrutura do repositório" | [39876721757](https://github.com/moon-byme/feneme-tech/actions/runs/39876721757) |
| 26/10 18:50 | Commit direto: "Adição dos requisitos funcionais" | [40407702577](https://github.com/moon-byme/feneme-tech/actions/runs/40407702577) |
| 26/10 19:22 | Commit direto: "remoção do código na main" | [40411912590](https://github.com/moon-byme/feneme-tech/actions/runs/40411912590) |
| 27/10 14:39 | Merge do PR #1 | [40552576742](https://github.com/moon-byme/feneme-tech/actions/runs/40552576742) |
| 29/10 12:45 | Merge do PR #2 | [40904717652](https://github.com/moon-byme/feneme-tech/actions/runs/40904717652) |
| 29/10 14:38 | Merge do PR #3 | [40923195980](https://github.com/moon-byme/feneme-tech/actions/runs/40923195980) |
| 29/10 14:58 | Merge do PR #3, segunda execução (causa não identificada nos dados exportados) | [40926450769](https://github.com/moon-byme/feneme-tech/actions/runs/40926450769) |
| 29/10 17:09 | Merge do PR #4 | [40946472419](https://github.com/moon-byme/feneme-tech/actions/runs/40946472419) |
| 29/10 18:38 | Merge do PR #5 | [40959484596](https://github.com/moon-byme/feneme-tech/actions/runs/40959484596) |
| 29/10 19:10 | Merge do PR #6 | [40963771703](https://github.com/moon-byme/feneme-tech/actions/runs/40963771703) |
| 29/10 19:24 | Merge do PR #7 | [40965591244](https://github.com/moon-byme/feneme-tech/actions/runs/40965591244) |
| 29/10 19:46 | Merge do PR #8 | [40968402490](https://github.com/moon-byme/feneme-tech/actions/runs/40968402490) |
| 29/10 20:00 | Merge do PR #9 | [40970019321](https://github.com/moon-byme/feneme-tech/actions/runs/40970019321) |
| 29/10 20:06 | Merge do PR #10 | [40970818209](https://github.com/moon-byme/feneme-tech/actions/runs/40970818209) |
| 29/10 22:32 | Commit direto: "atualização do readme" | [40986454546](https://github.com/moon-byme/feneme-tech/actions/runs/40986454546) |
| 29/10 23:03 | Commit direto: exclusão de `ata-retrospectiva.md` | [40989441878](https://github.com/moon-byme/feneme-tech/actions/runs/40989441878) |
| 29/10 23:03 | Commit direto: exclusão de `ata-review.md` | [40989458116](https://github.com/moon-byme/feneme-tech/actions/runs/40989458116) |
| 29/10 23:03 | Commit direto: exclusão de `dod-sprint-1.md` | [40989472188](https://github.com/moon-byme/feneme-tech/actions/runs/40989472188) |
| 29/10 23:03 | Commit direto: exclusão de `metricas-e-impedimentos.md` | [40989490051](https://github.com/moon-byme/feneme-tech/actions/runs/40989490051) |
| 29/10 23:04 | Commit direto: "Add files via upload" | [40989562323](https://github.com/moon-byme/feneme-tech/actions/runs/40989562323) |
| 29/10 23:12 | Commit direto: "atualização do readme 2" (**commit da tag `v1.0.0`**) | [40990301407](https://github.com/moon-byme/feneme-tech/actions/runs/40990301407) |

### 3.2 Execuções em outras branches

| Branch | Execuções | Período |
| --- | --- | --- |
| `feature/ft-54-login-motorista` (PR #2) | 7 | 28/10 00:07 a 29/10 12:46 |
| `test/isolamento-entregas-motoristas` (PR #7) | 3 | 29/10 19:22 a 19:23 |
| `test/validacao-funcional` (PRs #8 e #10) | 4 | 29/10 19:40 a 19:59 |
| `docs/sprint-1-fechamento` (PR #9) | 3 | 29/10 19:53 a 20:44 |
| `feature/login` (PR #1) | 3 | 26/10 19:12 a 27/10 14:38 |
| `fix/corrigir-temperatura` | 2 | 26/10 19:13 a 19:25 |
| `refactor/execucao-local` (PR #3) | 2 | 29/10 14:33 a 14:37 |
| `test/ft-78-credenciais-sessoes-invalidas` (PR #4) | 2 | 29/10 16:44 a 17:09 |
| `feature/web-entregas-motorista` (PR #5) | 2 | 29/10 18:35 a 18:38 |
| `teste-isolamento-motoristas` (PR #6) | 2 | 29/10 19:08 a 19:10 |

**Concentração:** 38 das 51 execuções (75%), 9 dos 10 merges e 7 dos 10 commits diretos aconteceram em **29/10**, último dia da release.

## 4. Falhas, causas e correções

**Nenhuma execução da R1 terminou com falha**, portanto não há causas ou correções de pipeline a registrar.

Esse resultado precisa ser lido com cautela, porque um "sucesso" na R1 nem sempre significava código verificado:

- **22/10 e 26/10 19:22 (`main`):** nessas versões não havia `backend/manage.py` nem `frontend/package.json`, então os jobs de backend e frontend foram pulados. O sucesso comprova apenas que o workflow rodou.
- **Até o PR #3:** os testes de backend rodavam em SQLite, banco diferente do PostgreSQL usado pela aplicação.
- **Frontend:** só o build era verificado. Nenhum teste de interface rodava.

Os problemas reais da R1 estavam no **processo** em torno do pipeline, e não nas execuções (seções 5 e 6).

## 5. Limitações do CI na R1

1. **Sem testes Cucumber/Cypress.** Não havia cenários BDD nem E2E no CI. O Cypress só foi integrado em 03/11, pelo PR #12, já na R2.
2. **Sem testes de frontend.** Não existia script `test` no `frontend/package.json`.
3. **CI não bloqueava merge.** Sem proteção da `main`, o resultado do CI não era condição para integrar. Em 6 PRs, o merge ocorreu **menos de 1 minuto depois do início da execução do CI do PR**: #1 (34 s), #3 (39 s), #4 (5 s), #5 (9 s), #6 (12 s) e #7 (58 s). Isso indica que o resultado não foi aguardado.
4. **Banco de testes divergente** (SQLite) até 29/10, como descrito na seção 4.
5. **CI disponível só nos últimos 8 dias** da release (22/10 a 29/10), e não desde o início em 06/10.

## 6. Proteção da `main` e aprovação de PRs

**A `main` não tinha proteção na R1.** Isso permitiu commits diretos e merges sem revisão.

### 6.1 PRs da R1

| PR | Autor | Merge por | Aprovação | Tempo entre abertura e merge |
| --- | --- | --- | --- | --- |
| #1 | moon-byme | moon-byme | Nenhuma | 38 s |
| #2 | jpauloaraujo | jpauloaraujo | Nenhuma | 1 dia e 12 h |
| #3 | moon-byme | moon-byme | Nenhuma | 44 s |
| #4 | moon-byme | moon-byme | Nenhuma | 11 s |
| #5 | moon-byme | moon-byme | Nenhuma | 14 s |
| #6 | moon-byme | moon-byme | Nenhuma | 18 s |
| #7 | moon-byme | moon-byme | Nenhuma | 1 min 3 s |
| #8 | moon-byme | jpauloaraujo | Nenhuma | 2 min 23 s |
| #9 | jpauloaraujo | LittleNeto | Nenhuma (*) | 3 min 57 s |
| #10 | moon-byme | jpauloaraujo | Nenhuma | 7 min 6 s |

(*) O PR #9 recebeu apenas um comentário automático do Copilot, que informou não ter conseguido revisar por falta de cota. Não houve revisão humana.

**Resultado:** **0 de 10 PRs** (0%) tiveram aprovação de outro integrante antes do merge, o que confirma o impedimento I-03 e o indicador Q-04 = 0%. Em 7 PRs, o próprio autor fez o merge.

### 6.2 Commits diretos na `main`

Foram feitos **10 commits diretamente na `main`**, sem PR:

| Data | Commits |
| --- | --- |
| 22/10 | `e7caa58` — estrutura do repositório |
| 26/10 | `de2b3d9` — requisitos funcionais; `c48007d` — remoção do código na main |
| 29/10, 22:32 a 23:12 | `bbb14a9` e `929d907` (README), `84e7e13`, `d26b99c`, `d106cfe`, `b6209f7` (exclusão de atas e DoD da Sprint 1) e `0b67ae4` (upload de arquivos) |

A tag `v1.0.0` aponta para `929d907`, um **commit direto** feito depois do último PR.

Os 7 commits diretos de 29/10 à noite passaram no CI (seção 3.1), inclusive o da tag ([run 40990301407](https://github.com/moon-byme/feneme-tech/actions/runs/40990301407)). Mesmo assim, entraram na `main` sem revisão, e o CI rodou **depois** da integração, não antes.

## 7. R1 × R2

| Aspecto | R1 | R2 (até 10/11/2026, segundo a FT-89) |
| --- | --- | --- |
| Proteção da `main` | Inexistente | Ativada em 04/11: PR obrigatório, 1 aprovação, checagens de CI obrigatórias, regras aplicadas a administradores |
| Aprovação de PRs | 0/10 | Todos os PRs integrados depois de 04/11 aprovados por outro integrante. Única exceção na S2: PR #12 (03/11), anterior à proteção |
| Commits diretos na `main` | 10 (todos com CI verde, executado depois de já estarem na `main`) | Bloqueados pela proteção |
| CI como condição de merge | Não | Sim: `Backend`, `Frontend` e `E2E (@smoke)` obrigatórios |
| Testes E2E/BDD | Nenhum | Cucumber/Cypress no CI desde o PR #12 (03/11). Regressão `@R1` (PR #15), `@smoke` com CT-22 e CT-23 (PR #18), `@US-07` e `@US-08` |
| Banco nos testes de backend | SQLite até 29/10, depois PostgreSQL | PostgreSQL |
| Falhas registradas | 0 em 51 execuções | 7 em 69 execuções na S2 (03 a 10/11), todas em branches de feature e corrigidas antes do merge; `main` com 100% de sucesso |

Os números da R2 são parciais. O consolidado da release fica na FT-92.

## 8. Avaliação

**Estabilidade:** o pipeline foi **estável, mas pouco exigente**. Não houve nenhuma falha nas 51 execuções. Isso se explica menos pela qualidade do código e mais pelo escopo reduzido do CI: build do frontend, testes de backend com SQLite na maior parte do período, nenhum teste E2E e jobs pulados quando não havia código. Além disso, o pipeline **não funcionava como portão de qualidade**: os merges não esperavam o resultado, e a `main` aceitava commits diretos, inclusive o commit da tag `v1.0.0`.

**Pendências da R1 tratadas na R2:**
- Proteção da `main` e aprovação obrigatória (I-03): resolvido em 04/11.
- Cucumber/Cypress no CI: resolvido a partir de 03/11.
- PostgreSQL nos testes: resolvido em 29/10, ainda na R1.

**Pendências remanescentes:**
- Os cenários `@US-06` (FT-46) têm etapas implementadas, mas não estão em nenhuma seleção de tags do CI.
- O frontend continua sem testes unitários (`npm test`). A cobertura de interface é feita só pelo E2E.
- O deploy automatizado em homologação ainda não existe (FT-110, Sprint 3).
- O histórico da R1 é mantido como está. Os PRs sem aprovação e os commits diretos **não** recebem aprovação retroativa.

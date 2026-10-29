# Métricas e impedimentos — Sprint 1 (FT Sprint 1)

**Período:** 21/10/2026 a 29/10/2026 | **Release:** R1  
**Fonte:** Jira (projeto FT, board 1), estado final das 23 issues da FT Sprint 1 com story points, após a atualização de encerramento. A consulta intermediária das 20h10 foi mantida apenas como referência histórica.  
**Responsável pelo registro:** SM — João Paulo de Araujo

Este documento consolida os indicadores observados durante a Sprint 1 e os impedimentos discutidos na reunião de encerramento e retrospectiva. Os valores representam o estado do Jira no horário da consulta indicado acima.

## 1. Burndown

![Burndown da Sprint 1](img/burndown-sprint-1.png)

Story points restantes ao fim de cada dia:

| Dia | 21/10 | 22/10 | 23/10 | 24/10 | 25/10 | 26/10 | 27/10 | 28/10 | 29/10 (20h10) |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Sprint completa (64 SP) | 64 | 64 | 64 | 64 | 64 | 51 | 51 | 49 | **0** |
| Ideal | 64 | 56 | 48 | 40 | 32 | 24 | 16 | 8 | 0 |
| Histórias de usuário (15 SP) | 15 | 15 | 15 | 15 | 15 | 2 | 2 | 0 | **0** |

### Análise do burndown

- Não houve conclusão de itens nos cinco primeiros dias (21 a 25/10). A partir de 26/10, as entregas ocorreram em blocos: FT-43, FT-44, FT-45 e FT-55 (13 SP) em 26/10; FT-54 (2 SP) em 28/10; e os demais itens foram concluídos até o fechamento de 29/10.
- A consulta intermediária realizada às 20h10 de 29/10 apontava 36 SP ainda não concluídos. Após essa consulta, os 13 itens restantes foram atualizados para Done no Jira. Por isso, o estado final da sprint registra **0 SP restantes**, em concordância com o gráfico `burndown-sprint-1.png`.
- Quatro US foram movidas para Done em 26/10, antes do merge do PR #1 em 27/10 e sem a DoD da US integralmente marcada. Esse fato foi discutido na retrospectiva e motivou ações para reforçar o fluxo de revisão e validação.

A equipe avaliou que a distribuição do trabalho ao longo da sprint precisa melhorar. Embora todo o escopo tenha sido concluído até o encerramento, o progresso ficou concentrado nos últimos dias; para a Sprint 2, foi recomendado acompanhar o fluxo de entrega desde o início.

## 2. Velocity

| Indicador | Valor |
|---|---:|
| Comprometido na sprint | 23 itens / 64 SP |
| Concluído (Done) | **23 itens / 64 SP** |
| **Velocity da sprint** | **64 SP** (100% do comprometido) |
| Velocity funcional (US) | 15 SP de 15 SP (100%) |
| Em andamento ao final da sprint | **0 itens / 0 SP** |

### Atualização dos itens inicialmente pendentes

Na consulta intermediária das 20h10, 13 itens (36 SP) ainda apareciam em In Review ou In Progress. No estado final consultado para o encerramento, todos esses itens foram atualizados para **Done**, totalizando 23 de 23 issues concluídas e 64 de 64 SP entregues. Portanto, não há itens da Sprint 1 que precisem retornar ao backlog por não conclusão.

A velocity observada foi de **64 SP**. Esse resultado deve ser considerado como dado histórico para a Sprint 2, mas não como capacidade garantida: o PO e o SM devem avaliar disponibilidade dos integrantes, complexidade, dependências e prontidão dos itens antes de definir o próximo compromisso.

## 3. Impedimentos

| ID | Data | Descrição | Impacto | Status | Resolução / encaminhamento |
|---|---|---|---|---|---|
| I-01 | 26/10/2026 | Desvio do fluxo de Pull Request: o código das US-01, US-03, US-04 e US-05 foi commitado diretamente na `main` (`de2b3d9`) e removido em seguida (`c48007d`). | A `main` ficou sem o código entre 26/10 às 19h22 e 27/10 às 14h38, aproximadamente 19 horas. As quatro US foram marcadas Done nesse intervalo. | **Resolvido** | O código foi reintegrado pelo PR #1 (revert `86d9eba`, merge `8496e3a` em 27/10/2026). Na retrospectiva, a equipe definiu como ação reforçar a proteção da branch `main` e exigir revisão antes dos merges. |
| I-02 | 29/10/2026 | Ambiente Docker substituído por execução local (PR #3). | A alteração do procedimento de execução ocorreu no último dia da sprint e exigiu atualização das instruções para evitar divergência entre os integrantes. | **Resolvido** | As instruções foram atualizadas em `README_IMPLEMENTACAO_SPRINT1.md`. A equipe deverá manter o procedimento documentado e comunicar alterações de ambiente durante a sprint. |
| I-03 | 29/10/2026 | Nenhum PR recebeu revisão de outra pessoa antes do merge (0 de 8). | Q-04 ficou em 0%; o critério de revisão de código da DoD das US não foi atendido. | **Aberto** | A equipe definiu que todo PR deverá receber revisão de outro integrante antes do merge. Também foi estabelecida a ação de configurar proteção da `main`, com acompanhamento pelo SM durante a Sprint 2. |

## 4. Decisões e encaminhamentos da reunião

Com base nos indicadores, a equipe registrou os seguintes encaminhamentos:

1. Utilizar a velocity final de 64 SP como referência histórica, sem assumir que esse volume será automaticamente repetido na Sprint 2.
2. Distribuir as atividades ao longo da sprint, buscando concluir pelo menos um item até o terceiro dia.
3. Exigir revisão por outro integrante antes do merge de cada Pull Request.
4. Atualizar as issues com os links dos PRs e evidências correspondentes.
5. Não considerar uma US concluída sem os critérios aplicáveis da DoD verificados e o aceite do PO registrado.
6. Acompanhar o impedimento I-03 e verificar a configuração de proteção da branch `main`.

Os responsáveis, prazos e critérios de verificação dessas ações estão detalhados em `ata-retrospectiva.md`.

## 5. Referência para a Sprint 2

A principal conclusão das métricas foi que todo o escopo comprometido (64 SP) foi concluído até o fechamento da sprint. A consulta intermediária das 20h10 ainda mostrava 36 SP em aberto, mas os 13 itens restantes foram posteriormente movidos para Done. A Sprint 2 deverá ser planejada com base na capacidade efetivamente disponível e no refinamento do backlog, usando os 64 SP apenas como referência histórica, não como meta automática.

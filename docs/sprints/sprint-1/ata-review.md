# Ata da Sprint Review — Sprint 1

**Sprint:** FT Sprint 1 (21/10/2026 a 29/10/2026) | **Release:** R1  
**Data:** 29/10/2026  
**Participantes:** José Araújo Agra Neto (PO/DevOps), João Paulo de Araujo (SM) e Lethycia Zenaide Queiroz Melo (QA)  
**Facilitação:** João Paulo de Araujo (SM) | **Registro:** João Paulo de Araujo

**Sprint Goal:** Implementar o fluxo básico de gestão de entregas do Feneme, permitindo que Gestor e Motorista realizem login com segurança e que o Gestor cadastre, consulte e atribua entregas a motoristas.

A Sprint Review teve como objetivo apresentar o incremento desenvolvido, verificar o progresso em relação ao Sprint Goal e discutir os próximos ajustes do Product Backlog. A demonstração foi acompanhada pelas evidências de testes e integração disponíveis no repositório.

## 1. Incremento apresentado

**Versão demonstrada:** branch `main`, commit `7960995` (29/10/2026).  
**Resultado da suíte do backend:** 102/102 testes aprovados.  
**Integração contínua:** execução bem-sucedida no GitHub Actions (run 40965591244).

Foram apresentados os seguintes fluxos:

| US / Issue | Funcionalidade e resultado demonstrado | Evidência técnica | Avaliação registrada |
|---|---|---|---|
| FT-43 — US-01 Login do Gestor | O Gestor realiza login com credenciais válidas e recebe o perfil GESTOR. Uma senha incorreta gera mensagem genérica, sem emissão de token. | PR #1; testes `test_login_returns_role`, `test_q10_01` e `test_q10_04`. | Funcionalidade apresentada. Permanecem as ressalvas gerais de revisão de código e formalização da DoD. |
| FT-54 — US-02 Login do Motorista | O Motorista realiza login pelo mesmo endpoint. Tentativas de executar operações exclusivas do Gestor, como criar entrega ou listar motoristas, são bloqueadas com resposta 403. | PR #2; testes de bloqueio de cinco operações do Gestor. | Funcionalidade apresentada. A DoD da US ainda precisava de conferência complementar. |
| FT-44 — US-03 Cadastrar entrega | O Gestor cadastra uma entrega com origem, destino e carga. Campos obrigatórios vazios são rejeitados e o Motorista não possui permissão para cadastrar. | PR #1; testes `test_gestor_can_create_and_list_delivery` e `test_missing_required_fields_are_rejected`. | Funcionalidade apresentada. Permanecem as ressalvas gerais de revisão de código e formalização da DoD. |
| FT-55 — US-04 Consultar entregas | O Gestor consulta entregas persistidas. A interface apresenta a mensagem "Nenhuma entrega cadastrada" quando não existem registros. | PR #1; o estado vazio foi identificado, mas não possuía teste automatizado específico. | Funcionalidade apresentada com pendência de automação do cenário de lista vazia. |
| FT-45 — US-05 Atribuir motorista | O Gestor atribui um motorista à entrega. Usuários sem perfil Motorista são rejeitados. | PR #1; o caso de motorista inexistente ainda não possuía teste automatizado específico. | Funcionalidade apresentada com pendência de automação do cenário de motorista inexistente. |

Além das cinco US previstas no Sprint Goal, foi apresentada a consulta de entregas pelo próprio Motorista, implementada nos PRs #5 a #8, incluindo testes de isolamento entre motoristas.

## 2. Drivers, riscos e qualidade

Os resultados de qualidade e os pontos de atenção foram apresentados à equipe:

| Item | Resultado observado | Situação / discussão |
|---|---|---|
| FT-30 — DA-SEG-JP-01: credenciais e sessões inválidas | 20 de 20 casos rejeitados (100%). | Issue Done; prioridade Alta confirmada. |
| FT-61 — R02: risco de autenticação | Risco reavaliado de 15 para residual 10. | Issue Done; registro atualizado no Jira e na planilha de riscos. |
| FT-29 — DA-SEG-LZ-01: acesso cruzado | Issue consta como Done no estado final do Jira. | Item concluído; manter a evidência vinculada à issue. |
| FT-72 — Q-04: revisão de código | 0 de 8 PRs aprovados antes do merge (0%). | Meta não atingida. O tema foi encaminhado à retrospectiva e gerou ações para a Sprint 2. |
| FT-83 — Q-15: rastreabilidade | Indicador chegou a 100% após a inclusão dos links e evidências, partindo de 0% na medição inicial. | Issue Done; a equipe deverá manter o registro durante a execução, e não apenas no encerramento. |
| CI — Q-09 | Execuções consultadas na branch `main` concluídas com sucesso. | Evidência disponível no GitHub Actions; DevOps deverá manter o acompanhamento. |

A equipe reconheceu que os resultados dos testes foram positivos, mas que a ausência de revisão por outro integrante nos PRs representa uma não conformidade importante em relação ao processo de qualidade definido.

## 3. Métricas da Sprint 1

| Indicador | Resultado |
|---|---:|
| Itens comprometidos | 23 |
| Story points comprometidos | 64 SP |
| Itens concluídos (Done) | **23** |
| Story points concluídos | **64 SP** |
| Percentual da estimativa concluída | **100%** |
| Story points das cinco US do Sprint Goal | 15/15 SP (100%) |
| Itens ainda em andamento ao encerramento | **0 itens / 0 SP** |

O burndown e o histórico da atualização dos itens estão detalhados em [metricas-e-impedimentos.md](metricas-e-impedimentos.md). A consulta intermediária das 20h10 ainda apontava 13 itens (36 SP) em andamento; após essa consulta, todos foram atualizados para Done. O estado final do Jira registra 23 de 23 itens e 64 de 64 SP concluídos, em concordância com o burndown que termina em zero.

Para a Sprint 2, a equipe deverá considerar os 64 SP como velocity histórica da Sprint 1, mas definir o novo compromisso a partir da disponibilidade real, das dependências e da prontidão dos itens. Não ficou estabelecido que 64 SP devam ser repetidos automaticamente.

## 4. Avaliação do Sprint Goal

Com base na demonstração das cinco histórias e nos resultados dos testes apresentados, a equipe considerou que o **objetivo funcional da Sprint 1 foi alcançado**.

Essa avaliação não significa que todos os critérios de qualidade e de conclusão das US tenham sido integralmente atendidos. Foram registradas as seguintes ressalvas:

- Os oito PRs da sprint não tiveram aprovação de outro integrante antes do merge.
- A DoD de algumas US não estava integralmente preenchida.
- O aceite formal do PO precisava ser registrado nas issues correspondentes.
- Dois cenários importantes ainda precisavam de testes automatizados: lista vazia na FT-55 e motorista inexistente na FT-45.

**Encaminhamento:** o incremento foi considerado demonstrável e alinhado ao objetivo funcional, mas as ressalvas deverão ser acompanhadas como pendências de qualidade e processo na Sprint 2. O registro formal do aceite individual do PO deve permanecer nas respectivas issues do Jira.

## 5. Situação dos itens ao encerramento

Na consulta intermediária realizada às 20h10 de 29/10, 13 issues (36 SP) ainda apareciam em In Review ou In Progress. Após essa consulta, a equipe concluiu as atividades restantes e atualizou seus status no Jira. No estado final utilizado para o encerramento, **todas as 23 issues da Sprint 1 estavam em Done, totalizando 64 SP**.

Assim, não há itens não concluídos da Sprint 1 a serem devolvidos ao Product Backlog por falta de conclusão. As melhorias de processo e os cenários de teste ainda não automatizados permanecem como assuntos a serem considerados na priorização do PO, sem serem confundidos com issues da Sprint 1 ainda abertas.

## 6. Feedback e encaminhamentos para o Product Backlog

A Review destacou a necessidade de priorizar, para a próxima sprint, atividades que consolidem a qualidade do incremento já desenvolvido. Foram registrados os seguintes encaminhamentos para avaliação do PO:

1. Considerar a implementação dos testes automatizados pendentes da FT-55 (estado de lista vazia) e da FT-45 (motorista inexistente).
2. Considerar as ações de melhoria definidas na retrospectiva, especialmente proteção da branch `main`, revisão obrigatória dos PRs e aplicação da DoD antes de mover histórias para Done.
3. Revisar a priorização das 13 histórias do Product Backlog e confirmar a prontidão dos itens antes da Planning.
4. Planejar a Sprint 2 considerando os 64 SP como velocity histórica da Sprint 1, mas ajustar o compromisso à disponibilidade real, às dependências e à prontidão dos itens, sem assumir a repetição automática desse volume.

A priorização final e a seleção dos itens da Sprint 2 permanecem sob responsabilidade do Product Owner e deverão ser formalizadas no Jira durante a Sprint Planning.

## 7. Encerramento

A Sprint Review concluiu que o incremento da Sprint 1 apresentou os fluxos funcionais centrais de autenticação, cadastro, consulta e atribuição de entregas. Ao fechamento, o Jira registrava 23/23 issues e 64/64 SP em Done, e o burndown indicava zero story points restantes. Os resultados dos testes automatizados e do CI foram positivos, mas a equipe identificou melhorias necessárias no processo de revisão, rastreabilidade e aplicação da Definition of Done.

As pendências técnicas e de qualidade foram mantidas visíveis para orientar a priorização e o planejamento da próxima sprint.

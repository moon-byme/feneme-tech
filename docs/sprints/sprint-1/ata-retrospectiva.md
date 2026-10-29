# Ata da Retrospectiva — Sprint 1

**Sprint:** FT Sprint 1 (21/10/2026 a 29/10/2026)  
**Data:** 29/10/2026  
**Facilitador (SM):** João Paulo de Araujo  
**Participantes:** José Araújo Agra Neto, João Paulo de Araujo e Lethycia Zenaide Queiroz Melo  
**Registro:** João Paulo de Araujo

A retrospectiva teve como objetivo avaliar o processo de trabalho da Sprint 1, identificar práticas que contribuíram para os resultados e definir melhorias para a Sprint 2. A discussão foi conduzida a partir dos dados do Jira, do GitHub e das métricas consolidadas pelo Scrum Master.

## 1. Dados apresentados à equipe

Durante a reunião, foram apresentados e discutidos os seguintes resultados:

- Ao encerramento, a equipe concluiu **64 SP de 64 SP comprometidos** (23 de 23 issues), correspondendo a 100% do escopo estimado. A consulta intermediária das 20h10 ainda apontava 36 SP em aberto; os itens restantes foram concluídos após essa consulta.
- As cinco histórias de usuário relacionadas ao objetivo funcional da sprint, totalizando 15 SP, foram concluídas.
- O burndown permaneceu sem redução nos cinco primeiros dias (21 a 25/10), com concentração de entregas nos últimos dias.
- Nenhum dos oito Pull Requests recebeu revisão de outro integrante antes do merge (Q-04 = 0%).
- Em 26/10, o código de quatro US foi commitado diretamente na branch `main` e removido posteriormente. A branch permaneceu sem esse código por aproximadamente 19 horas (I-01).
- Quatro US foram movidas para Done antes da reintegração do código pelo PR e sem a DoD integralmente preenchida.
- Os links de PR e as evidências das histórias foram adicionados ao Jira em 29/10; a medição inicial de rastreabilidade (Q-15) era de 0%, chegando a 100% após a correção.
- O GitHub Actions apresentou execuções bem-sucedidas, e a suíte de testes do backend passou de 38 para 102 testes na verificação registrada em 29/10.

A equipe reconheceu que a entrega das funcionalidades principais foi positiva, mas que o processo de integração, revisão e registro das evidências precisa ser mais disciplinado.

## 2. O que funcionou bem

A equipe destacou os seguintes pontos positivos:

- O pipeline do GitHub Actions permaneceu estável e executou os testes nas atualizações do repositório.
- Foram implementados testes de segurança relevantes, incluindo 20 casos negativos de autenticação e testes de isolamento entre motoristas.
- As cinco histórias de usuário previstas para o objetivo funcional foram entregues.
- A equipe conseguiu recuperar a integração das funcionalidades após o problema ocorrido na branch `main`, por meio do PR #1.
- As evidências e os vínculos entre issues e Pull Requests foram organizados no Jira ao final da sprint.

## 3. O que precisa melhorar

A discussão identificou oportunidades de melhoria no processo:

- **Revisão de código:** os PRs foram integrados sem aprovação de outro integrante, reduzindo a capacidade de identificar problemas antes do merge.
- **Uso da DoD:** histórias foram movidas para Done sem que todos os critérios aplicáveis estivessem verificados.
- **Distribuição do trabalho:** não houve conclusão de itens nos cinco primeiros dias, e parte significativa das entregas ocorreu no final da sprint.
- **Planejamento e fluxo:** embora os 64 SP comprometidos tenham sido concluídos até o encerramento, as entregas ficaram concentradas nos últimos dias. A equipe deverá usar a velocity de 64 SP como referência histórica, sem tratá-la como capacidade garantida para a próxima sprint.
- **Rastreabilidade:** os links de PR e as evidências não foram registrados nas issues durante a execução, exigindo uma correção concentrada no encerramento.
- **Comunicação de mudanças técnicas:** a alteração do procedimento de execução do ambiente no último dia reforçou a necessidade de manter a documentação atualizada e comunicar mudanças à equipe.

## 4. Ações de melhoria definidas

Ao final da discussão, foram estabelecidas as seguintes ações para a Sprint 2:

| # | Ação acordada | Responsável | Prazo | Como verificar |
|---|---|---|---|---|
| 1 | Configurar a proteção da branch `main`, exigindo Pull Request, uma aprovação de outro integrante e CI verde antes do merge. | Lethycia (responsável pelo repositório) | Até a Planning da Sprint 2 | Evidência da configuração em Settings → Branches, anexada à FT-72. |
| 2 | Garantir que todo Pull Request receba revisão de outro integrante pela aba Reviews antes do merge, utilizando o template do Modelo 3. | Todos; acompanhamento do SM | Durante toda a Sprint 2 | Indicador Q-04 da Sprint 2 igual ou superior a 80%. |
| 3 | Mover uma US para Done somente após a DoD estar preenchida, o PR estar integrado e o aceite do PO estar registrado na issue. | QA (Lethycia), com aceite do PO (José) | Durante toda a Sprint 2 | Issues sem necessidade de correção posterior da rastreabilidade Q-15. |
| 4 | Planejar a Sprint 2 considerando a velocity final de 64 SP como referência histórica, mas dimensionando o compromisso conforme disponibilidade, dependências e prontidão dos itens. | PO (José) e SM (João Paulo) | Planning da Sprint 2 | Total de story points selecionados e justificativa da capacidade registrada no Jira. |
| 5 | Distribuir as atividades ao longo da sprint e buscar concluir pelo menos um item até o terceiro dia. | Todos; acompanhamento do SM nas dailies | Durante a Sprint 2 | Burndown da Sprint 2 sem período inicial prolongado sem entregas. |
| 6 | Incluir a chave FT-XX no nome da branch e do PR e adicionar o link do PR à issue correspondente assim que o PR for aberto. | Autor de cada PR | Durante a Sprint 2 | Campo de Web links preenchido nas issues correspondentes. |
| 7 | Implementar os testes que faltam para o estado de lista vazia (FT-55) e para a atribuição a motorista inexistente (FT-45). | Lethycia (QA), com apoio dos desenvolvedores | Primeira semana da Sprint 2 | Testes executados no CI e evidência/comentário nas US correspondentes. |

## 5. Acompanhamento da retrospectiva anterior

Não foi localizada uma ata da retrospectiva da Sprint 0 no repositório ou no Jira. Por esse motivo, a equipe não encontrou ações anteriores formalmente registradas para acompanhar.

Ficou definido que o acompanhamento das sete ações desta retrospectiva será realizado no início da retrospectiva da Sprint 2. O Scrum Master ficará responsável por atualizar o status de cada ação e reunir as evidências correspondentes.

## 6. Encerramento

A equipe concluiu que o principal resultado positivo da Sprint 1 foi a entrega das funcionalidades centrais previstas para o incremento. Como principal ponto de melhoria, ficou estabelecida a necessidade de fortalecer o fluxo de Pull Requests e tornar a aplicação da DoD parte efetiva do trabalho diário, e não apenas uma conferência no encerramento.

As ações definidas deverão ser acompanhadas ao longo da Sprint 2, com verificação baseada em evidências no Jira e no GitHub.

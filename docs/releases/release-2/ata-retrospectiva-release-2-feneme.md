# Feneme — Ata da Retrospectiva da Release 2

**Release:** R2 · **Sprints:** 2 (03–12/11) e 3 (17–26/11/2026)  
**Data:** 26/11/2026, período da tarde  
**Modalidade:** Google Meet e WhatsApp  
**Equipe:** Lethycia Zenaide Queiroz Melo (SM), João Paulo de Araujo (PO/DevOps), José Araújo Agra Neto (QA).  
**Registro:** síntese documental elaborada em 26/11, a partir da confirmação da SM de que os tópicos da pauta foram tratados, exceto a revisão de riscos. Horários exatos e falas individuais não informados. A avaliação abaixo é uma síntese qualitativa fundamentada nas evidências, não uma votação individual nem atribuição de falas aos integrantes.

## 1. Resultado e evolução da equipe

A R2 avançou na disciplina de integração, na automação de testes, na rastreabilidade e na entrega de funcionalidades. O fluxo de PR evoluiu em relação à R1 (Q-04 histórica 0/10 no merge; na S3, 19/19 aprovações prévias até #57). Foram incorporados Cypress/Cucumber ao CI, regressão de 29/29 cenários e homologação automatizada. Foram entregues as funcionalidades de status, andamento, histórico, cidades e catálogo de cargas. A mudança de escopo FT-112 organizou a evolução para rotas automáticas e comparação térmica na R3. As regularizações documentais da R1 também avançaram.

Os indicadores operacionais finais, conferidos em 26/11, foram de 36/36 SP (11 issues) na S2 e 48/48 SP (15 issues) na S3, totalizando 84/84 SP e 26/26 issues por status na R2, com zero SP restantes. A fotografia anterior de 38/48 SP da S3 é preservada como histórico; FT-90/91/92 passaram a Concluído. Os pontos por status não equivalem automaticamente à velocity validada pela DoD. Ver [relatório consolidado de métricas da R2](relatorio-metricas.md).

## 2. Avaliação interna de desempenho por integrante

### Lethycia Zenaide Queiroz Melo — Scrum Master

**Contribuições:** organização das cerimônias e registros de Planning, acompanhamento de DoR, DoD, impedimentos, métricas Q-04/Q-15 e mudanças de escopo; regularização documental da R1; contribuição técnica às funcionalidades de status, andamento e histórico e ao driver de persistência.  
**Pontos de melhoria:** distribuir a consolidação de documentos e indicadores ao longo das sprints, estabelecer verificações intermediárias de DoD e acompanhar capacidade e dependências antes do encerramento.  
**Síntese:** atuação consistente na organização e transparência do processo e contribuição técnica ao incremento; fortalecer a previsibilidade e o fechamento contínuo.  
**Evidências:** FT-87, FT-90, FT-124, FT-34, FT-48, FT-49, FT-59 e PRs correspondentes.

### João Paulo de Araujo — Product Owner

**Contribuições:** esclarecimento e priorização de requisitos, aceites das US, organização do novo escopo de rotas (FT-112), definição das regras de negócio, catálogo de cargas e lista de cidades; decisão de carryover das FT-115/116 e da FT-57.  
**Pontos de melhoria:** estimar o impacto das mudanças antes de comprometer a capacidade, manter aceites e decisões de produto atualizados durante a execução e concluir as decisões de fechamento no período planejado.  
**Síntese:** evolução relevante do produto e preparação da R3, com oportunidade de melhorar previsibilidade e formalização das decisões.  
**Evidências:** FT-89, FT-92, FT-112, FT-113, FT-114 e documento de aceite S3.

### João Paulo de Araujo — DevOps

**Contribuições:** evolução do fluxo de integração e proteção da main, Cypress/Cucumber no CI, implantação automatizada em homologação, recuperação das falhas de deploy, relatórios técnicos e regularização dos indicadores históricos.  
**Pontos de melhoria:** atualizar o relatório de pipeline a cada recorte, antecipar validações de infraestrutura, conferir dependências e branch de destino, organizar evidências de segurança, segredos e falhas, e concluir publicação da versão.  
**Síntese:** contribuição importante para estabilidade e automação; fortalecer a confiabilidade do fechamento e a atualização contínua das evidências.  
**Evidências:** FT-89, FT-92, FT-110, PRs #52/53/55 e CI #351/#375/#394.

### José Araújo Agra Neto — QA

**Contribuições:** ampliação de cenários funcionais e de exceção, regressão R1/R2, verificação de indicadores de segurança, persistência e falhas de API, conferência de DoD e validação manual do catálogo em homologação.  
**Pontos de melhoria:** atualizar o Plano de Testes e o Plano de Qualidade após cada medição, formalizar defeitos e retestes com severidade, publicar relatório consolidado antes do fechamento e registrar limitações metodológicas (Q-07 sem cronometragem).  
**Síntese:** evolução importante da cobertura e automação de testes; reforçar a formalização dos resultados e gestão documental da qualidade.  
**Evidências:** FT-88, FT-91, FT-73, FT-80, FT-81, FT-114/10325, PRs #51 e #58.

### 2.1. Ratificação da avaliação entre pares — 26/11/2026

Conforme confirmação da Scrum Master, os três integrantes concordaram com as avaliações qualitativas discutidas na retrospectiva da R2, incluindo as contribuições, os pontos positivos e as oportunidades de melhoria registradas acima para cada integrante nos respectivos papéis.

| Integrante | Participação e concordância |
| --- | --- |
| Lethycia Zenaide Queiroz Melo — SM | Confirmada |
| João Paulo de Araujo — PO/DevOps | Confirmada |
| José Araújo Agra Neto — QA | Confirmada |

A avaliação coletiva foi ratificada pelos três integrantes, sendo utilizada como evidência do critério 14 da DoD da Release 2. O registro não atribui notas numéricas, falas ou respostas individuais não documentadas, nem afirma que formulários separados foram preenchidos. Caso a disciplina exija um formato específico, este deverá ser observado.

**Rastreabilidade:** [FT-90](https://feneme.atlassian.net/browse/FT-90) · [FT-124](https://feneme.atlassian.net/browse/FT-124) · [DoD — FT-38](https://feneme.atlassian.net/browse/FT-38) · [PR #63](https://github.com/moon-byme/feneme-tech/pull/63).

## 3. Pontos de melhoria e ações

| Ponto de melhoria | Ação / acompanhamento | Responsabilidade na R3 | Evidência esperada |
| --- | --- | --- | --- |
| Documentação concentrada no encerramento | Atualizar DoD, métricas e evidências durante a sprint | Todos; acompanhamento SM | FT-124 e registros por sprint |
| Capacidade e desvios de escopo | Comparar métricas R1/R2 e acompanhar ações durante S4 | Neto (SM) | [FT-126](https://feneme.atlassian.net/browse/FT-126), S4, 2 SP propostos |
| Mudança de escopo e regressão | Atualizar matriz CT, mocks e estratégia de testes | João Paulo (QA) | [FT-125](https://feneme.atlassian.net/browse/FT-125), S4, 2 SP propostos |
| Cobertura isolada do CI | Automatizar cobertura de linhas e publicação de evidências Q-08 | Lethycia (DevOps) | [FT-127](https://feneme.atlassian.net/browse/FT-127), S5, 3 SP propostos |
| Dependências e integração de PR | Conferir branch de destino, revisão externa e checks antes do merge | Todos; SM e DevOps | FT-72, I-03, PRs |
| Defeitos e limitações de medição | Registrar bugs confirmados e retestes; cronometrar usabilidade se mantido o limite | QA; PO valida critério | FT-10, FT-9, FT-67/75 |
| Google Cloud e falhas externas | Concluir orçamento/alertas, restrições, cache e simulações de falhas/cota | Responsáveis das issues | FT-115/116/121 |
| Encerramento de release | Reservar capacidade para documentação, QA, aceite e publicação | Todos | FT-90/91/92 e continuidade R3 |

As três novas tasks foram criadas em 26/11 após o alinhamento, com prioridade alta e Release 3. Os SP são propostas para confirmação nas respectivas Plannings; não foram registrados votos, datas ou compromissos individuais não informados.

## 4. Revisão de riscos — encaminhamento pendente

A revisão dos riscos R01–R10 não foi realizada nesta reunião. Por decisão informada pela SM, José Neto e João Paulo ficaram responsáveis por conferir evidências, reavaliar os riscos residuais e atualizar o registro oficial FT-8/planilha, compartilhando os resultados com a equipe. A revisão permanece pendente até o registro das evidências, incluindo os riscos R08 e R10 em tratamento na R3. Não alterar valores sem justificativa. A SM acompanha a conclusão na FT-90; a delegação não equivale à execução.

## 5. Passagem de papéis e continuidade

| Integrante | R2 | R3 |
| --- | --- | --- |
| Lethycia | SM | PO/DevOps |
| João Paulo | PO/DevOps | QA |
| José Neto | QA | SM |

Rotação conforme README. As responsabilidades de fechamento da R2 permanecem com os papéis da R2; as novas tarefas de melhoria seguem a rotação da R3. Confirmar capacidade, estimativas e dependências na Planning 4; as FT-115/116 antecedem geração automática das rotas, e FT-57/122 permanecem na S5.

## 6. Fechamento e evidências

A retrospectiva e os demais tópicos da pauta foram tratados conforme relato da SM, com revisão de riscos delegada e ainda não executada. As ações acima organizam a continuidade sem declarar a publicação formal da R2, a velocity definitiva ou a aprovação de critérios ainda pendentes. O registro está sujeito à revisão documental dos participantes via PR.

**Referências:** [Review S3](../../sprints/sprint-3/ata-review.md) · [Métricas S3](../../sprints/sprint-3/metricas-e-impedimentos.md) · [FT-90](https://feneme.atlassian.net/browse/FT-90) · [FT-91](https://feneme.atlassian.net/browse/FT-91) · [FT-92](https://feneme.atlassian.net/browse/FT-92) · [FT-8](https://feneme.atlassian.net/browse/FT-8) · [FT-124](https://feneme.atlassian.net/browse/FT-124) · [README](../../../README.md).

# Release 2 — Acompanhamento das entregas e base da nova linha do produto

**Versão:** `v2.0.0` · **Período:** 03/11/2026 a 26/11/2026 (Sprints 2 e 3) · **PO/DevOps:** João Paulo de Araujo
**Jira:** versão Release 2 do projeto [FT](https://feneme.atlassian.net/jira/software/projects/FT/summary) · **Publicação:** [FT-92](https://feneme.atlassian.net/browse/FT-92)

A Release 2 fecha o ciclo da entrega: o Gestor cadastra e acompanha, o Motorista atualiza o andamento e tudo fica registrado. Ela também prepara a nova linha do Feneme, aprovada em 14/11/2026: comparar rotas reais e indicar a que expõe menos a carga ao calor.

## O que muda para quem usa

**Gestor**
- Acompanha o andamento de todas as entregas em uma tela, com o status atual e o Motorista responsável (FT-49, US-12).
- Consulta o histórico de cada entrega: quem mudou o status, de quê para quê e quando (FT-59, US-13).
- Escolhe origem e destino em uma lista fechada de 26 cidades, a mesma da previsão do clima; não há mais cidade digitada errada (FT-113, US-14).
- Consulta o catálogo de 7 tipos de carga com o limite de temperatura e a fonte de cada um (FT-114, US-15).
- Consulta a previsão de temperatura do ambiente para uma cidade, pela Open-Meteo; se o serviço falhar, o cadastro continua funcionando e a tela avisa (FT-47, US-08).
- Cadastra e compara manualmente até 2 alternativas de trajeto (FT-46 e FT-56, US-06 e US-07). *Será substituído pelas rotas automáticas na R3.*

**Motorista**
- Vê só as entregas atribuídas a ele (FT-58).
- Atualiza o status de Pendente para Em transporte e para Entregue; cada mudança é gravada com o histórico na mesma operação (FT-48, US-11).

## Qualidade e operação

- 194 testes automatizados de backend e cenários Cucumber/Cypress no CI (`@smoke`, regressão da R1, comparação de trajetos e Open-Meteo).
- Persistência de status medida: 20 de 20 atualizações válidas recuperadas com o histórico correto (R05, Q-12).
- Falhas da Open-Meteo: 10 de 10 cenários simulados sem bloquear cadastro e comparação manual (R06, Q-13).
- `main` protegida desde 04/11: só por PR aprovado e com CI verde; 100% das execuções na `main` passaram.
- Deploy automatizado em homologação (Render) depois do CI verde, com verificação de saúde e varredura de segredos (FT-110).

## Mudança de escopo

A Review da Sprint 2 (12/11) levou à nova linha do produto, registrada na [FT-112](https://feneme.atlassian.net/browse/FT-112): rotas reais pela Google Routes API, mapa e comparação térmica conforme o tipo de carga. Na R2 entraram a lista de cidades e o catálogo de cargas. A comparação climática das rotas (FT-57) **saiu da R2** e foi para a Sprint 5 (R3).

## Limitações conhecidas

- A temperatura é a **prevista do ambiente**, não a medida da carga.
- A comparação de trajetos ainda é manual (até 2 alternativas, sem mapa).
- Tipo de carga e data/hora de saída ainda não fazem parte do cadastro da entrega (US-16, Sprint 4).
- Entregas cadastradas antes da lista de cidades com texto não reconhecido aparecem com a etiqueta "revisar cidades".
- A homologação usa o plano gratuito do Render: hiberna sem uso (primeiro acesso leva cerca de 1 minuto) e o banco gratuito expira em 30 dias.
- A configuração do Google Cloud (FT-115) e o risco R10 (FT-116) ficaram preparados, mas dependem da evidência no console.

## Próximos passos (R3)

Tipo de carga e saída na entrega, até 3 rotas automáticas com mapa, comparação de exposição ao calor por rota e registro da rota escolhida pelo Gestor (FT-117, FT-118, FT-120, FT-57 e FT-122).

**Relatório do pipeline:** [`relatorio-pipeline.md`](relatorio-pipeline.md) · **Aceite do PO:** [`aceite-po-sprint-3.md`](aceite-po-sprint-3.md)

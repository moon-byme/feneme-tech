# Modelo 1 — Issue de História de Usuário (US)

Fonte: FT-51 (catálogo de modelos oficiais, conforme arquivos da professora). Copie para a descrição da Story no Jira e preencha todos os campos.

TÍTULO: [US-XX] <Título curto da funcionalidade>

FEATURE / ÉPICO: <ex.: Gestão de usuários>
RELEASE: <R1 | R2 | R3 | R4> | SPRINT: <0 a 7>
PRIORIDADE: <Alta | Média | Baixa> | STORY POINTS: <1, 2, 3, 5, 8, 13>
RESPONSÁVEL: <@usuário> | PAPEL DE REVISÃO: <PO | QA>

### HISTÓRIA DE USUÁRIO

Eu como <perfil de usuário>,
preciso <ação ou funcionalidade>,
de modo que <benefício ou valor de negócio>.

### CONTEXTO E OBSERVAÇÕES

<Regras de negócio, protótipos, links, dependências de outras US>

### CRITÉRIOS DE ACEITE — GHERKIN

**Cenário 1 — Caminho feliz**
Dado que <contexto inicial>
Quando <ação do usuário>
Então <resultado esperado>

**Cenário 2 — Alternativa ou erro**
Dado que <contexto inicial>
Quando <ação do usuário>
Então <resultado esperado>
E <resultado adicional, se houver>

### DEFINITION OF READY (DoR)

- [ ] História no formato Eu como / preciso / de modo que
- [ ] Critérios Gherkin definidos
- [ ] Story Points estimados pela equipe
- [ ] Prioridade definida pelo PO
- [ ] Dependências identificadas
- [ ] Cabe em uma sprint

### DEFINITION OF DONE (DoD)

- [ ] Código revisado e integrado por PR
- [ ] Critérios validados pelo QA
- [ ] Testes escritos e passando
- [ ] Pipeline CI sem falhas
- [ ] Implantado em homologação quando exigido
- [ ] Documentação atualizada
- [ ] Aceite do PO

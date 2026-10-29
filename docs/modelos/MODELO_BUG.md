# Modelo 2 — Issue de Bug

Fonte: FT-51 (catálogo de modelos oficiais, conforme arquivos da professora). Use o tipo de issue **Bug** no Jira e preencha todos os campos.

TÍTULO: [BUG] <Título curto do problema>

RELEASE: <R1 | R2 | R3 | R4> | SPRINT: <0 a 7>
SEVERIDADE: <Crítica | Alta | Média | Baixa>
PRIORIDADE: <Alta | Média | Baixa>
RESPONSÁVEL: <@usuário> | REPORTADO POR: <@usuário (QA)>
US RELACIONADA: <FT-XX, se houver>

### DESCRIÇÃO

<O que está acontecendo de errado, em uma ou duas frases>

### AMBIENTE

Ambiente: <local | homologação | produção>
Navegador / versão: <ex.: Chrome 130>
Sistema operacional: <ex.: Windows 11>
Versão / commit / branch: <ex.: main, a1b2c3d>

### PASSOS PARA REPRODUZIR

1. <passo 1>
2. <passo 2>
3. <passo 3>

### RESULTADO ESPERADO

<O que deveria acontecer>

### RESULTADO OBTIDO

<O que aconteceu de fato>

### EVIDÊNCIAS

<Capturas de tela, vídeo, logs ou mensagens de erro>

### CRITÉRIO DE CORREÇÃO — GHERKIN (opcional)

Dado que <contexto>
Quando <ação>
Então <comportamento correto>

### CHECKLIST DE ENCERRAMENTO

- [ ] Causa identificada e registrada em comentário
- [ ] Correção via PR referenciando esta issue
- [ ] Teste de regressão criado ou atualizado
- [ ] Correção verificada pelo QA

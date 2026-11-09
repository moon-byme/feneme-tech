# Guia de DevOps e fluxo de desenvolvimento — Feneme

**Projeto:** Feneme — Gestão de Transporte de Alimentos  
**Repositório:** [moon-byme/feneme-tech](https://github.com/moon-byme/feneme-tech)  
**Jira:** [Projeto FT](https://feneme.atlassian.net/jira/software/projects/FT/boards/1)  
**Atualizado em:** 09/11/2026  
**Escopo:** fluxo atualmente identificado no repositório e ajustes planejados para a Release 2.

> O arquivo de referência `FENEME_GUIA_DEVOPS_UNIFICADO.md` permanece anexado à issue FT-85 no Jira. Este documento registra a leitura atual do repositório; não substitui nem remove o anexo original.

## 1. Estrutura atual do repositório

```text
feneme-tech/
├── .github/
│   ├── ISSUE_TEMPLATE/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/ci.yml
├── backend/
│   ├── accounts/       # usuários, perfis, autenticação e permissões
│   ├── config/         # configurações e rotas Django
│   ├── deliveries/     # cadastro, consulta e atribuição de entregas
│   ├── manage.py
│   └── requirements.txt
├── frontend/
│   ├── cypress/
│   │   ├── e2e/        # cenários Gherkin .feature
│   │   └── support/    # configuração e step definitions
│   ├── src/
│   │   ├── components/
│   │   ├── App.tsx
│   │   ├── api.ts
│   │   └── types.ts
│   ├── package.json
│   └── cypress.config.ts
├── docs/
├── evidencias/
├── scripts/
├── .env.example
├── CONTRIBUTING.md
└── README.md
```

## 2. Fluxo de branches

A branch principal é `main`. O trabalho deve ser desenvolvido em branches próprias, sem commits diretos na principal.

Padrões recomendados:

| Tipo | Padrão | Exemplo |
|---|---|---|
| Funcionalidade | `feature/FT-XX-descricao` | `feature/FT-46-alternativas-trajeto` |
| Correção | `fix/FT-XX-descricao` | `fix/FT-32-falha-open-meteo` |
| Testes/QA | `qa/FT-XX-descricao` | `qa/FT-88-cenarios-sprint-2` |
| Documentação | `docs/FT-XX-descricao` | `docs/FT-85-guia-devops` |

Passos:

1. Atualizar a referência local de `main`.
2. Criar uma branch com o padrão acima.
3. Implementar apenas o escopo da issue relacionada.
4. Executar os testes pertinentes.
5. Fazer commit com mensagem objetiva e referência à issue.
6. Abrir Pull Request para `main`.
7. Solicitar revisão de outro integrante e aguardar aprovação.
8. Corrigir comentários, aguardar CI verde e só então realizar o merge.

## 3. Pull Requests

O modelo oficial está em `.github/PULL_REQUEST_TEMPLATE.md`.

Todo PR deve informar:
- issue Jira relacionada (chave FT-XX);
- objetivo e justificativa;
- arquivos/funcionalidades alterados;
- passos para testar;
- evidências reais;
- checklist do autor e pontos de atenção ao revisor.

A aprovação deve ser feita por outro integrante. O autor não deve aprovar o próprio PR. Não marcar testes como aprovados antes da execução e não declarar DoD completa apenas porque o PR foi aberto.

## 4. Integração contínua (GitHub Actions)

Workflow: `.github/workflows/ci.yml`.

Gatilhos identificados:
- push em branches;
- Pull Request direcionado a `main`;
- execução manual (`workflow_dispatch`).

Jobs principais:
1. **Detect application components:** identifica backend e frontend.
2. **Backend - Django checks and tests:** instala dependências, prepara PostgreSQL, executa `python manage.py check` e `python manage.py test`.
3. **Frontend - build and tests:** executa `npm ci` e `npm run build`; executa `npm test` se o script estiver configurado.
4. **E2E - Cucumber/Cypress (@smoke):** prepara banco e contas fictícias, inicia Django e executa os cenários `@smoke`.

Comandos locais:

```bash
# Backend
cd backend
python -m pip install -r requirements.txt
python manage.py check
python manage.py test

# Frontend
cd frontend
npm ci
npm run build
npm run e2e
npm run e2e:smoke
```

A branch de trabalho do PR #15 também introduz `npm run e2e:r1` e a regressão `@R1` no workflow. Essa mudança deve ser considerada parte da configuração principal somente depois do merge do PR.

## 5. Variáveis de ambiente e segredos

- Copiar `.env.example` para `.env` no ambiente local.
- Nunca versionar `.env`, senhas reais, tokens JWT ou credenciais de banco.
- Usar variáveis do ambiente/Secrets do GitHub Actions para CI.
- Em produção, definir `DJANGO_DEBUG=False`, uma `DJANGO_SECRET_KEY` forte, `DJANGO_ALLOWED_HOSTS` e `CORS_ALLOWED_ORIGINS` restritos.
- As senhas das contas E2E devem ser fictícias e exclusivas do banco efêmero de CI.

## 6. Jira e rastreabilidade

- Cada branch e PR deve citar a chave Jira correspondente.
- Atualizar a issue com link do PR, resultado do CI e evidência de teste.
- Manter o vínculo CT ↔ US ↔ PR quando houver cenário de teste.
- Registrar defeitos confirmados como Bugs separados, com severidade, passos de reprodução, resultado esperado/observado e evidência.
- Não alterar retroativamente resultados históricos de métricas; registrar novos resultados na release correspondente.

## 7. Papéis da Release 2

A rotação registrada para a R2 é:
- **Product Owner / DevOps:** João Paulo de Araujo.
- **Scrum Master:** Lethycia Zenaide Queiroz Melo.
- **QA:** José Araújo Agra Neto.

As atribuições devem ser revistas a cada release conforme o acordo da equipe. A execução de testes e o aceite de qualidade pertencem ao QA; configuração de CI e proteção da branch pertencem ao DevOps; priorização e aceite funcional pertencem ao PO.

## 8. Proteção da branch principal

O documento `docs/devops/protecao-main.md` descreve a configuração proposta para `main`: PR obrigatório, ao menos uma aprovação, CI obrigatório, resolução de conversas e bloqueio de force push/exclusão.

**Estado:** a existência das regras no GitHub precisa ser conferida nas configurações do repositório. A documentação da regra não é evidência de que ela já esteja ativa.

## 9. Critério operacional de conclusão

Uma entrega só deve ser considerada pronta quando:
- o escopo da issue foi implementado;
- os testes pertinentes foram executados e registrados;
- o CI aplicável terminou com sucesso;
- houve revisão e aprovação por outra pessoa;
- o PR foi integrado à branch principal;
- documentação e issue Jira foram atualizadas com evidências.

## 10. Referências

- [Repositório Feneme](https://github.com/moon-byme/feneme-tech)
- [Backlog Jira](https://feneme.atlassian.net/jira/software/projects/FT/boards/1/backlog)
- [Workflow CI](../../.github/workflows/ci.yml)
- [Contribuição](../../CONTRIBUTING.md)
- [Proteção da main](./protecao-main.md)

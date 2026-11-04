# Proteção da branch `main`

**Release:** R2 · **Responsável:** DevOps · **Rastreabilidade:** FT-89, impedimento I-03 (FT-87), Q-04 (FT-72)

## Por que

Na Release 1, a `main` recebeu commit direto de código (I-01) e nenhum dos PRs foi aprovado por outro integrante antes do merge (I-03, Q-04 = 0%). A proteção abaixo faz o GitHub impedir esses dois desvios, em vez de depender só de combinação entre a equipe.

## Regras a configurar

| Regra | Valor | Efeito |
| --- | --- | --- |
| Exigir Pull Request antes do merge | Sim | Bloqueia push direto na `main` |
| Aprovações obrigatórias | 1 | Outro integrante precisa aprovar |
| Descartar aprovações quando houver novos commits | Sim | A aprovação vale para o código final |
| Exigir checagens de status | Sim, com a branch atualizada | O CI precisa passar antes do merge |
| Checagens obrigatórias | `Backend - Django checks and tests`, `Frontend - build and tests`, `E2E - Cucumber/Cypress (@smoke)` | Testes do back-end, build do front-end e cenários `@smoke` |
| Exigir resolução das conversas | Sim | Comentários da revisão não ficam pendentes |
| Bloquear force push e exclusão | Sim | Preserva o histórico |
| Aplicar também a administradores | Sim | Ninguém contorna a regra |

## Quem pode configurar

Só quem tem permissão de **Admin** no repositório (hoje, a dona da conta `moon-byme`). O DevOps tem permissão de escrita, que não basta para alterar a proteção. Há duas saídas: a dona aplica a configuração, ou concede o papel Admin ao DevOps da release.

## Passo a passo (interface do GitHub)

1. **Settings → Branches → Add branch ruleset** (ou *Add classic branch protection rule*).
2. Em *Target branches*, inclua `main` (ou o padrão *Default branch*).
3. Marque as regras da tabela acima.
4. As checagens obrigatórias só aparecem na busca depois de rodarem pelo menos uma vez. Por isso, faça o merge do PR que adiciona o job E2E antes de selecionar as três checagens.
5. Salve. Em seguida, tente um `git push` direto na `main`: o GitHub deve recusar. Guarde o print como evidência.

## Alternativa por linha de comando (Admin)

```bash
gh api -X PUT repos/moon-byme/feneme-tech/branches/main/protection \
  -H "Accept: application/vnd.github+json" \
  --input - <<'JSON'
{
  "required_status_checks": {
    "strict": true,
    "contexts": [
      "Backend - Django checks and tests",
      "Frontend - build and tests",
      "E2E - Cucumber/Cypress (@smoke)"
    ]
  },
  "enforce_admins": true,
  "required_pull_request_reviews": {
    "required_approving_review_count": 1,
    "dismiss_stale_reviews": true
  },
  "required_conversation_resolution": true,
  "restrictions": null,
  "allow_force_pushes": false,
  "allow_deletions": false
}
JSON
```

Conferência: `gh api repos/moon-byme/feneme-tech/branches/main/protection`.

## Evidências a registrar no Jira (FT-89)

- [ ] Print ou saída da regra aplicada na `main`.
- [ ] Tentativa de push direto recusada.
- [ ] Primeiro PR da R2 com aprovação de outro integrante e as três checagens verdes.

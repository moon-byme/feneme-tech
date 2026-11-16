# Google Maps Platform — projeto, chaves, cotas e alertas

> Responsável pela conta: **João Paulo de Araujo** (conta pessoal, projeto `feneme` no Google Cloud). Decisão registrada em [FT-112](https://feneme.atlassian.net/browse/FT-112); tarefa de configuração em [FT-115](https://feneme.atlassian.net/browse/FT-115).

## APIs usadas

| API | Uso no Feneme | Onde é chamada |
| --- | --- | --- |
| Routes API | Rotas, distâncias, tempos e polilinhas (US-17) | Somente no backend |
| Maps JavaScript API | Desenho das rotas no mapa (US-18) | No navegador |

A previsão de temperatura continua na Open-Meteo, que não exige chave.

## Chaves

| Chave | Restrição de API | Restrição de aplicação | Variável |
| --- | --- | --- | --- |
| `feneme-routes-backend` | Só Routes API | Desenvolvimento: nenhuma; homologação: IP do servidor | `GOOGLE_MAPS_API_KEY` |
| `feneme-maps-frontend` | Só Maps JavaScript API | Sites: `http://localhost:*/*` e o domínio de homologação | `VITE_GOOGLE_MAPS_JS_KEY` |

Regras:

- As chaves ficam no `.env` local (já ignorado pelo Git) e nos *secrets* da homologação. **Nunca** no repositório, em prints, em mensagens ou em arquivos gerados que sejam versionados.
- Cada integrante usa a própria chave de desenvolvimento, restrita da mesma forma, para poder revogá-la sem afetar os outros.
- A chave do mapa fica visível no navegador por natureza; por isso a restrição por domínio é obrigatória.

## CI

O GitHub Actions **não recebe chave**. Testes de rotas, mapa e comparação térmica usam *mocks* com as respostas JSON gravadas nos spikes. Nenhum teste automatizado pode chamar as APIs reais.

## Custos, cotas e alertas

- O uso previsto (desenvolvimento, testes manuais e demo) fica dentro da cota gratuita mensal da plataforma, que é contada por produto.
- **Alerta de orçamento:** US$ 1 em *Billing → Budgets & alerts* (só avisa).
- **Cota diária:** limite por API em *APIs & Services → [API] → Quotas* (ex.: 300 requisições/dia na Routes API). Esse limite bloqueia chamadas e evita cobrança; o sistema cai no aviso de indisponibilidade.
- **Cache de rotas** por par origem–destino por 24 h (RN-07) reduz o número de chamadas.
- Conferir o painel de faturamento após a primeira semana de uso real.

## Acesso da equipe

José e Lethycia entram no projeto com papel de leitura, para acompanhar uso, cotas e alertas.

## Se uma chave vazar

1. Revogar a chave em *APIs & Services → Credentials*.
2. Criar outra com as mesmas restrições e atualizar `.env`/*secrets*.
3. Registrar o ocorrido em [FT-103](https://feneme.atlassian.net/browse/FT-103).

## Contingência

Se a conta ou a API ficarem indisponíveis, o sistema usa o cache de rotas (RN-07) quando houver e mostra aviso quando não houver; os demais fluxos continuam funcionando ([DA-CON-JP-02, FT-121](https://feneme.atlassian.net/browse/FT-121); risco [R10, FT-116](https://feneme.atlassian.net/browse/FT-116)).

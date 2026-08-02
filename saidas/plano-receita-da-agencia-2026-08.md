# Plano — fazer a receita da agência existir no sistema

> Escrito em 02/08/2026. Ordem recomendada, do que dói agora pro que é visão.
> Contexto financeiro: `../../holding-maier/saidas/procedimento-fechamento-mensal.md`

## O diagnóstico em uma frase

A tela existe, o catálogo existe, o modelo de dados existe. **O que não existe é a
ponte entre "marquei como fechado" e "virou dinheiro no sistema".**

Verificado no banco e no código em 02/08:

| Peça | Estado |
|---|---|
| `business_unit` enum com `rede_publicidade` | ✅ existe |
| `unit` + `product` em customers, invoices, subscriptions | ✅ existe |
| Catálogo `rp_products` com preço e ciclo | ✅ existe |
| Tela Braço Forte com candidatos, status `fechado`/`perdido` | ✅ existe |
| Invoices com `unit: rede_publicidade` | ❌ **zero** |
| Ponte "fechado" → cliente + fatura | ❌ **não existe** |

Marcar "fechado" hoje muda a cor de um badge. O dinheiro não é registrado em lugar
nenhum — foi exatamente assim que o Site Parceiro de R$590 (Nick, 30/07) sumiu do
relatório de julho, que reportou R$699,30 num mês de R$1.289,30.

---

## Passo 0 — registrar a venda da Anny (agora, sem código)

Antes de construir qualquer coisa: **a venda de R$590 precisa existir no banco**, senão
o relatório corrigido e os dados seguem discordando.

Um `crm_customers` + `crm_invoices` com `unit: rede_publicidade`,
`product: site-parceiro`, `amount: 590`, `sold_by: Nick`, `paid_at: 30/07`. É inserção
direta, não precisa de tela.

**Critério de pronto:** somar as invoices de julho no banco e dar R$1.289,30.

---

## Peça 1 — a ponte "fechado → venda" 🎯 *é aqui que se começa*

**O problema que resolve:** venda da agência deixa de sumir.

**O que fazer:** ao marcar um candidato como `fechado` na Braço Forte, abrir um passo que
pergunta **qual produto** (do `rp_products`) e **por quanto** (preço sugerido do catálogo,
editável — desconto acontece), e então gravar:

- `crm_customers` — se a empresa ainda não for cliente, com `unit: rede_publicidade`
- `crm_invoices` — `unit: rede_publicidade`, `product: <slug>`, `amount`, `sold_by`,
  `indicated_by`, `paid_at`
- `crm_commissions` — a comissão do vendedor, do jeito certo (`type: venda` amarrado à
  invoice), não como "ajuste" solto, que foi o que aconteceu com os R$200 do Nick

**O que NÃO entra nesta peça:** gerar a cobrança no Asaas. Hoje dá pra criar a cobrança
lá na mão, e a dor não é cobrar — é registrar. Cobrança automática é a Peça 2.

**Critério de pronto:** marcar um candidato como fechado e o valor aparecer no
fechamento do mês sem ninguém digitar nada em planilha.

**Tamanho:** uma sessão. É uma tela e uma mutação — o modelo de dados não muda.

---

## Peça 2 — cobrança recorrente (Asaas `/subscriptions`)

**O problema que resolve:** o Plano Movimento (R$250/mês) não vira receita recorrente
hoje, porque a integração só sabe cobrar uma vez (`asaas-create-payment` usa `/payments`).

Já há cliente esperando: **Acquarius sinalizou Plano Movimento** e não há como cobrá-la
mensalmente.

**O que fazer:**
- Nova edge function usando `/subscriptions` do Asaas
- Gravar `crm_subscriptions` com `asaas_subscription_id`, `billing_cycle: mensal`
- Estender `asaas-webhook` pra reconhecer pagamento de assinatura (hoje ele trata
  cobrança avulsa; o `externalReference` é `company_id|plan_slug|offer|unit`, feito pro
  Rede Baixada — precisa aceitar a forma da agência)

**Por que vem depois da Peça 1:** sem o registro da venda, uma assinatura criada no Asaas
teria o mesmo destino do site de R$590 — dinheiro entrando e nada no sistema.

**Aritmética que justifica:** R$77,70 por 6 meses = R$12,95/mês. **2 clientes no Plano
Movimento valem mais que 39 vendas de porta a porta.**

**Tamanho:** duas sessões. Mexe em edge function e webhook — é onde mora o risco.

---

## Peça 3 — status de serviço e ticket de suporte 🔵 *visão, não agenda*

A visão do Lucio (02/08): **um painel único do Rede — Baixada e Publicidade juntos** —
onde o cliente nasce lá dentro com financeiro, serviço, status e um chat estilo ticket
de suporte.

O modelo de dados já aponta pra lá (é o mesmo `crm_customers` servindo as duas unidades).
Mas isto são **duas frentes novas**, com tabelas novas:

- **Status de serviço** — o que foi contratado × o que foi entregue (site no ar? GMN
  otimizado? campanha rodando?)
- **Ticket/chat** — histórico de conversa por cliente

⚠️ **Fica registrado e não agendado.** O risco nº1 declarado do Lucio é fragmentação, e
estas duas peças não resolvem nenhuma dor de agosto. Revisitar quando as Peças 1 e 2
estiverem rodando e a receita da agência tiver volume que justifique.

---

## Ordem, e por quê

```
Passo 0  →  registrar a Anny        (hoje, sem código — fecha julho)
Peça 1   →  ponte fechado→venda     (uma sessão — para de sumir dinheiro)
Peça 2   →  cobrança recorrente     (duas sessões — destrava R$250/mês)
Peça 3   →  status + ticket         (visão — não agendar agora)
```

Cada peça é útil sozinha. Se parar depois da Peça 1, já resolveu o problema que causou o
erro de julho.

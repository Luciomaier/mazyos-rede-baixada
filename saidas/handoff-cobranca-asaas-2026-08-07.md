# Handoff — a cobrança fantasma do Asaas (07/08/2026)

> **Para quem pegar isso depois.** A parte operacional já foi feita (conta limpa, 22+38 registros
> removidos). O que sobrou é **código**, e está descrito aqui com arquivo, linha e critério de
> pronto. Contexto humano completo na memória: `rede-baixada-cobranca-nao-por-robo`.

---

## Em cinco linhas

A régua de cobrança do Asaas perseguia **clientes em dia**. O Giovani (Lava Rápido, Fundador da
Rede Baixada) recebeu semanas de *"Não registramos o pagamento"* tendo pago em 28/07 — havia uma
cobrança gêmea esquecida. A Floricultura Anny estava no mesmo caso e **não tinha reclamado**. E o
Naldo, cliente pagante do UniMasso, acumulou **16 assinaturas ativas / R$1.147,60** porque cada
clique no checkout criava uma assinatura no Asaas e quebrava logo depois.

**A regra que passou a valer: a Rede não cobra por robô. Quem cobra é gente, no WhatsApp, com
nome.** Todo código de cobrança daqui pra frente passa por essa régua.

---

## ⚠️ Antes de qualquer coisa: o estado do disco

**Há trabalho pronto e NÃO COMMITADO em dois repositórios.** Confira antes de escrever qualquer
linha — provavelmente já está feito o que você ia fazer.

### `portal/` (repo `Luciomaier/redebaixada`, branch `main`, base `fc292e5`)

| Arquivo | O que mudou |
|---|---|
| `supabase/functions/asaas-create-payment/index.ts` | `calibrarRegua()` (desliga os `PAYMENT_OVERDUE` do cliente antes de emitir) · `cobrancaReaproveitavel()` (reusa cobrança viva em vez de duplicar) · trava de empresa já `active` com `plan_expires_at` no futuro |
| `supabase/functions/asaas-webhook/index.ts` | `apagarCobrancasGemeas()` — no `PAYMENT_CONFIRMED`/`RECEIVED`, apaga as irmãs `PENDING`/`OVERDUE` da mesma `externalReference`. Só `unit === "rede_baixada"`, best-effort |
| `src/pages/OfertaParceiro.tsx` · `src/pages/Plans.tsx` | tratam `already_active` como boa notícia (toast de sucesso), não como erro |

`npx tsc --noEmit -p tsconfig.app.json` limpo (os 2 erros em `map-location-picker.tsx` e
`useAgentesDoCrm.ts` são pré-existentes, não mexer aqui).

### `unimasso/` (branch `fix/ritmo-disparo-views`, 1 commit à frente da `main`)

| Arquivo | O que mudou |
|---|---|
| `supabase/functions/asaas-create-checkout/index.ts:248` | `plan.cycle` → `subscription.cycle`. **Era o bug do Naldo** |
| `supabase/functions/_shared/whatsapp-templates.ts` | ⚠️ **NÃO É MEU** — alteração do Lucio de 04/08, não commitada. Não misturar no mesmo commit |

### `rede-baixada/` (workspace)

`scripts/auditoria-asaas.py` (novo, não versionado) e `_memoria/pendencias.md`.

---

## 🔴 TAREFA 1 — Subir o que já está pronto (bloqueada)

**Bloqueio:** o CLI do Supabase responde **403** nos dois projetos (`functions list`,
`secrets list`). O token perdeu privilégio. Destravar com `npx supabase login`.

```bash
# portal — projeto donaobtlwqrjmvjqflxz
cd portal
npx supabase functions deploy asaas-create-payment
npx supabase functions deploy asaas-webhook
npm run build && git add -A && git commit && git push   # front vai pela Vercel na main

# unimasso
cd ../../unimasso
npx supabase functions deploy asaas-create-checkout
```

**Enquanto isso não sobe, o bug do UniMasso segue criando assinatura órfã a cada clique.** É a
tarefa mais urgente da lista — a limpeza feita em 07/08 é pano no chão, isto é a torneira.

**Como verificar (sem cobrar ninguém de verdade):**
1. `asaas-create-payment`: abrir a `/oferta-parceiro` com uma empresa **já ativa** → tem que
   aparecer *"o plano já está ativo até…"*, e **nenhuma cobrança nova** no Asaas.
2. Duplo clique no checkout de empresa não paga → **uma** cobrança só; o segundo clique devolve
   `reused: true` no log da function.
3. Cliente novo criado pelo fluxo → conferir `GET /v3/customers/{id}/notifications`: os dois
   `PAYMENT_OVERDUE` com `enabled: false`.
4. ⚠️ **Testar o PaP publica empresa de verdade** (publish-first) — nomear "TESTE …" e apagar.

---

## TAREFA 2 — UniMasso: os furos que ficaram

Nenhum destes foi tocado. Em ordem de dano:

1. **`cancel-subscription` NÃO EXISTE.** `src/hooks/useSubscriptionOperations.ts:93` invoca uma
   edge function que nunca foi criada (não está em `supabase/functions/` nem no `config.toml`).
   **Ninguém consegue cancelar sozinho** — é a causa-raiz da base de churn que ficou cobrando por
   meses. Criar: `DELETE /v3/subscriptions/{id}` no Asaas + `status=canceled`, `plan_id='free'`,
   `tipo_conta='Free'` no banco. Cancelar no Asaas **já remove as cobranças pendentes e vencidas**
   da assinatura.
2. **`notificationDisabled: false` explícito** em 4 checkouts — `asaas-create-checkout:77`,
   `asaas-campaign-checkout:59`, `promo-checkout:41`, `upgrade-checkout:42`. Trocar pela mesma
   `calibrarRegua()` do portal (desliga só `PAYMENT_OVERDUE`; **não** usar `notificationDisabled`,
   que mata o recibo junto). Cliente novo **sempre** nasce com a régua padrão ligada — por isso
   tem que rodar a cada venda, não uma vez.
3. **Churn não cancela assinatura.** `asaas-webhook` trata `PAYMENT_OVERDUE` marcando `past_due`
   no banco e nada mais (*"don't immediately cancel"*, linha ~248). A assinatura PIX segue gerando
   cobrança nova todo mês, pra sempre. Definir a régua — sugestão coerente com o que foi feito na
   mão em 07/08: **30+ dias de atraso → cancelar a assinatura**; abaixo disso, deixa viva (quem
   tem 15 dias de atraso esqueceu, não saiu).
4. **`cancela-e-recria` pula `past_due`.** Os 4 checkouts filtram `.in("status",["active","pending"])`
   ao procurar a assinatura a cancelar. Quem estava em atraso e reativou fica com **duas** — foi o
   caso do Adeilton. Incluir `past_due` no filtro e **checar `response.ok` do DELETE** antes de
   criar a nova (hoje não checa: se o cancel falha, nasce duplicada assim mesmo).
5. **Sem idempotência**: duplo clique = duas assinaturas. O `upsert` por `user_id` guarda a
   última; a outra vira órfã.
6. 🔒 **Segurança, fora do escopo desta dor mas achado no caminho:** o webhook aceita POST anônimo
   se `ASAAS_WEBHOOK_TOKEN` não estiver setada (`if (webhookToken && ...)`) — dá pra forjar
   `PAYMENT_CONFIRMED` e virar Pro de graça. E `promo-checkout` não tem autenticação nenhuma:
   com o e-mail de alguém dá pra gravar CPF no cadastro dele e cancelar a assinatura dele.
7. **Verificar no banco**: nenhuma migration cria `UNIQUE(user_id)` em `subscriptions`, mas 6
   `upsert` usam `onConflict: "user_id"`. Ou foi criada na mão, ou esses upserts falham com 42P10
   **depois** de a assinatura já existir no Asaas.

---

## TAREFA 3 — Rede Baixada: o que ainda pode morder

1. **Cobrança abandonada não morre sozinha.** Quem gera o PIX na rua e não paga deixa a cobrança
   viva pra sempre. Hoje o `dueDate` é +3 dias (`dueDateStr(3)`). Opções:
   - rotina diária que apaga cobrança `rede_baixada` `PENDING`/`OVERDUE` com N dias de vencida
     (filtrar por `externalReference` terminando em `|rede_baixada` — **a conta é compartilhada**);
   - `daysAfterDueDateToRegistrationCancellation` na criação: documentado para boleto e o PIX
     associado a ele; **para PIX puro a doc não garante** — testar em sandbox antes de confiar.
2. **Cliente Asaas duplicado.** O Giovani tem `cus_000190077528` e `cus_000190077529`, mesmo CNPJ,
   criados no mesmo segundo. `findOrCreateCustomer` busca por `cpfCnpj`, então a corrida foi de
   dois cliques simultâneos. Não quebra nada hoje, mas suja a carteira.
3. **`crm_invoices` só conhece fatura PAGA.** O webhook só grava no `PAYMENT_CONFIRMED`. Por isso
   ninguém tinha como saber, pelo nosso sistema, que havia 263 cobranças vivas — foi preciso ir
   no Asaas. Se for gravar cobrança emitida, cuidado com o gatilho `trg_comissao_da_fatura`
   (comissão nasce da fatura; fatura pendente não pode gerar comissão).

---

## 🚫 A régua da casa — não desfazer sem decisão do Lucio

- **Nunca reativar `PAYMENT_OVERDUE`** em cliente nenhum. É a notificação que repete a cada 7 dias
  pra sempre e aciona robô de voz. Ficam ligados `PAYMENT_CREATED`, os dois
  `PAYMENT_DUEDATE_WARNING`, `SEND_LINHA_DIGITAVEL`, `PAYMENT_RECEIVED` e `PAYMENT_UPDATED`.
- **Não usar `notificationDisabled: true`** como padrão: mata o recibo e o aviso de vencimento
  junto, que são o que o cliente *quer* receber. É o botão nuclear, para caso extremo.
- **Nunca emitir cobrança pra quem já está em dia.** Se a empresa está `active` com validade no
  futuro, o caminho é dizer "está tudo certo", não gerar boleto.
- **Atraso curto não é churn.** Cancelar assinatura apaga as cobranças pendentes dela — ou seja,
  tira do cliente a chance de pagar. Abaixo de 30 dias, deixa viva e sem robô.

---

## Fatos da API do Asaas já apurados (não repesquisar)

- A configuração da régua mora no **CLIENTE**; o disparo é **por cobrança**. Não existe régua por
  produto, plano ou cobrança individual.
- **As notificações são agendadas quando a cobrança NASCE, e o agendamento não é cancelável.**
  Calibrar o cliente só vale pra cobrança futura. Cobrança já viva → apagar a cobrança.
- Cirúrgico: `GET /v3/customers/{id}/notifications` → `PUT /v3/notifications/batch`
  (`{customer, notifications:[{id, enabled:false}]}`). As 8 notificações são fixas: dá pra
  editar, nunca criar nem apagar.
- `DELETE /v3/payments/{id}` é reversível: `POST /v3/payments/{id}/restore`.
- `DELETE /v3/subscriptions/{id}` **remove as cobranças pendentes e vencidas** dela; as pagas
  ficam no histórico. Alternativa reversível: `status: INACTIVE`.
- Assinatura gera a próxima cobrança **40 dias antes** do vencimento.
- Chave de API é **da conta**, não do negócio — qualquer chave enxerga RB + Publi + UniMasso.
  Chave sem uso é desabilitada em 3 meses e expira em 6.

## Ferramenta

`scripts/auditoria-asaas.py` — relatório de cobrança viva, gêmeas e régua, com
`--apagar` / `--calibrar` / `--silenciar`. Leitura automática; escrita só com ID explícito.
Chave em `~/.asaas-key`, fora do repo.
⚠️ A heurística de "gêmea" por `externalReference` **dá falso positivo no UniMasso**, que usa o
slug do plano (`pro_monthly`) igual pra todo mundo. Na RB a referência carrega o `company_id` e é
única. Se for mexer no script, corrigir isso: gêmea de verdade é **avulsa** (sem `subscription`),
vencida, e com outra cobrança **paga** da mesma referência.

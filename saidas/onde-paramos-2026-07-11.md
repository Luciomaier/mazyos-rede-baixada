# Onde paramos — 11/07/2026 (fim da sessão) · **HANDOFF pro Bloco 3**

> Leia este arquivo inteiro antes de começar. Ele existe pra uma sessão nova conseguir continuar
> sem repetir descoberta nenhuma.
>
> **Próxima tarefa: Bloco 3 — Ciclo do trial.** Plano completo:
> [`sprint-2-2026-07.md`](sprint-2-2026-07.md) · raio-X: `~/.claude/plans/polished-sparking-lerdorf.md`

---

## ✅ O que ficou PRONTO hoje (tudo em produção, verificado)

| Bloco | Estado |
|---|---|
| **Teste do fluxo 77,70** | ✅ passou ponta a ponta em produção (link → cadastro → auto-login → CPF → checkout Asaas em R$77,70, com PIX) |
| **Faxina do banco** | ✅ 46→39 empresas, 18→3 usuários (Lucio, Elis, Nick), 40→36 leads. Nada órfão |
| **Bloco 1 — quick wins** | ✅ `main = 4679a44` |
| **Bloco 2 — Fase 0 (keystone)** | ✅ `main = 6861bac` · webhook **v15** · create-payment **v20** · migration `20260711220000_fase0_crm_ledger.sql` |

### Fase 0 — o que o webhook faz agora
`asaas-webhook` (ACTIVATE) → escreve **`crm_customers`** (com `owner_user_id` = a carteira) →
**`crm_subscriptions`** (`next_due_date` = relógio da renovação) → **`crm_invoices`** (`sold_by`,
`indicated_by`, `unit`). REVOKE (estorno) reverte tudo. **Idempotente** (3 eventos → 1 fatura).

`externalReference` v2 = `company_id|plan_slug|offer|unit|sold_by|indicated_by`
*(as 3 primeiras posições são as da v1 — cobranças antigas continuam sendo lidas)*.

---

## 🎯 BLOCO 3 — Ciclo do trial (a próxima tarefa)

**Por que:** metade do playbook de porta a porta **não tem sistema**. O caminho do "vou pensar"
(trial) hoje é planilha + WhatsApp. A empresa nasce `approved` direto, sem relógio, sem cinza, sem
expiração, sem repescagem. É o que converte o indeciso em dinheiro.

**Regra de negócio completa:** [`regra-negocio-parceiro-2026-07.md`](regra-negocio-parceiro-2026-07.md)

**Estados:** `trial 7d → pago 6m → 🩶 cinza/inclicável → oculto → expirado`

**O que construir:**
1. **Migração de estados** — enum/colunas de ciclo + **gravar o vencimento** (7d de trial / 6m de plano).
2. **Jobs `pg_cron`** que viram o estado sozinhos (trial vence → cinza → oculto → expirado).
3. **Repescagem** por e-mail (Brevo) na janela.
4. ⚠️ **Desenhar a máquina de estados GENÉRICA** — o mesmo motor vai servir pro ciclo do agente depois
   (ver `modelo-abc-agentes-2026-07.md`).

**Já existe pronto (reusar, não reconstruir):**
- 🩶 **O "cinza" já existe pela metade**: `src/components/CompanyCard.tsx:32` aplica `grayscale opacity-60`
  + badge "Inativo" quando `isPlanExpired(company)`.
- `isPlanExpired()` e `getPlanBadges()` em `src/hooks/usePlans.ts` — **fonte única** dos selos/estado visual.
  **Não espalhar comparação de `plan_slug` pelos componentes** — foi assim que quebrou antes.
- `companies.plan_expires_at` já é gravado pelo webhook.

---

## 🧠 Fatos do banco que custaram caro pra descobrir (não redescobrir)

1. **As EMPRESAS nunca foram migradas pros planos novos.** Distribuição real das 39:
   `free`=21 · **`pro`=12** · **`profissional`=3** · **`premium`=1** · `destaque`=1 · `autoridade`=1 ·
   **`presenca`=0**. O código suporta os dois mundos via `LEGACY_PLAN_EQUIVALENT` (`usePlans.ts`).
   ➡️ Migrar as 16 legadas é **decisão comercial pendente do Lucio** (muda preço e recursos).
2. **`companies` NÃO tem coluna de dono.** A titularidade vive em **`company_members`** (`user_id` + `role`).
   E existe um **trigger** que cria o `company_members` no insert usando `auth.uid()`.
3. **`crm_customers` não tinha campo de agente** — foi a Fase 0 que criou `owner_user_id`.
4. **Enums do CRM** (usar exatamente estes):
   - `crm_customer_status`: `ativo | inadimplente | cancelado | trial`
   - `crm_invoice_status`: `pending | confirmed | overdue | refunded`
   - `crm_subscription_status`: `active | overdue | canceled | expired`
   - `crm_payment_method`: `pix | boleto | cartao` *(quando a loja de créditos existir, add `credito_carteira`)*
   - `crm_lead_status`: 7 valores (`novo | qualificacao | contato_feito | negociando | convertido | requalificacao | perdido`)
5. **Idempotência do PostgREST exige CONSTRAINT, não índice parcial.** `upsert onConflict` **não infere
   índice parcial** — o insert falha calado. (Foi o bug da Fase 0: a fatura não era criada e o webhook
   respondia 200.) Em Postgres, `unique` já permite vários NULL.

## 🔧 Como operar (o que funciona / o que não funciona)

- **SQL em produção:** pelo **SQL Editor do Supabase no browser** (o Lucio está logado). O CLI **não está
  linkado** e não temos a senha do banco.
  - ⚠️ **Digitar no Monaco não é confiável** (concatena com o texto salvo). Setar assim:
    `window.monaco.editor.getModels()[0].setValue(sql)` → clicar no botão **Run** → confirmar o diálogo
    "Run query" (aparece pra query destrutiva).
  - Pra inserir empresa via SQL, precisa simular o usuário (por causa do trigger):
    `select set_config('request.jwt.claims','{"sub":"<uuid>","role":"authenticated"}', true);` **na mesma
    transação** do insert.
- **Deploy de edge function:** `supabase functions deploy <nome> --project-ref donaobtlwqrjmvjqflxz` — **funciona**.
- **Testar o webhook sem gastar dinheiro:** POST direto na URL do webhook (o token está no painel do
  Asaas → Integrações → Webhooks → "Rede Baixada"; **NÃO está neste repo, por segurança**). Foi assim que
  a Fase 0 foi validada.
- **Deploy do front:** branch → preview Vercel (o preview exige login Vercel — abrir pelo Chrome do Lucio) →
  merge na `main` → produção.
- **Contas de teste:** admin `redebaixada@gmail.com` · agente `elis@redepublicidade.com.br` — senha `123456`.
- **Sempre marcar dado de teste como "TESTE ..." e limpar no fim.**

## 📌 Pendências que dependem do Lucio (não são código)

- [ ] **Cancelar a fatura Asaas 855418887** (R$77,70, vence 14/07) — sobra do teste de hoje.
- [ ] **Decidir:** migrar as 16 empresas dos planos legados?
- [ ] **Ir pra rua.** O gargalo do caixa é venda, não commit.

## 🅿️ Estacionado (com gatilho) — NÃO construir agora

**Loja de créditos / lotes**, **modelo ABC (qualificação de agentes)**, **carteira virtual**,
**supervisor**, **override/MLM** *(esse foi **decidido: não**)*. Tudo em
[`modelo-abc-agentes-2026-07.md`](modelo-abc-agentes-2026-07.md) — com os gatilhos de quando destravar.
A Fase 0 já deixou as portas abertas (`sold_by`, `indicated_by`, `owner_user_id`).

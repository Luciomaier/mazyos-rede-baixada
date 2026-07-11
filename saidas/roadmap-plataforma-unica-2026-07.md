# Roadmap — Rede Baixada como plataforma única do grupo (evolução gradual)

> Fonte viva do roadmap. Decidido e aprovado com o Lucio em **10/07/2026** (plan mode).
> Companion: regra do parceiro → [`regra-negocio-parceiro-2026-07.md`](regra-negocio-parceiro-2026-07.md) ·
> oficina/manual do agente → [`oficina-agente-2026-07.md`](oficina-agente-2026-07.md) ·
> sprint técnico → [`sprint-nick-crm-mobile-2026-07.md`](sprint-nick-crm-mobile-2026-07.md).

## Por que existe

O Rede Baixada é o **cavalo-de-troia** da holding: ticket baixo (parceiro R$77,70/6m = plano Presença), baixa resistência, **porta de entrada** pro foco nº1 (Rede Publicidade). O LTV real não está no portal — está na graduação do cliente pra **GMN Turbinado (R$149,70)**, **Site Parceiro (R$590/ano)** e **Plano Movimento (R$250/mês, tráfego)**.

O Lucio quer que o cliente veja **"uma rede só"**: um registro único, com histórico de serviços, pagamentos guardados, e um link no próprio dashboard pra contratar mais ou falar com a equipe.

**Descoberta que muda a viabilidade (sessão 10/07):** o backbone de ERP/CRM **já existe no schema do portal** — grande parte do roadmap é "ligar fio", não construir do zero.

## Decisão de arquitetura

**Rede Baixada = plataforma ÚNICA ("uma rede só"), monólito modular, em camadas.** Portal-como-porta e ERP-de-serviços são duas vistas do MESMO registro de cliente. Guardrail: um só banco, com **tag de unidade (Rede Baixada × Rede Publicidade)** pra separar receita — **sem** ERP separado. **UniMasso fica fora** (SaaS próprio; só compartilha a conta Asaas).

## O que já existe vs greenfield

| Já existe no schema (só ligar) | Greenfield de verdade |
|---|---|
| `crm_customers` (carteira, CRUD pronto) | Webhook Asaas → CRM (hoje só toca `companies`) |
| `crm_subscriptions` (recorrência: `next_due_date`, `asaas_subscription_id`…) — sem UI | Tag de unidade (RB × Publi) |
| `crm_invoices` (faturas) — sem UI | Claim/ghost (reivindicar empresa) |
| `crm_commissions` (agente, %, tipo) — só leitura | Estados de ciclo (trial/cinza/oculto/expirado unificados) |
| `moderator_assignments` (território bairro/categoria) | Projetos/briefings/propostas/OS |
| `company_members` (multi-empresa, sem limite) + transfer-owner | — |
| `plans` + `useCompanyPlan()` (plan gating maduro) | — |

## Fases (por dependência — gradual)

- **Fase 0 ⭐ (keystone):** fechar o ciclo de cobrança no CRM. `asaas-webhook` passa a escrever `crm_customers`+`crm_subscriptions`+`crm_invoices`; `externalReference` carrega `unit`; coluna `unit` (enum `rede_baixada|rede_publicidade`). Alicerce de tudo. **[M]**
- **Fase 1:** Carteira/LTV (admin: ligar UI de subscriptions/invoices, receita por unidade) + **"Meus Serviços"** no dash do cliente (histórico + CTA "contratar / falar com a equipe"). **[M]**
- **Fase 2:** GMN Turbinado, Site Parceiro, Movimento como **produtos vendáveis** no mesmo ledger (a escada real, pedido/pagamento guardados). **[M–G]**
- ~~**Fase 3:** Comissão automática (invoice paga → comissão pro `assigned_to`) + painel do "representante".~~
  ⛔ **SUBSTITUÍDA em 11/07/2026 — decisão do Lucio: o LOTE DE CRÉDITO mata a comissão.**
  O agente **compra crédito em lote com desconto** (ex.: 10 a R$54,39), cobra o cliente **em dinheiro/PIX na
  hora** e **ativa na hora** debitando o saldo. **A comissão vira SPREAD** — já embolsada na venda. Não existe
  cálculo, aprovação, repasse nem inadimplência. E a casa **recebe antes** da venda acontecer (caixa
  antecipado). Detalhe e riscos: [`modelo-abc-agentes-2026-07.md`](modelo-abc-agentes-2026-07.md).
  ➡️ **Nova Fase 3 = "Loja de créditos"**: lotes promocionais + ledger da carteira + ativação por saldo
  (grava `crm_invoice` com `payment_method = credito_carteira`, **sem passar pelo Asaas**). **[M]**
  ⚠️ **A comissão NÃO morreu na escada de upsell** (GMN R$149,70 · Site R$590 · Movimento R$250/mês) — esses
  têm **entrega real** por trás e não cabem num crédito de ativação. **E é ali que mora o LTV.** Como o agente
  ganha no upsell é **pergunta em aberto** (comissão? crédito? split?) — resolver na **Fase 2**.
  ⚠️ **Antes do primeiro lote vendido:** falar com **CONTADOR** — vender crédito muda a natureza fiscal de
  *agência com comissão* pra **distribuição/revenda** (quem emite nota pro cliente final?).
  📈 **Métrica que nasce de graça:** a **taxa de recompra de lote** É a medida de atividade do agente. Quem
  vende, acaba o crédito e volta. Quem não vende, não volta. **Sem meta, sem fiscalização, sem relatório.**
- **Fase 4** *(paralelo)*: **Claim/ghost** — perfil-fantasma + "esta empresa é sua? ative agora", com o contato já capturado como isca ("8 pessoas já te procuraram"). Moderação **no claim**. **[M–G]**
- **Fase 5:** **Chamados / OS** + entrega (briefings/propostas/status). 100% greenfield, por último. **[G]**

**Quick wins (encaixam cedo):** selo **Verificado na Presença** (ressignificado como "negócio visitado/confirmado" — a visita do agente É a verificação; 2 selos: ✅ Verificado × 👑 Autoridade) · alinhar **status agente×admin** (matar "Qualificação" órfã) · fix de copy do Mini CRM ("Premium" → "Autoridade").

**Fora por agora:** franquia formal (COF/jurídico) — começar como "rede de representantes" · auto-roteamento de lead por território · hierarquia de sub-agentes.

## Execução

Cada fase é execução separada, no fluxo provado na sessão: **branch → preview Vercel → verificar → promover pra produção**. Detalhe técnico completo (arquivos, tabelas, verificação por fase) no plano aprovado: `~/.claude/plans/sim-ativei-o-modo-jaunty-brook.md`.

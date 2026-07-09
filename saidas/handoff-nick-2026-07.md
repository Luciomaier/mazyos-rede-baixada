# Handoff pro Nick — Rede Baixada (09/07/2026)

> ⚠️ **ATUALIZAÇÃO 09/07 (tarde):** o Nick está **fora do projeto por ora** — a execução (dev
> incluído) é Lucio + Claude. Este doc virou **backlog de execução nosso**, não fila pro Nick.
> Estado atual e ordem de retomada: `saidas/onde-paramos-2026-07-09.md`.
>
> Tudo num lugar só. **O fluxo de pagamento do `/oferta-parceiro` já está 100% no ar e verificado
> (09/07) — não precisa mexer.** O que sobra é o mobile da rua (P1, em preview) + self-serve + ciclo.
> Repo do site: `github.com/Luciomaier/redebaixada` (pasta `portal/`). Supabase: `donaobtlwqrjmvjqflxz`.

## ✅ P0 — Pagamento do link de rua: FEITO (verificado 09/07, não fazer nada)

Conferido via CLI, tudo ACTIVE em produção:
- Functions `asaas-create-payment` (v19) e `asaas-webhook` (v14) deployadas.
- Secrets `OFFER_PARCEIRO_KEY` (=`b036e66...`) e `OFFER_PARCEIRO_VALUE` (=`77.70`) setados e corretos.
- Asaas em produção (`www.asaas.com/api/v3`). Gate do preço é server-side; ativa presença 6 meses.
- Webhook exige token (`ASAAS_WEBHOOK_SECRET`) → 401 sem ele; idempotente; revoga estorno/chargeback.
  **→ o item "webhook validar assinatura" do sprint já está coberto. Sai da lista.**

## P1 — Visão do agente mobile (destrava a captura na rua) — prioridade

Fricção é de fluxo/UX, **não** de performance (~180ms). Do `saidas/sprint-nick-crm-mobile-2026-07.md`:
- **Cards no lugar da tabela** em "Meus Leads" — **reusar o card do kanban do admin** (já existe),
  não construir do zero.
- **Botão flutuante "＋ Novo Lead"** + **PWA "adicionar à tela inicial"** → captura em 1 toque.
- **+4 campos** no form de lead: ramo, bairro, oferta (77,70/250), próxima ação (podem começar em `notes`).
- **Unir Telefone + WhatsApp**; **Origem default "Visita"** (hoje vem "Outro").
- **Consertar deep-link** (`/dashboard/...` cru joga pro `/dashboard`) e **persistência de sessão**
  (deslogou sozinho numa das vezes) — pra salvar atalho e não cair no meio da rua.

## P2 — Self-serve + ciclo de estados (em seguida)

- **"Criar Empresa" na mão do agente** (hoje só no admin) — no card do lead *Convertido*; publica
  como **trial** + alerta "pending moderate" pro admin (1 clique, não bloqueia).
- **Ciclo de estados da empresa:** `demo → publicado-trial (7d) → publicado-pago (6m) → cinza/inclicável
  → oculto → expirado`. Timer de 7d (pagamento × moderação desacoplados). **Oculto não apaga**
  (reativa em 1 clique). **Gravar o vencimento desde o 1º parceiro** (pro facão dos 6 meses).
- **Referência externa por unidade** na cobrança (separar receita RB × UniMasso na conta única).
  *(Obs.: o `externalReference` já carrega `company_id|plan_slug|parceiro` — falta só a marca de unidade.)*

Regra de negócio completa: `saidas/regra-negocio-parceiro-2026-07.md`.

---

## Mensagem pra mandar (WhatsApp)

> Nick, o pagamento do link de rua do Rede Baixada **já tá no ar e testei tudo** (functions,
> secrets, Asaas produção, webhook) — não precisa mexer nisso. Consolidei o que falta num doc só
> (`saidas/handoff-nick-2026-07.md`), quando você voltar pra esse projeto:
>
> **P1 (destrava a rua):** visão do agente mobile — trocar a tabela de leads por cards (reusa o
> card do kanban do admin), botão flutuante "＋ Novo Lead" + PWA, e consertar deep-link/sessão
> (tá deslogando na rua).
>
> **P2:** "Criar Empresa" self-serve no card do lead + ciclo de estados da empresa (gravar
> vencimento desde já).
>
> Sem pressa — detalhe de cada um no doc. Valeu!

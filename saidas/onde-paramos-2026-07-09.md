# Onde paramos — sessão 09/07/2026 (ponto de retomada)

> Pausa combinada com o Lucio pra retomar em algumas horas e "torar" o P2.
> **Contexto de time:** Nick fora do projeto por ora — execução (front + backend Supabase) é
> **Lucio + Claude**. Ver memória `rede-baixada-nick-fora-execucao`.

## ✅ Concluído hoje

1. **Fluxo `/oferta-parceiro` verificado 100% no ar** (era pendência velha). Provado por CLI:
   functions `asaas-create-payment` v19 + `asaas-webhook` v14 ACTIVE; secrets
   `OFFER_PARCEIRO_KEY`=`b036e660589d546db056951c` e `OFFER_PARCEIRO_VALUE`=`77.70` (hash conferido);
   Asaas produção (`www.asaas.com/api/v3`); webhook seguro por token; ativa 6 meses. Front live (HTTP 200).
2. **Faxina de pendências** — `_memoria/pendencias.md` reescrito pro estado real.
3. **Preço travado** R$77,70/6m (justificativa "produto com serviço embutido" na skill + memória).
4. **Logo** colorido em `identidade/logo.png` + design-guide atualizado.
5. **P1 (mobile do agente) — corte rápido FEITO e EM PREVIEW** (ver abaixo).

## 🔵 P1 — em preview, aguardando merge

- **Branch:** `p1-agente-mobile` (repo `portal/`, já commitada e pushada). Commit `92a7d32`.
- **Preview Vercel (produção intacta):**
  `https://redebaixada-git-p1-agente-mobile-lucio-maiers-projects.vercel.app`
  → logar como agente/moderador → `/dashboard/minha-area/leads`.
- **O que mudou** (`src/pages/dashboard/agent/AgentLeads.tsx`): tabela de 6 colunas → **cards**
  responsivos; **botão flutuante "Novo Lead"**; **contato unificado** (WhatsApp/Telefone) + link
  wa.me tocável; **origem default "Visita"**; as +4 infos entram em Observações (versão leve).
- **Lucio testou e aprovou** ("ficou muito bom"). **➡️ Próximo passo: merge na `main`** (aí vai pro
  ar). Comando: `git checkout main && git merge p1-agente-mobile && git push` (dentro de `portal/`).
- **P1 fase 2 (backlog):** PWA "adicionar à tela inicial" (falta manifest), +4 campos como colunas
  dedicadas, e consertar deep-link/persistência de sessão.

## 🟠 P2 — nosso backlog (é backend; achados técnicos já levantados)

**Item 1 — "Criar Empresa" self-serve no card do lead Convertido do agente:**
- ✅ RLS deixa o agente criar **company** (policy "Authenticated users can create companies").
- ❌ RLS **NÃO** deixa o agente criar **crm_customers** (policy "Admins can manage crm_customers" =
  só admin) → precisa de **migração**: um RPC `SECURITY DEFINER` (ex.: `agent_create_company_from_lead`)
  OU uma policy pra moderator. O admin hoje cria company `approved` + crm_customer `trial`
  (`src/pages/dashboard/admin/crm/Leads.tsx:106`).
- ⚠️ Público só mostra empresa **`approved`** (`src/hooks/usePublicCompanies.ts:22`) → "publicar na
  hora" = criar como `approved`.
- ⚠️ **Gap de design a resolver:** empresa criada pelo agente (sem owner) × pagamento do cliente
  pelo link (a `OfertaParceiro` amarra pagamento à empresa do usuário logado). Precisa de um passo
  de **claim/vínculo** pra o pagamento do cliente ativar a empresa que o agente criou. **Decidir isso
  antes de codar** — é o coração do "done-for-you".

**Item 2 — Ciclo de estados da empresa** (`demo → publicado-trial 7d → publicado-pago 6m → cinza →
oculto → expirado`):
- ❌ enum `company_status` só tem `pending/approved/rejected` → precisa **migração** (novos estados ou
  colunas: `trial_expires_at`, flag de visibilidade "cinza/oculto") + **jobs agendados (pg_cron)** pros
  timers de 7d/6m. É a parte mais pesada. **Gravar o vencimento desde o 1º parceiro** (já dá pra usar
  `plan_expires_at`, que o webhook já seta em 6m).

**Item 3 — Referência externa por unidade** (separar receita RB × UniMasso na conta única):
- Mexe na edge function `asaas-create-payment` (o `externalReference` já é `company_id|plan_slug|parceiro`;
  falta a marca de unidade) + ajustar o parse no `asaas-webhook`. Backend de produção — cuidado.

## ▶️ Como retomar ("torar" o P2) — ordem sugerida

1. **Merge do P1 na main** (destrava a rua pra valer) — se o Lucio confirmar.
2. **Decidir o gap de design do item 1** (claim/pagamento da empresa criada pelo agente) — 10 min de conversa.
3. **Item 1 backend + UI:** migração do RPC `agent_create_company_from_lead` (company approved +
   crm_customer trial + link do lead) → botão "Criar Empresa" no card do agente → testar no preview.
4. **Testar o FLUXO COMPLETO** no preview: captura lead → converte → cria empresa → paga pelo link 77,70 → 6 meses.
5. **Item 2 (ciclo/cron)** e **item 3 (ref por unidade)** como fases seguintes, com cuidado em produção.

## 🔑 Referências rápidas

- Supabase project-ref: `donaobtlwqrjmvjqflxz` (CLI desta máquina TEM acesso; o 403 antigo acabou).
- Link da oferta (QR da folha): `redebaixada.com.br/oferta-parceiro?k=b036e660589d546db056951c`.
- Roadmap da holding: `../holding-maier/saidas/plano-prospeccao-redes-2026-07.md` + `decisoes-comercial-rede-2026-07-09.md`.
- Skill de venda: `.claude/skills/venda-porta-a-porta/`.
- Backlog detalhado do portal: `saidas/handoff-nick-2026-07.md` (agora backlog nosso) + `regra-negocio-parceiro-2026-07.md`.

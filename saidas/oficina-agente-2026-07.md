# Oficina do Agente — treino + refino do fluxo (Rede Baixada)

> **Lucio + IA** (o Nick está só no Holos Connect até entrar aqui). Visão dupla **AGENTE × ADMIN**.
> Objetivo: o Lucio virar um agente excelente e **depois duplicar** (Barça/Gi), refinando o portal
> enquanto opera. Criado 10/07/2026.

## Contexto a ler antes (nesta pasta)
- **Regra de negócio:** `saidas/regra-negocio-parceiro-2026-07.md` (trial + publish-first + 7d + cinza + repescagem)
- **Fricções a consertar:** `saidas/sprint-nick-crm-mobile-2026-07.md`
- **Teste do link 77,70:** `saidas/teste-e-limpeza-fluxo-77.md`
- **Playbook de venda:** `.claude/skills/venda-porta-a-porta/` (SKILL.md + folha-vendas.md)
- **Código:** `portal/` · Agente: `/dashboard/minha-area/leads` · Admin: `/dashboard/admin/crm/leads`

## Parte 1 — Percorrer o fluxo AO VIVO (visão dupla) e marcar o que trava
Cada passo: o que o **AGENTE** faz × o que o **ADMIN** vê/faz.
> **Rodado 10/07 (Lucio+IA).** Ambiente: dev local + preview Vercel contra Supabase de produção;
> visão dupla com conta agente (Elis, `moderator`) × conta admin (`redebaixada@`, super_admin).
- [x] 1. Login agente (Elis) → **caía na home** (bug F1) → **corrigido**: agora cai direto em `/minha-area/leads`.
- [x] 2. **Capturar lead** "TESTE Claude" — criado como cards (`crm_leads`, status `novo`, `assigned_to=Elis`); ADMIN viu no kanban (Novo). ✓
- [x] 3. **Mover status** Novo→Qualificação→Negociando — persistiu e cruzou pros dois lados. ✓
- [x] 4. **Fechou → Criar Empresa** (ADMIN, card Convertido) — cria `companies` **approved (live)** + `crm_customer` **trial**, vincula o lead. Funciona, mas **diverge da regra** (ver Parte 2).
- [ ] 5. **Publicar como trial + "pending moderate"** — ❌ **NÃO existe**: a empresa nasce `approved` (pública/indexável na hora), sem portão de moderação.
- [ ] 6. **Link de pagamento** (Asaas) — caminho **separado** (`/oferta-parceiro`), não plugado no "Criar Empresa". É a **Parte 3**.
- [ ] 7. **cinza/expirado** — ❌ estados do ciclo não implementados; sem vencimento gravado (7d/6m).
- [ ] 8. **Comissão** por `assigned_to` — `assigned_to` grava certo, mas **sem tela/dados** (fase 2).

### Bugs de fluxo achados e JÁ CORRIGIDOS (no ar em produção — 10/07)
- **F1 — login caía na home pública.** Agora roteia por papel: agente→`/minha-area/leads`, admin→`/dashboard/admin`. (`Login.tsx` + `signIn` prima o contexto).
- **F2 — deep-link/refresh de rota protegida bounceava pro `/dashboard`.** Causa: `AuthContext` zerava `isLoading` antes de carregar os papéis. Corrigido → atalho PWA do agente agora é viável.
- **View de cards + botão flutuante** (P1 do sprint, que estava só no preview) **promovida pra produção** junto. `main = 8e767bc`.
- ⚠️ **Nota de teste:** o Radix Select (dropdown de status) e drawers só commitam por **teclado/pointer real**, não por clique sintético — lembrar ao automatizar.

## Parte 2 — Refinar o portal (status em 10/07)
**Já no ar (promovido nesta sessão):**
- [x] Cards no lugar da tabela · [x] Botão flutuante "＋ Novo Lead" · [x] Unir Telefone+WhatsApp · [x] Origem default "Visita"
- [x] Consertar **deep-link** (F2) — feito. (Persistência de sessão: não reproduziu de novo; observar.)

**Backlog priorizado (o que ficou):**
1. [ ] **Alinhar status agente × admin** — o dropdown do agente tem 7 status (inclui *Qualificação*), o kanban admin só 6 (`STATUS_COLUMNS` sem `qualificacao`). Lead em "Qualificação" **some do kanban** e o admin não consegue tirar. Barato: add coluna OU remover do agente.
2. [ ] **"Criar Empresa" self-serve no agente** — hoje só admin (`CrmLeads.tsx`). Expor no card do lead convertido do agente.
3. [ ] **Ciclo do trial de verdade** (o mais pesado, casa com a regra): empresa entra como **trial/pending-moderate** (não `approved` direto) + **gravar vencimento** (7d pagamento / 6m) + alerta "pending moderate" pro admin. Hoje `handleCreateCompanyFromLead` cria `approved` sem relógio.
4. [ ] **+4 campos estruturados** no form (ramo, bairro, oferta, próxima ação) — hoje vivem só no placeholder de `notes`.
5. [ ] **"Adicionar à tela inicial" (PWA)** — agora viável com o F2 corrigido.
6. [ ] **Comissão** — wire da tela por `assigned_to` (tabela existe, sem dados/rota).
7. [ ] Webhook `asaas-webhook`: **validar assinatura** · **Referência externa por unidade** (RB × UniMasso).

## Parte 3 — Teste do link 77,70 de ponta a ponta
- [ ] Abrir o link de oferta parceiro → ir até o checkout/PIX (o "teste final do operador" pendente)

## Regras da oficina
- Dado de teste sempre marcado **"TESTE Claude"** + limpar no fim.
- Nada em produção sem confirmar.
- Cada melhoria **commitada** (`/salvar`) na pasta `rede-baixada`.
- Ao final, este roteiro vira o **manual do agente** pra duplicar (Barça/Gi).

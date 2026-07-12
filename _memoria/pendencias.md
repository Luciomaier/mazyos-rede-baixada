# Pendências

> O que ficou em aberto e precisa de ação. Atualizar conforme for resolvendo.
> Última faxina: **09/07/2026** (bateu contra o estado real do repo/portal).

## Abertas

### Backlog de execução — dev do portal (Lucio + Claude; **Nick fora** por ora)
> Ponto de retomada detalhado: `saidas/onde-paramos-2026-07-09.md`.
- [x] **P1 — visão do agente mobile** — **na `main` e em produção** (`main = 8e767bc`, 10/07), junto
  com os fixes de login F1/F2 (rota por papel, deep-link/refresh).
- [ ] **P1 fase 2** — PWA (manifest), +4 campos dedicados, persistência de sessão.
- [ ] **P2 item 1 — "Criar Empresa" self-serve** — precisa migração (RPC `SECURITY DEFINER`; agente
  não pode inserir `crm_customers`) + decidir o gap de claim/pagamento da empresa criada pelo agente.
- [ ] **P2 item 2 — ciclo de estados** (`trial 7d → 6m → cinza → oculto → expirado`) — migração de
  enum/colunas + jobs agendados (pg_cron). ➡️ **Promovido a item 4 do Sprint 2** (na frente da Fase 1):
  é a metade do playbook de PaP que não tem sistema.
- [ ] **P2 item 3 — referência externa por unidade** (RB × UniMasso) — edge function de pagamento.
  ➡️ Absorvido pela **Fase 0** do Sprint 2 (junto com a tag de unidade e o **vendedor** no
  `externalReference` — hoje é só `company_id|plan_slug|parceiro`, sem agente).

### Depende do Lucio (ação manual)
- [ ] **Cancelar a fatura Asaas 855418887** (R$77,70, vence 14/07) — sobra do teste de 11/07.
- [ ] **DECISÃO: migrar as 16 empresas dos planos legados?** (descoberto 11/07) — a base paga ainda está
  em `pro` (12), `profissional` (3) e `premium` (1); os planos novos (`presenca`/`destaque`/`autoridade`)
  têm **outro preço e outros recursos**. O código hoje trata os dois mundos (`LEGACY_PLAN_EQUIVALENT` em
  `usePlans.ts`), então **não é urgente** — mas enquanto não migrar, convivem dois vocabulários de plano.
  Migrar é decisão comercial (o que cada cliente passa a receber e a pagar), não técnica.
- [ ] **Imprimir a folha de vendas** — conteúdo já corrigido e conferido (6 meses,
  "menos de R$13/mês", sem vitrine/vagas). PDF pronto: `marketing/folha-vendas-parceiro-v2.pdf`
  (cliente) e `marketing/folha-operador-pap.pdf` (interno). Abrir → Ctrl+P → A4, frente-e-verso.
- [ ] **Conectar Meta Ads + Google Ads (MCP)** — exige OAuth em sessão interativa: rodar `/mcp`.
- [ ] **Substituir o Uber pela Rede Baixada** — rotina mapeada em
  `saidas/rotina-substituir-uber-2026-07.md`. A troca em si é comportamental/consistência.
  (Referência: R$338,50 em 4h na RB vs ~R$150 em 5h no Uber.)

### Micro-tarefas (quando precisar)
- [ ] **Versão branca do logo** (fundo escuro) — só quando houver peça visual sobre o
  gradiente azul (slide final de carrossel, hero). Colorido já em `identidade/logo.png`.

## Adiadas (com gatilho)

- **Conta Asaas separada da Rede Baixada** — hoje a RB divide a conta Asaas (conta única
  do grupo/Rede Publicidade) e funciona (webhooks se ignoram por referência externa).
  **Gatilho pra isolar:** quando o caixa da RB justificar (receita recorrente própria) OU
  quando a contabilidade exigir separar. Sem urgência.

## Resolvidas

- [x] **Faxina do banco de produção** (11/07/2026) — apagados **7 empresas**, **15 usuários** e **4 leads**
  de teste. Sobrou: **3 usuários** (Lucio, Elis, Nick) e **39 empresas** (todas reais). Nenhuma empresa
  ficou órfã (conferido antes: `company_members` dos apagados = 0).
  ⚠️ **Falta só o Lucio:** cancelar a **fatura Asaas 855418887** (R$77,70, vence 14/07) — o Chrome não tem
  sessão no Asaas, não dá pra fazer por aqui.
- [x] **Teste do fluxo 77,70 ponta a ponta** (11/07/2026) — rodado em **produção**, tudo passou: link
  privilegiado → R$77,70 (de R$155,40) · "trocar de conta" · cadastro inline · auto-login · modal do CPF ·
  **checkout Asaas em R$77,70** com PIX/boleto/crédito/débito. Gate de preço server-side confirmado por
  hash (`ASAAS_BASE_URL` = produção). **Não validado:** cronômetro QR→PIX ≤2min (precisa de celular real).
  ⚠️ **Limpar rastros:** fatura Asaas **855418887** · empresa "TESTE Claude — Apagar" · usuário
  `redebaixada+testeclaude1107@gmail.com`.
- [x] **Preço da oferta de parceiro decidido** (09/07/2026) — **manter R$77,70/6m**. A
  diferença pro site (R$147/ano) é intencional: na rua o cliente ganha o agente que monta
  tudo + a chance de experimentar 6 meses. Produto com serviço embutido, não desconto.
  (Script de objeção gravado na skill `/venda-porta-a-porta`.)
- [x] **Fluxo `/oferta-parceiro` 100% no ar e verificado** (deploy 07/07, verificado 09/07) —
  front (PR #1 na `main`, HTTP 200) **+ backend Supabase** (o 403 acabou): functions
  `asaas-create-payment` (v19) e `asaas-webhook` (v14) ACTIVE; secrets `OFFER_PARCEIRO_KEY`
  (=`b036e66...`) e `OFFER_PARCEIRO_VALUE` (=`77.70`) conferidos por hash; Asaas em
  **produção** (`www.asaas.com/api/v3`). Gate do preço é server-side; ativa presença 6 meses.
- [x] **Webhook `asaas-webhook` seguro** — exige `ASAAS_WEBHOOK_SECRET` (via `?token=` ou header
  `asaas-access-token`) → 401 sem ele. Idempotente; ativa 6m na oferta parceiro, revoga em
  estorno/chargeback. (Resolve o item "validar assinatura" do sprint.)
- [x] **Folha de vendas v2 corrigida** (07/07/2026) — HTML+PDF em `marketing/`, texto certo
  (6 meses, menos de R$13/mês, sem vitrine/vagas). Só falta a impressão física.
- [x] **Logo colorido em `identidade/logo.png`** (09/07/2026) — copiado do portal; caminho
  atualizado no `design-guide.md`.
- [x] **MCPs Canva, Gmail, Google Calendar, Google Drive conectados** (jul/2026).
- [x] **Pagamento em produção** (jun/2026) — checkout Asaas integrado e testado com cartão
  real. Ciclo completo: paga → empresa ativa (plano/aprovada/+1 ano); estorna/chargeback →
  revoga (free/pendente). Webhook seguro (token na URL) e idempotente.
- [x] **Funil de conversão** (jun/2026) — criar empresa leva direto ao `/planos`; banner
  "escolher plano" na lista, no dashboard e pós-criação. Checkout coleta CPF/CNPJ.

## Backup do banco — Supabase Pro (decidido: assim que as primeiras vendas entrarem)
O Supabase está no **Free Plan, que NÃO tem backup nenhum**. **Pro (~US$25/mês) = 7 dias de backup
diário.** Decisão do Lucio (12/07): comprar quando a receita da rua começar a entrar.

⚠️ **Mitigado em parte (12/07):** existe agora a tabela `companies_history` — toda alteração/exclusão
de empresa guarda a versão anterior, e `company_restore_content(<snapshot>)` desfaz. Isso cobre o
risco REAL (alguém escrever por cima de dado bom), que é diferente do que o backup cobre (o banco
morrer). Os dois se complementam — o Pro nunca vai devolver UM campo.

## Reescrever o "Sobre" da empresa Jota Vimax
Descrição perdida em 12/07 (erro em teste de RLS contra linha real). Irrecuperável.

## BREVO_API_KEY
A repescagem do trial está no ar em **no-op** (roda, conta o que mandaria, não envia). Ligar a chave
liga os e-mails do ciclo (dia 0 / 5 / 7 / 14).

## Contas de vendedor pro Barça e pra Gi
Sem conta no portal, não existe link de vendedor (`?v=`) — e a venda deles nasceria órfã.

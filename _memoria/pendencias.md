# Pendências

> O que ficou em aberto e precisa de ação. Atualizar conforme for resolvendo.

## Abertas

- [ ] **Logo** — baixar do site redebaixada.com.br e salvar em `identidade/logo.png` (+ versão branca pra fundo escuro). Depois atualizar os caminhos em `identidade/design-guide.md`.
- [ ] **Conectar MCPs** — Meta Ads, Google Ads, Google Calendar, Canva (checkboxes no `CLAUDE.md`). Marcar conforme instalar.
- [ ] **Substituir Uber pela Rede Baixada** — mapear o processo de venda como rotina via `/mapear-rotinas` (referência: R$338,50 em 4h na Rede Baixada vs ~R$150 em 5h no Uber).
- [ ] **Conta Asaas separada (futuro)** — hoje a Rede Baixada compartilha a conta Asaas com o UniMasso (funciona e é seguro: os webhooks se ignoram). Isolar em conta própria é mais limpo a longo prazo.
- [ ] **Subir o link privilegiado `/oferta-parceiro`** (PR #1 no repo redebaixada) — **deploy com o Nick**: 2 edge functions (asaas-create-payment, asaas-webhook) + secrets `OFFER_PARCEIRO_KEY`/`OFFER_PARCEIRO_VALUE` no Supabase, depois merge na main. A CLI da máquina do Lucio deu 403 (sem privilégio). Passo a passo em `saidas/deploy-oferta-parceiro.md`.
- [ ] **Reimprimir a folha de vendas** — corrigir "1 ano" → "6 meses", tirar vitrine/vagas (não são da presença) e "R$1,50/dia" → "menos de R$13/mês". Conteúdo já corrigido em `.claude/skills/venda-porta-a-porta/folha-vendas.md`.
- [ ] **Decidir coerência de preço** — R$77,70 × 2 = R$155,40/ano vs presença R$147/ano (fundador) no site: no anual, a oferta de parceiro fica um pouco ACIMA do site. Manter, baixar o semestral, ou ajustar o site?

## Resolvidas

- [x] **Pagamento em produção** (jun/2026) — checkout Asaas integrado e testado com cartão real. Ciclo completo: paga → empresa ativa (plano/aprovada/+1 ano); estorna/chargeback → revoga (free/pendente). Webhook seguro (token na URL) e idempotente.
- [x] **Funil de conversão** (jun/2026) — criar empresa leva direto ao `/planos`; banner "escolher plano" na lista, no dashboard e pós-criação. Checkout coleta CPF/CNPJ.

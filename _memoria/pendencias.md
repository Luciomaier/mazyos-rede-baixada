# Pendências

> O que ficou em aberto e precisa de ação. Atualizar conforme for resolvendo.

## Abertas

- [ ] **Logo** — baixar do site redebaixada.com.br e salvar em `identidade/logo.png` (+ versão branca pra fundo escuro). Depois atualizar os caminhos em `identidade/design-guide.md`.
- [ ] **Conectar MCPs** — Meta Ads, Google Ads, Google Calendar, Canva (checkboxes no `CLAUDE.md`). Marcar conforme instalar.
- [ ] **Substituir Uber pela Rede Baixada** — mapear o processo de venda como rotina via `/mapear-rotinas` (referência: R$338,50 em 4h na Rede Baixada vs ~R$150 em 5h no Uber).
- [ ] **Conta Asaas separada (futuro)** — hoje a Rede Baixada compartilha a conta Asaas com o UniMasso (funciona e é seguro: os webhooks se ignoram). Isolar em conta própria é mais limpo a longo prazo.

## Resolvidas

- [x] **Pagamento em produção** (jun/2026) — checkout Asaas integrado e testado com cartão real. Ciclo completo: paga → empresa ativa (plano/aprovada/+1 ano); estorna/chargeback → revoga (free/pendente). Webhook seguro (token na URL) e idempotente.
- [x] **Funil de conversão** (jun/2026) — criar empresa leva direto ao `/planos`; banner "escolher plano" na lista, no dashboard e pós-criação. Checkout coleta CPF/CNPJ.

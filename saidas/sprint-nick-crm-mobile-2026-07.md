# Sprint do Nick — CRM mobile do agente + Criar Empresa + webhook (jul/2026)

> Deixar o portal do Rede Baixada pronto pra prospecção PaP com equipe. Prioridades tiradas do
> **teste ao vivo (09/07)** na visão do agente (conta de teste Elis, `/dashboard/minha-area/leads`).
> ⚠️ **Performance NÃO é o gargalo** (~180ms em cache/wifi) — a fricção é de **fluxo/UX**.

## 1. Visão do agente mobile-first (a captura na rua) — prioridade máxima
- **Cards no lugar da tabela.** Hoje "Meus Leads" é uma **tabela de 6 colunas** (rola horizontal no celular). **Reusar o componente de card do kanban do admin** (já existe) na visão do agente — não construir do zero.
- **Botão flutuante "＋ Novo Lead"** + **"adicionar à tela inicial" (PWA)** → captura em **1 toque** (hoje são 4: toggle → Minha Área → Leads → Novo Lead).
- **+4 campos no formulário** de lead: **ramo, bairro, oferta (77,70 / 250), próxima ação** (podem começar em `notes` e virar coluna).
- **Unir Telefone + WhatsApp** num campo só. **Origem: default "Visita"** (hoje vem "Outro" → 1 toque perdido por lead).
- **Consertar deep-link** (abrir `/dashboard/...` cru joga pro `/dashboard`) e **persistência de sessão** (numa das vezes caiu pro `/login` sozinho) — pra salvar atalho e não deslogar na rua.

## 2. Camada "Criar Empresa" na mão do agente (self-serve)
- Expor o **"Criar Empresa"** (hoje só no admin) na visão do agente, no card do lead **Convertido**.
- Publica como **trial** + dispara alerta **"pending moderate"** pro admin (1 clique, não bloqueia).
- Detalhe da regra: [`regra-negocio-parceiro-2026-07.md`](regra-negocio-parceiro-2026-07.md).

## 3. Ciclo da empresa (estados) — implementar
`demo → publicado-trial (7d) → publicado-pago (6m) → cinza/inclicável → oculto → expirado`
- Timer de 7 dias (pagamento × moderação desacoplados). **Oculto não apaga** → reativa em 1 clique.
- **Gravar o vencimento** de cada assinatura desde o 1º parceiro (pro facão dos 6 meses depois).

## 4. Asaas / cobrança
- **Corrigir o webhook `asaas-webhook` pra validar assinatura** (falha de segurança). O Asaas está **em produção** (conta única do grupo — Rede Publicidade).
- Marcar cada cobrança com **referência externa por unidade** (separar receita RB × UniMasso na conta única).

## Modelo de trabalho
Sprint fechado — o Nick executa; o Lucio roda o PaP em paralelo. **Primeiro corte:** item **1 (mobile)** destrava a rua; 2–4 vêm em seguida.

---
Ligações: organograma → [`../../rede-publicidade/saidas/organograma-comercial-2026-07.md`](../../rede-publicidade/saidas/organograma-comercial-2026-07.md) · regra → [`regra-negocio-parceiro-2026-07.md`](regra-negocio-parceiro-2026-07.md)

# Onde paramos — 13/07/2026, madrugada · **A RUA ESTÁ LIBERADA**

> Continua de `onde-paramos-2026-07-12-tarde.md`. Este cobre da comissão até a virada do dia.

---

## 🟢 O QUE FICOU PRONTO E PROVADO COM DINHEIRO REAL

**O ciclo do dinheiro fecha nos dois sentidos**, testado com eventos reais do Asaas:

| caminho | resultado |
|---|---|
| PIX pago → perfil ativo 6 meses (184d) + comissão R$50 pra quem vendeu | ✅ |
| Estorno → empresa despublicada, fatura, cliente, lead e comissão — **tudo sozinho** | ✅ |
| Estorno de comissão **já paga** → contra-lançamento de −R$50 que abate do próximo acerto | ✅ |

**Custo real dos testes: R$ 2,98** (a taxa do PIX). O resto voltou.

---

## 💰 A COMISSÃO ESTÁ VIVA (decidida E no ar)

```
venda ......... R$ 50   →  sobra R$ 24,72 pra casa
recorrência ... R$ 15   →  sobra R$ 59,72  ← É AQUI QUE A CASA LUCRA
indicação ..... R$ 15   (uma vez, na 1ª venda)
```
Regras moram em **tabela** (`crm_commission_rules`): calibrar é um `UPDATE`, **sem deploy**.

**Escada até o Plano Diretor:** crédito de ativação a R$20 → o credenciado fica com R$57,70 (mais que
o comissionado — senão a escada não sobe) e a casa recebe **caixa ANTES da venda**.

**Trigger na FATURA, não no webhook** — a comissão nasce do DINHEIRO, então todo caminho paga de graça.
Com backfill (a venda que a Elis fez antes do gatilho existir foi recuperada — sem isso, ela veria R$ 0
pra sempre sobre uma venda real).

### O ciclo de pagamento (decidido)
**Vende na semana → FECHA na sexta → RECEBE na sexta seguinte.** O lag de uma semana joga quase toda
comissão pra **fora dos 7 dias de arrependimento do CDC** (vende segunda, recebe 11 dias depois).
**Com adiantamento sob demanda** ("pega antes se precisar") — que é a **ponte do vendedor novo**: sem
ela, o Barça levaria 12 dias pra ver o primeiro dinheiro, e é aí que se desiste.

⚠️ **O adiantamento é o furo da própria trava** (puxar no dia 2 volta pra dentro da janela). Por isso o
contra-lançamento é obrigatório, não opcional: ele é **a rede que sustenta o adiantamento**.

### Os prazos de reembolso (pesquisados, não chutados)
```
LEI (CDC art. 49) ..... 7 dias de arrependimento, SEM justificativa.
                        Porta a porta é o caso original do artigo. Não é negociável.
Asaas (PIX) ........... você pode estornar até 90 dias. A TAXA NÃO VOLTA.
CARTÃO (chargeback) ... o cliente contesta em até 120 dias (540 se parcelado!).
                        Debita da conta sem pedir licença.
```
🔴 **RECOMENDAÇÃO NÃO DECIDIDA: travar a oferta da rua em PIX.** Hoje o `billingType` é `UNDEFINED` —
o cliente pode escolher cartão, e aí a cauda de risco vai de **7 para 120 dias**. Nenhum lag semanal
cobre isso.

---

## 🔴 A ATRIBUIÇÃO QUEBROU NA RUA (e o conserto)

**Caso real:** a **"Neri salgados"** — primeira venda de campo do Barça — nasceu **ÓRFÃ**: `sold_by`
nulo, fora da carteira dele, sem comissão. **Não foi erro do vendedor.**

**A causa:** o `?v=` (o crachá) morava em `sessionStorage`, que **morre com a aba e não existe em outro
aparelho**. E o que aconteceu na rua foi exatamente isso: **o FILHO da dona fez o cadastro no celular
DELE**. O crachá nunca pisou naquele aparelho.

**Isso não é caso de borda — é O fluxo da rua.** O cliente sempre vai querer usar o próprio celular.
E o sistema **falhava em silêncio** (o código já desiste da atribuição de propósito quando a FK falha:
*"perder o cliente é pior que perder a comissão"*).

**Consertos (nas duas camadas):**
1. **BANCO** — trigger `stamp_seller_from_session`: quando quem cria o perfil é o **próprio vendedor
   logado**, o `sold_by` vem da **SESSÃO**. Não há URL, aba nem aparelho que possa perdê-lo.
   *(Dono de negócio que se cadastra sozinho pelo site NÃO vira vendedor de si mesmo — venda orgânica
   é órfã mesmo, e está certo.)*
2. **FRONT** — o `?v=` passou pro `localStorage` (sobrevive a fechar a aba e voltar amanhã, **no mesmo
   aparelho**). Não resolve outro aparelho — só o item 1 resolve.

**A Neri foi carimbada no Barça em produção.** Está na carteira dele, lead em `negociando`, trial de 7
dias correndo. **Se a dona pagar, os R$ 50 caem pra ele sozinhos.** Ele fala com ela hoje (13/07).

### ⚡ A REGRA DE CAMPO (vale hoje, sem depender de código)
> **O vendedor abre O LINK DELE no celular DELE. O cliente digita ali.**
>
> Se o cliente insistir no próprio celular: ele tem que **abrir o link do vendedor** (WhatsApp), nunca
> digitar o site. O crachá viaja dentro do link.

---

## 📱 O CELULAR DO VENDEDOR (o painel explodia)

**O `<main>` estava com 702px numa tela de 341px — o dobro.** Item flex nasce com `min-width: auto`:
**se recusa a encolher abaixo do próprio conteúdo**. Bastava uma tela ter algo largo (a TabsList de 8
abas do "Editar Empresa") pra o main esticar e **arrastar o header e a página inteira** pra fora.

Era por isso que **"Nova Empresa" abria bem e "Editar" não** — a diferença nunca foi a página, foi só o
conteúdo dela ser largo o bastante pra disparar o bug.

**Conserto:** `min-w-0` no layout do painel. Vale pra **todas** as telas, inclusive as que ainda não
quebraram. Medido antes do deploy: **702px → 341px**, página parou de rolar de lado.

Junto: **a carteira virou card no celular** (tabela de 6 colunas ali era ilegível), com "Editar perfil"
ocupando a linha inteira — é o botão que o vendedor mais aperta.

---

## 🐴 O CAVALO DE TROIA (palavras do Lucio)

**O portal é o cavalo. Quem paga a conta é a Rede Publicidade** (R$250/mês = **19× um cliente de
portal**). Mas cavalo só serve se alguém abrir a porta por dentro — e **o vendedor é a única pessoa que
vai pisar dentro daquela loja**.

✅ **Construído:** o botão **"Candidato a Publi"** (megafone) na carteira do vendedor — ele marca *ainda
dentro da loja*, com a observação da visita. Tabela própria e fechada (não em `companies`, que é de
leitura **pública** — uma nota tipo *"dono tem grana mas é desorganizado"* vazaria pro mundo).

**O VALOR da comissão da Publi ficou parqueado** (a Publi não tem forma ainda). **O CAMPO nasce agora**,
porque colher é barato e recuperar é impossível.

---

## ✅ Outros consertos do dia
- **Kanban de 5 colunas** + `FALLBACK_COLUMN` (status sem coluna cai no `novo` em vez de sumir).
- **A Elis estava invisível** na lista de Agentes Comerciais — a lista era montada a partir dos
  **territórios**, e quem não tinha bairro não aparecia. (TERRITÓRIO ≠ CARTEIRA, de novo.)
- **O Lucio não tinha "Meu Link" no menu** — o gate era `isModerator && !isAdmin`: alguém assumiu que
  admin não vende. Ele é o principal vendedor da rua.
- **O painel da Elis mostrava "—" no lugar do cliente** — o nome vinha do LEAD (campo opcional), e o
  webhook nunca preenchia `lead_id`. Agora vem da EMPRESA (que todo cliente pagante tem), e um trigger
  liga cliente↔lead em qualquer caminho.

---

## 🔴 DECISÕES TRAVADAS (é o que bloqueia trabalho)

**1. Quando o VENDEDOR cria um perfil pelo painel, ele nasce no ar em trial de 7 dias — ou nasce parado
esperando você publicar?**
Hoje nasce **`pending` + `active` + `free`** = invisível, sem relógio, sem selo. Isso **bloqueia o
"perfil pré-montado"** (a jogada mais forte e nunca usada: chegar na visita com o perfil pronto na tela).
⚠️ **E colide com os ~60 do WordPress:** se toda empresa criada por admin entrar em trial sozinha, a
importação vira massacre — todos ficam cinza e o portal desaba.

**2. Trava a oferta da rua em PIX?** (cauda de risco de 120 dias → 7 dias)

**3. A RECUPERAÇÃO** — o que acontece com o perfil do ex-cliente quando o trial de 7 dias acaba e ele
não paga? **Segue travada desde 12/07. Não trava a rua.** *(Os 34 perfis SÃO o ativo — recomendação:
fica no ar, mas perde o selo e o botão de WhatsApp.)*

---

## 🟡 A CONSTRUIR (mapeado, não feito)

**Pagamento (falta pra pagar de verdade):**
- **A tela do acerto** — "quem recebe nesta sexta": vendedor, quantas vendas, total já líquido de
  estorno, chave PIX. Sem ela, essa conta é na mão toda semana.
- **O painel do vendedor com 3 números** — *"fechando agora: R$X"*, *"cai na sexta dia N: R$Y"*, e o
  botão **"preciso antes"**. É o que faz a espera de uma semana parecer salário, e não dívida.
  *(A view `crm_agent_balance` já separa "liberado" de "fechando agora".)*

**Mobile / formulários:**
- **Botão fixo na oferta** — o 1º campo está a **1.159px do topo** (3 telas de rolagem na calçada).
  Melhor retorno por minuto da lista.
- **Quiz (uma pergunta por tela)** — NÃO precisa de Typebot (ele roda em iframe externo, e a sessão do
  usuário, o crachá `?v=` e o publish-first **não atravessam iframe**). É uma máquina de passos no
  mesmo estado do formulário. **Mas o quiz sozinho não conserta:** o formulário do painel tem **26
  campos** — vira 26 telas. O ganho de verdade é **CORTAR** (na rua bastam 4: nome, categoria, cidade,
  WhatsApp).
- **NÃO trocar de framework.** React+Tailwind faz tudo isso. Trocar = meses e risco de perder o que subiu.

**As 3 alavancas (escolhidas, NENHUMA construída):** order bump +R$47 · plano anual R$137 ·
**Rede Publicidade R$250/mês**. O portal sozinho **não paga uma equipe** — 386 clientes é uma máquina de
vender pra ficar no zero.

---

## 🧹 LIXO DE TESTE NO BANCO (limpar)
- **"Teste 35 elis"** — empresa + cliente + fatura + comissão. ⚠️ **A comissão da Elis está marcada como
  "paga" e com um estorno de −R$50 — EU simulei isso pra testar o contra-lançamento. Ela nunca recebeu
  PIX nenhum.** Apagar a empresa leva tudo em cascata e zera o painel dela.
- **"Teste"** (do Barça) e **"teste usuário cliente"** (do teste12).
- **Leads fantasma** dos testes (apagar empresa **não apaga** o lead: `company_id` vira NULL).
- Contas de teste: `teste12@`, `teste13@`, `redebaixada-teste888/889@`, `redebaixadatedte654@`.
- **NÃO APAGAR a "Neri salgados"** — é prospecto real, trial correndo, Barça fala com ela hoje.

---

## 📌 Pendências do Lucio (não são código)
- **A Gi ainda não se cadastrou** (o Barça já: `matheusamaral23102008@gmail.com`, Agente Comercial).
  Caminho: `/cadastro` (Google é mais rápido) → você promove em **Admin → Usuários → Agente Comercial**.
  *(O rótulo na tela é "Agente Comercial"; no banco o papel se chama `moderator`. Mesmo bicho.)*
- Cancelar faturas antigas do Asaas (`855418887` + `op4crxlwhc1jn5pe`)
- Reescrever o **"Sobre" da Jota Vimax**
- Export do **WordPress** (~60 clientes)
- **Supabase Pro** (backup) — quando a rua pagar
- ⏱️ **O cronômetro QR→PIX nunca foi medido.** "Foi rápido" não é medida. **Cravar na primeira visita.**

## 🐛 Dívidas técnicas
- **`types.ts` do Supabase desatualizado** (não conhece `lifecycle_state`) → 2 erros de tipo em
  `Companies.tsx`. Regerar os tipos.
- **O diálogo de excluir empresa NÃO diz QUAL empresa.** Foi assim que a Jota Vimax morreu.

---

## 🧠 Não redescobrir (custou caro)
- **`min-width: auto` em item flex** é o que explode layout no celular. `min-w-0` resolve.
- **`sessionStorage` morre com a aba e não existe em outro aparelho** — não serve pra atribuição.
- **View no Postgres ATRAVESSA a RLS** por padrão. `security_invoker = true` é obrigatório, senão um
  vendedor vê o saldo de todos.
- **O gatilho só olha pra frente** — toda migration que cria regra precisa de **BACKFILL**, senão o que
  já existia nasce invisível.
- **NÃO se apaga um pagamento feito. Lança-se o contrário** (contra-lançamento).
- **No PIX o Asaas manda só `PAYMENT_RECEIVED`** (não `CONFIRMED`).
- **Dá pra provar o webhook SEM dinheiro:** POST na URL real com evento que o código ignora
  (`PAYMENT_CREATED`) → 200; token errado → 401.
- **Preview da Vercel (`*.vercel.app`) fica CONGELADO num commit antigo.** Testar sempre em
  `redebaixada.com.br`, senão você conserta numa e testa na outra.
- **Conferir deploy pelos BYTES:** `curl` o bundle da produção e compare o md5 com o `dist/` local.

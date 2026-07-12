# Onde paramos — 12/07/2026, tarde · **O GATE DO PaP CAIU**

> Sessão da tarde. O handoff da madrugada é `onde-paramos-2026-07-12.md` — este continua de lá.

---

## 🟢 O ÚNICO GATE DO PaP CAIU: o PIX real rodou, nos dois sentidos

**O medo era legítimo:** todos os testes do webhook tinham sido POST direto (pagamento fake). Provavam
que o webhook **funciona** — não que o **Asaas o chama**. Esse elo nunca tinha rodado, e é o elo que,
se falhasse, falharia **na frente do cliente**.

**Rodou.** Com dinheiro de verdade.

| | |
|---|---|
| **PIX pago** | 11:49 · R$ 77,70 · `pay_zqakxn0y5f06o22o` |
| **Asaas disparou** | 11:50 · evento `PAYMENT_RECEIVED` (no PIX ele **não** manda `CONFIRMED`) |
| **externalReference** | `a3493cbe…\|presenca\|parceiro\|rede_baixada` — 60 chars, **v3, intacto** |
| **Ativou** | 184 dias (6 meses — a oferta parceiro foi honrada, não caiu nos 12) |
| **CRM** | Clientes ativos 0→1 · MRR R$0→**R$ 12,95** (=77,70/6) · lead → Convertido |
| **Carteira** | a venda nasceu **no nome do vendedor** (`sold_by`) |
| **Estorno** | `PAYMENT_REFUNDED` → empresa **despublicada + Expirada**, MRR→0, lead→Perdido. **Sozinho.** |
| **Custo real** | **R$ 2,98** (taxa do PIX). Os R$77,70 voltaram. |

### O que evitou o teste falhar na calçada
Antes de gastar um centavo, li a config do webhook no painel do Asaas e **provei o elo de graça**:
- A URL registrada **tem o `?token=`** que o código exige (se não tivesse → 401 → cliente paga e não ativa).
- POST na URL real com evento inofensivo (`PAYMENT_CREATED`, que o código ignora) → **200**.
- Controle: token errado → **401**. Sem token → **401**. Logo o 200 é aceitação real, não endpoint frouxo.

**Lição:** dá pra provar quase tudo do webhook **sem dinheiro**. O dinheiro só prova a última milha
(o Asaas disparar). Fazer os dois é o certo — mas o barato vem primeiro.

### ⏱️ O cronômetro QR→PIX
**Não foi medido** (o Lucio não cravou). Relato: "foi bem rápido". **Medir na primeira visita real.**

---

## 💰 A COMISSÃO: decidida hoje, com dois especialistas na mesa

`crm_commissions` existia desde fevereiro — tipo (`venda|recorrencia|indicacao`), status
(`pendente|pago|cancelado`), duas telas **lendo** dela. **Ninguém escrevia.** A Elis venderia, o dinheiro
entraria, e o painel dela mostraria **R$ 0**. Não é um bug que quebra — é um que **mente em silêncio**
pra quem está na rua confiando no sistema.

### A escada (decidida)

| nível | como ganha | por venda | a casa recebe |
|---|---|---|---|
| **A — Comissionado** (entrada, risco zero) | comissão | **R$ 50** | R$ 24,72 *depois* |
| **B — Carteira** (quem fica) | + renovação | **+R$ 15** | **R$ 59,72 — é aqui que a casa lucra** |
| **C — Plano Diretor** (autonomia) | **compra crédito a R$ 20**, vende a R$77,70 | **R$ 57,70** | **R$ 20 ANTES** |

**Indicação: R$ 15.** Paga uma vez, na primeira venda (renovação não repaga).

O credenciado **tem** que ganhar mais que o comissionado (R$57,70 > R$50) — senão a escada não sobe.
Ele paga por isso com capital e risco. E a casa recebe **caixa antes da venda** — que é exatamente o
que falta (o Lucio não tem reserva).

### As leis que os dois especialistas cravaram, independentes
1. **Valor fixo, nunca percentual.** O vendedor soma o dia **de cabeça, na calçada**. "R$50 por porta
   fechada" existe; "64% do bruto" não existe.
2. **PIX na mesma noite.** Maior alavanca de comportamento — **maior que o valor**. "Fecho o mês e pago
   dia 10" mata o time.
3. **A primeira venda é CAC, não receita.** A casa lucra na **renovação** (custo zero: a máquina já cobra
   sozinha) e no **upsell**.
4. **A renovação TEM que pagar** — não pra ele "cuidar do cliente", mas pra **segurar o vendedor no mês 6**,
   exatamente quando ele ia sumir. É o que transforma bico em carteira.
5. **Estorno cancela comissão — e isso se fala no primeiro dia**, não quando acontece.
6. **Família paga igual a externo.** Pagar menos "porque é de casa" fabrica ressentimento. E **o PIX tem
   que sair de fato**, mesmo que reinvista depois. Trabalho invisível apodrece.
7. **A Elis não deve entrar na comissão de venda individual** — ela é gestora; se ganha por venda, compete
   com o time que deveria estar ajudando. Pagar pelo que ela controla (conversão de trial / % da carteira).

### ⚠️ O benchmark do Uber estava ERRADO (correção do Lucio, e ele tem razão)
Os especialistas ancoraram em **R$30/h de Uber** — mas isso é **bruto**. Tirando combustível, desgaste/
aluguel e as 10-12h sentado, o líquido real é **R$ 12-18/h**. O piso local de verdade:

```
Servente de pedreiro ..... R$ 100/dia, sol a sol, trabalho pesado   (~R$ 11/h)
Uber (líquido real) ...... R$ 150-200/dia, 10-12h no carro          (~R$ 15/h)
Rede Baixada @ R$ 50 ..... 2 vendas = R$ 100 · 3 vendas = R$ 150, em algumas horas
```
**Duas vendas empatam com o dia inteiro do servente.** E dá pra fazer como **renda extra** sem largar a
atividade principal — coisa que nem o Uber nem a obra permitem. Os R$50 não são "10% acima do Uber":
são **uma porta de saída**. É isso que o Lucio quer construir, e o número certo sustenta a decisão.

### A conta dos 10/dia (o enquadramento do Lucio: a equipe é investimento)
O vendedor **vende E coloca a empresa no ar** (cadastro, fotos, onboarding). A casa **só modera** — e o
sistema modera sozinho. Os R$50 não pagam a venda: pagam a **operação inteira**.
```
10 vendas/dia × 22 dias = 220 clientes/mês
  bruto R$ 17.094  –  Asaas R$ 655  –  comissão R$ 11.000  =  CASA R$ 5.439/mês
  + 220 perfis novos no catálogo (o ativo)  + a anuidade das renovações (R$59,72 líquidos cada)
```
**A casa nunca fica negativa:** a comissão sai do dinheiro que o cliente **acabou de pagar**. Risco de
caixa zero — é isso que torna possível ser generoso sem quebrar.

### 🔴 As 3 alavancas (escolhidas: TODAS) — sem elas a conta não fecha
O portal sozinho **não paga uma equipe**. A meta de 386 clientes é uma máquina de vender pra ficar no zero.
1. **Order bump no PIX (+R$47)** — "selo destaque + 5 fotos tiradas agora". Custo marginal ZERO. A 35% de
   adesão → ticket médio R$94.
2. **Plano anual R$137** (contra R$155,40 em 2× semestral) — **caixa hoje**, mata o risco de renovação.
3. **Rede Publicidade (R$250/mês)** — **1 Publi = 19 clientes de portal.** Vira "150 portal + 15 Publi =
   R$4.940/mês" em vez de caçar 386. Mesma meta, **30× menos porta**. *O portal talvez não seja o produto:
   seja o abre-porta.*

**Nenhuma das três está construída.** É o próximo sprint.

---

## ✅ Entregue e no ar

**Kanban de 5 colunas** (`edea9cd`) — `Novo · Negociando · Convertido · Requalificação · Perdido`.
- Cortadas: `qualificacao` e `contato_feito`. **Nunca receberam um lead** — a máquina só escreve
  negociando/convertido/requalificacao/perdido, e a visita da rua **nasce em negociando**. Cerimônia.
- **`novo` FICOU** — e não por estética: é o **default do banco E do formulário de lead manual**. É o ralo
  onde cai todo lead que não veio de visita. Sem a coluna, ele **nasceria invisível**.
- **`FALLBACK_COLUMN`**: status sem coluna cai no `novo` em vez de sumir. É o que torna seguro mexer nessa
  lista — e protege quem mexer depois.
- Os valores continuam no enum: quando a **Recuperação** começar, "Contato Feito" é a coluna da ligação e
  volta com uma linha.
- Bug do grid morreu junto (eram 7 colunas num `grid-cols-6`; a 7ª quebrava a linha).

**Migration da comissão escrita** — `20260712160000_comissao_do_vendedor.sql`. **NÃO SUBIU** (ver abaixo).
- **Trigger na FATURA, não no webhook** — mesma filosofia do `lead_segue_o_ciclo`: assim **todo caminho**
  paga comissão de graça (webhook hoje, admin amanhã, ERP depois). A comissão nasce do **dinheiro**.
- **Nenhuma mudança no webhook foi necessária** (a fatura já grava `sold_by`/`indicated_by`/`confirmed`).
- Regras em **tabela** (`crm_commission_rules`): o Lucio calibra com um `UPDATE`, **sem deploy**.
- Trava contra pagar 2× (índice único) — o Asaas **reenvia evento**.
- **Estorno → comissão `cancelado`** automático.
- RLS conferida: existe "Agents can view own commissions" — o vendedor **lê a própria comissão**.

**Limpeza:** as 2 empresas de teste foram apagadas (portal de volta a **37**).

---

## 🔒 Adiado DE PROPÓSITO (não é esquecimento)

**Comissão de venda vinda de TRÁFEGO PAGO.** A casa paga o clique **e** pagaria R$50 em cima — pagar duas
vezes pela mesma aquisição. Rua e tráfego pago **não podem valer o mesmo**.
**Decisão do Lucio: definir quando for a hora.** Nesse estágio a qualificação será por **IA**, o anúncio
vira **quiz** (menos ruído, mais conversão), o suporte resolve "com um empurrãozinho" — e a remuneração
é **outra coisa** (perfil tipo Giovanna, não vendedor de rua).

✅ **O código já é seguro por padrão:** a comissão só nasce com `sold_by`, que só é carimbado pelo `?v=`
do link do vendedor. **Lead de tráfego pago não tem vendedor → não gera comissão.** O buraco existe no
futuro, não hoje.

---

## 🔴 Bloqueado — precisa das mãos do Lucio

1. **`supabase login` + `link`** — o CLI não está autenticado nesta máquina (o token de ontem se foi).
   Sem isso a **comissão não sobe**:
   ```bash
   cd portal && supabase login && supabase link --project-ref donaobtlwqrjmvjqflxz
   ```
2. **Login no portal** — a sessão expirou no meio (refresh_token deu 400). Faltam apagar **2 leads
   fantasma** dos testes (apagar a empresa **não apaga** o lead: `company_id` vira NULL e o card fica
   no funil).

---

## 📌 Pendências que continuam

- Cancelar faturas do Asaas (`855418887` + `op4crxlwhc1jn5pe`)
- Reescrever o **"Sobre" da Jota Vimax**
- Export do **WordPress** (~60 clientes)
- Contas de vendedor pro **Barça e a Gi** (sem conta → sem link → venda órfã)
- **A decisão da Recuperação** (o que acontece com o perfil do ex-cliente que não paga) — **segue travada,
  e não trava a rua**
- Supabase Pro (backup) — quando a rua pagar

## 🐛 Dívidas novas encontradas hoje

- **`types.ts` do Supabase desatualizado**: não conhece `lifecycle_state` → 2 erros de tipo em
  `Companies.tsx`. Não quebra o build, mas vai morder. (Regerar os tipos.)
- **O diálogo de excluir empresa NÃO diz QUAL empresa** está apagando ("Esta ação é irreversível" e só).
  **Foi assim que a Jota Vimax morreu.** Pôr o nome no diálogo.

## 🧠 Não redescobrir

- **No PIX o Asaas manda só `PAYMENT_RECEIVED`** (não `PAYMENT_CONFIRMED`). O código trata os dois.
- **A config do webhook do Asaas é legível pelo painel** (shadow DOM: `data-webhook-log-data` nas linhas
  de log tem o payload inteiro). Dá pra auditar entrega e evento **sem API key**.
- **Apagar empresa NÃO apaga o lead** (`company_id` → NULL, card fica órfão no funil).
- **Taxa do Asaas medida:** R$ 2,98 num PIX de R$ 77,70 (~3,8%). Líquido: **R$ 74,72**.

# Bloco 3 — Ciclo do trial ✅ ENTREGUE (12/07/2026, verificado em produção)

> `main = 5f7a694` · migration `20260712140000_bloco3_ciclo_de_vida.sql` ·
> `asaas-webhook` **v17** · `generate-sitemap` **v19** · `lifecycle-dunning` **v1**

O caminho do "vou pensar" agora existe no sistema. Antes, a empresa nascia **invisível**
(`status=pending`, default do banco), sem relógio, sem cinza, sem expiração e sem repescagem —
quem não pagava na hora sumia do processo e virava linha de planilha.

```
(nasce na visita) → trial 7d → pago 6m → 🩶 cinza → oculto → expirado
                             ↖______ pagar reativa de QUALQUER estado ______↙
```

---

## A decisão de desenho que sustenta tudo: dois relógios

A regra de negócio (09/07) dizia, com todas as letras: *"7 dias, dois relógios **independentes**"*.
O código agora diz a mesma coisa:

| campo | relógio | quem manda |
|---|---|---|
| `companies.status` (pending/approved/rejected) | **moderação** — o negócio é real? | admin (fila "Pendentes", intocada) |
| `companies.lifecycle_state` + `state_expires_at` | **comercial** — pagou? | pagamento + pg_cron |

**Visibilidade = `status='approved'` E `lifecycle_state IN (trial, active, grace)`.**

O atalho tentador era enfiar `trial`/`oculto` dentro do `company_status`. Seria um erro caro:
quebraria a fila de moderação do admin, obrigaria a reescrever toda query que filtra `approved`,
e deixaria *"pagou mas o admin ainda não clicou"* sem representação — sendo que a regra diz que um
**não derruba** o outro. Dois campos ortogonais dizem a verdade; um campo só mente.

## O motor é genérico de propósito

`lifecycle_policies` · `lifecycle_events` · `lifecycle_reminders` — todos com `subject_type`.
As durações são **dado, não código**:

```sql
-- muda a régua do cinza de 7 pra 3 dias. Sem deploy, sem esperar por mim.
update lifecycle_policies set duration = interval '3 days'
 where subject_type = 'company' and from_state = 'grace';
```

Quando o **modelo ABC** destravar, o ciclo do agente (6 meses renovados por **atividade** em vez de
**pagamento**) é o mesmo relógio com outro gatilho: 1 linha de policy + 1 função de tick.

## O que roda sozinho

| job | quando | o que faz |
|---|---|---|
| `lifecycle-tick-companies` | 00:05 BRT | vira os estados. **SQL puro, sem rede** |
| `lifecycle-dunning` | 09:00 BRT | manda o e-mail da repescagem (Brevo) |

São **dois jobs separados de propósito**: a máquina de estados nunca pode depender do Brevo estar
de pé. Se o e-mail cair, o negócio continua andando e o aviso sai na rodada seguinte.

O tick avança **1 passo por rodada**. Se o cron ficar 40 dias parado, um trial vencido não pula pra
`expired`: entra em `grace` e ganha a janela inteira de cinza. **Falha a favor da venda, nunca contra.**

## A repescagem

E-mail no momento em que ele **perde** algo — o dia em que o perfil fica cinza é o que converte.
`expired` **não** manda e-mail: insistir depois do fim é o que vira spam.

O link do e-mail carrega a chave da oferta **e o vendedor** (`?k=…&v=…`) — senão a venda que
converte dias depois nasceria órfã.

---

## ⚠️ O que ficou pendente (e é do Lucio)

1. **`BREVO_API_KEY` não existe no projeto.** A repescagem está no ar em **no-op consciente**:
   ela roda, conta o que mandaria, e não envia. Verificado: `{"brevo":false,"simulados":4}`.
   Pra ligar (a conta Brevo você já tem):
   ```bash
   supabase secrets set BREVO_API_KEY='...' --project-ref donaobtlwqrjmvjqflxz
   supabase secrets set BREVO_SENDER_EMAIL='contato@redebaixada.com.br' --project-ref donaobtlwqrjmvjqflxz
   supabase secrets set SITE_URL='https://redebaixada.com.br' --project-ref donaobtlwqrjmvjqflxz
   ```
   *(O remetente precisa estar **verificado** no Brevo, senão a API recusa.)*
   **A máquina de estados funciona sem isso** — o e-mail é o acelerador, não o motor.

2. **As durações do cinza (7d) e do oculto (30d) são palpite meu.** Trial 7d e plano 6m vieram da
   regra; essas duas não estavam escritas em lugar nenhum. Mude na `lifecycle_policies` quando tiver
   opinião — é um UPDATE.

3. **🔓 Buraco de segurança PRÉ-EXISTENTE (não foi este bloco que criou).** A policy de INSERT em
   `companies` é `WITH CHECK (auth.uid() IS NOT NULL)` — sem restrição de coluna. Ou seja:
   **qualquer usuário logado sempre pôde inserir empresa já com `status='approved'`** e ficar no ar
   sem moderação. Hoje o portão da moderação só existe porque o *front* não faz isso. Vale fechar
   (uma policy que force `status='pending'` no insert, com exceção pro fluxo do agente).

---

## Como foi verificado (produção, dado real)

| teste | resultado |
|---|---|
| As 39 empresas da base | ✅ intactas — todas `active`, **sem relógio** (o cron não as toca) |
| Empresa nasce em trial | ✅ `trial`, vence em 7d, `approved`, plano Presença, dono criado, evento `signup` logado |
| A escada, pelo tick | ✅ `trial → grace → hidden → expired`, cada hop carimbado `[cron]` |
| Terminal é terminal | ✅ tick extra não move nada; relógio vira `null` |
| Sumiu das buscas | ✅ `hidden`/`expired` não aparecem na query pública (nem no sitemap) |
| Perfil não foi apagado | ✅ continua acessível pelo link — "reativar é 1 clique" |
| 🩶 Cinza inclicável | ✅ badge "Inativo", grayscale, `cursor-not-allowed`, **sem link pro perfil** |
| Pagamento reativa | ✅ `expired → active` (+6m) e **volta pra busca** — do pior estado possível |
| Estorno | ✅ `active → expired`, volta pra `free`/`pending`, sai do ar |
| Log de auditoria | ✅ `signup · cron · cron · cron · payment · refund` — cada writer carimbou seu motivo |
| Repescagem | ✅ 401 sem segredo · com segredo: 4 e-mails simulados, 1 pulado (`expired`, correto) |
| Rastro de teste | ✅ limpo (39 empresas, 0 TESTE, 0 eventos) |

## Duas coisas que só apareceram olhando o código de perto

1. **O sitemap não filtrava NADA** — mandava pro Google até empresa `pending` e `rejected`. Sem
   corrigir, a empresa sairia das buscas do portal e o Google seguiria indexando o perfil morto:
   exatamente a visibilidade que ela deixou de pagar. Corrigido.
2. **O cinza já existia pela metade** (grayscale desde sempre) mas o card **continuava clicável**.
   Sem tirar o clique, expirar era um filtro bonito sem consequência nenhuma. Agora o que ele perde
   é o cliente — que é o produto que deixou de pagar.

## Detalhe técnico que vale guardar

**Pagamento virou UMA transação** (`company_apply_payment`). Dois writes separados (plano, depois
ciclo) podiam produzir o pior estado possível: **cliente que PAGOU e continua oculto**, ou trial que
pagou e amanheceu cinza porque o relógio velho continuou correndo. Uma função = uma transação = isso
não pode acontecer. O estorno tem a gêmea (`company_revoke_payment`).

---

# 🚨 Adendo (12/07) — o ensaio de porta a porta achou uma mina da Fase 0

Rodei o fluxo PaP **de verdade** (link real com `?k=` **e** `&v=`, celular simulado, ponta a ponta).
Achou dois bugs que nenhum teste de banco pegaria — os dois matavam a venda **na calçada**.

### 1. O `externalReference` estourava o limite do Asaas → **o cliente não conseguia pagar**

```
invalid_externalReference: [...] exceeds the maximum size of [100]
```

O formato v2 da Fase 0 (`company_id|plan|offer|unit|sold_by|indicated_by`) tem **141 caracteres** com os
dois uuids. O Asaas corta em **100**. Toda cobrança gerada por um **link com `?v=`** — que é o link do
vendedor, exatamente o que a Fase 0 criou pra não deixar venda órfã — **era rejeitada antes de nascer**.

Não explodiu ainda só porque os links em uso hoje são só `?k=` (69 chars). Era uma mina esperando o
primeiro vendedor com link próprio — ou seja, esperando o momento em que o negócio começasse a escalar.

**v3 = `company_id|plan_slug|offer|unit`** (67 chars). A atribuição mudou de casa: mora em
`companies.sold_by/indicated_by`, que é onde ela **já nasce** desde o Bloco 3. O `create-payment` carimba
na empresa (sem roubar carteira de quem já é dono) e o webhook lê de lá — com fallback pras posições 4/5
caso ainda exista alguma cobrança v2 no ar. De quebra, a atribuição virou dado consultável em vez de
string espremida num campo de texto.

### 2. Atribuição inválida no link **impedia o perfil de nascer**

O `?v=` ia direto pra uma coluna uuid com FK. Link torto (ou vendedor que não existe mais) → o INSERT
estourava e o perfil não era criado. Agora: valida o formato, e se o banco recusar a referência (23503),
**recria sem atribuição**. Regra que ficou escrita no código: *perder de quem é a comissão é ruim; perder
o cliente é pior — reconciliar atribuição é uma query, reconquistar o cara é outra visita.*

### Ensaio completo, verificado em produção (`main = 71546de`)

| passo | resultado |
|---|---|
| Link `?k=…&v=…` abre | ✅ R$77,70 (de R$155,40), `?v=` guardado na sessão |
| Cadastro inline → auto-login | ✅ 6 campos, sem redirect, sem confirmar e-mail |
| **Perfil nasce NO AR** | ✅ `approved` + `trial` (7d) + plano Presença + **`sold_by` = Lucio** |
| CPF → checkout Asaas | ✅ R$77,70, "Plano Presença - Rede Baixada Oferta Parceiro 6 meses" |
| Webhook `PAYMENT_CONFIRMED` | ✅ `trial → active`, parceiro por 6 meses (12/01/2027) |
| Carteira (`crm_customers`) | ✅ ativo, **dono = Lucio**, MRR R$12,95 |
| Assinatura + Fatura | ✅ semestral ativa · fatura R$77,70 confirmada, **PIX**, **vendedor = Lucio** |
| **Atribuição sem os uuids na cobrança** | ✅ a fatura saiu com o vendedor certo — o conserto se sustenta |
| Idempotência | ✅ 3 eventos → **1** fatura, validade não empilhou |
| Estorno | ✅ `active → expired`, fatura `refunded`, assinatura `canceled`, cliente `cancelado` |
| Rastro | ✅ limpo (39 empresas, 3 usuários, 0 eventos) |

### ⚠️ Mudou como se testa o PaP

**Testar o fluxo agora PUBLICA uma empresa de verdade no portal** (é o efeito do publish-first: o perfil
nasce `approved` + visível). Antes ele nascia `pending`, invisível, e o teste não aparecia pra ninguém.
Todo ensaio precisa nascer como **"TESTE ..."** e ser apagado no fim — e, enquanto durar, ele está no ar.

### Ainda não testado

- **Repescagem chegando de verdade no e-mail** → depende de `BREVO_API_KEY`.
- **Cronômetro QR → PIX ≤ 2 min** → só dedo humano, celular real, primeira visita.

---

# Adendo 2 (12/07) — a carteira do vendedor, e um erro meu que custou dado

## 🩸 INCIDENTE: perdi a descrição da empresa "Jota Vimax" (dado real, irrecuperável)

Testando a nova policy de RLS, usei uma **linha real de produção** como cobaia em vez de criar
uma empresa descartável. Escrevi por cima da `description` e, ao "desfazer", gravei **`null`** —
sem ter guardado o valor original. Wayback e índice do Google não ajudam (o portal é SPA; o texto
nunca vai pro HTML). **Não há como restaurar.** Alguém precisa reescrever o "Sobre" da Jota Vimax.

Auditado: **só ela** foi afetada.

**Regra que fica:** teste de permissão/escrita **nunca** contra linha real. Cria uma empresa
`TESTE ...`, testa nela, apaga. Se por algum motivo precisar tocar numa real, **leia e guarde a
linha inteira antes** — e restaure o valor, não `null`.

## 🚨 O PROJETO NÃO TEM BACKUP NENHUM

O incidente acima expôs isto, que é muito maior que ele: o Supabase diz, literalmente,
**"Free Plan does not include project backups"**.

39 empresas reais, clientes pagantes e um CRM financeiro rodando **sem nenhuma cópia**. Hoje foi
uma descrição perdida por descuido; amanhã pode ser uma migration errada. O **Pro (~US$25/mês)**
dá 7 dias de backup diário. É a coisa mais barata a comprar agora.
➡️ **Pendência do Lucio.**

---

## ✅ A carteira do vendedor (`main = 48387d6`)

**Problema:** a Elis vende um cliente na rua e depois **não consegue ver nem editar o perfil dele**.
E "eu monto seu perfil e seu anúncio, você não faz nada" é o que fecha a venda — o **done-for-you
É o produto**. Sem isso, o vendedor vende e não consegue entregar.

**Causa:** o sistema só conhecia dois jeitos de mandar numa empresa:

| função | quem é |
|---|---|
| `can_manage_company()` | membro/dono (`company_members`) → **o CLIENTE** |
| `can_moderate_company()` | moderador do **bairro/categoria** → **território** |

Nenhum dos dois é *"eu vendi esta empresa"*. São **eixos diferentes**:

> **TERRITÓRIO** = quem fiscaliza uma região (moderação de conteúdo)
> **CARTEIRA** = quem trouxe e cuida do cliente (relação comercial) ← **não existia**

Conflatar os dois deixava o vendedor **cego**: a empresa criada no porta a porta **nem bairro tem**
(o formulário só pede cidade), então nunca cairia no filtro de território. E a query era
`enabled: hasAssignments` — vendedor **sem área atribuída** (a Elis, hoje) não via **nada**, nem a
própria venda.

A carteira já existia no banco desde o Bloco 3 (`companies.sold_by`). Faltava ligar:

- **RLS**: a policy de UPDATE reconhece `sold_by = auth.uid()` → **quem vendeu, edita**.
- **`useAgentCompanies`**: carteira **sempre** + território quando houver. Sem gate de atribuição.
- **AgentDashboard**: quem tem carteira não bate mais no muro de "sem atribuições".
- **AgentCompanies**: selo **"Minha"**, coluna de **Ciclo** (Trial · faltam 5d) e **"Editar perfil"**
  — botão que **já existia e falhava em silêncio**, porque a RLS barrava.

**Verificado contra a RLS real:** Elis **edita** a carteira dela (204) e **não consegue** alterar
empresa de terceiro (0 linhas).

## ✅ Link do vendedor no dash dele (`main = 6c7897b`)

`Dashboard → Minha Área → Meu Link`: link + **QR pra imprimir** + copiar. A chave da oferta **não
foi pro front** (no bundle, qualquer um leria o JS e teria o R$77,70) — vem da edge function
`agent-link`, que confere o papel de quem pede.

**Pra ter link, o vendedor precisa ter conta no portal.** Barça e Gi ainda não têm.
Verificado: a Elis pega o link dela sozinha, e os testes do Lucio com esse link nasceram com
`sold_by = Elis` ✅.

## ✅ O CPF: mantido, mas escondido de quem não decidiu

O Asaas **não emite cobrança sem CPF** — a pergunta era *quando* pedir. Pra quem vai pagar custa 10
segundos. O estrago é pedir documento pra quem ainda não decidiu (*"por que você quer meu CPF se é
grátis?"*), no momento mais frágil da visita.

**Um botão "grátis 7 dias" ao lado do "Ativar agora — R$77,70" foi DESCARTADO**: grátis ao lado de
pago, com o mesmo peso, entrega o caminho fácil de bandeja — **pro cliente E pro vendedor**. Ninguém
pede dinheiro com um botão "de graça" brilhando ao lado.

O grátis **nunca é oferecido**: é uma **saída discreta dentro do modal do CPF** — só aparece pra
quem já clicou em ativar. Leva o cliente **pro próprio perfil no ar**, com faixa de "faltam X dias"
que **só o dono vê**. O indeciso termina a visita olhando o negócio dele publicado, não um
formulário de pagamento que acabou de recusar.

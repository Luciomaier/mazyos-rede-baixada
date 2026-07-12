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

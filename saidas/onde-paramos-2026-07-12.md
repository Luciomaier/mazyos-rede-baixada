# Onde paramos — 12/07/2026 · **HANDOFF**

> Sprint pausado pelo Lucio (madrugada). Leia isto antes de continuar.

---

## 🧭 A SEPARAÇÃO QUE ORGANIZA TUDO (conclusão do Lucio, no fim da noite)

**PaP e Recuperação são DUAS OPERAÇÕES DIFERENTES.** Não é a mesma venda com público diferente —
são dois produtos de vendas distintos. Misturar as duas foi o que embaralhou o conselho.

| | **PaP (rua)** | **Recuperação** |
|---|---|---|
| Quem | negócio que nunca te viu | ex-cliente que **já pagou** |
| O perfil | **não existe** — nasce na visita | **já existe** — e ele *É* o portal |
| O link | `?k=&v=` | `?k=&v=&c=` (claim) |
| Canal | porta, celular dele | telefone / WhatsApp |
| Argumento | *"olha teu negócio no ar"* | *"voltamos — e você já está no ar"* |
| Se não pagar | **some** (grátis: não existia) | **NÃO PODE SUMIR** ← a decisão travada |
| Prontidão | 🟢 **um PIX de distância** | 🔴 **travada na decisão** |

**Ordem decidida: a rua PRIMEIRO.** Motivos:
1. O PaP está pronto; a recuperação precisa de decisão + kanban + os 60 do WordPress.
2. **PaP é dinheiro novo; recuperação é dinheiro parado** — parado há 12 meses, aguenta mais 3 dias.
3. E a rua devolve **a taxa de conversão real** — que é o dado que falta pra decidir a agressividade
   da recuperação. Hoje essa decisão seria no escuro.

---

## 🎯 O ÚNICO GATE DO PaP: um PIX de verdade (15 min)

**Nenhum dinheiro real jamais passou pelo caminho completo.** Todos os testes do webhook foram POST
direto (pagamento fake) — isso prova que o webhook **funciona**, mas **não prova que o Asaas o chama**,
com o payload e o evento certos. O elo `cliente paga PIX → Asaas dispara → sistema ativa` **nunca rodou**.

E é justamente o elo que, se falhar, falha **na frente do cliente**.

**O teste:** abrir o próprio link → empresa "TESTE — Apagar" → **pagar R$77,70 no PIX de verdade** →
conferir ativação (6 meses + fatura no CRM) → **estornar no Asaas**. Custo: R$77,70 por alguns minutos
(volta) + centavos de taxa. **Crava também o cronômetro QR→PIX**, o único número que só dedo humano mede.

Depois: **imprimir a folha com o QR** (`Minha Área → Meu Link → Baixar o QR`) e ir pra rua.

---

## 💡 A jogada que ele ainda NÃO usou: o perfil pré-montado

O `?c=` abre três formas de "eu crio pra você", não uma:

| situação | link | o que acontece |
|---|---|---|
| Rua, na hora | `?k=&v=` | o perfil **nasce ali**, no celular dele |
| **Perfil pré-montado** | `?k=&v=&c=` | monta **antes** da visita (do Google, da fachada); chega e mostra: *"já está no ar"* |
| Reconquista | `?k=&v=&c=` | o perfil já existe (migrado) |

**A do meio é a mais forte e nunca foi usada.** Chegar com o perfil pronto na tela não é promessa,
é entrega.

---

## 🔴 A DECISÃO QUE FICOU EM ABERTO (é a primeira coisa de amanhã)

**Quando o trial de 7 dias da RECONQUISTA acabar e o ex-cliente não pagar, o que acontece com o perfil dele?**

Isto **trava a campanha inteira**. Não ativar trial pra ninguém antes de decidir.

| opção | consequência |
|---|---|
| **A) Fica no ar, sem selo** *(minha recomendação)* | Perde o selo de Verificado e o botão de WhatsApp — **exatamente o que vendemos**. O perfil continua listado. O catálogo (o ativo do portal) fica intacto e a pressão de perda continua real. |
| **B) Some, como o trial da rua** | Máxima pressão (cinza → oculto). Mas se a conversão for baixa, **o portal vai de 37 perfis pra 3** — e aí não há mais o que vender pra ninguém. |
| **C) Não mexer no plano** | Zero risco, zero pressão. E os **14 que hoje têm plano pago DE GRAÇA** continuam de graça. |

**Por que isso é diferente do trial da rua:** lá o perfil **não existia** antes — sumir não custa nada.
Aqui, **os 34 perfis SÃO o portal**. Queimá-los pra tentar cobrar por eles é destruir o ativo.

⚠️ **A mecânica da reconquista PRECISA ser diferente da mecânica da rua.** Hoje elas são a mesma —
e é por isso que ninguém deve ser ativado antes da decisão.

---

## 🟡 O Lucio tem razão: o lugar disso é o KANBAN, não uma planilha

Passamos o dia matando planilha e eu entreguei uma planilha (`folha-reconquista.csv` + a do Drive).
Foi atalho, não desenho. **Descartar como ferramenta principal.**

O kanban já existe (`/dashboard/admin/crm/leads`, 7 colunas) e **já se move sozinho** (trial → negociando,
pagou → convertido, cinza, oculto, expirado). O que **falta no card** pra ele aguentar a ligação:

- [ ] **Ligar os 35 leads aos perfis** (`crm_leads.company_id` está **NULO em todos**). Já cruzei:
      34 de 35 casam por nome/telefone. **O Lucio confere antes.**
- [ ] No card: **visualizações** (o gancho: "93 pessoas viram sua página"), **botão de WhatsApp**,
      **link do perfil**, **copiar link de reativação**.
- [ ] Botão **"Ativar trial 7 dias"** direto no card — é o gesto operacional da ligação.
- [ ] Bug pequeno: `STATUS_COLUMNS` tem 7 colunas e o grid é `md:grid-cols-6`.

---

## 🟡 Faltam ~60 clientes que ainda estão no WordPress

O Lucio avisou: a base é maior. Os que estão no portal (37) são só os que ele migrou **à mão**.
Faltam uns **60 no WordPress**.

**Pra próxima sessão:** conseguir o export do WordPress (CSV/SQL/planilha) e criar os perfis
(done-for-you). Sem perfil no ar, a ligação perde o gancho — o argumento é *"seu perfil JÁ está no ar,
olha lá"*, não *"quer entrar?"*.

---

## ✅ O que ficou PRONTO hoje (tudo em produção, verificado)

| entrega | commit |
|---|---|
| **Bloco 3 — ciclo do trial** (trial 7d → pago 6m → cinza → oculto → expirado, pg_cron) | `5f7a694` |
| **Fix crítico:** `externalReference` estourava o limite de 100 do Asaas → **toda venda com link de vendedor morria** | `71546de` |
| **Link do vendedor** no dash dele (QR pra imprimir) + saída digna do CPF | `6c7897b` |
| **Carteira do vendedor** — quem vendeu, VÊ e EDITA o cliente (a Elis estava cega) | `48387d6` |
| **Histórico de empresas** — desfazer sobrescrita (nasceu do meu erro) | `6fc128e` |
| **Funil segue o ciclo** — a visita finalmente vira lead | `456283c` |
| **Repescagem pelo Resend** (transacional; Brevo fica pro marketing) | `5c3aec4` |
| **Link de reativação (claim)** — ex-cliente paga pelo perfil DELE, sem duplicata | `5bc80f4` |

**A repescagem está VIVA:** `redebaixada.com.br` verificado no Resend (DKIM+SPF+MX), e-mails reais
testados (dia 0, cinza, oculto, recibo). `{"resend": true}`.

---

## 📌 Pendências do Lucio (não são código)

- [ ] **A decisão lá de cima** ⬆️
- [ ] Cancelar as faturas do Asaas (**855418887** e a do teste `op4crxlwhc1jn5pe`)
- [ ] **Reescrever o "Sobre" da Jota Vimax** (descrição que eu apaguei num teste — irrecuperável)
- [ ] Export do **WordPress** (~60 clientes)
- [ ] Contas de vendedor pro **Barça e a Gi** (sem conta → sem link → venda órfã)
- [ ] **Supabase Pro** (backup) — decidido: quando a rua pagar

---

## 🗣️ O script da ligação (ele pediu; ainda não usado)

> *"Seu Fulano, aqui é o Lucio da Rede Baixada. Lembra que você entrou com a gente lá atrás?*
>
> *Pois é — o portal voltou, todo reconstruído. E eu já subi o seu perfil de novo.*
> ***Olha só: 93 pessoas já procuraram e viram a sua página.***
>
> *Ele está no ar agora. Vou te mandar o link no WhatsApp pra você ver como ficou.*
>
> *Se fizer sentido continuar, é o mesmo R$77,70 por 6 meses."*

**Prova → presente → prazo → preço conhecido.** Se hesitar, **não insistir** — a máquina cobra depois.

⚠️ **O trial só começa NO DIA da ligação.** Lotes de 5 a 8. Ativar todos de uma vez faria o cara ficar
cinza **sem nunca ter falado com você** — a repescagem chegaria como grosseria, não como oportunidade.

---

## 🧠 Coisas que custaram caro hoje (não redescobrir)

1. **`externalReference` do Asaas: limite de 100 caracteres.** Não cabe uuid de atribuição.
2. **Teste de escrita NUNCA contra linha real** — apaguei a descrição da "Jota Vimax" e não deu pra
   restaurar (não havia backup). Hoje existe `companies_history` + `company_restore_content()`.
3. **O SQL Editor do Supabase mente:** rodei um DELETE, o painel mostrou o resultado ANTIGO e eu quase
   acreditei. **Sempre conferir o efeito pelo REST**, não pela tela.
4. **`curl` POST precisa de `--http1.1`** (HTTP/2 dá PROTOCOL_ERROR contra o Supabase nesta máquina).
5. **TERRITÓRIO ≠ CARTEIRA.** Bairro/categoria é moderação; `sold_by` é a relação comercial.
6. **Testar o PaP PUBLICA empresa de verdade** (publish-first). Sempre nomear "TESTE ..." e apagar.

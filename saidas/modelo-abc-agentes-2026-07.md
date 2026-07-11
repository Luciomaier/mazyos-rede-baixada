# Modelo ABC — qualificação de novos agentes por indicação

> Ideia do Lucio, **11/07/2026**, refinada ao longo da conversa. **Status: NÃO decidido, NÃO no roadmap.**
> É captura + desenho, não plano de execução. O roadmap atual põe "hierarquia de sub-agentes" e "franquia
> formal" explicitamente **fora por agora** — ver [`roadmap-plataforma-unica-2026-07.md`](roadmap-plataforma-unica-2026-07.md).
>
> ⚠️ **Nomenclatura (decidida 11/07):** **não** usar "estágio"/"estagiário" — palavra regulada (Lei 11.788)
> e que sugere vínculo. Usar **qualificação** / **treinamento** / **agente em formação** / **candidato a
> agente**. O texto abaixo já segue isso.

## A ideia

O **agente entitulado** qualifica novos agentes. O candidato é **independente**: sem obrigação, sem
subordinação, sem meta, sem jornada. Ele apenas **indica clientes**. O agente vai junto, conduz a venda e
fecha.

1. O agente convida um candidato.
2. O candidato **indica clientes** — e acompanha o agente na porta (aprende vendo a venda acontecer).
3. **Quem vende é o agente**, e a venda é dele: comissão, cliente, carteira.
4. Ao cumprir a qualificação — **N indicações convertidas** (faixa citada: **5 a 10**) — o candidato ganha:
   - **o direito a uma conta de agente no sistema** (a "concessão"), e
   - um **bônus de conclusão** (valor a definir — citado "xx reais", exemplo anterior: R$200).
5. A partir daí ele opera **carteira própria, do zero** — e pode, ele mesmo, qualificar outros.
6. **Nível acima (futuro):** possivelmente um **supervisor** sobre os agentes.

## 🔑 A chave conceitual: a concessão é paga com indicação, não com dinheiro

*(Lucio, 11/07 — é a ideia que estava escondida atrás da mecânica.)*

As N indicações **são o preço da concessão**. Numa franquia comum, o candidato paga uma **taxa de entrada em
dinheiro** pra ter o direito de operar. Aqui ele **paga com indicação** — com clientes reais trazidos pra
rede.

> **Não é trabalhar de graça. É comprar a concessão com indicação em vez de capital.**

Isso resolve três coisas de uma vez:

- **É o pitch de recrutamento.** *"Você não paga nada pra entrar. Me indica 5 clientes, eu vou junto e
  fecho — você vê como se faz. Cumpriu, a conta de agente é sua, com bônus. Aí a carteira passa a ser sua."*
  Compare com a franquia que cobra R$5–20 mil de taxa de entrada de quem nem sabe se sabe vender.
- **Alinha o incentivo do agente:** cada candidato **fomenta a carteira do titular** — que é o ativo real
  (o LTV não está nos R$77,70, está na graduação do cliente pra Rede Publicidade).
- **É a blindagem jurídica** (ver seção própria): ninguém paga pra entrar, e o candidato **não trabalha** —
  ele **indica**.

## Posicionamento — o que este modelo NÃO é (Lucio, 11/07)

> *"Desta forma fugimos do modelo tradicional de MLM e entramos num formato que resulta **não em promessas
> de grandes ganhos insustentáveis**, e passamos a ter um modelo **mais real e sustentável, que não
> atrapalha — agrega**."*

Isso não é filosofia solta: é **guardrail de comunicação**. O que ele proíbe, na prática:

- ❌ **Nada de promessa de ganho.** Sem "ganhe R$10 mil/mês", sem print de extrato, sem "liberdade
  financeira". O que se promete é o que se entrega: **uma conta de agente + um bônus, ao cumprir N
  indicações convertidas.** Concreto, verificável, pequeno.
- ❌ **Nada de urgência fabricada nem hype** — mesma regra do playbook de rua (`preferencias.md`: tom
  consultivo de vizinho, nunca marketês).
- ❌ **Ninguém é recrutado pra "entrar numa rede"** — é convidado a **indicar vizinhos comerciantes** que
  ele acha que se beneficiariam. Se gostar, vira agente.
- ✅ **"Agrega, não atrapalha":** o indicador não larga o que faz. O cliente comerciante continua tocando o
  negócio dele; quem quer renda extra não precisa largar o emprego. **A indicação é aditiva**, não um
  substituto de renda vendido como sonho.

O teste de sanidade, sempre: **o dinheiro entra pela venda de um serviço real a um comerciante real** — não
pelo recrutamento. Se algum dia a receita passar a vir de quem entra em vez de quem compra, o modelo virou
outra coisa e deve ser parado.

## Quem é o indicador (duas fontes — decidido 11/07)

O candidato **não precisa ser um aspirante a vendedor**. São duas personas, e a primeira é a mais forte:

**1. O próprio cliente.** *"Os próprios clientes podem — e devem — ser os indicadores."* Quem acabou de
pagar os R$77,70 e **viu o perfil no ar** é o melhor advogado que existe: ele já acreditou, já tem a prova
na mão e conhece os vizinhos comerciantes da mesma rua. **Cada venda vira porta pra próxima** — o canal PaP
deixa de depender só das pernas do agente.

**2. Quem quer uma renda extra.** A persona clássica do modelo: entra pra virar agente e ter carteira
própria.

⚠️ **Pergunta de desenho em aberto:** as duas personas querem **prêmios diferentes**?
- O **aspirante a agente** quer a **conta de agente + bônus** (é o caminho de carreira).
- O **cliente comerciante** talvez não queira virar vendedor — pra ele, o prêmio óbvio é
  **renovação grátis / desconto / meses a mais de plano** (ou o bônus em dinheiro).

➡️ *Recomendação: dois trilhos com o mesmo motor.* O campo `indicated_by` e o contador servem aos dois; só
muda a recompensa no fim. **Não decidir isso agora** — mas saber que existe, porque muda a UI: o dashboard
do cliente precisaria de um **"indique e ganhe"** com link próprio (encaixa naturalmente no painel
**"Meus Serviços"** da Fase 1 do roadmap).

## 💱 A indicação é uma MOEDA — vale pra todo mundo (Lucio, 11/07)

> *"Um usuário indicando a cota de clientes, ele **ativa também o sistema dele**."*

Esta é a generalização que fecha o modelo: **indicação vale como dinheiro** — não só pra quem quer virar
agente, mas **pro cliente comum também**. Quem indica a cota **ativa/renova o próprio plano sem pagar**.

| Quem | Mantém o acesso... | ...ou, alternativamente |
|---|---|---|
| **Cliente** | pagando **R$77,70 / 6 meses** | **indicando a cota** → ciclo ativado **de graça** |
| **Candidato a agente** | — | **indicando a cota** → ganha a **conta de agente** + bônus |
| **Agente entitulado** | **ficando ativo** (produzindo no ciclo) | — |

**Uma moeda só, três usos.** É o que faz a "recorrência suave" girar por toda a rede: cliente, candidato e
agente sustentam seu lugar com a mesma coisa — **trazer negócio novo pra dentro**.

### O motor de crescimento (e por que isso é grande)

Todo cliente passa a ter **motivo próprio** pra trazer os vizinhos comerciantes. O canal PaP deixa de
depender das pernas do agente: **cada venda planta a próxima**. E o incentivo é honesto — o cliente não
ganha "dinheiro por recrutar", ele **ganha o próprio serviço**.

### ⚠️ A conta que decide tudo: qual é a COTA?

A cota é o **dial de caixa** — ela decide se isso **gera** dinheiro ou só **troca** dinheiro por crescimento.
Com renovação de R$77,70 e indicações **convertidas** (que pagaram):

| Cota | Entra em caixa | Deixa de entrar | Saldo | Leitura |
|---|---|---|---|---|
| **5 convertidas** | R$388,50 | R$77,70 | **+R$310,80** | 5× de retorno — folgado |
| **3 convertidas** | R$233,10 | R$77,70 | **+R$155,40** | 3× — confortável |
| **2 convertidas** | R$155,40 | R$77,70 | **+R$77,70** | 2× — ainda positivo |
| **1 convertida** | R$77,70 | R$77,70 | **R$0** | caixa **empata** — você troca receita por 1 cliente novo |

➡️ Mesmo na cota 1 você **ganha um cliente na base** (que pode indicar também), mas **não entra caixa novo**.
Se o objetivo é **caixa** (é: substituir o Uber, construir reserva), a cota tem que ser **≥3**. Se o objetivo
for **crescer a base rápido** numa janela específica, cota 1–2 vira uma campanha — mas com prazo, não como
regra permanente.

### Regras anti-abuso (não negociáveis, se isso for pra frente)

- **Só conta indicação CONVERTIDA** — cliente que **pagou**. Indicação "apresentada" não vale nada, senão
  vira lista telefônica.
- **Estorno/chargeback descontam** — se o indicado pediu o dinheiro de volta, a indicação **deixa de contar**
  (o webhook já sabe revogar em `PAYMENT_REFUNDED`/`CHARGEBACK` — a mesma trava serve aqui).
- **Nada de auto-indicação nem CPF repetido** — o Asaas identifica cliente por documento; usar isso.
- **Cota por ciclo, não acumulável pra sempre** — senão alguém indica 20 num mês e fica 10 anos de graça.

## ⏳ Validade do agente — a "recorrência suave" (Lucio, 11/07)

> *"Ele tem que estar **ativo durante o ciclo de 6 meses**, porque é como se ele **pagasse os R$77,70
> também**. Desta forma gira entre a equipe de vendas e agentes: uma **recorrência suave**."*

A conta de agente **tem validade** — o mesmo ciclo de 6 meses do plano do cliente. E a simetria é o coração
da ideia:

| | Como conquista | Como mantém | Ciclo |
|---|---|---|---|
| **Cliente** | paga R$77,70 | **paga** de novo | 6 meses |
| **Agente** | **N indicações convertidas** (a concessão) | **fica ativo** (produz) | 6 meses |

**O agente não paga a conta dele com dinheiro — paga com atividade.** É a mesma moeda da concessão: entrou
indicando, permanece produzindo. Nada é vitalício.

### Por que isso é forte (além da receita)

- **É a blindagem anti-MLM mais forte do modelo.** Mata a **renda passiva**: ninguém recebe pra sempre por
  trabalho feito uma vez. Pra continuar recebendo da carteira, tem que **continuar servindo a carteira**.
  Isso é o oposto exato da promessa de MMN ("monte sua rede e receba dormindo").
- **Resolve a pergunta "manutenção é direito ou dever?"** → **é os dois.** A receita recorrente da carteira
  é a contrapartida de manter o cliente atendido. Parou de atender, para de receber.
- **Mantém a base viva.** Agente parado não vira zumbi segurando carteira morta — o cliente dele estaria
  desassistido, e cliente desassistido não renova.

### ⚠️ A pergunta pesada que essa regra levanta (NÃO decidida)

**O que acontece com a CARTEIRA do agente que ficou inativo?** É a decisão mais delicada do modelo inteiro,
porque carteira = **receita recorrente de gente de verdade**:

- **(a) Ele perde a carteira** — os clientes voltam pra casa ou vão pra outro agente (o supervisor?
  quem assumir a manutenção?). Coerente com "quem serve, recebe" — mas é duro, e precisa estar **escrito
  antes**, nunca decidido no calor.
- **(b) Ele mantém a carteira, mas não pode captar novos** — mais brando; risco de carteira encostada com
  cliente mal atendido.
- **(c) Ele para de receber as renovações, mas o cadastro fica** — meio-termo: o dinheiro segue quem faz a
  manutenção, o histórico fica registrado.

Ligado a isso: **o que conta como "ativo"?** Quantas vendas/indicações por ciclo de 6 meses? **Não definido.**
Se a régua for alta demais, vira pressão (e cheiro de subordinação — ver riscos jurídicos). Se for baixa
demais, não filtra ninguém.

➡️ **Seja qual for a escolha, ela precisa estar no termo assinado ANTES do primeiro agente.** Tirar carteira
de alguém sem regra escrita é briga garantida.

## O que fica com quem

| | Durante a qualificação | Depois de entitulado |
|---|---|---|
| Quem **indica** | o candidato | ele mesmo |
| Quem **fecha a venda** | **o agente** | ele mesmo |
| **Comissão** da venda | **o agente** | ele |
| **O cliente / a carteira** | **o agente** | ele |
| **Renovação** (6m), **upsell** (GMN/Site/Movimento), **manutenção** | **o agente** | ele |
| O que o candidato leva | **conta de agente + bônus** ao cumprir | — |

O candidato **não tem direito residual** sobre os clientes que indicou — nem na hora, nem depois. Sua
carteira começa **do zero** quando ele se titula.

## ⚠️ Implicação técnica (isso importa AGORA, na Fase 0)

O modelo separa conceitos que hoje o sistema trata como um só — ou não trata:

| campo | quem é (na qualificação) | serve pra | hoje no código |
|---|---|---|---|
| **`indicated_by`** | o **candidato** | **contar as N indicações** que cumprem a qualificação | não existe |
| **`sold_by`** | o **agente** (é ele quem fecha) | métrica de venda, produtividade | não existe |
| **`credited_to`** | o **agente** | comissão daquela venda | não existe |
| **`owner`** (em `crm_customers`) | o **agente** | **carteira**: renovação, upsell, manutenção, LTV | tabela existe, o webhook **não escreve** nela |

Hoje o `externalReference` da cobrança é `company_id|plan_slug|parceiro` — **sem agente nenhum**
(verificado 11/07). A **Fase 0 do Sprint 2** vai reescrever exatamente esse campo.

➡️ **Recomendação pra Fase 0:**
1. `externalReference` carrega **`sold_by`, `credited_to` e `indicated_by`** (no caso normal — Lucio
   sozinho — os dois primeiros são ele e o terceiro é vazio).
2. O webhook, ao criar o `crm_customer`, grava **`owner` = `credited_to`** — é isso que faz **renovação e
   upsell caírem pro titular** sem reconciliação manual depois.
3. **`indicated_by` é o contador da qualificação** — e, de brinde, serve pra **qualquer indicação**
   (cliente satisfeito que indica outro), não só pro ABC. É um campo genérico e barato.

**Custo agora: colunas.** Custo depois: migração + reconciliar comissão paga **e carteira mal atribuída**
(essa é a pior — mexe em quem recebe a receita recorrente).

### A validade do agente reusa a máquina do trial (não é sistema novo)

O ciclo de 6 meses do agente (ativo → inativo) é **a mesma mecânica** do ciclo do cliente
(`trial → pago 6m → cinza → oculto → expirado`) que o **item 4 do Sprint 2** já vai construir: coluna de
vencimento + job agendado (**pg_cron**) que vira o estado sozinho. Muda só o **gatilho da renovação**:

| | gatilho que renova | o que o job checa |
|---|---|---|
| **cliente** | **pagamento** (webhook Asaas) | `plan_expires_at` |
| **agente** | **atividade** (vendas/indicações no ciclo) | `agent_active_until` + contador do ciclo |

➡️ Quando o item 4 for construído, **desenhar a máquina de estados genérica o bastante pra servir aos dois**.
Não construir o do agente agora — só não fechar a porta.

## Riscos e dials (não resolvidos — decidir com o Lucio)

1. **Retenção do candidato.** Sem obrigação nenhuma, o risco não é ele "desistir revoltado" — é ele
   simplesmente **não indicar** e a qualificação nunca acabar. O motor aqui é o **bônus + a conta de
   agente** parecerem valer a pena. Dials: valor do bônus (**"xx reais"** — não definido) e **N = 5 ou 10**.
2. **N = 5 ou 10?** É o **dial principal**: é literalmente o **preço da concessão**. Mais alto = mais ativo
   pro titular e entrada mais cara; mais baixo = mais agentes formados, mais rápido.
3. **Indicação "convertida" ou "feita"?** Conta a indicação que **virou venda paga**, ou a que só foi
   apresentada? *(Recomendação: **convertida** — senão vira lista telefônica.)*
4. **O titular ganha override depois que o candidato se titula?** Sem isso, o ganho dele termina na
   formatura. Com isso, vira estrutura de rede — e o cuidado jurídico muda de patamar.
5. **Quantos candidatos simultâneos**, se o agente vai junto em cada venda? O acompanhamento presencial é o
   gargalo físico — não escala como carteira escala.
6. **Manutenção é direito ou dever?** O titular acumula receita recorrente **e** carga de atendimento. Um
   agente com 50 clientes tem trabalho real de manutenção. É aí que **supervisor** ou um time de entrega
   centralizado deixa de ser luxo.
7. **Supervisor:** override sobre agentes? Quantos agentes por supervisor?

## Cuidados jurídicos

**1. Cheiro de multinível — defesa sólida.** O dinheiro vem da **venda de um serviço a um cliente final**
(R$77,70 de um comerciante), **não** de taxa de entrada de quem é recrutado. O candidato **não paga pra
entrar**. Regras a manter nítidas: **nunca cobrar do candidato** e **nunca remunerar o simples ato de
recrutar** — só o resultado da venda ao cliente final.

**2. Risco trabalhista — muito reduzido pelo desenho de 11/07, mas não zero.**
O desenho **independente / sem obrigação / sem subordinação / só indica** ataca exatamente os elementos que
geram vínculo (pessoalidade, habitualidade, subordinação, onerosidade). Somado a **não usar a palavra
"estágio"**, é uma estrutura bem mais defensável.

⚠️ **O que ainda pode furar — e não está no papel, está na prática.** No Brasil vale o **primado da
realidade**: o que manda é como a coisa acontece, não o nome no contrato. O desenho só se sustenta se, na
rua, for verdade:
- **Sem jornada.** Nada de "toda segunda 9h a gente bate perna". Ele aparece quando quer.
- **Sem meta obrigatória nem cobrança.** A qualificação é um **direito que ele persegue**, não uma **cota
  que ele deve**.
- **Sem punição/disciplina.** Não indicar não gera consequência nenhuma.
- **Sem exclusividade.** Ele pode fazer o que quiser da vida dele.

Se na prática houver escala, cobrança e subordinação, o rótulo "independente" não segura.

**Mitigações a fechar com advogado** (isto não é parecer jurídico):
- **Contrato/termo escrito** do programa de qualificação: independente, sem vínculo, sem obrigação, com a
  regra da concessão explícita (N indicações convertidas → conta de agente + bônus).
- **Considerar uma ajuda de custo por indicação convertida** — muda a natureza de "sem remuneração" pra
  "remuneração autônoma por resultado", e ainda resolve o dial de retenção (risco nº 1).
- **Barça e Gi são família** → risco prático baixo pra começar. O **primeiro candidato de fora é a hora de
  ter o termo assinado** — não depois.

O roadmap já anota "franquia formal (COF/jurídico)" como fora por agora, começando como **rede de
representantes**. Este documento reforça: **a formalização vem antes de recrutar o primeiro de fora.**

---
Ligações: [`sprint-2-2026-07.md`](sprint-2-2026-07.md) (Fase 0 — atribuição) ·
[`regra-negocio-parceiro-2026-07.md`](regra-negocio-parceiro-2026-07.md) (comissão amarrada ao pagamento) ·
[`oficina-agente-2026-07.md`](oficina-agente-2026-07.md) (duplicar Barça/Gi) ·
[`.claude/skills/venda-porta-a-porta/SKILL.md`](../.claude/skills/venda-porta-a-porta/SKILL.md) (o playbook que o candidato aprende vendo) ·
organograma comercial → `../../rede-publicidade/saidas/organograma-comercial-2026-07.md`

---
name: venda-porta-a-porta
description: >
  Playbook da venda porta a porta da Rede Baixada — abordagem consultiva a empresas e
  profissionais da Baixada pra cadastro no portal e assinatura. Modelo híbrido: fecha na
  hora quem está quente (R$77,70) e coloca quem hesita num trial grátis que vira link no
  vencimento. Use quando o Lucio for prospectar, disser "/venda-porta-a-porta", "vou bater
  perna", "roteiro de visita", "como abordar", "montar a folha" ou pedir ajuda pra preparar
  ou revisar um dia de prospecção.
---

# /venda-porta-a-porta — Playbook de prospecção da Rede Baixada

Roteiro operacional da venda porta a porta. Não é texto decorado — é a sequência
que o Lucio segue na rua, calibrada no tom **consultivo de vizinho** (lidera com
pergunta, nunca com pitch). Benchmark a bater: **R$338,50 em 4h** (melhor por hora
que o Uber — esse é o objetivo: provar consistência e largar o Uber).

> Preço confirmado pelo Lucio: **R$77,70**.

> Tom: ver `_memoria/preferencias.md`. Visual da folha: `identidade/design-guide.md`.
> Nunca usar urgência fabricada, marketês ou falar de cima pra baixo. Vizinho com vizinho.

---

## Modelo da venda (híbrido)

Todo prospect sai da visita **dentro do funil** — ninguém sai como "não" puro:

- **Quente** (já quer, gostou do preço) → **fecha na hora**: cria login, paga R$77,70 (PIX/cartão), perfil no ar.
- **Morno / "vou pensar" / em cima do muro** → **trial grátis**: ativa a conta de graça, monta o perfil, e o sistema cuida do link no vencimento + nutrição na janela.
- **Frio / "agora não"** → **agenda volta** ou entra numa lista de re-visita. Não força.

A regra de ouro: **sempre criar o login na visita**. O login é o sinal de compra — quem
cria, comprou (só falta pagar). Quem não cria, não estava pronto; vira re-visita.

---

## A oferta (o que vai na folha e no link)

- **Preço de parceiro:** **R$77,70 — 6 meses** (renova por R$77,70 · semestral · menos de R$13/mês).
- **Link privilegiado (exclusividade):** esse preço só existe no link/folha que você entrega na
  visita. Quem você não visitou vê o preço normal no site. *"Esse valor é pra quem eu visito."*
- **Você monta tudo (perfil + anúncio):** o cliente não mexe em nada. **Zero fricção** = fecha mais na hora.
- **Preço travado:** quem entra agora mantém o R$77,70 na renovação enquanto for parceiro ativo.

**Linha de fechamento (do Lucio):**
> "Fechando comigo agora você entra por R$77,70 por 6 meses — preço de parceiro, travado enquanto você
> estiver ativo, um valor que só quem eu visito tem. E eu monto seu perfil e seu anúncio, você não faz nada."

Por que cada peça importa:
- **Exclusividade do link:** dá motivo pra fechar AGORA com você (não no site, não depois). Vale mesmo se fechar depois.
- **Done-for-you:** tira a fricção — ele só diz sim.
- **Preço travado:** o anti-cancelamento — sair = perder o preço de parceiro. Segura a recorrência.
- **Janela de 6 meses:** cria o re-contato semestral pra renovar (R$77,70) e oferecer planos maiores (upsell).

> **Como cobrar hoje:** ✅ **no ar e verificado ponta a ponta (11/07/2026)**. O **link privilegiado**
> `/oferta-parceiro?k=b036e660589d546db056951c` (o QR da folha) faz tudo sozinho: cadastro enxuto na
> própria página → auto-login → modal do CPF → **checkout Asaas em R$77,70** (PIX, boleto, crédito ou
> débito) → o webhook ativa **presença por 6 meses**. O gate do preço é server-side: sem o `?k=`, o preço
> é o do site. **Não precisa mais gerar cobrança na mão no painel.**
>
> Se o celular já estiver logado (na tua conta ou na do cliente anterior), toque **"trocar de conta"** no
> rodapé do card — é o que te deixa emendar uma venda na outra no mesmo aparelho.
>
> ⚠️ **O que ainda é manual** (não confie no sistema pra isso): o **trial** do indeciso (não tem relógio,
> não expira, não nutre sozinho — controle na planilha e mande o link por WhatsApp) e a **atribuição do
> vendedor** (o link não sabe quem vendeu — se não for você, anote). E-mails transacionais não existem.

---

## Fase 1 — Preparar o dia (antes de sair)

**Roteiro geográfico** (não andar à toa):
- Escolher **1 rua/bairro de comércio** e varrer em sequência — não pular de um lado pro outro da cidade.
- Mirar negócio com **vitrine física e dono presente**: salão, mercadinho, oficina, pet, lanchonete, ótica, loja de roupa. Onde dá pra falar com quem decide na hora.
- Meta de visita por saída: definir um número (ex: 15–20 portas) pra medir conversão depois.

**Material na mão:**
- A **folha** impressa (vantagens + R$77,70) — ver `folha-vendas.md` nesta pasta.
- Celular com o site `redebaixada.com.br` aberto e login funcionando (pra criar a conta na hora).
- Maquininha / PIX pronto pra cobrar os R$77,70 na hora.
- Lista/planilha pra anotar cada visita (nome, contato, status, próxima ação).

## Fase 2 — A abordagem (na porta)

1. **Chega simpático e contente.** Energia leve. Quebra o gelo antes de qualquer coisa.
2. **Abre com a pergunta consultiva** (nunca com pitch):
   > "Estou visitando aqui a vizinhança empreendedora pra entender como vocês estão fazendo
   > pra divulgar e atrair cliente hoje em dia."
3. **Escuta e diagnostica.** Deixa falar. Perguntas que abrem o jogo:
   - "Você divulga de alguma forma? Como as pessoas te encontram hoje?"
   - "Tem algum desafio pra aparecer / trazer cliente novo?"
   - "Você tem Google Meu Negócio?" (se não tem ou não sabe, é dor clara — anota.)
4. **Lê a temperatura.** A reação varia muito (quente, morno, "vem outra hora", muro, não).
   Não tratar todo mundo igual — o diagnóstico decide o fechamento (Fase 3).

## Fase 3 — A oferta + fechamento

5. **Mostra a folha.** Conecta a dor que ele acabou de falar com a vantagem no papel.
   Apresenta o **R$77,70** com naturalidade — é a âncora que derruba a objeção. Sem drama no preço.
6. **Lê de novo a temperatura e escolhe o caminho:**

   **→ Fechou na hora (quente):**
   - Cria o login com ele ali (sinal de compra).
   - Cobra os **R$77,70** (PIX/cartão). Perfil ativado e publicado.
   - **Trava o preço:** "esse R$77,70 fica travado enquanto você estiver ativo" — é o que faz ele querer continuar.
   - **Você monta o perfil + o anúncio** (pelo painel admin) — o cliente não toca em nada.
     Entrega no mesmo dia amarra a venda: ele vê o valor entregue, não só prometido.

   **→ Hesitou ("vou pensar" / muro / morno):**
   - Não empurra. Oferece o **trial grátis**: "Deixa eu já te deixar no ar de graça por
     [X dias] pra você ver funcionando, sem compromisso."
   - **Cria o login mesmo assim** (é o sinal de compra — não pula esse passo).
   - Monta o perfil/anúncio dele igual. Ele entra na janela de nutrição (Fase 4).

   **→ Frio ("agora não" / "vem outra hora"):**
   - Agenda a volta ou anota pra re-visita. Pega o contato. Sai bem — vizinho não queima ponte.

## Fase 4 — Trial → nutrição → link (o braço que converte depois)

Pra quem entrou no trial, a venda continua sozinha na janela entre ativar e vencer:

- **Ativação:** conta grátis no ar, perfil montado (valor entregue antes de cobrar).
- **Nutrição na janela:** lembretes/provas de valor até o vencimento (ex: "seu perfil já
  apareceu em X buscas", "tá no ar, dá uma olhada"). Modelo que o Lucas validou em outro nicho.
- **Vencimento:** dispara o **link de pagamento** dos R$77,70 pra manter o perfil no ar.

> ⚠️ **Dependências de sistema** (sem isso, esse braço é manual):
> - **E-mails transacionais** — confirmação de cadastro, ativação do trial, lembrete de
>   vencimento e link de pagamento. (Hoje a plataforma **promete** "enviamos confirmação" e
>   não envia — gap a fechar. Ver pendências.)
> - **Modo trial no portal** — ativar conta grátis com prazo e gerar o link no vencimento.
> Enquanto não existir no portal: rodar **manual** (ativar na mão, controlar vencimento na
> planilha/CRM, mandar link por WhatsApp). O Mini CRM pode segurar esse controle.

## Fase 5 — Objeções (calibradas no tom vizinho)

Responder com pergunta/escuta, nunca com pressão:

| Ele diz | Resposta (vizinho, sem empurrar) |
|---------|----------------------------------|
| "Tá caro" | "Você entra por R$77,70 a cada 6 meses — preço de parceiro, só pra quem eu visito. Menos de R$13 por mês. Que retorno já pagaria isso?" |
| "Vou pensar" | "Tranquilo. Deixa eu já te deixar no ar de graça pra você ver funcionando — aí você pensa com a coisa na mão, sem pagar nada." → **trial** |
| "Mas no site tá mais barato / R$147 no ano" | "É outro pacote. No site você mesmo monta tudo e paga o ano cheio de uma vez. Comigo você não faz nada — **eu monto seu perfil e seu anúncio** — e ainda entra por 6 meses pra experimentar, sem travar o ano. Você paga um pouquinho mais porque tem gente fazendo por você." |
| "Já tô no Instagram / Google" | "Massa. E quando alguém procura [seu ramo] em [cidade], você aparece? O portal é mais um lugar onde te acham — soma, não substitui." |
| "Não tenho tempo agora" | "Sem problema, eu monto tudo pra você. Você só me passa 2 ou 3 infos e eu deixo pronto." |
| "Vem outra hora" | "Combinado. Melhor dia/horário pra eu voltar?" → **agenda, anota** |

## Fase 6 — Fechar o dia (registro + métrica)

- Anotar cada visita: **nome, contato, ramo, status** (fechou / trial / re-visita / não), próxima ação.
- Calcular o **R$/hora** do dia e comparar com o Uber (~R$150/5h = R$30/h). Benchmark: R$338,50/4h = **R$84,60/h**.
- Quem entrou no trial: registrar **data de vencimento** pra disparar o link.
- Re-visitas: agendar a volta. Não deixar lead esfriar sem follow-up.

---

## Regras

- **Sempre** liderar com pergunta, nunca com pitch. Diagnóstico antes de oferta.
- **Sempre** criar o login na visita (quente ou trial) — é o compromisso que amarra.
- **Sempre** registrar a visita e a próxima ação. Lead sem follow-up é dinheiro na mesa.
- **Nunca** urgência fabricada, marketês ou tom de cima pra baixo.
- **Nunca** sair com um "não" puro se dá pra oferecer o trial ou agendar volta.
- O preço (**R$77,70**) entra com naturalidade — a folha faz o trabalho, não a pressão.

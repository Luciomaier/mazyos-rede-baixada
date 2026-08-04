# Recadastramento real + Alamedas — plano de agosto/2026

> Base: banco de produção, conferido em 02/08/2026.
> Cobre o que foi pedido: jornada do cliente migrado, script de contato,
> desfechos, continuidade, exclusões reais, matérias e o hub de alameda.

---

## 1. O diagnóstico que muda o plano

**Os 37 perfis antigos estão todos numa conta só: a tua.** Foram importados do
WordPress sob o teu usuário. Nenhum daqueles donos tem login.

Consequência dura: **nenhum deles consegue ver painel, botão de pagar ou editar
nada.** O portão da jornada inteira não é preço, é **claim** — reivindicação.
Enquanto o dono não criar a conta dele, não existe nada pra ele fazer.

O resto da base diz o seguinte:

| | |
|---|---|
| Perfis na tua conta | **37** |
| Com WhatsApp preenchido | **37 de 37** — dá pra rodar 100% WhatsApp-first |
| Tiveram ao menos 1 visualização em julho | **34 de 37** |
| Alguém clicou pra contatar | **7 de 37** |

**A leitura que importa: 27 negócios foram vistos em julho e ninguém conseguiu
chamar nenhum deles.** Não é um argumento de venda inventado — é o registro da
tabela `company_events`.

---

## 2. A virada: isso não é cobrança, é entrega

O bloqueio conhecido é que cobrar ex-cliente trava. Então o fluxo não cobra.

O perfil **nunca saiu do ar**, está indexado e recebeu visita em julho. O que a
gente faz no primeiro contato é **entregar um ativo que já está rendendo** e que
hoje está no login errado. Isso é literalmente verdade, e inverte a conversa:

> Não é *"você parou de pagar"*.
> É *"isso aqui é teu, está funcionando, e está na minha conta por engano da migração"*.

A cobrança só aparece **depois do claim**, e nunca como resgate de dívida — como
a diferença entre ser achado e ser chamado. É a política do acervo virando
roteiro: **a página é o portal, o contato é o produto.**

---

## 3. A jornada

```
37 no acervo (conta do Lucio)
        │
        ▼
  [E0] O negócio ainda existe?  ──── não ──▶  EXCLUSÃO REAL
        │ sim
        ▼
  [E1] WhatsApp com o número de julho
        │
        ├── não respondeu ──────────▶ fica no acervo · novo lote em 30 dias
        ├── pediu pra sair ─────────▶ EXCLUSÃO REAL
        │ respondeu
        ▼
  [E2] Link de claim (&c=)
        │
        ├── não reivindicou ────────▶ fica no acervo · lote seguinte
        │ reivindicou
        ▼
  [E3] Conta própria · edita o perfil · vê o painel
        │
        ├── ativa (R$77,70) ────────▶ CLIENTE · selo + WhatsApp ligados
        │                              renova em 6m pelo botão do painel
        └── ainda não ──────────────▶ botão fica no painel
                                       régua de e-mail assume · volta pro E3
```

### E0 — Curadoria antes do contato (a etapa que ninguém pula)

Antes de mandar mensagem, confirmar que o negócio existe: o WhatsApp tem foto e
recado recente, o Google Maps mostra aberto, o Instagram postou nos últimos meses.

É rápido e evita dois desastres: mandar mensagem pra número morto (queima o
número do disparo) e manter no ar a página de um negócio que fechou — que é
exatamente o erro do concorrente aquitemnegocios: casca sem dono.

### E1 — O contato (WhatsApp, sempre)

Um lote por semana. Nunca dispara tudo de uma vez: mensagem em massa queima o
número e some com a taxa de resposta.

**Ordem dos lotes — não é alfabética, é por prova:**

| Lote | Quem | Por quê |
|---|---|---|
| **1** | os **7 com clique** em julho | alguém tentou chamar. É a prova mais forte que existe |
| **2** | os com **≥10 views** e nenhum clique | tráfego real, contato desligado |
| **3** | o resto que teve view | argumento mais fraco, mas existe |
| **4** | os **3 sem view nenhuma** | aqui a pergunta é se o negócio ainda existe |

**Lote 1 — nominal, começa por aqui:**

| Empresa | Views/jul | Tentativas de contato |
|---|---|---|
| **Casa do Pão Dona Nobre** | 63 | **15** (9 WhatsApp · 5 telefone · 1 Instagram) |
| Emporium JB Vida Saudável | 10 | 3 |
| MM Tintas | 12 | 1 |
| Mega Lojas Mosqueteiro (PG) | 5 | 1 |
| Fabi Marmitas Fit | 4 | 1 |
| START CELL Assistência Técnica | 4 | 1 |

A Casa do Pão sozinha teve **15 pessoas tentando falar com ela** pelo portal em
julho, de graça. Se existe uma primeira ligação pra fazer, é essa.

### E2 → E3 — Claim e ativação

O link de claim já existe e sai pronto do painel do vendedor (`agent-link` com
`company_id`, botão de copiar). Ele aponta pro perfil que **já existe** — sem
ele o dono cria um perfil novo e vazio e paga por ele, enquanto o de verdade,
com histórico e visualizações, fica órfão do lado.

Depois do claim o dono tem conta, edita o perfil, e o botão de R$77,70 passa a
existir no painel dele. **A partir daí a máquina assume** e o Lucio sai do meio.

---

## 4. Os scripts

### A — Quem teve clique (lote 1)

> Oi, aqui é o Lucio da Rede Baixada. A página da **[empresa]** no portal nunca
> saiu do ar — e em julho **[N] pessoas** abriram ela procurando vocês.
>
> **[X] delas tentaram falar com você por ali** e não conseguiram, porque o botão
> de contato fica desligado quando o perfil não está ativo.
>
> Tô passando os perfis pros donos, porque hoje o de vocês está no meu login e
> devia estar no de vocês. Te mando o link, você cria a senha em 1 minuto e a
> página é sua — edita foto, horário, o que quiser.

### B — Quem tem tráfego mas nenhum clique (lote 2 e 3)

> Oi, aqui é o Lucio da Rede Baixada. A página da **[empresa]** continua no ar e
> aparecendo no Google — em julho **[N] pessoas** abriram ela.
>
> Tô devolvendo os perfis pros donos. O de vocês ficou na minha conta desde a
> migração do site antigo. Te mando o link pra você criar a senha e assumir.

### C — Quem não teve view nenhuma (lote 4)

Aqui não existe número pra mostrar. O contato é de curadoria, não de venda:

> Oi, aqui é o Lucio da Rede Baixada. A **[empresa]** ainda está funcionando? Tô
> revisando os cadastros antigos do portal pra tirar do ar o que não existe mais
> e atualizar o que continua.

Quem responde "estou funcionando" acabou de se qualificar sozinho.

### D — Depois do claim, a conversa do contato

Só entra **depois** que a pessoa reivindicou. Nunca antes:

> Uma coisa que você vai notar no painel: das [N] pessoas que viram, nenhuma
> conseguiu te chamar direto — o botão de WhatsApp e o selo só ligam com o perfil
> ativo. São R$77,70 por 6 meses e liga na hora. **A página continua sua de
> qualquer jeito** — isso não muda.

### Objeções que já apareceram

| Objeção | Resposta |
|---|---|
| *"Não quero mais"* | *"Sem problema. Quer que eu tire a página do ar ou prefere deixar, já que ela aparece no Google de graça?"* — a maioria deixa. |
| *"Não uso, não dá retorno"* | O número de julho responde sozinho. Se o número for baixo, é lote 4: curadoria, não venda. |
| *"Já paguei isso antes"* | *"Pagou, e a página nunca saiu do ar por causa disso — é por isso que ela ainda tem visita hoje."* |
| *"Quanto é?"* antes do claim | *"Pra assumir a página não é nada. Ativar o contato é R$77,70 por 6 meses, mas isso é depois, se você quiser."* |

---

## 5. A régua da exclusão (as "anulações reais")

A política do 1º ano diz que perfil de negócio **constatado real** nunca sai do
ar. Isso não é o mesmo que "nunca se apaga nada". A régua:

**EXCLUIR:**
- negócio **encerrado / não existe mais** (confirmado, não presumido)
- o dono **pediu** pra sair
- duplicata do mesmo negócio

**NÃO EXCLUIR:**
- não respondeu o WhatsApp
- respondeu e não quis pagar
- tem pouca visita

Manter no ar a página de um negócio morto é o passivo reputacional que a gente
já identificou no concorrente. Tirar do ar quem só não pagou é destruir o acervo
que sustenta o SEO. **São coisas opostas e a régua precisa separar as duas.**

⚠️ Excluir do banco **não desindexa** do Google. Quem sai precisa sair pelo
caminho do `noindex` (o mesmo do `hidden`/`expired`), senão a URL vira 404 e o
domínio acumula erro.

---

## 6. Alamedas — o hub que a rua constrói sozinha

Testei a ideia contra o banco: **funciona, e já tem três prontas.**

52 das 55 empresas têm endereço e 51 têm coordenada. Aplicando a mesma régua
anti-thin dos hubs (≥3 perfis):

### Av. Monteiro Lobato — Mongaguá · **9 empresas**

Serralheria Pai e Filho · Flora Raiz São José · Jupyara Imóveis · Du Queijo ·
GAF Embalagens · Monitex Cama Mesa e Banho · SOS Reparos Hidráulicos ·
MD Material para Construção · Centro de Treinamento Rodrigo Almeida

**Sete categorias diferentes na mesma via.** É exatamente o que um hub de rua
faz e um hub de categoria não faz: quem procura "loja na Monteiro Lobato" não
está pensando em categoria. É a Times Square de Mongaguá.

### Rua João Mariano Ferreira — Itanhaém · **4 empresas**

Salão Belle Concept · Gorks Auto Center · Roger Motos · Gonzaga Projetores

**Três das quatro são vendas de julho.** Essa alameda não existia em 30/06 — ela
nasceu do porta a porta. É a prova de que a rua gera cluster.

### Av. Nossa Senhora de Fátima — Mongaguá · **4 empresas**

Mega Loja Mosqueteiros · MM Tintas · Papelaria e Aviamentos N.S. de Fátima ·
Panela Velha

### E mais 7 vias com 2 empresas — a uma visita do gate

Esse é o achado operacional: **cada visita numa rua que já tem 2 perfis cria uma
página nova indexável.** A rota de caminhada e a estratégia de SEO viram a mesma
decisão. Bater perna na Monteiro Lobato deixa de ser "vender pra mais um" e vira
"adensar um hub que já existe".

### O que falta pra construir

O `companies.address` é **texto livre**, e está sujo: tem registro com duas
avenidas no mesmo campo, "Av: Nossa Senhora de Fátima" e "Nossa Sra. de Fátima"
como se fossem vias diferentes, espaço sobrando no início.

Então a alameda precisa de um passo de dado antes do passo de página:

1. **Campo de logradouro normalizado** — como já existe pra bairro
   (`neighborhoods`), com uma tabela `streets` ou coluna normalizada
2. **Backfill com curadoria** — parser resolve a maioria, olho humano resolve os
   casos duplos (são poucos: 52 endereços)
3. **Só então** a rota `/empresas/{cidade}/rua/{via}`, com o mesmo gate ≥3 e o
   mesmo pacote de schema dos hubs atuais

Enquanto o logradouro for texto livre, hub de alameda gera página errada — e
página errada indexada é pior que página nenhuma.

---

## 7. Matérias

O blog tem motor pronto e **1 post**. A alameda resolve a pauta:

- **Uma matéria por alameda** — "Os 9 negócios da Av. Monteiro Lobato" — que
  linka pro hub da alameda, que linka pros 9 perfis. Post → hub → perfil, que é
  exatamente o encadeamento que o plano de SEO desenhou.
- **Uma matéria por recadastramento com história** — negócio de 13 anos que
  voltou. É conteúdo evergreen e é prova social ao mesmo tempo.
- A matéria também é a **desculpa de contato**: *"vou escrever sobre a Monteiro
  Lobato e a [empresa] vai estar"* abre porta que preço não abre.

---

## 8. Os que ainda não estão no sistema (WordPress + Facebook)

Faltam ~25 do WordPress, e tem a lista antiga do Facebook, de até 13 anos.

⚠️ **Aqui mora a única armadilha grave deste plano.** A diretriz de 19/07 matou
"popular em massa" porque casca sem dono é passivo reputacional — o erro exato
do concorrente. Uma lista de 13 anos atrás importada em lote seria isso.

A trava é a que tu mesmo já enunciou ao pedir *"recadastramento real com visitas
reais"*: **só entra no sistema negócio constatado vivo** — por visita, ligação
ou WhatsApp respondido. A ordem é constatar → cadastrar → claim, nunca
cadastrar → torcer.

Na prática, a lista do Facebook não é uma lista de perfis a criar: é uma **lista
de portas a bater**, e ela é ótima nisso — são negócios que já conheceram a
marca. Cruzar essa lista com as alamedas dá a rota: quem daquela lista está numa
via que já tem 2 perfis vai primeiro.

---

## 9. Ordem de execução

| # | O quê | Depende de |
|---|---|---|
| 1 | **Botão de R$77,70 no painel** (18 empresas com conta) | decidido, pronto pra construir |
| 2 | **Nome do contato** no cadastro + rótulo do botão da oferta | mesmo deploy do item 1 |
| 3 | **Lote 1 da reconquista** — os 7 com clique, começando pela Casa do Pão | nada; dá pra rodar hoje |
| 4 | **Curadoria + lotes 2 a 4**, um por semana | item 3 rodado |
| 5 | **Logradouro normalizado** + backfill dos 52 endereços | nada |
| 6 | **Hub de alameda** + as 3 primeiras páginas | item 5 |
| 7 | **Matéria da Monteiro Lobato** | item 6 |

Os itens 1–4 não dependem dos 5–7: a reconquista roda enquanto a alameda é
construída.

### Como saber se funcionou (30 dias)

- **claim ≥ 10–15%** dos contatados — abaixo disso o problema é a mensagem, não a base
- **≥ 5 ativações** vindas de recadastramento
- **≥ 3 alamedas** no ar com ≥3 perfis cada
- quantos negócios foram **confirmados encerrados** — é resultado tão válido
  quanto venda, porque limpa o acervo

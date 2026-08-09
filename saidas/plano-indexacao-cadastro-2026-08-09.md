# A fase de cadastramento e indexação — 09/08/2026

> Números lidos do banco de produção e do sitemap no ar. O ranking de categorias
> vem de pesquisa externa, com o nível de evidência declarado em cada linha.
> **Regra que rege tudo:** a PÁGINA é o portal, o CONTATO é o produto.

---

## 1. Onde a máquina está hoje

| Número | Valor | Leitura |
|---|---|---|
| URLs no sitemap | **92** (era 87 em 06/08) | acumulando sozinho |
| Empresas aprovadas | **63** | +4 desde 06/08 |
| **Páginas de hub** | **11** | 8 de categoria + **3 de cidade** |
| Hubs represados | **0** | os 8 cadastrados estão todos publicados |

**Descoberta que muda a alavanca:** não existe hub esperando aprovação de texto.
Os 8 que existem são exatamente os 8 pares que passam do gate de ≥3 perfis vivos.
Para ter página nova, precisa de **cadastro novo** — é a rua que destrava o Google.

⚠️ **O hub de cidade depende do hub de categoria.** O sitemap só publica
`/empresas/<cidade>` se aquela cidade tiver ao menos um guia vivo. Praia Grande
tem 4 empresas e **nenhuma** página, por isso.

---

## 2. Se os 5 forem preenchidos: 11 → 16. Com a recategorização, 17.

| Cenário | Categoria | Cidade | **Total** |
|---|---|---|---|
| Hoje | 8 | 3 | **11** |
| Só recategorizar Itanhaém | 10 | 3 | **13** |
| Só os 5 cadastros | 13 | 3 | **16** |
| **Os dois juntos** | **14** | **3** | **17** |

> 🎁 **Praia Grande/Serviços vale por dois:** é o único cadastro que acende o hub
> da categoria **e** o hub da cidade de Praia Grande ao mesmo tempo.

---

## 3. O ranking de categorias — o que o Google realmente quer

⚠️ **Aviso metodológico honesto:** não existe ranking público confiável de volume
de busca por categoria no Brasil. Volume real exige ferramenta paga (Keyword
Planner, Ahrefs). Quem entregar tabela numerada está inventando. Abaixo, cada
linha vem com o nível de evidência.

| Categoria | Evidência | O que sustenta |
|---|---|---|
| **Alimentação** | 🟢 medido | "restaurantes próximos de mim" **+210%** no Brasil (Think with Google); nº1 em "perto de mim" no mundo; maior nº de visualizações no Google Meu Negócio (~2.520/mês, BrightLocal) |
| **Saúde** | 🟡 indício | "dentista perto de mim" ~40,5 mil buscas/mês (fonte secundária — ordem de grandeza) |
| **Beleza** | 🟡 indício | Recorrente e hiperlocal: ninguém atravessa cidade pra cortar cabelo |
| **Manutenção** | 🟡 indício | Eletricista, encanador, chaveiro — urgente, sem fidelidade de marca |
| **Automóveis** | 🟡 indício | Borracharia, oficina, guincho — urgência + trânsito de veraneio |
| **Pet & Veterinário** | 🟠 inferência | Recorrente e emocionalmente urgente |
| **Imóveis** | 🟢 medido (sazonal) | Temporada da Baixada **+50–80%**; ~125 mil imóveis de temporada na região |

**Baixo potencial de busca local:** Marketing Digital (busca-se nacionalmente,
não "perto de mim"), Educação, Eventos, Construção.

### 🔴 "Serviços" e "Comércio" não estão em nenhum tier
São as suas **duas maiores categorias** — e ninguém digita "comércio em Mongaguá".
Elas são grandes por **erro de cadastro**, não por demanda. Isso reforça a
recategorização do item 5.

---

## 4. 🥊 O buraco na armadura do concorrente (conferido no sitemap dele)

**aquitemnegocios.com.br: 16.826 URLs e ZERO páginas de cidade×categoria.**

Ele tem 89 páginas de categoria **nacionais** — a dele se chama literalmente
*"Restaurante | Guia de Empresas **Brasil**"*. Está brigando por "restaurante" no
Brasil inteiro, onde não tem chance, em vez de "restaurante em Santos", onde teria.

👉 **A página que falta nele, você já tem.** `/empresas/mongagua/restaurantes`
existe. **Sua arquitetura está certa e a dele está errada** — com 21 mil perfis
contra 63. A jogada não é copiá-lo: é replicar o padrão que você já tem em mais
pares antes que ele perceba.

**Presença dele na Baixada** (contagem no sitemap — corrige a estimativa anterior,
que dizia que ele estava ausente do litoral sul):

| Cidade | Perfis dele |
|---|---|
| Santos | 484 |
| Praia Grande | 458 |
| São Vicente | 352 |
| Guarujá | 337 |
| Cubatão | 220 |
| **Itanhaém** | **141** |
| **Peruíbe** | **115** |
| **Mongaguá** | **104** |

Ele **está** no litoral sul. Não é campo vazio — é campo onde ele é fraco (1/4 da
massa de Santos) e onde você tem presença física e 13 anos de marca.

O blog dele (~109 posts, quase todos "guia de [categoria] em [cidade]") entrega o
que ele acha que converte: farmácia, borracharia, oficina mecânica, supermercado,
encanador, chaveiro, energia solar, vidraçaria. **Ele sabe que cidade×categoria é
o caminho — mas só faz isso no blog, não na estrutura do site.**

---

## 5. A ordem de ataque (cruzando fila real × ranking de busca)

### 🥇 Prioridade 1 — os 5 a um cadastro, nesta ordem

| # | Alvo | Tier | Já tem no portal | Que porta bater |
|---|---|---|---|---|
| 1 | **Praia Grande / Serviços** | — | Grow Beach · WL Advogados | **vale 2 páginas** (abre a cidade). Qualquer prestador: contador, gráfica, dedetizadora |
| 2 | **Itanhaém / Saúde** | 🟡 alto | Acquarius · Centro Aquático | clínica, dentista, fisioterapeuta, psicólogo |
| 3 | **Mongaguá / Pet** | 🟠 médio | Casa de ração Bryan · Agro Fenix | pet shop com banho e tosa, ou veterinário |
| 4 | **Mongaguá / Imóveis** | 🟢 sazonal | Jupyara · Daiane Goulart | imobiliária — **ver alerta de calendário** |
| 5 | **Itanhaém / Comércio** | 🔻 fraco | Cheiro do Belém · Magia Divina | genérica: menos valiosa que as de cima |

### ⏰ ALERTA DE CALENDÁRIO — Imóveis
Temporada é **sazonal e precisa estar indexado ANTES do verão**. Página de
imobiliária de temporada escrita em dezembro chega tarde: o Google leva semanas
pra indexar e rankear. **Alvo: no ar em setembro/outubro.**

### 🥈 Prioridade 2 — os 4 a dois cadastros
- **Peruíbe / Serviços** (tem 1) — **o mais alavancado da lista**: 2 cadastros
  abrem uma cidade inteira (categoria + cidade), onde ele tem 115 perfis e você 1.
- **Itanhaém / Beleza** (tem 1) — tier 🟡, e Beleza já provou volume em Mongaguá (5).
- Praia Grande / Automóveis (tem 1) — tier 🟡.
- Praia Grande / Comércio (tem 1) — genérica, baixa prioridade.

### 🥉 Prioridade 3 — as categorias que faltam INTEIRAS
Nenhuma cidade tem hub de **Alimentação** fora de Mongaguá — e Alimentação é a
única categoria 🟢 **medida** do ranking. Restaurante em Itanhaém e em Praia
Grande é a categoria de maior busca comprovada e você tem **zero** perfis nas duas.
**3 restaurantes em Itanhaém = 1 hub na categoria mais buscada que existe.**

Mesma lógica para **Manutenção** (eletricista/encanador/chaveiro): tier 🟡 e
**zero hubs em qualquer cidade**.

---

## 6. Recategorizar Itanhaém — 15 min, +2 hubs, custo zero

**10 das 15 empresas de Itanhaém** estão em "Serviços". Recategorizando 7:

| Empresa | Hoje | Deveria ser |
|---|---|---|
| Kumon Itanhaém | Serviços | **Educação** |
| Gorks auto center | Serviços | **Automóveis** |
| Roger motos | Serviços | **Automóveis** |
| Lava rápido Giovani | Serviços | **Automóveis** |
| W & M Eventos | Serviços | **Eventos** |
| Old Floricultura | Serviços | **Casa & Jardim** ⏳ |
| Floricultura Anny | Serviços | **Casa & Jardim** ⏳ |

**Conta simulada (não estimada):** Itanhaém sai de **1 hub para 3**. Serviços cai
pra exatamente 3 (segura no gate por um fio), **Automóveis nasce com 3**, Comércio
sobe pra 4.

⏳ **Decisão pendente:** as floriculturas vão pra **Casa & Jardim** ou **Comércio**?
Com o ranking na mesa, **Casa & Jardim ficou mais defensável** — "floricultura" e
"jardinagem" têm busca própria; "comércio" não tem nenhuma.

---

## 7. O que trava e não é código

**O Search Console.** Nenhuma das 92 URLs pode ser confirmada como indexada sem
ele. A meta combinada (≥70% indexado em 30 dias, contada de 27/07) **vence em
26/08** e ninguém está medindo. É acesso, não desenvolvimento.

---

## 8. Ordem recomendada

1. ✅ **Fotos destravadas** — feito em 09/08 (`1c9980d`), **já validado na prática**:
   a Smart Hair foi salva com logo, capa e descrição às 18h52.
2. **Recategorizar as 7 de Itanhaém** — 15 min, +2 hubs, custo zero.
3. **Search Console** — submeter o sitemap e ler o que já indexou.
4. **Os 5 cadastros cirúrgicos** — na ordem do item 5.
5. **Restaurantes em Itanhaém/Praia Grande** — a categoria 🟢 medida onde você tem zero.
6. Escrever os textos dos hubs novos (intro + FAQ — é o gate anti-thin).

**Projeção honesta:** 11 → 17 páginas sem uma linha de código nova, e com um
caminho claro pra 20+ atacando Alimentação e Manutenção.

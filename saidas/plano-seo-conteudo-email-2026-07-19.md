# Plano SEO + Conteúdo + E-mail + Conversão — Rede Baixada

> Criado em 19/07/2026. Nasce da mesa estratégica das frentes de cadastro + da análise do
> concorrente aquitemnegocios (`analise-aquitemnegocios-2026-07-19.md`). Objetivo: transformar
> o portal numa **máquina de tráfego local** que alimenta a venda — o oposto do dump morto do
> concorrente. Base técnica: React + Supabase (controle total; fim da limitação do WordPress).

---

## 🎯 A tese em uma frase

**Conteúdo e páginas de hub trazem o visitante de graça pelo Google; o visitante cai num perfil
REAL; o perfil vira "93 pessoas viram sua página" — a prova que fecha a venda na rua.**

O concorrente não roda esse loop: as páginas de categoria dele estão **vazias** e os perfis são
**casca**. A nossa vantagem não é volume — é **páginas cheias e perfis vivos**. Curadoria vence
raspagem no único juiz que importa: o Google servindo quem busca em Mongaguá.

---

## 🧱 As 4 camadas

### Camada 1 — O HUB de páginas (SEO estrutural / programático)
As páginas que respondem à busca de dinheiro. É o que o concorrente tem oco e a gente vai ter cheio.

- **Estrutura de URL** (definir na Fase 1, proposta):
  - `/[cidade]` — hub da cidade (ex: `/mongagua`)
  - `/[cidade]/[categoria]` — ex: `/mongagua/restaurantes` ← **a página que ranqueia**
  - `/[cidade]/[bairro]` — ex: `/mongagua/centro` (quando houver densidade)
- **Cada página precisa de** (senão o Google trata como thin/duplicate — o erro deles):
  - H1 com local ("Restaurantes em Mongaguá")
  - **Parágrafo de introdução ÚNICO** por página (não boilerplate repetido — texto com sabor
    local; pode ser IA-assistido, mas revisado)
  - A **lista de perfis reais** (o corpo — nunca "nenhum resultado")
  - **Links internos** pros perfis e pras páginas irmãs (categoria↔bairro↔cidade)
  - **Schema LocalBusiness / ItemList** (dados estruturados) + meta/OG corretos
  - Entrada no **sitemap** (geração automática já existe no portal)
- **Regra de ouro:** página só entra no ar/sitemap **quando tem pelo menos ~3–5 perfis reais**.
  Página vazia é lixo que derruba o domínio. Melhor 8 categorias cheias que 60 vazias.

### Camada 2 — Hidratação (o que enche o hub)
- **Dados:** o **acervo curado** — perfis reais, dado limpo, cidade por cidade. Mongaguá primeiro
  (é o nosso centro e a periferia deles). NÃO raspar: curadoria é o diferencial.
- **Trilho certo:** perfil de acervo nasce `active`/`listed` — **fica na busca pra sempre** (só
  perde selo/WhatsApp se não pagar). É a camada de SEO que NÃO some. O trilho **rua** (some em 7d)
  é venda, não SEO — ver diretriz em `_memoria/estrategia.md`.
- **Conteúdo:** o blog (Camada 3) aponta pras páginas de hub (link interno = autoridade).

### Camada 3 — O BLOG (`redebaixada.com.br/blog`, DENTRO do portal)
Subdiretório do domínio principal (concentra autoridade no domínio de 2013 — vantagem sobre o
domínio deles de nov/2025). **Três correntes de conteúdo:**

| Corrente | O que é | Serve pra | SEO |
|---|---|---|---|
| **Evergreen** (80%) | Guias: "melhores restaurantes de Mongaguá", "onde consertar celular em PG" | Fundação de SEO — ranqueia por meses/anos | 🟢 Alto e durável |
| **Hype / news urgente** (20%) | Evento do momento, o que rola no fim de semana | Combustível de e-mail e redes; tráfego pico | 🟡 Curto (exceção: evento recorrente vira página fixa anual) |
| **Notícias / fatos** | Abertura de negócio, novidade do bairro (matéria de rua com FOTO real) | Hiperlocal que ninguém copia; toque de venda | 🟢 Médio + engajamento |
| **Patrocinado** | Terceiro paga por post + backlink (publieditorial) | **Receita nova** | ⚠️ ver guarda-chuva abaixo |

- **Cadência sustentável:** ~1–2 evergreen/semana + hype quando acontece. Constância > surto.
- **Técnico:** tabela `blog_posts` no Supabase, rota `/blog` + `/blog/[slug]`, fluxo
  `draft → published` (as skills `/publicar-tema` e `/aprovar-post` já preveem isso — hoje
  apontam pra um `site/` separado que não existe; religar pro portal), OG por post, sitemap.

### Camada 4 — E-MAIL (dois motores, domínios separados)
| Motor | Papel | Volume | Domínio |
|---|---|---|---|
| **Resend** | **Transacional** (ciclo de vida: boas-vindas, cobrança, recibo) | 100/dia · 3.000/mês (grátis) — sobra pro transacional hoje | remetente atual verificado (ex: `contato@redebaixada.com.br`) |
| **Brevo** | **Marketing** (newsletter, campanhas, reconquista em massa) | conta compartilhada (UniMasso/Holos Connect), praticamente ilimitada | **SUBDOMÍNIO/DOMÍNIO SEPARADO** (ex: `news@` ou `mkt.redebaixada.com.br`) |

- ⚠️ **Nunca disparar marketing do remetente transacional.** Reputação de marketing (aberturas
  baixas, descadastros) contamina a entrega da cobrança. Domínios separados protegem os dois.
  Isso é exatamente o que o comentário do Brevo no código já antecipava.
- **Newsletter "O que rolou na Baixada"** (semanal, via Brevo): aqui o **hype brilha** — conteúdo
  do momento + 1 parceiro em destaque por edição + links de volta pro blog/diretório.
- **Segmentar:** parceiro (dono de negócio) ≠ consumidor.
- **Verificação DNS do domínio de marketing no Brevo** (SPF/DKIM/DMARC) antes do 1º disparo.

---

## 💰 Camada de monetização (backlinks patrocinados) + O GUARDA-CHUVA CRÍTICO

Vender post/backlink pra terceiro é receita legítima (publieditorial — mídia local vive disso). MAS:

> ⚠️ **TODO link pago DEVE ter `rel="sponsored"` (ou `rel="nofollow"`).** Vender link "dofollow"
> sem marcar viola a política do Google e pode gerar **penalidade manual que derruba o domínio
> inteiro** — justamente o ativo de SEO que estamos construindo. Isso não é opcional nem
> negociável. O post patrocinado também deve ser **rotulado como "Publicidade/Patrocinado"** na
> página (transparência + lei). Com o `rel` certo, vender backlink é seguro e escala; sem ele, é
> uma bomba-relógio no domínio.

Preço/pacote decidimos depois. O guarda-chuva técnico é o que precisa estar certo desde o post nº 1.

---

## 🗺️ Faseamento (respeitando o foco: a rua não pode parar)

**Quem faz o quê é a chave anti-fragmentação:** o **build é do Claude** (dev), a **matéria-prima
é da rua do Lucio** (observações + fotos, que ele já coleta). O Lucio não vira gargalo de dev.

- **FASE 0 — AGORA, custo zero (esta semana):**
  - Ligar o **banco de conteúdo de rua**: cada acontecimento/abertura/evento vira nota + foto no
    celular. Vira estoque de matéria pronto pra quando o blog existir.
  - **Acoplar no discurso de venda diariamente** (pedido do Lucio): usar o que vê na rua como
    gancho de conversa e prova de que a RB é daqui.
  - Definir a **lista de palavras-chave locais** (Mongaguá primeiro) e a **estrutura de URL** do hub.

- **FASE 1 — O HUB (maior ROI de SEO; ataca a brecha exata do concorrente):**
  - Popular o **acervo de Mongaguá** com curadoria (dado limpo).
  - Construir os **templates** de página cidade/categoria/bairro (com texto único + schema + sitemap).
  - Publicar só as páginas que já têm ≥3–5 perfis.

- **FASE 2 — O BLOG:** tabela `blog_posts` + rota `/blog` + religar `/publicar-tema` e
  `/aprovar-post` pro portal + primeiros 5 evergreen de Mongaguá (do banco da Fase 0).

- **FASE 3 — E-MAIL MARKETING (Brevo):** verificar domínio separado + montar a newsletter
  "O que rolou na Baixada" + segmentos.

- **FASE 4 — MONETIZAÇÃO:** pacote de post patrocinado **com `rel="sponsored"`** + rótulo de
  publicidade. Só depois do blog ter audiência que justifique cobrar.

---

## 🚧 Riscos e guarda-chuvas (não redescobrir na dor)

1. **`rel="sponsored"` em todo link pago** — penalidade de domínio se ignorar. (Camada 4)
2. **Thin/duplicate content** — cada página de hub precisa de texto ÚNICO e de perfis reais;
   página vazia derruba o domínio (o erro do concorrente). (Camada 1)
3. **Deliverability** — Resend (transacional) e Brevo (marketing) em domínios/subdomínios
   separados, cada um com DNS verificado. (Camada 4)
4. **Foco** — o blog é ativo de mês 2+; não pode puxar o Lucio da rua/cartões/reconquista. O dev
   é do Claude; o Lucio só alimenta com matéria de rua (custo ~zero de atenção).
5. **Cadência** — constância mata volume. 1 bom post/semana sustentável > 10 num surto e silêncio.

---

## ✅ Primeiros passos concretos

1. **Hoje:** ativar o banco de conteúdo de rua (nota + foto por acontecimento) e usar no discurso.
2. **Fase 1, passo 1:** lista de palavras-chave locais de Mongaguá + estrutura de URL do hub
   (decisão de ~30 min, faço a proposta).
3. **Fase 1, passo 2:** curar o acervo de Mongaguá (quais categorias têm ≥3–5 negócios reais).
4. Daí seguimos camada por camada. Cada fase é um sprint fechado, testado em preview antes da `main`.

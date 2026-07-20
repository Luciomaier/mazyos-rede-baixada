# Spec Fase 1 — Hub de páginas SEO (cidade × categoria) de Mongaguá

> Gerado em 19/07/2026 por workflow (keywords + desmonte do concorrente + boas práticas +
> auditoria do código/dados). Pronto pra construir. Base do plano:
> `plano-seo-conteudo-email-2026-07-19.md`. Concorrente: `analise-aquitemnegocios-2026-07-19.md`.

## 🔗 Estrutura de URL — DECIDIDA

`/empresas/{cidade-sem-acento}/{categoria-keyword}`
Ex: `/empresas/mongagua/restaurantes` · `/empresas/mongagua/salao-de-beleza` · `/empresas/mongagua/materiais-de-construcao`

**Porquê:** (1) subdiretório no domínio raiz consolida a autoridade (nunca subdomínio); (2) é
**exatamente a rota que o concorrente já tem indexada e VAZIA** — publicar a mesma forma **cheia**
canibaliza a busca dele no dia 1; (3) o prefixo `/empresas` isola do catch-all do SPA (uma raiz
`/mongagua/...` colidiria com `/planos`, `/login`); (4) reusa o template que já existe e funciona
(`/vitrine/:citySlug/:categorySlug`). **Bairro NÃO vira URL na Fase 1** (nenhum bairro×categoria
chega a 3 perfis) — fica como âncora `#centro` dentro do hub de cidade. PG/Itanhaém = Fase 2.

## 📊 Densidade real em Mongaguá (36 perfis auditados) e lote 1

| Ordem | Categoria | Perfis | Hub (H1) | Prioridade |
|---|---|---|---|---|
| 1 | Alimentação | 6 | Restaurantes e delivery em Mongaguá | 🔥 head-term altíssimo + dobra como lista de venda |
| 2 | Beleza | 4 | Salões de beleza e estética em Mongaguá | Alta — muito microempreendedor; é onde o concorrente tem o título quebrado |
| 3 | Construção | 3 | Materiais de construção em Mongaguá | Alta (ticket alto) — **no piso do gate**, monitorar |
| 4 | Saúde | 4 | Clínicas e profissionais de saúde em Mongaguá | Média — Doctoralia domina a busca profissional |
| 5 | Serviços | 8 | Serviços e assistência em Mongaguá | Maior densidade; âncora de link interno; **auditar** p/ split (oficina/ar-cond.) |
| 6 | Comércio | 6 | Lojas e comércio em Mongaguá | Média — **auditar** p/ split (pet shop/roupas) |
| 7 | Casa & Jardim | 3 | Casa e jardim em Mongaguá | Baixa — **no piso do gate**, por completude |

## 🧩 Template da página de hub

- **H1 único da variável real** (`hub_pages.h1`). ⚠️ **Se cidade OU categoria vier nula → não
  publica (noindex/404)** — mata o bug "Academia em Categoria" do concorrente. Sempre "Mongaguá"
  **com acento** no H1/title/breadcrumb (o concorrente exibe "Mongagua").
- **Breadcrumb visível** Início > Empresas > Mongaguá > Restaurantes (alimenta BreadcrumbList).
- **Intro editorial ÚNICA** (2–4 parágrafos, ~300+ palavras, boilerplate <40%): o que procurar,
  faixa de preço, bairros com mais opções, sazonalidade de verão.
- **Estatística local única**: "Mongaguá tem X restaurantes cadastrados na Rede Baixada, Y no Centro".
- **Lista dos perfis reais (≥3–5)** ordenados por is_featured + prioridade de plano; card com foto,
  bairro, horário, telefone, WhatsApp direto e link pro `/empresa/:slug`.
- **Âncoras de bairro** (`#centro`, `#agenor-de-campos`) — jump interno, nunca rota indexável.
- **FAQ local** (3–5 perguntas específicas) → schema FAQPage.
- **Bloco "Guias e leituras"**: 2–4 links pros posts de blog da mesma categoria — fecha o silo
  hub↔blog↔perfil.
- **Schema JSON-LD**: ItemList (todos os perfis visíveis) + BreadcrumbList + FAQPage +
  CollectionPage. **LocalBusiness fica só no perfil**, não aqui. Só marcar o que está visível.
- **Meta/OG**: title ≤60 ("Restaurantes em Mongaguá | Rede Baixada"), description curada ≤155,
  canonical próprio por hub, og/twitter.
- **GATE regra de ouro**: contar perfis vivos (approved + lifecycle visível); se <3 → noindex +
  fora do sitemap + 302 pro hub de cidade. **Nunca renderizar "nenhuma empresa" pro robô.**
- **Pré-render pro robô** (`api/hub-og.js`, espelhando `profile-og.js`): o HTML entregue já vem
  com H1/title/intro/perfis no source — o Google indexa a página **cheia**, nunca o estado vazio.

## 🛠️ Checklist técnico (ordem de construção)

1. **Corrigir o helper de slug** (bug já em produção — `Vitrine.tsx:31/117` gera `mongagu-`):
   `.normalize('NFD').replace(/[̀-ͯ]/g,'').toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/(^-|-$)/g,'')` → `mongagua`. **Antes de replicar.**
2. **Migration `hub_pages`** (city_slug, city_name, category_id FK, slug, h1, title_tag,
   meta_description, intro_md, faq_json, is_published, updated_at) + RLS público. É a fonte única
   do texto único + mapeamento slug↔categoria (o schema hoje **não tem nenhum campo de SEO**).
   Seed dos 7 hubs.
3. **Rota** `/empresas/:citySlug/:categorySlug` → componente `HubEmpresas` (espelha `Vitrine.tsx`).
4. **Componente `HubEmpresas`** com o template completo + guarda de variável.
5. **`<SEO>`** com canonical segmentado (resolve o canonical fixo `/empresas` de `Companies.tsx:115`).
6. **Schema**: criar `BreadcrumbListSchema` + estender `CompanyListSchema` (ItemList já existe) + FAQ.
7. **Gate**: helper único `countLiveCompanies(city, category_id)` usado no render E no sitemap.
8. **`api/hub-og.js`** (pré-render) + rewrite no `vercel.json`.
9. **Estender `generate-sitemap`**: emitir `/empresas/{city}/{cat}` só quando count≥3, com lastmod.
10. **Validar** no Rich Results Test + submeter sitemap no Search Console. **Meta: ≥70% indexado
    em 30 dias antes de escalar; se <50%, parar e melhorar densidade/texto.**

## 📝 As 5 primeiras páginas
1. `/empresas/mongagua/restaurantes` — Restaurantes e delivery em Mongaguá (6)
2. `/empresas/mongagua/salao-de-beleza` — Salões de beleza e estética em Mongaguá (4)
3. `/empresas/mongagua/materiais-de-construcao` — Materiais de construção em Mongaguá (3, no piso)
4. `/empresas/mongagua/saude` — Clínicas e profissionais de saúde em Mongaguá (4)
5. `/empresas/mongagua/servicos` — Serviços e assistência em Mongaguá (8, âncora interna)

## ✍️ Os 5 primeiros posts de blog (apontam pro hub)
1. "Onde comer em Mongaguá: os melhores restaurantes e delivery da cidade" → `/restaurantes`
2. "Salão de beleza em Mongaguá: onde cuidar do visual no Centro e em Agenor de Campos" → `/salao-de-beleza`
3. "Vai reformar na praia? Onde comprar material de construção em Mongaguá" → `/materiais-de-construcao`
4. "Guia de saúde em Mongaguá: clínicas, dentistas e onde se cuidar perto de casa" → `/saude`
5. "Chegou o verão: serviços de casa em Mongaguá (ar-condicionado, elétrica, encanador)" → `/servicos`

## 🤝 Decisões do Lucio
- **Confirmar a URL** `/empresas/mongagua/restaurantes` (recomendação decidida — seção-primeiro).
- **O texto único é o GARGALO da Fase 1**: quem escreve/aprova os 2–4 parágrafos + FAQ dos 7 hubs
  na voz vizinho/consultivo? (Claude pode rascunhar, Lucio revisa.) Sem isso, página não publica.
- **Auditar os buckets genéricos** "Serviços" (8) e "Comércio" (6): se houver ≥3 oficinas ou ≥3
  pet shops, spin-up de hub granular ("Oficinas mecânicas em Mongaguá") que casa com head-term forte.
- **🎯 Sinergia venda×SEO**: alinhar a lista de porta a porta R$77,70 com as micro-verticais do
  keyword research (pizzaria, hamburgueria, pet shop, oficina, academia, ar-condicionado,
  eletricista). **Vender nessas categorias fura o ≥3 e destrava hubs granulares** — SEO + venda no
  mesmo movimento.
- **Comportamento do gate <3**: noindex navegável OU 302 pro hub de cidade.
- **Confirmar foco 100% Mongaguá** na Fase 1 (PG/Itanhaém têm 2 perfis cada — nenhum hub viável).

## ⚠️ Riscos
- **Texto único é o risco crítico**: 7 hubs sem intro real = thin/duplicate → queda de core update
  (scaled content abuse, quedas de 60–80% em 2025/26). Página não publica sem os parágrafos + FAQ.
- **SPA sem SSR**: `api/hub-og.js` NÃO é opcional — sem ele o Google pode não ver a página cheia.
- **Bug de slug com acento já em produção** — corrigir o helper (NFD) antes de tudo.
- **Construção e Casa&Jardim estão exatamente em 3** (piso): uma empresa que expira derruba a
  página. Gate automático + monitoramento.
- **Head-terms genéricos** (Serviços, Comércio) captam pouca busca — priorizar head-term limpo
  (restaurantes, salão, materiais) e usar os genéricos como âncora até auditar/splitar.
- **Não escalar cedo**: piloto de 5–7 páginas, medir ≥70% indexado em 30 dias, só então escalar
  (bairro, cidade vizinha). Escalar antes = repetir o erro do concorrente ao contrário.

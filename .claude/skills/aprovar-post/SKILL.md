---
name: aprovar-post
description: >
  Aprova e publica um post da fila — sobe os PNGs do carrossel pro Storage, flipa o post de
  draft pra published na tabela blog_posts do portal (fica no ar na hora, sem deploy), e
  posta o carrossel no Instagram + Facebook via Meta Graph API. Use quando o
  usuário disser "aprovar post X", "publicar o post do tema Y", "/aprovar-post X", ou quando
  quiser disparar a publicação automática de um conteúdo já criado pela skill /publicar-tema.
---

# /aprovar-post — Pipeline de aprovação e publicação automática

Faz a ponte entre o conteúdo aprovado (blog + carrossel + legendas, criado por `/publicar-tema`)
e a publicação real no feed (site + Instagram + Facebook).

## Quando NÃO usar

- Conteúdo ainda não foi criado → use `/publicar-tema` primeiro
- Usuário ainda está revisando → não rodar até ele dizer "aprovado" / "pode postar"
- Site não está deployado / Meta API não configurada → seguir setup abaixo

## Pré-requisitos (uma vez só)

- `.env` na raiz com:
  - `META_PAGE_ACCESS_TOKEN` — token de longa duração da Página FB
  - `META_PAGE_ID` — ID da Página FB
  - `META_IG_USER_ID` — ID da conta Insta Business
  - `SITE_URL` — ex: `https://exemplo.com.br`
- Site com deploy automático a partir do `main` do GitHub (Netlify, Vercel, etc.)
- Conta Insta Business conectada à Página FB
- Página FB com permissões corretas no Meta App
- Scripts `scripts/postar-instagram.js` e `scripts/postar-facebook.js` configurados

Se algo disso faltar: parar e apontar pro guia de setup (criar `marketing/automacao-meta-setup.md` se ainda não existir).

## Argumento

`/aprovar-post <slug>` — onde `<slug>` é o `slug` da linha em `blog_posts`.

Exemplo: `/aprovar-post como-conservar-produto`

Se o usuário não passou slug, listar os posts em rascunho
(`GET /rest/v1/blog_posts?status=eq.draft` com sessão admin) e perguntar qual.

## Workflow

### Passo 1 — Localizar o post e as peças

- Blog: a linha em `blog_posts` com esse `slug` (Supabase `donaobtlwqrjmvjqflxz`). Ler com
  sessão **admin** — a RLS esconde rascunho do anon. **Não existe pasta `site/`**: o blog vive
  no portal, em `redebaixada.com.br/blog/<slug>`.
- Carrossel: procurar `marketing/conteudo/<slug>-*` (a pasta tem sufixo de data)
- Validar que existem PNGs em `<pasta-carrossel>/instagram/slide-XX.png` (2 a 10)
- Validar que existem `legenda.md` e `legenda-linkedin.md`

Se faltar qualquer um, parar e relatar.

### Passo 2 — Mostrar resumo + pedir confirmação final

Mostrar pro usuário:
- Título do blog
- Quantos slides do carrossel
- Primeiras 200 chars da legenda
- URL final que vai ser publicada

Perguntar: **"Confirma publicação? (sim/não)"**. Só seguir se ele disser sim.

### Passo 3 — Subir os PNGs do carrossel pro Storage

A Meta API busca a imagem por **URL pública** — por isso os slides sobem antes de publicar.

- Origem: `marketing/conteudo/<slug>-<data>/instagram/slide-*.png`
- Destino: bucket **`company-assets`**, pasta `blog/<slug>/slide-XX.png` (upsert, pra
  re-publicação sobrescrever)
- A URL pública fica `https://donaobtlwqrjmvjqflxz.supabase.co/storage/v1/object/public/company-assets/blog/<slug>/slide-01.png`

Se algum upload falhar, parar antes de publicar — post no ar sem carrossel é meio trabalho.

### Passo 4 — Publicar o post

```
PATCH /rest/v1/blog_posts?slug=eq.<slug>
{ "status": "published", "published_at": "<agora em ISO>" }
```

Com sessão admin. Se o post não tiver `cover_url`, usar a URL pública do `slide-01.png`.

**Não há commit nem deploy:** o portal lê do banco. A página fica no ar na hora, e o
`generate-sitemap` passa a emitir `/blog/<slug>` na próxima leitura do robô.

### Passo 5 — Conferir que está no ar

```bash
curl -sf -o /dev/null -w "%{http_code}" "https://redebaixada.com.br/blog/<slug>"
```

Aguardar HTTP 200 e conferir que o `<title>` do HTML é o do post (o `api/blog-og.js` injeta
title/description/OG server-side — é o que o robô e o WhatsApp leem).

⚠️ **Uma requisição por vez, sem rajada de `curl`** — rajada aciona a DDoS Mitigation da Vercel
contra o próprio IP e tudo vira 403.

### Passo 7 — Postar no Instagram

```bash
node --env-file=.env scripts/postar-instagram.js marketing/conteudo/<slug>-<data>
```

Capturar o post id retornado. Se falhar, **não seguir pra Facebook** — relatar e parar.

### Passo 8 — Postar no Facebook

```bash
node --env-file=.env scripts/postar-facebook.js marketing/conteudo/<slug>-<data>
```

Capturar o post id retornado.

### Passo 9 — LinkedIn

LinkedIn é manual por enquanto (API de empresa precisa de aprovação demorada). Mostrar pro usuário:

```
LinkedIn: cole esse texto manualmente em https://linkedin.com/in/<seu-perfil>:
<conteúdo de legenda-linkedin.md>
```

### Passo 10 — Resumo

Mostrar:
```
✓ Post publicado: <título>

Site:        https://redebaixada.com.br/blog/<slug>
Instagram:   <link do post>
Facebook:    <link do post>
LinkedIn:    pendente — texto pronto em legenda-linkedin.md (postar manual)
```

## Tratamento de erro

- Upload dos slides falhou: para ANTES de publicar (sem imagem pública a Meta API falha)
- PATCH de publicação falhou: relata e para — nada foi publicado
- Página não responde 200 em 2 min: rollback (`status: "draft"`), relata e para
- Insta API falhou: para e relata. O post já está no ar no portal — só o feed que não foi
- FB falhou mas Insta OK: relata, sugere tentar de novo só o FB depois

## Princípios

1. **Confirmação humana antes de qualquer coisa irreversível.** Nunca pular o passo 2.
2. **Idempotente onde possível.** Re-rodar com mesmo slug deve detectar publicação prévia (`status = published`, PNGs já no Storage) e perguntar se é pra re-postar ou só atualizar.
3. **Falha cedo, falha alto.** Qualquer pré-requisito faltando = abortar e explicar o que falta.
4. **Logar tudo.** Cada passo imprime o que está fazendo e o resultado.

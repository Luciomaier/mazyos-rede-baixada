# Search Console — o que falta fazer · atualizado 09/08/2026 (noite)

> **REVIRAVOLTA:** a propriedade `redebaixada.com.br` **JÁ EXISTE e está
> verificada** (tipo Domínio, via DNS — por isso não há tag no site), com dado
> acumulado desde **abril/2025**: 2,22 mil cliques · 223 mil impressões ·
> posição média 8. A conta dona parece ser a **redebaixada@gmail.com** (é a
> dona do export que você me mandou). Os passos de criar/verificar propriedade
> do guia anterior estão OBSOLETOS — sobrou o que está abaixo.

---

## O que EU já fiz com o dado que você mandou (09/08, no ar)

- **301 de `/litoral-sp/<slug>` → `/empresa/<slug>`** — a estrutura antiga do
  WordPress ainda concentrava **~40% dos cliques do site** (839 cliques, 52,9
  mil impressões em 75 URLs) caindo num soft-404. A página nº 1 do site inteiro
  era `/litoral-sp/casa-do-pao-dona-nobre/` (296 cliques). Agora a autoridade
  antiga escorre pros perfis vivos — e acaba a canibalização dos 66 slugs que
  rankeavam em dobro.
- **Taxonomias mortas do WP** (`/localizacao /especialidade /portfolio
  /categoria /tag`) → 301 pra `/empresas`.
- **`trailingSlash: false`** — com/sem barra final eram duas URLs duplicadas
  aos olhos do Google (39 casos no relatório); agora normaliza com 308.
- **Slug da MM Tintas consertado** (`-mm-tintas` → `mm-tintas`): o Google
  indexou a URL limpa e o perfil respondia só na torta. Mais 8 slugs com hífen
  nas pontas limpos, e o gerador de slug unificado pra não nascer mais torto.

## O que SÓ VOCÊ consegue fazer (nesta ordem)

### 1. Exportar o relatório de INDEXAÇÃO (o que você mandou era o de Desempenho)
Search Console → **Indexação → Páginas → Exportar** (botão no canto superior
direito) → Google Sheets → me manda o link. É esse que tem os **9 motivos das
821 não indexadas** — o de Desempenho que veio não traz essa tabela.

### 2. Submeter os DOIS sitemaps
**Indexação → Sitemaps** → adicionar um por vez:
- `sitemap.xml`
- `sitemap-dinamico.xml` (93 URLs, cresce sozinho)

Confere na mesma tela se já não há um sitemap velho do WordPress listado —
se houver (ex: `sitemap_index.xml` com erro), pode remover.

### 3. Pedir indexação das 12 que pagam a conta
**Inspeção de URL** (barra do topo) → colar → **"Solicitar indexação"**.
Limite ~10-12/dia = exatamente uma sessão:

```
https://redebaixada.com.br/
https://redebaixada.com.br/empresa/casa-do-pao-dona-nobre   ← herda o 301 da nº1
https://redebaixada.com.br/empresas/mongagua
https://redebaixada.com.br/empresas/itanhaem
https://redebaixada.com.br/empresas/itanhaem/automoveis
https://redebaixada.com.br/empresas/itanhaem/servicos
https://redebaixada.com.br/empresas/mongagua/restaurantes
https://redebaixada.com.br/empresas/mongagua/saude
https://redebaixada.com.br/empresas/mongagua/salao-de-beleza
https://redebaixada.com.br/empresas/mongagua/servicos
https://redebaixada.com.br/empresas/mongagua/lojas
https://redebaixada.com.br/empresas/mongagua/casa-e-jardim
```

### 4. 🔴 Consertar o www (é na VERCEL, 2 minutos, e está QUEBRADO)
`https://www.redebaixada.com.br` dá **erro de certificado** — o TLS não cobre
o subdomínio. Quem digita "www" vê aviso de segurança e não entra.
**Vercel → projeto redebaixada → Settings → Domains → Add** →
`www.redebaixada.com.br` → escolher "Redirect to redebaixada.com.br".
A Vercel emite o certificado sozinha.

### 5. Toda semana: olhar 2 números (2 min)
- **Indexação → Páginas**: indexadas ÷ total do sitemap (meta ≥70% até 26/08)
- **Desempenho**: cliques da semana — devem SUBIR nas próximas semanas com os
  301 consolidando a autoridade antiga nos perfis vivos.

---

## Por que a meta de 26/08 mudou de cara

O painel diz "57 indexadas / 821 não" — mas as 821 incluem centenas de URLs
mortas do WordPress que o Google está esquecendo (a curva cinza caindo).
O número honesto é **quantas das 93 do sitemap atual estão dentro** — e é o
export do passo 1 que responde isso. Enquanto isso, o relatório de Desempenho
prova que **498 páginas tiveram impressão** no período — o portal está longe
de ser invisível.

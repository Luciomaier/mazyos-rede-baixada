# Search Console — o passo a passo exato · agosto/2026

> **Por que isso importa:** é o ÚNICO lugar que diz o que o Google de fato
> indexou. Hoje temos 93 URLs no sitemap dinâmico + as fixas, e a meta
> combinada (≥70% indexado em 30 dias, contada de 27/07) **vence em 26/08**
> — está correndo sem ninguém medir. Só o dono do domínio consegue entrar.
> Tempo total: ~20 min, uma vez. Depois é olhar 1×/semana.

---

## Passo 1 — Entrar

Abrir **search.google.com/search-console** logado na conta Google que você
usa pro negócio (a `holos.site@gmail.com` serve — dá pra adicionar outras
pessoas depois em Configurações → Usuários).

## Passo 2 — Adicionar a propriedade (escolher UM dos dois caminhos)

**Caminho A — "Domínio" (recomendado):** digite `redebaixada.com.br`.
Cobre www, sem-www, http e https de uma vez. A verificação é um registro
**TXT no DNS** — o Google te dá um código tipo
`google-site-verification=abc123...` e você cola onde o domínio é
gerenciado (Registro.br ou painel da Vercel, onde estiver o DNS).
Propagação leva de minutos a algumas horas; aí clica **Verificar**.

**Caminho B — "Prefixo do URL" (mais fácil, sem mexer em DNS):** digite
`https://redebaixada.com.br`. Escolha o método **"Tag HTML"**: o Google
mostra uma linha `<meta name="google-site-verification" content="...">`.
👉 **Me manda só o código do `content` e eu coloco no site e faço deploy
em minutos** — aí você volta e clica Verificar. (Conferi: o site ainda
não tem nenhuma tag dessas, então esse passo é obrigatório.)

## Passo 3 — Submeter os DOIS sitemaps

Menu **Indexação → Sitemaps** → no campo "Adicionar novo sitemap", enviar
um de cada vez:

1. `sitemap.xml` — as páginas fixas (home, /empresas, /planos…)
2. `sitemap-dinamico.xml` — perfis + hubs + blog (**93 URLs, cresce sozinho**)

Os dois já estão no ar e apontados no robots.txt. Status esperado:
**"Êxito"** com a contagem de URLs descobertas.

⚠️ **Nunca** submeter a URL da função no `supabase.co` — sitemap de outro
domínio não vale (um comentário antigo no código mandava fazer isso;
já corrigi o comentário).

## Passo 4 — Furar a fila das páginas que pagam a conta

Barra de cima → **Inspeção de URL** → colar a URL → botão **"Solicitar
indexação"**. O limite é ~10–12 por dia, então esta lista é exatamente
uma sessão. Na ordem:

```
https://redebaixada.com.br/
https://redebaixada.com.br/empresas/mongagua
https://redebaixada.com.br/empresas/itanhaem
https://redebaixada.com.br/empresas/itanhaem/automoveis   ← a recém-nascida
https://redebaixada.com.br/empresas/itanhaem/servicos     ← texto reescrito hoje
https://redebaixada.com.br/empresas/mongagua/restaurantes
https://redebaixada.com.br/empresas/mongagua/saude
https://redebaixada.com.br/empresas/mongagua/salao-de-beleza
https://redebaixada.com.br/empresas/mongagua/servicos
https://redebaixada.com.br/empresas/mongagua/lojas
https://redebaixada.com.br/empresas/mongagua/casa-e-jardim
https://redebaixada.com.br/empresas/mongagua/materiais-de-construcao
```

## Passo 5 — Ler o veredito (o número da meta)

Menu **Indexação → Páginas**. É AQUI que mora a resposta que ninguém tem:

- **Indexadas** ÷ total ≥ 70% → a máquina está aprovada, pode escalar.
- **< 50%** → regra combinada: **parar de escalar e melhorar** antes.

Os motivos de "não indexada" que podem aparecer e o que significam pra nós:

| Motivo no relatório | Tradução | O que fazer |
|---|---|---|
| "Rastreada, mas não indexada no momento" | o Google viu e não achou digna AINDA | normal nas primeiras semanas; se persistir em hub, o texto precisa engordar |
| "Detectada, mas não rastreada" | está na fila, nem visitou | submeter o sitemap + pedir indexação (passos 3–4) resolve |
| "Excluída pela tag noindex" | nós mandamos não indexar | certo em /oferta-parceiro e perfis ocultos; **errado se aparecer num hub** — me avisa |
| "Página com redirecionamento" / "Duplicada" | URL antiga ou variação | em geral ignorar; me traz se for perfil vivo |

## Passo 6 — Daqui a alguns dias: o relatório Desempenho

Menu **Desempenho**: quais buscas mostram o portal, cliques e posição
média. É onde vamos medir a briga com o concorrente nas buscas de
dinheiro ("guia comercial mongaguá", "empresas em itanhaém",
"restaurante em mongaguá"...). Sem dado nos primeiros dias é normal.

---

## O que me trazer de volta (é o que destrava o resto)

1. **Os números de Indexação → Páginas**: quantas indexadas, quantas não,
   e os motivos listados (print serve).
2. Se escolheu o Caminho B: **o código da tag HTML** pra eu subir no site.
3. Qualquer aviso vermelho que aparecer — não resolve nada sozinho, só me traz.

Com isso eu: calculo a % real contra a meta de 26/08 · conserto qualquer
noindex errado · decido com você se escala (mais hubs) ou engorda o que existe.

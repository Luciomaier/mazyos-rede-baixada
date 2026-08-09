# A fase de cadastramento e indexação — 09/08/2026

> Estado real lido do banco e da produção hoje, não da memória.
> **Regra que rege tudo isto:** a PÁGINA é o portal, o CONTATO é o produto.

---

## 1. Onde a máquina está hoje

| Número | Valor | Leitura |
|---|---|---|
| URLs no sitemap | **92** (era 87 em 06/08) | acumulando sozinho, como projetado |
| Empresas aprovadas | **63** | +4 desde 06/08 |
| Hubs cadastrados | **8** | todos publicados — **não há nada represado** |
| Hubs de cidade | 2 (Mongaguá, Itanhaém) | Praia Grande não tem |

**Descoberta importante:** não existe hub esperando aprovação de texto. Os 8 que
existem são exatamente os 8 pares cidade×categoria que passam do gate de ≥3
perfis vivos. Para ter página nova, precisa **criar hub novo** — e para criar hub
novo, precisa do 3º cadastro naquele par.

---

## 2. A alavanca: 5 pares a UMA empresa de virar página

Cada um destes precisa de **um único cadastro** para nascer uma página indexável:

| Cidade | Categoria | Tem | Falta | Já no portal |
|---|---|---|---|---|
| Itanhaém | **Comércio** | 2 | **1** | Cheiro do Belém · Magia Divina |
| Itanhaém | **Saúde** | 2 | **1** | Centro Aquático Ideal · Acquarius |
| Praia Grande | **Serviços** | 2 | **1** | WL Advogados · Grow Beach |
| Mongaguá | **Pet & Veterinário** | 2 | **1** | — |
| Mongaguá | **Imóveis** | 2 | **1** | — |

> **É isto que transforma a rua em SEO.** Não é "mais uma venda": é uma página
> nova no Google, que passa a trabalhar de graça para sempre. Cinco cadastros
> escolhidos a dedo valem mais, em indexação, que vinte cadastros aleatórios.

**Rota sugerida (uma tarde):** um pet shop e uma imobiliária em Mongaguá, uma
loja e uma clínica em Itanhaém, um prestador em Praia Grande. **5 portas = 5
páginas novas.**

---

## 3. O desequilíbrio que ninguém tinha visto

| Cidade | Empresas | Hubs de categoria |
|---|---|---|
| Mongaguá | 43 | 7 |
| **Itanhaém** | **15** | **1** ← desproporcional |
| Praia Grande | 4 | 0 |
| Peruíbe | 1 | 0 |

Itanhaém tem 1/3 das empresas de Mongaguá e 1/7 das páginas. O motivo está no
item 4.

---

## 4. 🔴 "Serviços" virou lixeira — e isso custa busca

**10 das 15 empresas de Itanhaém** e **10 de Mongaguá** estão em "Serviços".
Existem **16 categorias** no portal, mas a genérica está absorvendo tudo.

O problema é de SEO puro: **ninguém busca "serviços em Itanhaém"**. As pessoas
buscam "floricultura em Itanhaém", "lava rápido em Itanhaém", "auto center".
Uma empresa na categoria errada é uma empresa que não aparece na busca que
importa — e uma página de hub que nunca nasce.

**Recategorizações óbvias (Itanhaém), só de olhar o nome:**

| Empresa | Hoje | Deveria ser |
|---|---|---|
| Kumon Itanhaém | Serviços | **Educação** |
| Gorks auto center | Serviços | **Automóveis** |
| Roger motos | Serviços | **Automóveis** |
| Lava rápido Giovani | Serviços | **Automóveis** |
| W & M Eventos | Serviços | **Eventos** |
| Old Floricultura | Serviços | **Comércio** ou Casa & Jardim |
| Floricultura Anny | Serviços | **Comércio** ou Casa & Jardim |

> ⚠️ **Efeito colateral a respeitar:** mexer nestas 7 derruba "Itanhaém/Serviços"
> de 10 para 3 — continua passando do gate, mas por pouco. Em compensação
> **acende Automóveis (3) na hora**, e leva Comércio de 2 para 4. Saldo: de
> 1 hub para 3 em Itanhaém, sem sair de casa.

**Decisão necessária do Lucio antes de eu mexer:** as duas floriculturas são
Comércio ou Casa & Jardim? (Casa & Jardim casa melhor com o que as pessoas
buscam para planta; Comércio é mais literal para "loja de flores".)

---

## 5. O que trava a indexação e não é código

**O Search Console.** Nenhuma das 92 URLs pode ser confirmada como indexada sem
ele. Não sabemos se o Google já rastreou os 8 hubs de 27/07 — e a meta combinada
(≥70% indexado em 30 dias) **está correndo sem ninguém medir**. Os 30 dias
venceram em 26/08.

Isso é acesso, não desenvolvimento: só o dono do domínio consegue.

---

## 6. Ordem recomendada

1. ✅ **Fotos destravadas** — feito hoje (`1c9980d`).
2. **Recategorizar as 7 de Itanhaém** — 15 min, +2 hubs, custo zero.
3. **Search Console** — submeter `sitemap-dinamico.xml` e ler o que já indexou.
4. **Os 5 cadastros cirúrgicos** — a rota de rua acima, +5 hubs.
5. Escrever os textos dos hubs novos (intro + FAQ; é o gate anti-thin).

**Projeção honesta:** 8 → 15 hubs sem nenhuma linha de código nova. O que muda
não é o portal — é quantas buscas ele responde.

# Rede Baixada — Relatório de Julho/2026

> Fonte: banco de produção (Supabase `donaobtlwqrjmvjqflxz`), extraído em 01/08/2026.
> Todos os números saem de tabela. Nada é estimativa.
>
> **Revisado em 02/08/2026.** A primeira versão continha dois erros que se
> anulavam ao contrário — ela subestimou o mês nos dois lados:
> 1. A venda do **Site Parceiro (R$590)** não estava na receita: existia só
>    como linha de comissão, sem fatura. Julho fechou **R$1.289,30**, não R$699,30.
> 2. Sete lançamentos de **teste da esteira de comissão** (13–15/07, anteriores
>    à primeira venda real) estavam somados como despesa. Foram removidos do
>    banco. A linha de comissão fechou **positiva**, não negativa.
>
> Diretoria deste relatório: **Lucio e Elis** (sócios do Rede Publicidade, a
> quem o Rede Baixada pertence). Não confundir com a Holos.

---

## 1. Resultado comercial

| | Julho/2026 |
|---|---|
| Vendas fechadas — portal | **9** |
| Receita portal (9 × R$77,70) | R$ 699,30 |
| Venda Site Parceiro (Floricultura Anny) | **R$ 590,00** |
| **Receita bruta total** | **R$ 1.289,30** |
| Taxa Asaas (R$2,98 × 9) | − R$ 26,82 |
| **Receita líquida** | **R$ 1.262,48** |
| Ticket médio | R$ 77,70 (produto único) |
| Forma de pagamento | 100% PIX |
| Estornos / inadimplência | **0** |
| Receita já contratada p/ renovação (jan/2027) | R$ 699,30 |

**Todas as 9 vendas são do produto Parceiro — R$77,70 por 6 meses**, assinatura semestral
registrada com vencimento em janeiro/2027.

### As 9 vendas

| Data | Empresa | Cidade | Valor |
|---|---|---|---|
| 20/07 | Gorks Auto Center | Itanhaém | R$ 77,70 |
| 21/07 | Grow Beach Growshop | Praia Grande | R$ 77,70 |
| 27/07 | Acquarius Hidro, Natação e Studio | Itanhaém | R$ 77,70 |
| 27/07 | Gonzaga Projetores | Itanhaém | R$ 77,70 |
| 28/07 | Lava Rápido Giovani | Itanhaém | R$ 77,70 |
| 28/07 | Despachante E-Digital | Itanhaém | R$ 77,70 |
| 30/07 | Kumon Itanhaém | Itanhaém | R$ 77,70 |
| 30/07 | Floricultura Anny | Itanhaém | R$ 77,70 |
| 30/07 | Salão Belle Concept | Itanhaém | R$ 77,70 |

### A curva importa mais que o total

- A **primeira venda da história do porta a porta foi 20/07**. O mês inteiro de receita
  aconteceu nos **últimos 11 dias**.
- **7 das 9 vendas caíram entre 27 e 30/07** — ritmo de saída de ~1,4 venda/dia útil.
- Junho fechou com **1 cadastro e R$0**. Julho foi o mês em que a operação de rua saiu do papel.

---

## 2. Funil de aquisição

| Etapa | Julho |
|---|---|
| Perfis novos criados | **18** (junho: 1) |
| Viraram pagantes | **9** |
| **Conversão cadastro → pago** | **50%** |
| Ficaram no acervo sem pagar (`listed`) | 6 |
| Trials abertos virando agosto | 3 |
| Leads registrados no CRM | 18 novos (base: 53) |

**Origem dos leads: 49 de 53 são `visita`.** O canal da empresa hoje é a rua — não o
tráfego pago, não o orgânico. Site e indicação somam 4.

Os 6 que não fecharam **não foram perdidos**: pela política do acervo, seguem publicados e
indexados no Google, sem selo e sem botão de WhatsApp. São base de reabordagem, não churn.

---

## 3. Expansão geográfica — o fato estrutural do mês

| Cidade | Antes de julho | Hoje |
|---|---|---|
| Mongaguá | 34 | 37 |
| **Itanhaém** | **0** | **13** |
| Praia Grande | 2 | 4 |
| Peruíbe | 1 | 1 |
| **Total** | **37** | **55** (+49%) |

**13 das 18 entradas do mês são de Itanhaém — uma cidade onde a Rede Baixada não tinha
um único cadastro em 30/06.** E 8 das 9 vendas também.

**Mongaguá, a cidade sede e maior base do portal (37 dos 55 perfis), vendeu zero.**
Não é "converteu menos" — é infinito contra nada. A diferença entre as duas cidades não
é o mercado: é que os perfis de Mongaguá vieram em boa parte da importação do WordPress
e nunca foram visitados, enquanto os de Itanhaém nasceram de visita.

**Conclusão que muda a operação: base cadastrada não é ativo comercial — porta visitada é.**
Não existe atalho de "reativar a base", e há chão virgem na cidade sede.

Isso valida a decisão de regionalização de 15/07 (deixar de ser "portal de Mongaguá" e
virar "plataforma da Baixada Santista") e o pitch de **"seja o primeiro Fundador da sua
cidade"**.

---

## 4. Entrega de valor ao cliente (o argumento da renovação)

| Métrica no portal | Junho | Julho | Variação |
|---|---|---|---|
| Eventos totais | 103 | **592** | **5,7×** |
| Visualizações de perfil | 89 | **517** | **5,8×** |
| **Contatos entregues às empresas** | 11 | **40** | **3,6×** |
| — WhatsApp | 4 | 25 | |
| — Telefone | 7 | 12 | |
| — Site | 0 | 3 | |

Também em julho: **56 fotos** e **58 serviços** cadastrados nos perfis (o maior volume
desde o lançamento) — os perfis deixaram de ser casca.

**Por que isso importa para a diretoria:** a renovação de janeiro/2027 não será vendida com
discurso, e sim com esse número por cliente ("X pessoas te acharam, Y te chamaram"). Ele já
está sendo medido por empresa desde julho.

---

## 5. Plataforma — o que foi construído

**96 deploys em produção em julho.** Os entregáveis que mudam o negócio, não só o código:

1. **Máquina de páginas (SEO)** — 8 páginas de hub cidade×categoria publicadas
   (`/empresas/mongagua/restaurantes` etc.) com texto próprio, perfis reais e dados
   estruturados. Sitemap subiu de 62 → 74 URLs. É a resposta direta ao concorrente
   `aquitemnegocios.com.br`, que ranqueia no Google com 21 mil perfis raspados e
   categorias vazias.
2. **Blog no ar** (`/blog`) — primeiro post publicado em 29/07.
3. **Política do 1º ano (acervo)** — perfil de negócio real nunca mais sai do ar nem do
   Google. O que expira é o *contato* (selo + WhatsApp), não a *página*. Muda a pressão de
   venda de "teu perfil some" para "quem te acha não consegue te chamar", e faz o portal só
   acumular ativo de SEO.
4. **Esteira de comissão e acerto** automatizada — carteira por vendedor, tela de acerto de
   sexta, pedido de adiantamento. O pagamento do time deixou de ser planilha.
5. **Operação de campo destravada** — perfil nasce publicado na visita (entrega, não
   promessa), link de reivindicação por empresa, gabarito de enquadramento de fotos,
   descrição por voz com IA, compartilhamento com preview correto no WhatsApp.

---

## 6. Time comercial

A contagem anterior ("4 vendedores com conta ativa") misturava papéis diferentes
no mesmo balde. A composição real:

| Pessoa | Papel | Situação em julho |
|---|---|---|
| **Lucio** | fecha (rua) | 9 vendas do portal — R$450 de comissão |
| **Nick** | levanta a bola (telefone) | **vendeu o Site Parceiro, R$590** — o maior ticket do mês |
| **Matheus "Barça"** | vendedor em teste | ainda sem a primeira venda |
| Paulo | testado em 27/07 | não performou |
| Giovanna | banco de reserva | atuando no comercial da Holos |
| Elis | **sócia**, não vendedora | comercial da Holos |

| | |
|---|---|
| Comissão real gerada | R$ 650 (Lucio R$450 · Nick R$200) |
| Adiantamentos pagos | R$ 300 (Lucio R$100 · Nick R$200) |
| **Saldo em aberto** | **R$ 350** (todo do Lucio) |

**O modelo Nick→Lucio já foi validado.** *"Ele levanta a bola por telefone e eu
vou lá marcar o gol"* não é plano: foi assim que saiu a venda de R$590. É o
único arranjo que produziu ticket alto até hoje, e não depende do Lucio bater
porta — depende dele só fechar.

**Dependência a registrar:** Giovanna e Elis estão alocadas no comercial da
Holos, e o contrato com a Holos ainda não foi fechado. A disponibilidade das
duas para o Rede é, portanto, **consequência daquela negociação** — não uma
decisão isolada de time.

---

## 7. Rede Publicidade — a tese do cavalo de troia

O portal existe também para abrir porta para a agência. Em julho isso começou a acontecer
de forma mensurável:

- **6 empresas marcadas como candidatas** a produto da Rede Publicidade, com o interesse
  registrado: Site Parceiro (R$590/ano), GMN Turbinado (R$149,70), Combo Google (R$197,70)
  e Plano Movimento (R$250/mês).
- **1 site já vendido** — Floricultura Anny, com comissão de R$200 lançada.

Ou seja: **6 dos 18 cadastros do mês (33%) levantaram a mão para um produto de ticket
maior.** É a validação inicial da tese de portfólio.

---

## 8. Riscos e pontos de atenção

1. **Concentração no fundador — real, mas não total.** 100% das vendas do portal são
   do Lucio. A maior venda do mês, porém, foi do **Nick** (Site Parceiro, R$590 — 46%
   da receita). O gargalo nº1 segue de pé, e a saída dele já tem forma testada: o
   modelo Nick levanta / Lucio fecha. O que falta não é achar vendedor do zero —
   é dar volume a esse arranjo e o Barça tirar a primeira venda.

2. **A matemática do R$77,70 não chega na meta.** R$77,70 por 6 meses equivale a
   **R$12,95 por cliente/mês**. Os 9 clientes de julho valem **R$116,55/mês** de recorrência.
   Para bater a meta de R$5.000/mês só com esse produto seriam necessários **~386 clientes
   ativos**. O produto de entrada é ferramenta de aquisição, não de faturamento — quem paga
   a meta é o Plano Movimento (R$250/mês) e a Rede Publicidade.

3. **Não existe cobrança recorrente.** A integração com o Asaas só sabe cobrar uma vez
   (`/payments`); mensalidade exige `/subscriptions`. Enquanto isso não for construído, o
   Plano Movimento de R$250/mês não vira MRR. **É o próximo passo de maior impacto financeiro.**

4. **Receita da Rede Publicidade fora do sistema.** O site da Floricultura Anny gerou
   comissão lançada, mas não há fatura correspondente no CRM. A receita da agência está
   sendo controlada fora da plataforma.

5. ~~**Caixa do mês foi negativo na linha de comissão.**~~ **Corrigido em 02/08:** era
   contaminação de dado de teste. Os R$930 incluíam 7 lançamentos da esteira de
   comissão testada em 13–15/07, antes da primeira venda real (20/07) — já removidos
   do banco. **Real: entraram R$1.289,30 e saíram R$300. Linha positiva em R$989,30.**

   **A causa segue viva:** teste e produção compartilham a mesma tabela, sem
   marcação. Vai voltar a acontecer no próximo teste. Correção pendente: uma flag
   `is_test` (ou contas de teste marcadas) que os relatórios saibam excluir.

6. **A base "paga" está inflada.** Dos 55 perfis, 16 são planos legados da importação do
   WordPress (`pro`, `destaque`, `profissional`) que não pagam nada hoje. Clientes pagantes
   de verdade: **9**.

7. **Sitemap ainda não submetido no Search Console.** As 8 páginas de hub estão no ar mas o
   Google ainda não foi convidado. A meta combinada é ≥70% indexado em 30 dias.

---

## 9. Fechamento para a diretoria

**Julho é o mês em que a Rede Baixada saiu de R$0 e virou operação.** Primeira venda em
20/07, 9 fechamentos em 11 dias, entrada em uma cidade nova do zero, e o portal entregando
5,7× mais movimento que em junho.

**Contra a meta de R$5.000/mês, julho entregou 26% (R$1.289,30).** Mas o número que decide
o próximo trimestre não é esse — é a constatação de que o produto de R$77,70 sozinho não
chega lá, e de que **46% da receita do mês já veio do degrau de cima**, não do portal.

A tese do cavalo de troia deixou de ser projeção: ela pagou quase metade de julho.

As três alavancas, em ordem de impacto:

1. **Trabalhar a fila que já existe.** 6 candidatos marcados valem **R$2.319 a R$2.816**
   — 3,3× toda a receita do portal no mês. **Cinco nunca foram contatados**, e três deles
   (Gorks, Acquarius, Gonzaga Projetores) **já são clientes pagantes**. É a venda mais
   barata disponível, e é trabalho de telefone: pauta do Nick.
2. **Ligar a cobrança recorrente** e vender o Plano Movimento (R$250/mês) — 2 clientes
   nesse plano valem mais que 39 no plano de entrada. A Acquarius já sinalizou
   Movimento e **não há como cobrá-la mensalmente hoje**.
3. **Tirar a primeira venda do Barça** e dar volume ao arranjo Nick→Lucio.

### A fila parada (situação em 02/08)

| Empresa | Cidade | Interesse | Valor | Status |
|---|---|---|---|---|
| Neri Salgados | Mongaguá | Site | R$ 590 | proposta — sem movimento desde 16/07 |
| Gorks Auto Center ✅ | Itanhaém | Site + GMN | R$ 739,70 | nunca contatado |
| Laika Automação | Itanhaém | GMN + Combo + Site | R$ 937,40 | nunca contatado |
| Roger Motos | Itanhaém | GMN | R$ 149,70 | nunca contatado |
| Acquarius ✅ | Itanhaém | **Plano Movimento** | R$ 250/mês | nunca contatado |
| Gonzaga Projetores ✅ | Itanhaém | GMN | R$ 149,70 | nunca contatado |

✅ = já é cliente pagante do portal.

# Onde paramos — 13/07/2026, tarde

> **As três decisões que travavam trabalho caíram. Todas as três estão em produção, verificadas.**
> E a rua ganhou o botão que faltava no celular.

---

## 1. O perfil do vendedor NASCE NO AR 🟢

**Antes:** "Nova Empresa" no painel nascia invisível — e **por omissão, não por desenho**. O insert
não falava de status/plano/ciclo, então a empresa caía nos defaults do banco (`pending` + `free`).
Resultado: era impossível pré-montar um perfil e chegar na loja mostrando *"olha, já está no ar"* —
a jogada mais forte do porta a porta.

**Agora:** vendedor cria → nasce `approved` + `trial` de 7 dias + plano `presenca` (é o plano que
acende o **selo de Verificado** e o **botão de WhatsApp**) + a venda já na carteira dele.

**A regra é POR ORIGEM, e é isso que salva o portal.** Não virou um `if` no formulário porque o
`CompanyForm` é **o mesmo** que o dono do negócio usa pra criar o próprio perfil pelo site — um `if`
ali publicaria todo cadastro orgânico. A regra foi pro banco, no trigger que já carimbava o vendedor
pela sessão (`stamp_seller_from_session`), onde o papel de quem insere é **fato**, não palpite.

| quem cria | o que acontece |
|---|---|
| **vendedor** (moderator puro) | publicado, trial 7d, selo aceso, na carteira dele |
| **admin / super_admin** | como sempre foi: `pending`, sem relógio |
| **importação em massa** (service role) | o gatilho nem age (`auth.uid()` é nulo) |
| **dono orgânico pelo site** | `pending`, sem relógio, venda **órfã de propósito** |

Os ~60 do WordPress entram pela mesma porta. Se toda empresa de admin virasse trial, eles entrariam
com relógio de 7 dias no pescoço — o "massacre". **Testado em produção nos dois sentidos.**

## 2. A rua trava em PIX 🟢

Cartão dá ao cliente **120 dias** de chargeback (540 se parcelar), e a comissão do vendedor sai na
sexta seguinte — pagaríamos R$50 sobre uma venda desfazível por quatro meses. PIX é a janela do CDC:
**7 dias**, que o ciclo do dinheiro já cobre inteira. Na calçada não custa venda nenhuma: o que
acontece lá é o QR mesmo.

Trava **só** na oferta da rua (`offerTag === 'parceiro'`). O checkout normal do site segue livre.

## 3. A recuperação NÃO apaga o portal 🟢

**PaP e Recuperação não diferem no tom — diferem no ATIVO.** Isso virou um campo:
`companies.lifecycle_track`.

| trilho | quem | não pagou → |
|---|---|---|
| `company` (rua) | o perfil **não existia**; nasceu na visita, de graça | trial → grace → hidden → **expired**. **Some.** Nada se perde, porque nada havia. |
| `acervo` | o perfil **já existe e É o portal** (os 37) | trial → **`listed`** e **PARA ALI**. Nunca sai das buscas. |

**`listed`** = no ar, clicável, **sem selo e sem WhatsApp**. E isso quase não custou código: os dois
já derivam do plano vigente (`getPlanBadges.paid`) e apagam sozinhos quando ele vence. O que faltava
era **impedir a esteira da rua de levar o perfil embora depois**.

Sem isso, o portal iria de **37 perfis pra 3** no dia em que o cron virasse — a gente destruiria o
produto tentando vendê-lo.

**Backfill:** 37 empresas (critério `active` + sem relógio) → acervo. O critério exclui sozinho a
**Neri** (trial real da rua) e o lixo de teste. **Rodei o cron simulando 60 dias**: o acervo inteiro
sobrevive; a Neri, sem pagar, some. Cada operação com seu destino.

⚠️ **O congelamento está LEVANTADO.** Pode ativar trial de recuperação.

---

## 🐛 Dois erros que quase foram pro ar

**1. O recibo de pagamento pra quem não pagou.** Eu ia terminar o trial da recuperação no estado
`active`. Só que o `lifecycle-dunning` monta o e-mail pelo estado de destino — e o texto de `active`
é *"Pagamento confirmado. Obrigado!"*. **Todo ex-cliente que NÃO pagasse receberia um recibo**,
automático. Daí nasceu o estado `listed` — e o e-mail dele virou a venda inteira da recuperação,
dita como fato: *"o botão de WhatsApp da sua empresa foi desligado — quem te procura te encontra,
mas não consegue mais falar contigo."*

**2. Um teste meu dando falso-verde.** Dois casos passaram sem nunca terem rodado como o vendedor
logado: usei `set_config(..., true)` (local à transação) fora de um bloco, e no psql cada comando é
sua própria transação — o "quem está logado" evaporava antes do INSERT. Refeito dentro de uma
transação de verdade. **É o caso 8 que importava**: quando o link é do vendedor B mas quem digita é
o A, a venda vai pro **B**. Sem roubo de carteira.

---

## 📱 A rua no celular

**Botão fixo na oferta.** O primeiro campo estava a ~1.100px do topo — uma tela e meia de rolagem
com o vendedor parado na calçada esperando. A barra põe **preço + ação sempre na tela**. E ela não é
só um atalho pro submit: se falta dado, **rola até o formulário e abre o teclado no primeiro campo
vazio**. Um toque leva o cliente de *"não sei o que fazer"* pra *"estou digitando"*.

Verificado dirigindo a página num Chrome real a 390×844.

## 🖲️ O botão que liga a recuperação

Na tela **admin → empresas**, botão verde de WhatsApp. Aparece **só** pra quem é do acervo e não tem
relógio correndo (numa empresa da rua ele seria uma armadilha). Liga selo + WhatsApp por 7 dias.
Sem ele, ligar a recuperação nos 37 seria rodar SQL na mão, 37 vezes.

**De quebra:** o diálogo de excluir empresa agora **diz o nome** de quem vai morrer. Era um id mudo —
foi assim que a descrição da Jota Vimax se perdeu, sem backup.

---

## 🔧 Acabou o "cola SQL no navegador"

O histórico de migrations estava quebrado **dos dois lados**: 33 versões fantasma no remoto (resíduo
do Lovable, timestamps 2s fora) e 12 aplicadas na mão que o remoto não registrava. Um `db push` teria
**re-rodado 12 migrations vivas**, incluindo `UPDATE` em dados reais.

Verifiquei objeto por objeto pelo REST (todas as 12 confirmadas em produção), consertei a
contabilidade com `migration repair` — **sem tocar em schema**. Hoje `npx supabase db push` e
`functions deploy` funcionam daqui.

⚠️ **`supabase functions download` SOBRESCREVE o fonte local** com o bundle publicado (sem
comentários, sem tipos). Se usar, `git checkout` depois.

---

---

## 💰 A SEXTA-FEIRA DEIXA DE SER NA MÃO

**A tela do acerto** — `/dashboard/admin/crm/acerto`. Abre e responde, em ordem: **quanto sai do
bolso na sexta**, pra quem, quanto de cada um. Um card por vendedor, botão "Já paguei".

Três decisões que valem mais que a tela:

- **O front não manda o valor.** Ele manda *"paguei o fulano"* e o **banco** decide quanto era. Uma
  tela aberta há 20 minutos — ou uma comissão estornada entre o render e o clique — pagaria errado.
- **É impossível pagar o que ainda não venceu.** A trava está no `where` da função, não na tela.
- **A tela NÃO paga.** O PIX é você, no teu banco. Aqui só se *baixa* a comissão. O dia em que o
  sistema mandar PIX sozinho, um bug vira prejuízo.

**Saldo negativo é real, não erro de conta.** Quando o cliente estorna *depois* de a comissão ter
sido paga, não se apaga o pagamento — lança-se o contrário. A tela diz **"deve R$ 50 · abate do
próximo acerto"**, não "recebe agora: R$ -50,00". É literalmente o estado da Elis hoje.

**Os 3 números do vendedor** (`/dashboard/minha-area/comissoes`), na ordem em que ele pensa na rua:
*fechando agora* (o número que sobe quando ele vende — é o que prova que bater perna paga) ·
*cai na sexta, dia N* (já é dele, não muda mais) · **"Preciso antes"** (pedido de adiantamento: o
Lucio decide, não paga sozinho — é a ponte do vendedor novo, que senão espera 12 dias pelo primeiro
PIX e desiste antes de ver).

## 🏆 O LUCIO TAMBÉM VENDE

Pela regra de hoje, "vendedor" é `moderator` **puro** — e o Lucio é admin, de propósito, pra que a
importação não vire trial. Efeito colateral: o perfil que **ele** criasse nascia invisível.

E agora sabemos que **a importação dos ~60 é MANUAL, pelo mesmo formulário** (uns 37 já entraram —
são o acervo de hoje). Ou seja: ele usa a **mesma tela pra duas coisas opostas**. Então a tela
pergunta — escrito pela consequência, não pelo nome do estado:

| escolha | o que acontece |
|---|---|
| **Cliente antigo (importação)** *(default)* | no ar agora, **sem prazo**. Nunca sai das buscas. |
| **Visita porta a porta** | no ar agora, com selo e WhatsApp, **7 dias**. ⚠️ Não pagou, **sai do ar**. |
| **Só cadastrar** | invisível até você aprovar. |

Default é *acervo* porque **o engano tem lado**: marcar "rua" num cliente antigo põe um relógio de 7
dias no pescoço dele — o massacre, uma linha por vez. O contrário custa uma mensalidade, não um
cliente. **O vendedor não vê essa escolha**: pro Barça e pra Gi o gatilho faz sozinho, sempre. Um
checkbox na calçada, com o dono da loja olhando, é uma coisa a esquecer.

## 👥 O time de rua

**Elis · Matheus "Barça" · Gi** — todos `moderator`. ✅ **A Gi está completa**: tem conta e tem o
papel, então o link dela carimba venda e o perfil que ela criar nasce publicado em trial.

---

## 🔴 O que ainda NÃO existe

1. **As 3 alavancas** — bump +R$47 · anual R$137 · **Rede Publicidade**. Nenhuma construída.
   O portal sozinho não paga equipe: **Publi = R$250/mês = 19× um cliente de portal**.
2. **Cortar os 26 campos** do formulário. (Confirmado ao dirigir a tela: é gigante. Quiz é fácil —
   mas **não usar Typebot**: iframe externo, a sessão e o crachá `?v=` não atravessam. E **não
   trocar de framework**.)
3. **Ligar leads aos perfis** (`crm_leads.company_id` NULO em todos; 34/35 casam).
4. **Terminar a importação: faltam ~25.** Manual, pelo formulário, na opção "Cliente antigo".

## Pendências do Lucio

- Faturas Asaas (`855418887` + `op4crxlwhc1jn5pe`) · **"Sobre" da Jota Vimax**
- **Lixo de teste no banco** (`Teste 35 elis`, `teste usuário cliente`, `Teste`) — inclusive a
  comissão "paga" da Elis, que **eu simulei** pra testar o estorno. Ela nunca recebeu PIX. O
  contra-lançamento de −R$50 está **vivo** e é o "deve R$ 50" que aparece na tela do acerto.
  **Limpar isso zera a tela.** Não fiz — falta teu OK.
- ⚠️ **NÃO apagar a "Neri salgados"** — prospecto real, trial até 19/07, trilho `company` (rua).

---

## 💪 O BRAÇO FORTE — a escada da folha virou sistema

> "O portal é o cavalo de troia." Quem paga a conta é isto: **1 Plano Movimento (R$250/mês) = 19
> clientes de portal.** O portal sozinho é máquina de vender pra ficar no zero.

⚠️ **A FONTE DA VERDADE É A FOLHA**, não o código
(`.claude/skills/venda-porta-a-porta/folha-vendas.md`). É ela que vai impressa na mão do vendedor.
*Aconteceu:* o Lucio me disse "GMN R$497"; a folha dizia **R$149,70** (decidido 07/07 com a Elis).
**A folha ganhou** — senão o vendedor promete um preço na calçada e o sistema cobra outro.

A escada virou catálogo (`rp_products`), com preço, ciclo, **quando ofertar** e a letra miúda:

| degrau | produto | preço | quando |
|---|---|---|---|
| 1 | Portal (Presença) | R$ 77,70/6m | na visita |
| 1.5 | GMN Turbinado | R$ 149,70 | **na ENTREGA**, nunca na visita |
| 1.5 | Combo "No Google 2×" | R$ 197,70 | só se **ELE** puxar |
| 1.7 | Site Parceiro | R$ 590/ano | "eu queria era um site" · executa **Nick** |
| 2 | **Plano Movimento** | R$ 250/mês | ~30 dias depois |

**O nome da rua é "Plano Movimento"** — nunca "Publi". E a folha proíbe chamar de "básico".

### 🚨 O bug que ninguém tinha visto
A regra de comissão era indexada **só por tipo**. A mensalidade do Movimento cairia na recorrência
do **PORTAL** — R$15 em vez de R$25. E pior: como o cliente já pagou o portal antes, a **PRIMEIRA**
mensalidade viraria "recorrência", e o vendedor **perderia os R$50 da entrada** na venda mais
importante que ele faz. Em silêncio, todo mês. Agora a regra é por **(PRODUTO, tipo)**.

### A comissão — ~20% da entrada, ~10% da recorrência
Portal R$50 (+15) · **Movimento R$50 + R$25/MÊS enquanto durar** · GMN R$30 · **Combo R$80** ·
Site R$120 (+59) · Alteração R$0.
**Uma padaria = R$155 + R$25/mês pra sempre** pro vendedor. É o que PRENDE vendedor.

🧭 **LIÇÃO CARA:** eu tinha posto o combo pagando **R$60**, contra R$80 vendendo separado — o
vendedor **perderia R$20** vendendo o que a casa quer. **Comissão de combo nunca pode ser menor que
a soma das partes**, senão você paga o vendedor pra sabotar o produto. Corrigido pra R$80.

### O candidato BATE NA PORTA (o Lucio pegou isso)
A esteira nova (`/dashboard/admin/crm/braco-forte`) é **passiva** — o Barça marca a padaria às 15h
dentro da loja e o Lucio abre o painel três dias depois, com o cara já frio.
Agora: gatilho no banco → pg_net → edge function → **e-mail na hora**, com o nome da loja, **o
degrau em que o dono mordeu**, o que o vendedor viu lá dentro, e o botão de WhatsApp pronto.
Escrito pra ser agido do celular, **sem abrir painel**.

### 🐛 Três falhas SILENCIOSAS achadas no caminho
1. **`verify_jwt`** — a função nova não estava no `config.toml` → o gateway do Supabase barrava com
   `401 UNAUTHORIZED_NO_AUTH_HEADER` **antes** de a função rodar. Candidato marcado, e-mail nunca saía.
2. 🔴 **O CRON DA REPESCAGEM TINHA 5 SEGUNDOS.** `timeout_milliseconds` default do pg_net, que
   ninguém tocou. A rodada das 12:00 **estourava todo dia**. A varredura de 200 eventos + Resend
   nunca coube nisso. **Voávamos cegos.** Agora 120s.
3. **O remetente** — eu tinha inventado um "nao-responda@"; o Resend só aceita o domínio verificado.

Fica no projeto: **`diag_avisos()`** — "por que o e-mail não chegou" deixa de ser adivinhação.

---

## 📱 Bugs do celular (todos corrigidos e verificados)

- 🔒 **O LOGOUT PRENDIA.** `signOut()` revoga no servidor; com o token morto (celular parado dias),
  o servidor diz "Auth session missing!", o código dava `throw` e **não limpava nada** → erro
  vermelho e o cara **continuava logado, sem conseguir sair**. Agora: tenta global, e se falhar
  limpa o local e apaga a chave `sb-*` na marra.
- **O diálogo não tinha teto nem rolagem** — defeito do componente **base**: o rodapé (onde ficam
  "Salvar"/"Marcar") saía da tela, inalcançável. `max-h-[90dvh] overflow-y-auto`
  (**dvh**, não vh: a barra do navegador some e volta).
- **O botão azul saía 84px pra fora** (tela 375, botão terminava em 459). `min-width:auto` de item
  flex **impede o encolhimento** — em vez de espremer, empurra pra fora.

## 🗺️ A home NÃO TINHA MAPA

A seção "Mapa Interativo" era um **`{/* Map Placeholder */}`**: caixa de gradiente azul com um
ícone. Do celular, "uma tela azul". E o ativo estava lá: **32 das 41 empresas já tinham lat/lng**.

**O pino diferencia quem paga:** grande, azul, **com a logo** = paga. Pontinho cinza = free.
É demonstração de rua — o vendedor abre a home dentro da loja: *"o pino do teu concorrente é aquele
grande, com a marca; o teu é o pontinho cinza"*. O cinza **continua clicável** (esconder do
VISITANTE seria atirar no próprio pé — a pressão é sobre o dono, não sobre o cliente dele).

Dois problemas medidos: `fitBounds` em todos os pinos afastava tanto que os 29 de Mongaguá viravam
um bolo (agora enquadra na cidade mais densa); e **5 empresas estão na MESMA coordenada exata** —
cluster com raio pequeno (30px), só quem se sobrepõe vira número. **44 pares empilhados → 0.**

## 📍 A busca de endereço não achava NADA

O código grudava **", Baixada Santista, SP, Brasil"** em toda consulta — e "Baixada Santista" é uma
**REGIÃO**, que o OpenStreetMap não indexa. **Zero pra tudo.**

E trocar pela cidade não bastava. Endereço brasileiro quebra o Nominatim de dois jeitos:
- **o NÚMERO** — texto livre com número quase sempre falha. A busca **estruturada** (`street=`/`city=`) tolera.
- **o BAIRRO** — contradiz o OSM ("Balneário Jussara" vs "Itapoan"). Agora **corta no " - "**.

```
"Av. Anna Seckler Malacco, 78 - Balneário Jussara"  (texto livre)   → 0
street="Av. Anna Seckler Malacco, 78" + city="Mongaguá"             → 1 ✅
```
E **resultado único = pino na hora** (antes ele buscava, via o endereço na lista, o mapa continuava
vazio, e concluía que quebrou).

## 🚨 Falso alarme que vale registrar

O `robots.txt` e o `sitemap.xml` deram **403 (Vercel Security Checkpoint)** — o que mataria o
portal (o produto É aparecer no Google). **Era eu:** centenas de `curl` conferindo deploy pelos
bytes acionaram a **DDoS Mitigation** automática da Vercel contra o meu IP (Firewall confirmou:
Bot Protection **Inactive**, Custom Rules **0**, "Challenged 104" ≈ regra DDoS 105, Allowed 216).
**Nada a desligar. O Google não está bloqueado.**
👉 **Não verificar deploy com rajada de curl** — usar o navegador.

---

## 🔴 O que ainda NÃO existe

1. **A COBRANÇA RECORRENTE.** O Asaas só sabe cobrar de uma vez (`/payments`). Mensalidade é outro
   objeto (`/subscriptions`) — **sem isso o Plano Movimento não vira MRR**, e é ele que paga a equipe.
   👉 **É o próximo passo.**
2. **Cortar os 26 campos** do formulário.
3. **Ligar leads aos perfis** (`crm_leads.company_id` NULO em todos).
4. **Terminar a importação: faltam ~25** (manual, pelo formulário, opção "Cliente antigo").

---

**Commits:** `b946549` (nascimento + PIX) · `a079baf` (acervo) · `89ecf7a` (barra fixa) ·
`83fe4f0` (recuperação + e-mail honesto) · `d4badf2` (o Lucio também vende) · `e7988d1` (a tela do
acerto) · `214941b` (lançamento manual) · `7311eb6` (o braço forte) · `23b6dec` (combo) ·
`60e0739` (3 bugs do celular) · `77eab44` (mapa + busca de endereço) · `3d7796c` (pino na hora).

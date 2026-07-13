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

## 🔴 O que ainda NÃO existe

1. **A tela do acerto** ("quem recebe nesta sexta") + **painel do vendedor com 3 números**
   (fechando agora / cai na sexta dia N / "preciso antes"). Sem isso, o acerto semanal é na mão.
2. **As 3 alavancas** — bump +R$47 · anual R$137 · **Rede Publicidade**. Nenhuma construída.
   O portal sozinho não paga equipe: **Publi = R$250/mês = 19× um cliente de portal**.
3. **Cortar os 26 campos** do formulário do painel. (Quiz é fácil — mas **não usar Typebot**: iframe
   externo, a sessão e o crachá `?v=` não atravessam. E **não trocar de framework**.)
4. **Ligar leads aos perfis** (`crm_leads.company_id` NULO em todos; 34/35 casam).
5. **Importar os ~60 do WordPress** — devem nascer com `lifecycle_track = 'acervo'`.

## Pendências do Lucio

- Faturas Asaas (`855418887` + `op4crxlwhc1jn5pe`) · **"Sobre" da Jota Vimax** · export do WordPress
- **A Gi ainda não se cadastrou.** Sem conta → sem link → a venda dela nasce órfã.
- **Lixo de teste no banco** (`Teste 35 elis`, `teste usuário cliente`, `Teste`) — inclusive a
  comissão "paga" da Elis, que **eu simulei** pra testar o estorno. Ela nunca recebeu PIX.
- ⚠️ **NÃO apagar a "Neri salgados"** — prospecto real, trial até 19/07, trilho `company` (rua).

---

**Commits:** `b946549` (nascimento + PIX) · `a079baf` (acervo) · `89ecf7a` (barra fixa) ·
`83fe4f0` (botão da recuperação + e-mail honesto).

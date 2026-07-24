# Estratégia

> O que importa agora. Prioridades, metas, prazos.
> O Claude usa isso pra decidir o que sugerir primeiro e o que adiar.
> Atualize sempre que as prioridades mudarem.

## 🌱 Diretriz da holding — 05/07/2026 (2ª mesa; ajusta QUEM TOCA)

Papel no portfólio: **cavalo de troia** — baixo ticket, baixa resistência, custeia a operação com leveza e **abre portas pro foco nº1 (Rede Publicidade)**: o empresário local que assina aqui é lead natural da agência.

- **QUEM TOCA: Giovanna** no porta-a-porta/vendas. ⚠️ Se o porta-a-porta virar tarefa do **Lucio**, estourou o teto de foco do portfólio (FOCA=1 = Rede Publicidade) — é fragmentação disfarçada.
- ✏️ **Ajuste 07/07/2026 (decisão do Lucio):** o Lucio assume o PaP como **protótipo solo com apoio de IA** — não é fragmentação porque a mesma visita vende o Baixada (77,70) E prospecta o Rede Publicidade (250/mês), ou seja, é trabalho do FOCO nº1 usando o Baixada como porta. **Critério de graduação:** 20 vendas OU 2 clientes Publi de 250 OU 45 dias → playbook revisado e a **Gi entra no volume**. Plano completo: `../holding-maier/saidas/plano-prospeccao-redes-2026-07.md`.
- Tráfego pago: dentro do que já roda; sem escalar verba antes do caixa justificar.
- Lucio entra só como decisor e no que cruzar com o trajeto natural dele (Modo Rua), nunca como executor dedicado.

Fonte: `../holding-maier/_memoria/estrategia.md`.

## 🏛️ Decisão de arquitetura — 10/07/2026 (RB = plataforma única)

Decidido (com apoio de IA): o Rede Baixada vira a **plataforma única do grupo ("uma rede só")** — um registro de cliente que gradua de assinante-do-portal → cliente-da-agência (Rede Publicidade), com carteira/faturas/comissões/serviços num lugar só, separados por **tag de unidade (RB × Rede Publicidade)**. **UniMasso fica fora** (SaaS próprio; só compartilha a conta Asaas). Não criar ERP separado — monólito modular, evolução **faseada** (Fase 0 = ligar o CRM ao webhook Asaas). Viável porque o backbone de ERP **já existe no schema** (só falta ligar). Roadmap completo: [`../saidas/roadmap-plataforma-unica-2026-07.md`](../saidas/roadmap-plataforma-unica-2026-07.md).

## 🗺️ Regionalização + posicionamento — 15/07/2026

**RB agora é a Baixada, não só Mongaguá.** Expansão pra **Praia Grande e Itanhaém** (muito mais estabelecimentos). A trava era de TEXTO (a home dizia "Oficial de Mongaguá", cidade fixa) e já perdeu prospectos de PG no passado. Corrigido: home = "Plataforma de Negócios da **Baixada Santista**", "Oficial de Mongaguá" virou crédito ("chegando em PG e Itanhaém"), cidade virou **dropdown real** (bairros já existem pra toda a Baixada). Folha regionalizada ("na sua cidade", "Fundador da sua cidade"). Empresas ainda 92% Mongaguá → PG/Itanhaém = pitch **"seja o primeiro Fundador da sua cidade"**.

**Posicionamento — de "EuGência" pra Agência.** Não é "o Lucio faz", é **"a Rede Publicidade faz com IA"** — time enxuto, rápido, preço imbatível. Os dois Redes são **dobradinha**: o Baixada abre a porta (oferta validada), a Rede Publicidade entrega e cuida. A IA é o *motivo pra acreditar* no preço/velocidade, não a manchete. Essa frase de autoridade vive no Treinamento do Agente e na folha.

## 🚀 Plano SEO + Conteúdo + E-mail + Conversão — 19/07/2026 (DECIDIDO, faseado)

Plano completo: [`saidas/plano-seo-conteudo-email-2026-07-19.md`](../saidas/plano-seo-conteudo-email-2026-07-19.md).
> ✅ **Camadas 1 e 3 CONSTRUÍDAS em 23/07** (ver política do 1º ano acima): 8 hubs
> cidade×categoria (`/empresas/mongagua/restaurantes`) e o blog (`/blog`) estão no código, com
> gate ≥3 perfis, schema (ItemList/Breadcrumb/FAQ/Article) e pre-render pro robô. **Os 8 hubs
> estão DESPUBLICADOS** esperando o Lucio aprovar os textos em
> [`saidas/textos-hubs-2026-07-23.md`](../saidas/textos-hubs-2026-07-23.md).
Tese: conteúdo + páginas de hub trazem tráfego de graça → cai em perfil REAL → "X pessoas viram"
fecha a venda. 4 camadas: (1) **hub de páginas** cidade/categoria/bairro com texto único + perfis
reais + schema (a brecha exata do concorrente, que tem categorias VAZIAS); (2) **hidratação** =
acervo curado (trilho acervo NÃO some — é a camada de SEO; rua é venda); (3) **blog** em
`redebaixada.com.br/blog` DENTRO do portal (evergreen 80% + hype/news + patrocinado); (4) **e-mail
dois motores**: Resend transacional (100/dia, 3k/mês) × **Brevo marketing** (conta compartilhada
UniMasso/Holos, ilimitada) em **domínio SEPARADO**. ⚠️ **GUARDA-CHUVA: todo link pago = `rel="sponsored"`**
(senão penalidade de domínio) + página de hub só entra com ≥3–5 perfis (thin content derruba). Build
é do Claude; matéria-prima é a rua do Lucio (anti-fragmentação). Fase 0 AGORA (custo zero): banco de
conteúdo de rua + acoplar no discurso de venda. Depois hub → blog → Brevo → monetização.

## 🏛️ POLÍTICA DO 1º ANO: todo cadastro real é acervo — 23/07/2026 (DECIDIDA, no ar)

**Decisão do Lucio:** perfil de negócio **constatado real** (a visita do agente é a constatação;
o orgânico passa pela moderação) **nunca mais sai do ar nem do Google** — nem o plantado na rua
que não fechou. É o "legado de cadastros": o portal só ACUMULA página. Revisar em jul/2027.

A pressão comercial muda de endereço, não desaparece: deixa de ser *"teu perfil some"* e vira
***"quem te encontra não consegue mais te CHAMAR"*** — o selo de Verificado e o botão de WhatsApp
continuam derivando do plano pago e apagando sozinhos no vencimento. **A PÁGINA é o portal; o
CONTATO é o produto.** É essa fronteira que deixa acumular página sem canibalizar a venda.

No banco: `lifecycle_track` default `'acervo'`, os 45 perfis migrados, trilho `'company'` (a
esteira que some) dormente nas policies — reverter é UPDATE, sem deploy. Trial de rua segue
7 dias, mas termina em `listed` (perde selo/WhatsApp, fica no ar) em vez de sumir.

**Consequência operacional:** a pergunta do dia seguinte à visita deixou de ser "quanto tempo
falta?" e virou **"o dono já reivindicou?"**. Por isso o admin ganhou os chips
*Plantadas (sem dono) · Reivindicadas · Selo vencido*, o vendedor ganhou o badge "Aguardando dono"
+ **botão de copiar o link de reivindicação** (`&c=`, agora pela `agent-link` — acabou o uuid na
mão), e o CRM ganhou o card "Plantadas aguardando claim". Casa com o kill criterion de 30 dias
(claim <10–15% → repensar trilho).

## 🧭 Diretriz das frentes de cadastro — 19/07/2026 (mesa /planejar: painel 5 lentes + entrevista)

**Norte:** o Lucio planta perfis na rua e no trajeto; **a máquina cobra** (Resend + ciclo de
vida, LIGADOS em produção) — ele nunca é o cobrador. Decisões do dono cruzadas com o painel:

- **Modo Rua (F1+F2 fundidas):** a visita fecha na hora (77,70) OU planta trial "rua" (perfil
  no ar 7 dias) + WhatsApp com link de reivindicar **no mesmo dia**. Regras: só empresa que ele
  viu/conversou · trial começa no dia do contato · e-mail da empresa sempre preenchido (senão o
  ciclo cobra o próprio Lucio) · pedir o e-mail real do dono na visita.
- **Reconquista dos 37: WhatsApp-first, Lucio assume** (número pequeno, histórico dele; ligação
  fria de cobrança trava — dado de projeto, não defeito). Lote semanal; liga só pra quem responder.
- ⚰️ **Popular PG/Itanhaém em massa: morto** (casca sem dono = passivo reputacional — o erro
  exato do concorrente aquitemnegocios; ver `saidas/analise-aquitemnegocios-2026-07-19.md`).
- 🌱 **Tráfego pago: gate completo** — 10 vendas manuais primeiro → LP pública "Fundador da sua
  cidade" (77,70) → ads verba mínima (R$10–15/dia).
- **Legados (16 planos antigos): todo antigo que voltar vira Parceiro R$77,70/6m.** Uma regra só.
- **Resposta estrutural ao concorrente (SEO):** acervo curado + páginas cidade×bairro×categoria
  — copiar a máquina de indexação deles, nunca o atalho da raspagem. Monitorar o sitemap deles 1×/mês.
- Kill criteria 30 dias: claim de perfil plantado <10–15% → repensar trilho · reconquista <5
  fechamentos → base fria morta, não insistir.

## Fase

**Reativação da Rede Baixada** (jun/2026). Voltar a oferecer e fechar as primeiras vendas/cadastros. Meta de 12 meses: R$5.000/mês.

**Marco (jun/2026):** o checkout/pagamento (Asaas) entrou em **produção** — empresa e profissional já assinam, pagam (cartão/PIX) e são publicados automaticamente; estorno/chargeback revoga o plano. Testado com dinheiro real. O motor de venda do produto está pronto.

## Prioridade principal

**Trazer gente pro site e fechar as primeiras assinaturas.** Com o pagamento já no ar, o gargalo é **100% aquisição** — não é mais o produto. Foco: prospecção (porta a porta) + tráfego pago levando empresas/profissionais pro `/planos`.

Dois canais já em jogo:
- **Porta a porta** — abordagem consultiva (visita a vizinhança empreendedora pra entender como divulgam hoje).
- **Tráfego pago** — já testado, com sinais positivos.

## O que pode esperar

Refinamentos de produto e processo enquanto a venda não roda. Primeiro fazer o motor de venda girar; otimizar depois.

## Contexto com prazo

**Substituir o Uber pela Rede Baixada.** Referência concreta do Lucio: Uber rende ~R$150 em 5h; a Rede Baixada já rendeu **R$338,50 em 4h**. A economia da Rede Baixada é muito melhor por hora — a meta é provar isso na consistência e largar o Uber. (Candidata a virar rotina/skill via `/mapear-rotinas`.)

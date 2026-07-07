# Spec — Fluxo do Vendedor de Rua v2 (anti-fricção)

> **Pra quem:** Nick (execução) · **Pedido do Lucio (07/07/2026):** eliminar fricção ao máximo no fluxo
> do link privilegiado (`/oferta-parceiro?k=...`) pra facilitar a vida do vendedor na porta.
> **Princípio de design:** o cliente NÃO monta nada (done-for-you) — o fluxo do cliente é só
> compromisso + pagamento (2 minutos); o fluxo guiado é ferramenta DO VENDEDOR.

## O fluxo-alvo (cliente na frente, vendedor conduz)

```
QR da folha
  → página da oferta (existe): preço travado + UM botão "Ativar minha empresa"
  → CADASTRO ENXUTO (60 segundos, 4 campos máx.)
  → auto-login (sem tela de "confirme seu e-mail" bloqueando)
  → CHECKOUT direto (CPF/CNPJ → PIX R$77,70)
  → tela final: "Pronto! Seu perfil entra no ar hoje — o Lucio monta tudo pra você."
```

O perfil em si é montado DEPOIS, pelo vendedor, no admin (wizard abaixo).

## MUST — corta fricção já (fase do protótipo)

1. **Cadastro enxuto: máximo 4 campos** — nome do negócio · WhatsApp · e-mail · senha.
   Todo o resto (categoria, endereço, fotos, horário, diferenciais) sai do cadastro → vai pro admin/wizard.
2. **Auto-login após cadastro** — sem exigir confirmação de e-mail pra seguir (confirmação pode
   acontecer depois, sem bloquear o caminho do dinheiro).
3. **Checkout na mesma sessão** — do cadastro cai direto no modal CPF/CNPJ → Asaas. Zero telas no meio.
4. **Caminho do trial com 1 toque** — pro morno: mesma conta criada, botão/flag "ativar grátis"
   (hoje é manual no admin — pode continuar manual, mas sem passos a mais pro cliente).

## SHOULD — a arma do vendedor (logo depois)

5. **Wizard "anúncio guiado" no admin, mobile-first, 5 passos** — pro VENDEDOR montar o perfil
   na calçada ou no fim do dia: ① categoria → ② fotos direto da câmera (as 5 da visita) →
   ③ WhatsApp/horário → ④ diferenciais (chips prontos por categoria) → ⑤ publicar.
   Meta: perfil completo em <5 minutos, pelo celular.

## LATER — fase 2 (quando a Gi entrar)

6. **Link por vendedor** — `?k=<segredo>&v=<vendedor>`: atribuição da venda (base da comissão da Gi).
   Já consta no backlog dos respiros (folha do operador, item 4).
7. **Onboarding self-serve** — o wizard guiado voltado ao CLIENTE só faz sentido no fluxo orgânico
   (`/planos`, tráfego pago) — aí sim o cara está sozinho e precisa de guia. Não priorizar antes do tráfego voltar.

## O que NÃO mudar

- **A ordem cadastro → pagamento fica.** O login é o sinal de compra (micro-compromisso), é a rede
  de segurança do trial, e o webhook do Asaas precisa da empresa existente pra ativar o plano.
  A fricção a matar é o NÚMERO DE CAMPOS e telas bloqueantes — não a ordem.
- O segredo do link (`k`) e o preço travado — mecânica da exclusividade, já provada.

## Critério de pronto (MUST)

Na rua: do QR ao PIX pago em **≤ 2 minutos**, com o vendedor digitando. Testar com 1 venda real.

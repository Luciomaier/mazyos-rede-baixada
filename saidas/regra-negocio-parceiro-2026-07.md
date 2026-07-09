# Regra de Negócio — ciclo do parceiro (Rede Baixada, jul/2026)

> Validada com o Lucio em 09/07/2026. Modelo: **trial + publish-first + expiração automática +
> repescagem (dunning)**. Mata a fricção de cobrar na rua; usa o perfil no ar como fechamento.

## Fluxo
1. **Visita:** o agente cria o perfil na hora, pronto e visível.
2. **Publica na hora** como *trial* → já aparece nas buscas + dispara alerta **"novo anúncio – pending moderate"** pro admin (1 clique, **não bloqueia**).
3. **7 dias, dois relógios INDEPENDENTES:**
   - **Pagamento (portão comercial):** link enviado na hora + repescagem. Pagou → **parceiro ativo 6 meses**. Não pagou em 7d → sai das buscas + **pool de repescagem**.
   - **Moderação (portão de conteúdo):** o admin confirma que é negócio real. Reprovou → sai (independe de pagar). **Pago mas o admin não clicou → NÃO derruba** (quem manda no comercial é o pagamento).
4. **Repescagem:** os não-pagos viram fila de nutrição — **email (Brevo) + link de pagamento** agora; WhatsApp em massa só quando a API Meta do Rede destravar (1:1 manual pode).
5. **6 meses:** o facão passa de novo (renovação). **Gravar o vencimento desde o 1º parceiro.**

## Dois status (não confundir)
- **Lead** (pipeline de venda): `Novo → Qualificado → Proposta → Fechado → Perdido/Nutrir`.
- **Empresa/assinatura** (ciclo do produto):
  `demo → publicado-trial (7d) → publicado-pago (6m) → 🩶 cinza/inclicável → oculto → expirado`
  - **Cinza/inclicável:** graça visível — aparece apagado, o público não clica, o dono vê morrendo. É o último pedágio da repescagem (link + mensagem batem mais forte aqui).
  - **Oculto não apaga** o perfil → **reativar é 1 clique** do dono ao pagar.

## Comissão
Amarra ao **pagamento**, não à criação do perfil (evita perfil-fantasma). Vai pro agente do `assigned_to`, seja na visita ou na repescagem.

## Dependências (o que trava o "pra valer")
- **Asaas:** em produção ✅ (conta única do grupo — Rede Publicidade). Falta o **webhook validar assinatura** (correção do Nick).
- **WhatsApp em massa:** bloqueado até a verificação Meta do Rede destravar. Email já roda.
- **Recorrência 6m:** fase 2 — mas gravar o vencimento desde já.

## Por que funciona
Remove a fricção nº1 da rua (cobrar no ato); o perfil no ar é o fechamento emocional (aversão à perda com o timer); repescagem pega o indeciso. Resultado: muitas conversões na visita **+** um pool que paga depois.

---
Ligações: organograma → [`../../rede-publicidade/saidas/organograma-comercial-2026-07.md`](../../rede-publicidade/saidas/organograma-comercial-2026-07.md) · sprint dev → [`sprint-nick-crm-mobile-2026-07.md`](sprint-nick-crm-mobile-2026-07.md)

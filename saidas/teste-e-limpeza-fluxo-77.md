# Teste final + limpeza — fluxo dos 77,70 (rodar quando voltar)

> Estado ao sair (07/07/2026): fluxo v2 NO AR (front + servidor + secrets). Falta só este
> roteiro — o teste do operador no celular e a faxina dos rastros de teste.

## Parte 1 — O teste do operador (5 min, no celular)

1. Abrir o **QR da folha** (link privilegiado completo, com `?k=`).
2. Conferir: o formulário aparece **na própria página** — nome do negócio · categoria · cidade · WhatsApp · e-mail · senha. (Nada de redirecionar pra /cadastro.)
3. Preencher como cliente fictício: nome **"Teste Final — Apagar"**, e-mail novo (ex.: `teuemail+testefinal@gmail.com`), senha qualquer (6+).
4. Tocar **"Ativar agora — R$ 77,70"** → deve cair DIRETO no modal do CPF, sem tela de "confirme seu e-mail", sem login manual.
5. CPF: o teu → "Continuar para o pagamento".
6. ✅ **CRITÉRIO DE PRONTO: o Asaas abre com R$ 77,70** (não 147). Cronometrar do QR à tela do PIX: **≤ 2 minutos**.
7. *(Opcional — ciclo completo)* Pagar os 77,70 → conferir no admin que a empresa virou **"approved"** com vencimento **+6 meses** → depois **estornar** no painel Asaas (o webhook revoga o plano sozinho no estorno — isso também testa a revogação!).
8. Testar o link **"trocar de conta"** no rodapé do card (é o que te deixa emendar uma venda na outra no mesmo celular).

## Parte 2 — Limpeza (10 min, nos painéis)

- [ ] **Asaas:** cancelar a cobrança de **R$147** do teste de hoje de manhã (Cobranças → cancelar).
- [ ] **Asaas:** cancelar a cobrança do teste da Parte 1 (se não pagou) — ou **estornar** (se pagou o ciclo completo).
- [ ] **Asaas (opcional/cosmético):** renomear ou excluir o cliente **"Miriam"** ligado ao teu CPF (registro velho de teste da UniMasso — a conta Asaas é compartilhada e o Asaas identifica cliente por CPF).
- [ ] **Portal (admin):** excluir a empresa "Teste Final — Apagar" da Parte 1. *(Se pagou e estornou, o plano já caiu sozinho — pode excluir igual.)*
- [ ] **Delegar pro Nick:** apagar no painel Supabase (Auth → Users) os usuários `teste.fluxo.v2*.apagar@example.com` + o usuário do teste da Parte 1.

## Se algo falhar

| Sintoma | Significa | Ação |
|---|---|---|
| Preço abre em R$147 | secret/função fora do lugar | Me chama — checo em 2 min |
| "Oferta inválida" com o QR certo | chave do link ≠ secret do servidor | Me chama — comparo os dois |
| Erro ao criar perfil | RLS/categoria/cidade | Print da tela e me chama |

---
*Contexto técnico completo: `spec-fluxo-vendedor-rua-v2.md` · Runbook original: `deploy-oferta-parceiro.md`.*

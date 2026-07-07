# Runbook — subir o link privilegiado /oferta-parceiro (pro Nick)

> O código já está no repo **redebaixada** (branch `oferta-parceiro`, **PR #1**).
> A página é o link de R$77,70/6 meses da venda porta a porta. Falta o deploy do backend
> (Supabase) + publicar o front. A CLI da máquina do Lucio deu **403** (sem privilégio no
> projeto) — por isso é com você, que tem acesso ao projeto Supabase `donaobtlwqrjmvjqflxz`.

## O segredo do link
- `OFFER_PARCEIRO_KEY = b036e660589d546db056951c`  ← é a chave que vai no fim da URL/QR
- `OFFER_PARCEIRO_VALUE = 77.70`
- (Se quiser, gere outro segredo: `openssl rand -hex 12`. Só mantenha consistente entre o secret e o link/QR.)

## Passos (rodar de dentro de `portal/`, autenticado com sua conta Supabase)

```bash
# 1) Secrets
supabase secrets set OFFER_PARCEIRO_KEY=b036e660589d546db056951c OFFER_PARCEIRO_VALUE=77.70 \
  --project-ref donaobtlwqrjmvjqflxz

# 2) Deploy das 2 edge functions (mudanças ADITIVAS — fluxo normal do /planos fica idêntico)
supabase functions deploy asaas-create-payment --project-ref donaobtlwqrjmvjqflxz
supabase functions deploy asaas-webhook        --project-ref donaobtlwqrjmvjqflxz

# 3) Publicar o front: dar merge no PR #1 na main → a Vercel publica /oferta-parceiro
```

## Testar (⚠️ Asaas está em PRODUÇÃO — pagamento real)
- Abrir `https://redebaixada.com.br/oferta-parceiro?k=b036e660589d546db056951c`
- Logar com uma empresa de teste (owner) → modal CPF/CNPJ → ir até o checkout do Asaas.
  - **Só conclui cobrança real se pagar.** Criar a fatura não cobra; pagar cobra R$77,70 (dá pra estornar).
- Conferir no banco: a empresa fica `plan_slug = "presenca"`, `plan_expires_at ≈ +6 meses`, `status = "approved"`.
- Sem `?k=` correto → página mostra "Link não reconhecido" / checkout retorna "Oferta inválida". (esperado)

## Link pra entregar na visita (vira o QR da folha)
`https://redebaixada.com.br/oferta-parceiro?k=b036e660589d546db056951c`

## Rollback
- Front: reverter o merge do PR #1 (Vercel republica a versão anterior).
- Functions: as mudanças são aditivas; se precisar, `git revert` do commit + `supabase functions deploy` de novo.

## O que NÃO entrou (próximos builds)
- Lembrete de renovação aos 6 meses (bot/CRM) · e-mails transacionais · código por prospect (atribuição).

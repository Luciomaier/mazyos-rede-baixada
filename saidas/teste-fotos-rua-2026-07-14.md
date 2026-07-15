# Teste ao vivo — fotos no celular (14/07/2026)

Aceite do pipeline de imagem antes de bater perna.

Legenda: ⬜ a testar · ✅ passou · ❌ falhou

---

## Regra que organiza tudo

O **pipeline de imagem** (comprimir, abrir a câmera, girar a foto, converter HEIC)
roda **no navegador** — é **idêntico nos 3 níveis**. Testar 3× é desperdício.

A **permissão** é o que muda. E ela não depende só de *quem você é*: depende de
**quem você é × quem criou a empresa × qual o plano dela**.

> ⚠️ **Não teste galeria num perfil do ACERVO.** Acervo nasce `plan_slug: free`, e
> free tem `max_photos = 0` — a galeria fica desabilitada com aviso de upgrade.
> Isso é **correto**, não é bug. Perfil de **rua** nasce `presenca` = **5 fotos**.

---

## BLOCO A — Aparelho (testar UMA vez só, em qualquer nível; sugiro no N3)

| # | Teste | Esperado | Status |
|---|---|---|---|
| A1 | Tocar **"Tirar foto"** no campo do **logo** | Abre a **câmera**. Não a galeria, não os arquivos. **(é o bug de hoje)** | ⬜ |
| A2 | Aba **Fotos** → **"Tirar foto"** | Câmera abre → "Otimizando..." → "Enviando..." → foto no grid | ⬜ |
| A3 | Tirar a foto com o celular **na vertical** | Aparece **em pé** na galeria e no perfil público. Não deitada | ⬜ |
| A4 | Tocar na área de upload e pegar foto **velha e pesada** do rolo | Entra normal. Sem "arquivo muito grande", sem clique morto | ⬜ |
| A5 | Repetir A2 **no 4G da rua**, fora do wi-fi | Poucos segundos. Se travar >30s em "Enviando...", me avise | ⬜ |
| A6 | Repetir A1–A3 num **iPhone** (se tiver) | Igual. Se aparecer aviso de **HEIC**, me avise — é o que não consigo reproduzir aqui | ⬜ |
| A7 | Classificado com **5 fotos** | As 5 entram; a 6ª avisa "Máximo de 5 fotos por anúncio" | ⬜ |

---

## BLOCO B — Permissão (aqui SIM, os 3 níveis)

### N1 — Empresa (o dono do negócio, sem cargo no portal)

| # | Situação | Esperado | Status |
|---|---|---|---|
| B1.a | Perfil que **ele mesmo** criou (auto-cadastro / oferta) | ✅ sobe foto | ⬜ |
| B1.b | Perfil criado pelo vendedor e **transferido** pra ele | ✅ sobe foto *(a transferência cria a linha de membro)* | ⬜ |
| B1.c | Perfil criado pelo vendedor **sem transferir** | ❓ ele provavelmente **nem enxerga** a empresa no painel — confirmar o que ele vê | ⬜ |
| B1.d | Perfil do **acervo** (plano free) | 🔒 galeria desabilitada + aviso de upgrade — **esperado, não é bug** | ⬜ |

### N2 — Moderador / Agente (Elis, Giovanna)

| # | Situação | Esperado | Status |
|---|---|---|---|
| B2.a | **Empresa que o próprio agente cadastrou na rua** ← *o caso real* | ✅ sobe foto (cadastrar o torna dono do perfil) | ⬜ |
| B2.b | Empresa cadastrada por **outra pessoa** / acervo | ❌ "Você não tem permissão para gerenciar as fotos dessa empresa" — **esperado hoje** | ⬜ |
| B2.c | Idem B2.b, mas **com atribuição** de bairro/categoria | ✅ deve subir — *só testável depois que você criar a atribuição* | ⬜ |

> **Já reproduzido**: a Elis, sem atribuição, numa empresa que não criou → bloqueada.
> Se você quer que ela mexa em qualquer empresa, precisa dar **atribuição de moderador**
> (bairro ou categoria). É decisão sua — me diga e eu faço.

### N3 — Admin / Super Admin (Lucio)

| # | Situação | Esperado | Status |
|---|---|---|---|
| B3.a | Empresa que **você criou** | ✅ sobe foto | ✅ comprovado |
| B3.b | Empresa que **você NÃO criou** ← *o bug de hoje* | ✅ sobe foto | ✅ comprovado (Brechó da Deva) |

---

## Já comprovado por verificação automatizada (não refazer)

- Foto de 8,3 MB (4000×3000) → ~500 KB, em ~0,4 s
- Foto com marca de rotação sai **em pé** (1200×1600 retrato)
- Logo PNG mantém **fundo transparente** (alpha do canto = 0)
- HEIC / PDF / arquivo quebrado → mensagem clara, sem travar
- Upload real chega ao storage **comprimido** (8,32 MB → 775 KB)
- Botão "Tirar foto" presente em viewport de celular, com `capture=environment`
- **N3 em empresa de terceiro** — o RLS corrigido, foto entrou e foi removida

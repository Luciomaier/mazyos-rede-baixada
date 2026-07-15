# Fluxo de teste — fotos nos 3 níveis (14/07/2026)

Um passo por linha. Faz, e me diz **"feito"** ou **"falhou: <o que apareceu>"**.
Eu marco aqui.

Legenda: ⬜ a fazer · ✅ passou · ❌ falhou

**Tudo no CELULAR** (é onde a câmera existe). Site: **redebaixada.com.br**

---

## PREPARO

- ⬜ **0.1** — No celular, logado como você, abrir **`/dashboard/minha-area/meu-link`** e **copiar o link do vendedor** (ele termina com `?v=algumacoisa`). É o crachá que atribui a venda.
- ⬜ **0.2** — Ter em mãos um **e-mail novo** que você controle. Dica: `holos.site+cliente1@gmail.com` — o Gmail entrega no seu inbox normal, mas o portal trata como conta nova.

---

## FLUXO 1 — N1 · CLIENTE (o dono do negócio, cadastrado pelo link da rua)

- ⬜ **1.1** — Abrir uma **janela anônima** no celular e colar o **link do vendedor** (o do passo 0.1).
- ⬜ **1.2** — Preencher o cadastro: e-mail `holos.site+cliente1@gmail.com`, senha `123456`, nome do negócio **"Teste Cliente 01"**, categoria e cidade quaisquer.
- ⬜ **1.3** — Concluir o cadastro. **Quando cair na tela de pagamento, PARE** — o perfil já foi criado antes do pagamento. Não precisa pagar.
- ⬜ **1.4** — Ainda logado como o cliente: **Dashboard → Empresas → "Teste Cliente 01"**.
- ✅ **1.5** — Botão "Tirar foto" + abrir câmera: **funcionou em vários celulares** (14/07). Rua liberada.
      - ⚠️ **Exceção — só o celular do Lucio**: mesmo em aba anônima (bundle novo, sem cache), a câmera não abre — o seletor mostra só "Arquivos" e "Galeria", sem "Câmera". **Não é o código** (todos os outros aparelhos funcionam). É config do próprio aparelho: navegador sem **permissão de câmera** no Android, ou app de câmera padrão desativado pra ele. A checar: permissão do navegador / testar outro navegador / app de câmera padrão.
      - ✅ **Workaround do Lucio confirmado**: tirar a foto pelo app de câmera → escolher na galeria → sobe normal (mesma compressão/rotação/upload).
      - ⏳ iPhone: pedido ao "Barça", ainda sem resposta.
- ⬜ **1.6** — Tirar a foto **com o celular em pé** e salvar. → Ela aparece **em pé**, não deitada?
- ⬜ **1.7** — Aba **Fotos** → **"Tirar foto"** → tirar. → A foto **entra na galeria**?
- ⬜ **1.8** — Abrir o **perfil público** da empresa. → A foto aparece lá também?

> Esperado: tudo ✅. O cliente criou a própria conta, então ele é o dono do perfil.

---

## FLUXO 2 — N2 · MODERADOR / AGENTE (Elis)

**Sair da conta. Entrar como `elis@redepublicidade.com.br` / `123456`.**

### 2A — perfil que o AGENTE cadastrou pelo painel

- ⬜ **2.1** — **Dashboard → Empresas → Nova empresa**. Na escolha do nascimento, marcar **"rua"** (não "acervo" — acervo nasce no plano free e **não tem galeria**).
- ⬜ **2.2** — Nome: **"Teste Agente 01"**. Salvar.
- ⬜ **2.3** — Abrir "Teste Agente 01" → aba **Fotos** → **"Tirar foto"** → tirar.
- ⬜ **2.4** — → A foto **entra**? *(Esperado ✅ — cadastrar torna o agente dono do perfil)*

### 2B — perfil do CLIENTE que o agente vendeu pelo link ⚠️ *o ponto crítico*

- ⬜ **2.5** — Ainda como Elis, procurar a empresa **"Teste Cliente 01"** (a do Fluxo 1). → **Ela consegue ENXERGAR?** Em `Minha área → Empresas`? Em `Empresas`?
- ⬜ **2.6** — Se conseguir abrir: aba **Fotos** → tentar subir uma foto.
- ⬜ **2.7** — → **O que aparece?** *(Minha previsão: ❌ "Você não tem permissão para gerenciar as fotos dessa empresa" — porque no link quem cria a conta é o CLIENTE, e o agente entra só como `sold_by`, não como membro)*

> **Se der erro aqui, é um buraco real do modelo de rua** — o vendedor vende, mas não
> consegue montar o perfil do cliente. Tenho duas correções prontas; escolhemos depois
> do teste.

---

## FLUXO 3 — N3 · ADMIN / SUPER ADMIN (você)

**Sair. Entrar como `redebaixada@gmail.com` / `123456`.**

- ⬜ **3.1** — Criar **"Teste Admin 01"** (nascimento **"rua"**) → aba Fotos → **"Tirar foto"** → entra? *(perfil que VOCÊ criou)*
- ⬜ **3.2** — Abrir **"Teste Cliente 01"** → subir foto. → Entra? *(perfil do CLIENTE — esperado ✅, é a correção de hoje)*
- ⬜ **3.3** — Abrir **"Teste Agente 01"** → subir foto. → Entra? *(perfil da ELIS — esperado ✅)*

---

## EXTRAS (se sobrar fôlego)

- ⬜ **4.1** — **No 4G da rua**, fora do wi-fi: repetir 3.1. → Trava em "Enviando..." por mais de 30 s?
- ⬜ **4.2** — Num **iPhone**: repetir 1.5–1.7. → Aparece algum aviso sobre **HEIC**? *(é o cenário que eu não consigo reproduzir aqui)*
- ⬜ **4.3** — Pegar uma foto **velha e pesada** do rolo (não tirar na hora): entra sem reclamar de tamanho?
- ⬜ **4.4** — Criar um **classificado com 5 fotos**: as 5 entram e a 6ª avisa o limite?

---

## LIMPEZA (no fim)

- ⬜ **5.1** — Apagar **Teste Cliente 01**, **Teste Agente 01**, **Teste Admin 01**.

---

## Já comprovado (não precisa refazer)

- Foto de 8,3 MB (4000×3000) → ~500 KB em ~0,4 s
- Foto com marca de rotação sai **em pé**
- Logo PNG mantém fundo **transparente**
- Admin sobe foto em empresa que **não criou** ← a correção de RLS de hoje
- Botão "Tirar foto" presente no celular, com `capture=environment`

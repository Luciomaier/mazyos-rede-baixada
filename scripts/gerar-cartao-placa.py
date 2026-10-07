#!/usr/bin/env python3
"""Gera a arte 11 x 16 cm que cobre a placa inteira (impressão em plotter, por metro).

Uso (um cartão):
  python3 scripts/gerar-cartao-placa.py --codigo RB7K3M --nome "Salão Belle Concept Ita" \
      --cidade Itanhaém --fundador --destino google

Uso (lote, direto do CSV que a tela "Placas e chips" exporta; usa codigo,nome,cidade,fundador,destino):
  python3 scripts/gerar-cartao-placa.py --csv dados/placas-piloto.csv --saida marketing/placa-prototipo/lote

Modelos (--modelo, ou coluna "modelo" no CSV): "classico" (padrão: estrelas + QR, fundo branco) e
"fundador" (Edição Fundador: fundo azul-noite, coroa dourada, praça em destaque, "Nº 007 de 100"),
"google" (100% foco no Google, VIBRANTE: fundo azul Google com formas coloridas, "Google" gigante, QR grande; só destino google),
"google-claro" (a mesma ideia em fundo claro, mais sóbria) e
"futurista" (fundo escuro estilo HUD, grade em perspectiva, brilho ciano). google e futurista não falam de fundador.
O modelo fundador só sai pra quem é Fundador e exige cidade; o número (--numero, coluna "numero") é opcional
e tem que ser o REAL (ordem dos 100 da cidade) — sem número, a placa diz "Uma das 100 primeiras".
--verificado (coluna "verificado") acrescenta "Verificada em visita pela Rede Baixada": só pra quem a visita confirmou.

Tamanho = o da placa (110 x 160 mm, em pé), sem margem: a faixa azul vai até a borda. Imprimir em 100% / tamanho real.
Com --sangria 2: a arte cresce 2 mm em cada lado (114 x 164 mm) pra o corte não deixar fio branco; cortar nos 110 x 160.
Saída: PDF vetorial (uma página por placa) + PNG de 300 dpi (só pra conferir).
O QR aponta pra https://redebaixada.com.br/p/CODIGO?s=qr. O chip NFC leva ?s=nfc (texto impresso no fim).
O código tem que existir na tabela `placas`; esta ferramenta NÃO cria código no banco.
"""
import argparse, base64, csv, html, os, shutil, subprocess, sys, tempfile
import qrcode

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARCA = os.path.join(RAIZ, "identidade", "marca.svg")  # vetor original; os PNG exportados saem cortados embaixo
FONTES = os.path.join(RAIZ, "scripts", "fonts")
BASE_URL = "https://redebaixada.com.br/p/"
ALFABETO = set("ABCDEFGHJKMNPQRSTUVWXYZ23456789")  # sem 0 O 1 I L


def qr_path(url):
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, box_size=1, border=0)
    q.add_data(url)
    q.make(fit=True)
    m = q.get_matrix()
    d = "".join("M%d,%dh1v1h-1z" % (x, y) for y, row in enumerate(m) for x, v in enumerate(row) if v)
    return len(m), d


def b64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


STAR = '<svg viewBox="0 0 24 24"><path fill="#FBBC04" d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"/></svg>'
NFC = ('<svg viewBox="0 0 48 48" fill="none" stroke="#1791CF" stroke-width="3" stroke-linecap="round" stroke-linejoin="round">'
       '<rect x="13" y="14" width="16" height="28" rx="3"/><path d="M19 38h4"/><path d="M33 20c2.2 2.4 2.2 6.6 0 9"/>'
       '<path d="M37 16c4 4.6 4 12.4 0 17"/><path d="M41 12c5.6 6.8 5.6 17.2 0 24"/></svg>')


def verdadeiro(v):
    return str(v or "").strip().lower() in ("1", "sim", "true", "x", "s")


def codigo_valido(p):
    code = p["codigo"].strip().upper()
    if len(code) != 6 or not set(code) <= ALFABETO:
        sys.exit("Código inválido: %r (6 caracteres, sem 0, O, 1, I, L)" % code)
    return code


def cartao(p, logo_uri):
    modelo = (p.get("modelo") or "classico").strip().lower()
    feitos = {"fundador": cartao_fundador, "google": cartao_google, "google-claro": cartao_google_claro, "futurista": cartao_futurista, "classico": cartao_classico}
    if modelo not in feitos:
        sys.exit("Modelo desconhecido: %r (use %s)" % (modelo, ", ".join(feitos)))
    return feitos[modelo](p, logo_uri)


def cartao_classico(p, logo_uri):
    code = codigo_valido(p)
    n, d = qr_path(BASE_URL + code + "?s=qr")
    google = (p.get("destino") or "google") == "google"
    nome = html.escape((p.get("nome") or "").strip())
    cidade = html.escape((p.get("cidade") or "").strip())
    fundador = str(p.get("fundador", "")).strip().lower() in ("1", "sim", "true", "x", "s")
    sub = ("Fundador · " + cidade) if (fundador and cidade) else cidade
    bloco_nome = ('<div class="nome">%s</div>' % nome + ('<div class="sub">%s</div>' % sub if sub else "")) if nome else ""
    estrelas = STAR * 5 if google else ""
    head = "Avalie nossa empresa<br>no Google" if google else "Conheça nosso perfil<br>no Rede Baixada"
    return f"""<div class="pg"><section class="card">
  <div class="nfc">{NFC}<span>Aproxime o celular</span></div>
  <div class="stars">{estrelas}</div>
  <div class="head">{head}</div>
  <div class="frame">
    {bloco_nome}
    <svg class="qr" viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><rect width="{n}" height="{n}" fill="#fff"/><path d="{d}" fill="#000"/></svg>
    <div class="code">{code}</div>
  </div>
  <div class="read">ou leia o QR com a câmera</div>
  <div class="sign"><div class="lock"><img src="{logo_uri}"><b class="rede">Rede</b><b class="baixada">Baixada</b></div><span>redebaixada.com.br</span></div>
  <div class="band"></div>
</section></div>"""


CROWN = ('<svg class="crown" viewBox="0 0 64 50"><defs><linearGradient id="ouro" x1="0" y1="0" x2="0" y2="1">'
         '<stop offset="0" stop-color="#F7E6A6"/><stop offset=".45" stop-color="#D9AE49"/><stop offset=".75" stop-color="#A97C1F"/><stop offset="1" stop-color="#E6C976"/></linearGradient></defs>'
         '<path fill="url(#ouro)" d="M5 40 L2 13 L18 27 L32 7 L46 27 L62 13 L59 40 Z"/>'
         '<rect x="6" y="43" width="52" height="5" rx="1.5" fill="url(#ouro)"/>'
         '<circle cx="2" cy="11" r="2.6" fill="url(#ouro)"/><circle cx="32" cy="4.5" r="3" fill="url(#ouro)"/><circle cx="62" cy="11" r="2.6" fill="url(#ouro)"/></svg>')
# "Google" nas cores da marca, letra a letra (é o que o cliente reconhece de longe)
GOOGLE = "".join('<i style="color:%s">%s</i>' % (c, l) for l, c in zip("Google", ("#4C8DF6", "#F25A4B", "#FBBC04", "#4C8DF6", "#3DBA5E", "#F25A4B")))
STAR_OURO = STAR.replace("#FBBC04", "#E6C26A")
NFC_OURO = NFC.replace("#1791CF", "#E6C26A")
MOLDURA = ('<svg class="f-frame" viewBox="0 0 110 160" preserveAspectRatio="none">'
           '<rect x="4" y="4" width="102" height="152" rx="4" fill="none" stroke="url(#ouro)" stroke-width=".55"/>'
           '<rect x="5.8" y="5.8" width="98.4" height="148.4" rx="2.8" fill="none" stroke="url(#ouro)" stroke-width=".25"/></svg>')


def cartao_fundador(p, logo_uri):
    code = codigo_valido(p)
    if not verdadeiro(p.get("fundador")):
        sys.exit("Modelo fundador é só pra Fundador (placa %s não tem fundador=sim)." % code)
    cidade = (p.get("cidade") or "").strip()
    nome = (p.get("nome") or "").strip()
    if not cidade or not nome:
        sys.exit("Modelo fundador exige nome e cidade (placa %s): a coroa nomeia a praça." % code)
    num = str(p.get("numero") or "").strip()
    if num and not (num.isdigit() and 1 <= int(num) <= 100):
        sys.exit("Número inválido na placa %s: %r (1 a 100, a ordem dos Fundadores da cidade)." % (code, num))
    n, d = qr_path(BASE_URL + code + "?s=qr")
    google = (p.get("destino") or "google") == "google"
    selo = ('<div class="f-num"><i></i><span>Nº %03d <em>de 100</em></span><i></i></div>' % int(num)) if num \
        else '<div class="f-num"><i></i><span>Uma das <em>100 primeiras</em></span><i></i></div>'
    estrelas = (STAR_OURO * 5) if google else ""
    head = ('Avalie nossa empresa no<span class="f-google">%s</span>' % GOOGLE) if google else "Conheça nosso perfil<br>no Rede Baixada"
    verif = '<div class="f-verif">&#10003; Verificada em visita pela Rede Baixada</div>' if verdadeiro(p.get("verificado")) else ""
    return f"""<div class="pg fund"><section class="card f">
  {MOLDURA}
  <div class="f-col">
    {CROWN}
    <div class="f-kicker">Empresa Fundadora</div>
    <div class="f-city">{html.escape(cidade)}</div>
    {selo}
    <div class="f-name">{html.escape(nome)}</div>
    <div class="f-stars">{estrelas}</div>
    <div class="f-head">{head}</div>
    <div class="f-tile">
      <svg class="qr" viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><rect width="{n}" height="{n}" fill="#fff"/><path d="{d}" fill="#000"/></svg>
      <div class="code">{code}</div>
    </div>
    <div class="f-nfc">{NFC_OURO}<span>Aproxime o celular ou leia o QR</span></div>
    {verif}
    <div class="f-sign"><img src="{logo_uri}"><b class="rede">Rede</b><b class="baixada">Baixada</b></div>
  </div>
  <div class="f-band"><span>redebaixada.com.br</span></div>
</section></div>"""


# ---- modelos "google" (claro, foco total) e "futurista" (escuro, HUD) ----
GOOGLE_CORES = ("#4285F4", "#EA4335", "#FBBC04", "#34A853")
GOOGLE_G = "".join('<i style="color:%s">%s</i>' % (c, l) for l, c in zip("Google", ("#4285F4", "#EA4335", "#FBBC04", "#4285F4", "#34A853", "#EA4335")))
GOOGLE_NEON = "".join('<i style="color:%s">%s</i>' % (c, l) for l, c in zip("Google", ("#5E9BFF", "#FF5F52", "#FFC933", "#5E9BFF", "#46D06E", "#FF5F52")))  # versão mais viva pro fundo escuro
STAR_G = STAR  # amarelo Google #FBBC04
NFC_AZUL = NFC.replace("#1791CF", "#1967D2")
NFC_CIANO = NFC.replace("#1791CF", "#30BAE8")


def cantos(cores, w, h, r=3.2, g=1.6, sw=.7):
    """4 cantoneiras (L) em volta de um retângulo w x h; cores = 1 ou 4 cores (sup.esq, sup.dir, inf.dir, inf.esq)."""
    cores = list(cores) * (4 if len(cores) == 1 else 1)
    L = r * 2
    ps = [("M%g,%g v%g M%g,%g h%g" % (g, g + L, -L, g, g, L)),
          ("M%g,%g h%g M%g,%g v%g" % (w - g - L, g, L, w - g, g, L)),
          ("M%g,%g v%g M%g,%g h%g" % (w - g, h - g - L, L, w - g, h - g, -L)),
          ("M%g,%g h%g M%g,%g v%g" % (g + L, h - g, -L, g, h - g, -L))]
    return "".join('<path d="%s" fill="none" stroke="%s" stroke-width="%g" stroke-linecap="round"/>' % (d, c, sw) for d, c in zip(ps, cores))


def cartao_google_claro(p, logo_uri):
    code = codigo_valido(p)
    if (p.get("destino") or "google") != "google":
        sys.exit("Modelo google/google-claro exige destino=google (placa %s)." % code)
    nome = html.escape((p.get("nome") or "").strip())
    n, d = qr_path(BASE_URL + code + "?s=qr")
    frase = ('Como foi sua experiência com<br><b>%s</b>?' % nome) if nome else "Como foi sua experiência?<br>Conta pra gente."
    qw, qh = 51, 51  # cartão do QR (mm)
    return f"""<div class="pg gg"><section class="card g">
  <div class="g-col">
    <div class="g-pill">{NFC_AZUL}<span>Toque ou leia o QR</span></div>
    <div class="g-lead">Sua opinião no</div>
    <div class="g-word">{GOOGLE_G}</div>
    <div class="g-stars">{STAR_G * 5}</div>
    <div class="g-txt">{frase}</div>
    <div class="g-qrwrap">
      <svg class="g-cant" viewBox="0 0 {qw + 8} {qh + 12}">{cantos(GOOGLE_CORES, qw + 8, qh + 12, r=4.5, g=.8, sw=1)}</svg>
      <div class="g-qr"><svg class="qr" viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><rect width="{n}" height="{n}" fill="#fff"/><path d="{d}" fill="#000"/></svg><div class="code">{code}</div></div>
    </div>
    <div class="g-sign"><img src="{logo_uri}"><b class="rede">Rede</b><b class="baixada">Baixada</b></div>
    <div class="g-url">redebaixada.com.br</div>
  </div>
  <div class="g-stripe"><i style="background:#4285F4"></i><i style="background:#EA4335"></i><i style="background:#FBBC04"></i><i style="background:#34A853"></i></div>
</section></div>"""


def cartao_google(p, logo_uri):
    """Vibrante: fundo azul Google, formas nas 4 cores, 'Google' colorido numa placa branca, QR grande."""
    code = codigo_valido(p)
    if (p.get("destino") or "google") != "google":
        sys.exit("Modelo google/google-claro exige destino=google (placa %s)." % code)
    nome = html.escape((p.get("nome") or "").strip())
    n, d = qr_path(BASE_URL + code + "?s=qr")
    frase = ('Como foi sua experiência com<br><b>%s</b>?' % nome) if nome else "Como foi sua experiência?<br>Conta pra gente."
    formas = ('<svg class="v-shapes" viewBox="0 0 110 160" overflow="visible">'
              '<circle cx="-2" cy="14" r="23" fill="#EA4335"/><circle cx="116" cy="4" r="21" fill="#FBBC04"/><circle cx="104" cy="38" r="7" fill="#34A853"/>'
              '<circle cx="-5" cy="118" r="23" fill="#34A853"/><circle cx="117" cy="128" r="21" fill="#EA4335"/><circle cx="8" cy="92" r="5" fill="#FBBC04"/>'
              '<circle cx="100" cy="100" r="4" fill="#fff" opacity=".55"/><circle cx="5" cy="72" r="3" fill="#fff" opacity=".55"/></svg>')
    return f"""<div class="pg vib"><section class="card v">
  {formas}
  <div class="v-col">
    <div class="v-pill">{NFC_AZUL}<span>Toque ou leia o QR</span></div>
    <div class="v-lead">Avalie nossa empresa no</div>
    <div class="v-plate"><div class="v-word">{GOOGLE_G}</div></div>
    <div class="v-stars">{STAR.replace("#FBBC04", "#FFCA28") * 5}</div>
    <div class="v-txt">{frase}</div>
    <div class="v-qr"><svg class="qr" viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><rect width="{n}" height="{n}" fill="#fff"/><path d="{d}" fill="#000"/></svg><div class="code">{code}</div></div>
  </div>
  <div class="v-foot"><div class="v-sign"><img src="{logo_uri}"><b class="rede">Rede</b><b class="baixada">Baixada</b></div><span>redebaixada.com.br</span></div>
</section></div>"""


def grade_perspectiva():
    """Chão em perspectiva (vetor): linhas que convergem pro ponto de fuga e horizontais que se abrem."""
    vx, vy = 55, 104
    linhas = []
    for i in range(-9, 10):
        linhas.append('<line x1="%g" y1="%g" x2="%g" y2="170"/>' % (vx, vy, vx + i * 17))
    y, passo = vy, 1.6
    while y < 162:
        linhas.append('<line x1="-5" y1="%.2f" x2="115" y2="%.2f"/>' % (y, y))
        y += passo
        passo *= 1.32
    return ('<svg class="x-grid" viewBox="0 0 110 160" preserveAspectRatio="none"><defs><linearGradient id="fade" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="#30BAE8" stop-opacity="0"/><stop offset=".55" stop-color="#30BAE8" stop-opacity=".5"/><stop offset="1" stop-color="#30BAE8" stop-opacity=".8"/></linearGradient></defs>'
            '<g stroke="url(#fade)" stroke-width=".18">%s</g></svg>' % "".join(linhas))


def cartao_futurista(p, logo_uri):
    code = codigo_valido(p)
    google = (p.get("destino") or "google") == "google"
    nome = html.escape((p.get("nome") or "").strip())
    cidade = html.escape((p.get("cidade") or "").strip())
    n, d = qr_path(BASE_URL + code + "?s=qr")
    chip = ('<div class="x-chip"><u></u><span>%s</span>%s</div>' % (nome, ('<em>· %s</em>' % cidade) if cidade else "")) if nome else ""
    if google:
        topo, miolo = "Avalie nossa empresa no", '<div class="x-word">%s</div><div class="x-stars">%s</div>' % (GOOGLE_NEON, STAR_G * 5)
    else:
        topo, miolo = "Conheça nosso perfil no", '<div class="x-word x-rb"><b class="rede">Rede</b><b class="baixada">Baixada</b></div>'
    qw = 42
    return f"""<div class="pg fut"><section class="card x">
  {grade_perspectiva()}
  <svg class="x-hud" viewBox="0 0 110 160" preserveAspectRatio="none">{cantos(("#30BAE8",), 110, 160, r=5, g=4.5, sw=.5)}</svg>
  <div class="x-col">
    <div class="x-nfc">{NFC_CIANO}</div>
    <div class="x-kick">Aproxime o celular</div>
    <div class="x-lead">{topo}</div>
    {miolo}
    {chip}
    <div class="x-qrwrap">
      <svg class="x-cant" viewBox="0 0 {qw + 10} {qw + 15}">{cantos(("#30BAE8",), qw + 10, qw + 15, r=4.5, g=.5, sw=.9)}</svg>
      <div class="x-qr"><svg class="qr" viewBox="0 0 {n} {n}" shape-rendering="crispEdges"><rect width="{n}" height="{n}" fill="#fff"/><path d="{d}" fill="#000"/></svg><div class="code">{code}</div></div>
    </div>
    <div class="x-or">ou leia o QR com a câmera</div>
    <div class="x-sign"><img src="{logo_uri}"><b class="rede">Rede</b><b class="baixada">Baixada</b></div>
  </div>
  <div class="x-bar"><span>redebaixada.com.br</span></div>
</section></div>"""


CSS = """
@page { size: __PW__mm __PH__mm; margin: 0 }
* { box-sizing: border-box; margin: 0; padding: 0 }
html, body { background: #fff }
@font-face { font-family: Inter; font-weight: 100 900; src: url(data:font/woff2;base64,__F1__) format('woff2'); unicode-range: U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, U+02DC, U+2000-206F, U+20AC, U+2122, U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD }
@font-face { font-family: Inter; font-weight: 100 900; src: url(data:font/woff2;base64,__F2__) format('woff2'); unicode-range: U+0100-02BA, U+02BD-02C5, U+02C7-02CC, U+02CE-02D7, U+02DD-02FF, U+0304, U+0308, U+0329, U+1D00-1DBF, U+1E00-1E9F, U+1EF2-1EFF, U+2020, U+20A0-20AB, U+20AD-20C0, U+2113, U+2C60-2C7F, U+A720-A7FF }
.pg { width: __PW__mm; height: __PH__mm; position: relative; overflow: hidden; background: #fff; page-break-after: always; break-after: page }
.pg:last-child { page-break-after: auto; break-after: auto }
.card { position: absolute; left: __S__mm; top: __S__mm; width: __W__mm; height: __H__mm; background: #fff; color: #0A141F; font-family: Inter, 'Liberation Sans', Arial, sans-serif }
.nfc { position: absolute; top: 8mm; left: 0; right: 0; text-align: center }
.nfc svg { width: 13mm; height: 13mm; display: block; margin: 0 auto 1mm }
.nfc span { font-size: 3.5mm; font-weight: 600; color: #0D66A5 }
.stars { position: absolute; top: 29mm; left: 0; right: 0; height: 8.5mm; display: flex; justify-content: center; gap: 1.3mm }
.stars svg { width: 8.5mm; height: 8.5mm }
.head { position: absolute; top: 40mm; left: 0; right: 0; text-align: center; font-size: 6.2mm; line-height: 1.12; font-weight: 800; letter-spacing: -0.02em }
.frame { position: absolute; left: 13mm; right: 13mm; top: 57mm; height: 63mm; border: 0.4mm solid #8FD6F0; border-radius: 3.2mm; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 1.2mm; padding: 2mm 3mm }
.nome { font-size: 4.6mm; font-weight: 800; line-height: 1.1; text-align: center; letter-spacing: -0.01em; max-height: 10.2mm; overflow: hidden }
.sub { font-size: 3.2mm; font-weight: 600; color: #4B5B6E; text-align: center }
.qr { width: 38mm; height: 38mm; display: block }
.code { font-size: 3.6mm; font-weight: 700; letter-spacing: 0.14em }
.read { position: absolute; top: 122mm; left: 0; right: 0; text-align: center; font-size: 3.4mm; font-weight: 500; color: #4B5B6E }
.sign { position: absolute; top: 128.5mm; left: 0; right: 0; text-align: center }
.sign .lock { display: flex; align-items: center; justify-content: center; gap: 2mm; margin-bottom: 1mm }
.sign img { width: 8.5mm; height: 8.5mm; display: block }
.sign b { font-size: 5.4mm; letter-spacing: -0.028em; line-height: 1 }
.sign .rede { font-weight: 700; color: #1791CF }
.sign .baixada { font-weight: 800; color: #F97A1F; margin-left: -1.7mm }
.sign span { font-size: 3.2mm; font-weight: 600 }
.band { position: absolute; left: -__S__mm; right: -__S__mm; bottom: -__S__mm; height: calc(13.5mm + __S__mm); background: #1791CF }
.band::before { content: ''; position: absolute; left: 0; right: 0; top: -2.4mm; height: 2.6mm; background: #8FD6F0; border-radius: 50% 50% 0 0 / 100% 100% 0 0 }

.pg.fund { background: #0A141F }
.card.f { background: radial-gradient(ellipse 85% 42% at 50% 12%, #1B3550 0%, #0A141F 72%); color: #fff }
.f-frame { position: absolute; inset: 0; width: 100%; height: 100% }
.f-col { position: absolute; left: 0; right: 0; top: 9.5mm; bottom: 10mm; display: flex; flex-direction: column; align-items: center; text-align: center }
.crown { width: 17mm; height: 13.3mm; display: block }
.f-kicker { margin-top: 2.2mm; font-size: 2.9mm; font-weight: 700; letter-spacing: .3em; text-transform: uppercase; color: #E6C26A; padding-left: .3em }
.f-city { margin-top: 1.4mm; font-size: 8.6mm; font-weight: 800; letter-spacing: .09em; text-transform: uppercase; line-height: 1; padding-left: .09em }
.f-num { margin-top: 2.6mm; display: flex; align-items: center; gap: 2.4mm; width: 78mm }
.f-num i { flex: 1; height: .3mm; background: linear-gradient(90deg, transparent, #D9AE49) }
.f-num i:last-child { background: linear-gradient(90deg, #D9AE49, transparent) }
.f-num span { font-size: 4mm; font-weight: 800; letter-spacing: .06em; color: #F2D88B; white-space: nowrap }
.f-num em { font-style: normal; font-weight: 600; font-size: 3.2mm; letter-spacing: .04em; color: #C9D6E2 }
.f-name { margin-top: 4.2mm; font-size: 5.6mm; font-weight: 800; line-height: 1.1; letter-spacing: -.01em; max-width: 84mm; max-height: 12.4mm; overflow: hidden }
.f-stars { margin-top: 3.6mm; height: 5.6mm; display: flex; gap: 1mm }
.f-stars svg { width: 5.6mm; height: 5.6mm }
.f-head { margin-top: 1.2mm; font-size: 4.2mm; font-weight: 700; line-height: 1.1; color: #E8EEF4 }
.f-google { display: block; margin-top: .6mm; font-size: 8.4mm; font-weight: 800; letter-spacing: -.03em; line-height: 1 }
.f-google i { font-style: normal }
.f-tile { margin-top: 3mm; background: #fff; color: #0A141F; border-radius: 3mm; padding: 3mm 3mm 2mm; display: flex; flex-direction: column; align-items: center; gap: .8mm; box-shadow: 0 0 0 .6mm #D9AE49 }
.f-tile .qr { width: 33mm; height: 33mm }
.f-tile .code { font-size: 3.2mm }
.f-nfc { margin-top: 3mm; display: flex; align-items: center; gap: 1.8mm }
.f-nfc svg { width: 5.6mm; height: 5.6mm }
.f-nfc span { font-size: 3mm; font-weight: 600; color: #C9D6E2 }
.f-verif { margin-top: 2mm; margin-bottom: 2mm; font-size: 2.8mm; font-weight: 600; color: #E6C26A; letter-spacing: .02em }
.f-sign { margin-top: auto; display: flex; align-items: center; gap: 1.6mm }
.f-sign img { width: 7mm; height: 7mm }
.f-sign b { font-size: 4.8mm; letter-spacing: -.028em; line-height: 1 }
.f-sign .rede { font-weight: 700; color: #fff }
.f-sign .baixada { font-weight: 800; color: #F97A1F; margin-left: -1.5mm }
.f-band { position: absolute; left: -__S__mm; right: -__S__mm; bottom: -__S__mm; height: calc(8mm + __S__mm); background: #1791CF; display: flex; align-items: center; justify-content: center; padding-bottom: 0 }
.f-band span { font-size: 3mm; font-weight: 700; letter-spacing: .06em; color: #fff; margin-top: -__S__mm }
.f-band::before { content: ''; position: absolute; left: 0; right: 0; top: -1.6mm; height: 1.8mm; background: #8FD6F0; border-radius: 50% 50% 0 0 / 100% 100% 0 0 }

/* ---- google (claro) ---- */
.pg.gg { background: radial-gradient(ellipse 120% 55% at 50% 0%, #E8F0FE 0%, #FFFFFF 62%) }
.card.g { background: transparent }
.g-col { position: absolute; left: 0; right: 0; top: 9mm; bottom: 7mm; display: flex; flex-direction: column; align-items: center; text-align: center }
.g-pill { display: flex; align-items: center; gap: 1.6mm; padding: 1.3mm 4mm 1.3mm 3mm; border-radius: 6mm; background: #E8F0FE; border: .3mm solid #C6DAFC }
.g-pill svg { width: 5mm; height: 5mm }
.g-pill span { font-size: 3mm; font-weight: 700; color: #1967D2; letter-spacing: .02em }
.g-lead { margin-top: 5mm; font-size: 5.2mm; font-weight: 700; color: #0A141F; letter-spacing: -.01em }
.g-word { font-size: 21mm; font-weight: 800; letter-spacing: -.045em; line-height: .95; margin-top: .6mm }
.g-word i { font-style: normal }
.g-stars { margin-top: 2.6mm; display: flex; gap: 1.2mm }
.g-stars svg { width: 9mm; height: 9mm }
.g-txt { margin-top: 3mm; font-size: 3.7mm; line-height: 1.28; color: #4B5B6E; font-weight: 500; max-width: 82mm }
.g-txt b { color: #0A141F; font-weight: 800 }
.g-qrwrap { position: relative; margin-top: 3.6mm; width: 59mm; height: 63mm; display: flex; align-items: center; justify-content: center }
.g-cant { position: absolute; inset: 0; width: 100%; height: 100% }
.g-qr { width: 51mm; background: #fff; border-radius: 3.2mm; padding: 3.4mm 3.4mm 2mm; display: flex; flex-direction: column; align-items: center; gap: .6mm; box-shadow: 0 .6mm 3mm rgba(10,20,31,.16) }
.g-qr .qr { width: 44mm; height: 44mm }
.g-qr .code { font-size: 3.2mm; font-weight: 700; letter-spacing: .14em; color: #0A141F }
.g-sign { margin-top: auto; display: flex; align-items: center; gap: 1.6mm }
.g-sign img { width: 6.4mm; height: 6.4mm }
.g-sign b { font-size: 4.6mm; letter-spacing: -.028em; line-height: 1 }
.g-sign .rede { font-weight: 700; color: #1791CF }
.g-sign .baixada { font-weight: 800; color: #F97A1F; margin-left: -1.5mm }
.g-url { margin-top: .6mm; font-size: 2.8mm; font-weight: 600; color: #4B5B6E }
.g-stripe { position: absolute; left: -__S__mm; right: -__S__mm; bottom: -__S__mm; height: calc(2.6mm + __S__mm); display: flex }
.g-stripe i { flex: 1 }
/* ---- futurista (escuro, HUD) ---- */
.pg.fut { background: #050B14 }
.card.x { background: transparent; color: #fff }
.pg.fut::before { content: ''; position: absolute; inset: 0; background: radial-gradient(ellipse 70% 38% at 50% 8%, rgba(48,186,232,.28) 0%, rgba(5,11,20,0) 70%), radial-gradient(ellipse 80% 30% at 50% 78%, rgba(23,145,207,.30) 0%, rgba(5,11,20,0) 70%) }
.x-grid, .x-hud { position: absolute; inset: 0; width: 100%; height: 100% }
.x-col { position: absolute; left: 0; right: 0; top: 9mm; bottom: 11.5mm; display: flex; flex-direction: column; align-items: center; text-align: center }
.x-nfc svg { width: 14mm; height: 14mm; display: block }
.x-kick { margin-top: 1.4mm; font-size: 2.8mm; font-weight: 700; letter-spacing: .34em; text-transform: uppercase; color: #30BAE8; padding-left: .34em }
.x-lead { margin-top: 3.8mm; font-size: 3.5mm; font-weight: 700; letter-spacing: .2em; text-transform: uppercase; color: #C9D6E2; padding-left: .2em }
.x-word { margin-top: .6mm; font-size: 18mm; font-weight: 800; letter-spacing: -.045em; line-height: .98 }
.x-word i { font-style: normal }
.x-rb b { font-size: 13mm; letter-spacing: -.03em }
.x-rb .rede { color: #fff } .x-rb .baixada { color: #F97A1F; margin-left: -2.4mm }
.x-stars { margin-top: 2mm; display: flex; gap: 1.2mm }
.x-stars svg { width: 6.4mm; height: 6.4mm }
.x-chip { margin-top: 3mm; display: flex; align-items: center; gap: 2mm; padding: 1.5mm 5mm; border: .3mm solid rgba(48,186,232,.7); border-radius: 8mm; background: rgba(48,186,232,.10) }
.x-chip u { width: 1.8mm; height: 1.8mm; border-radius: 50%; background: #30BAE8; display: block }
.x-chip span { font-size: 4mm; font-weight: 800 }
.x-chip em { font-style: normal; font-size: 3.2mm; font-weight: 600; color: #9FB3C8 }
.x-qrwrap { position: relative; margin-top: 3.2mm; width: 52mm; height: 57mm; display: flex; align-items: center; justify-content: center }
.x-cant { position: absolute; inset: 0; width: 100%; height: 100% }
.x-qr { width: 42mm; background: #fff; border-radius: 1.6mm; padding: 2.6mm 2.6mm 1.6mm; display: flex; flex-direction: column; align-items: center; gap: .5mm; color: #0A141F }
.x-qr .qr { width: 36.8mm; height: 36.8mm }
.x-qr .code { font-size: 3mm; font-weight: 700; letter-spacing: .16em }
.x-or { margin-top: 1mm; font-size: 2.7mm; font-weight: 600; letter-spacing: .08em; color: #9FB3C8 }
.x-sign { margin-top: auto; display: flex; align-items: center; gap: 1.6mm }
.x-sign img { width: 6.4mm; height: 6.4mm }
.x-sign b { font-size: 4.6mm; letter-spacing: -.028em; line-height: 1 }
.x-sign .rede { font-weight: 700; color: #fff }
.x-sign .baixada { font-weight: 800; color: #F97A1F; margin-left: -1.5mm }
.x-bar { position: absolute; left: -__S__mm; right: -__S__mm; bottom: -__S__mm; height: calc(7mm + __S__mm); background: linear-gradient(90deg, #0D66A5, #1791CF 50%, #30BAE8); display: flex; align-items: center; justify-content: center }
.x-bar span { font-size: 2.9mm; font-weight: 700; letter-spacing: .12em; color: #fff; margin-top: -__S__mm }

/* ---- google vibrante ---- */
.pg.vib { background: linear-gradient(180deg, #5A98FF 0%, #3B78EC 55%, #2A63D6 100%) }
.card.v { background: transparent; color: #fff }
.v-shapes { position: absolute; inset: 0; width: 100%; height: 100%; overflow: visible }
.v-col { position: absolute; left: 0; right: 0; top: 8mm; bottom: 19mm; display: flex; flex-direction: column; align-items: center; text-align: center }
.v-pill { display: flex; align-items: center; gap: 1.6mm; padding: 1.4mm 4.2mm 1.4mm 3.2mm; border-radius: 6mm; background: #fff }
.v-pill svg { width: 5mm; height: 5mm }
.v-pill span { font-size: 3.1mm; font-weight: 800; color: #1967D2; letter-spacing: .02em }
.v-lead { margin-top: 3.6mm; font-size: 4.8mm; font-weight: 800; color: #fff; letter-spacing: -.01em }
.v-plate { margin-top: 2.4mm; background: #fff; border-radius: 6mm; width: 88mm; padding: 2.4mm 0 3mm; box-shadow: 0 1.2mm 0 rgba(10,20,31,.18) }
.v-word { font-size: 22mm; font-weight: 800; letter-spacing: -.045em; line-height: .98 }
.v-word i { font-style: normal }
.v-stars { margin-top: 2.6mm; display: flex; gap: 1.2mm }
.v-stars svg { width: 8.4mm; height: 8.4mm }
.v-txt { margin-top: 2.4mm; font-size: 3.8mm; line-height: 1.26; font-weight: 500; color: rgba(255,255,255,.95); max-width: 84mm }
.v-txt b { font-weight: 800; color: #fff }
.v-qr { margin-top: 3.4mm; width: 53mm; background: #fff; border-radius: 4.4mm; padding: 3.6mm 3.6mm 2.2mm; display: flex; flex-direction: column; align-items: center; gap: .6mm; color: #0A141F; box-shadow: 0 1.2mm 0 rgba(10,20,31,.18) }
.v-qr .qr { width: 45.8mm; height: 45.8mm }
.v-qr .code { font-size: 3.2mm; font-weight: 700; letter-spacing: .14em }
.v-foot { position: absolute; left: -__S__mm; right: -__S__mm; bottom: -__S__mm; height: calc(16mm + __S__mm); background: #fff; border-radius: 6mm 6mm 0 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: .5mm; padding-bottom: 0 }
.v-foot > * { position: relative; top: -__S__mm }
.v-sign { display: flex; align-items: center; gap: 1.6mm }
.v-sign img { width: 6.6mm; height: 6.6mm }
.v-sign b { font-size: 4.8mm; letter-spacing: -.028em; line-height: 1 }
.v-sign .rede { font-weight: 700; color: #1791CF }
.v-sign .baixada { font-weight: 800; color: #F97A1F; margin-left: -1.5mm }
.v-foot span { font-size: 2.9mm; font-weight: 700; color: #4B5B6E }
"""


W, H = 110, 160  # mm: tamanho da placa (em pé)


def renderizar(paginas, saida_base, sangria=0):
    pw, ph = W + 2 * sangria, H + 2 * sangria
    logo_uri = "data:image/svg+xml;base64," + b64(MARCA)
    css = CSS.replace("__F1__", b64(os.path.join(FONTES, "inter-latin.woff2"))).replace("__F2__", b64(os.path.join(FONTES, "inter-latin-ext.woff2")))
    for k, v in (("__PW__", pw), ("__PH__", ph), ("__S__", sangria), ("__W__", W), ("__H__", H)):
        css = css.replace(k, str(v))
    corpo = "\n".join(cartao(p, logo_uri) for p in paginas)
    doc = "<!doctype html><meta charset='utf-8'><title>Placa 11 x 16 cm</title><style>%s</style>%s" % (css, corpo)
    chromium = shutil.which("chromium") or shutil.which("chromium-browser") or shutil.which("google-chrome")
    if not chromium:
        sys.exit("Chromium não encontrado.")
    os.makedirs(os.path.dirname(os.path.abspath(saida_base)), exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        h = os.path.join(tmp, "c.html")
        with open(h, "w", encoding="utf-8") as f:
            f.write(doc)
        # perfil temporário: nunca encosta no Chrome aberto do usuário
        base = [chromium, "--headless=new", "--disable-gpu", "--no-sandbox", "--user-data-dir=" + os.path.join(tmp, "perfil"), "--hide-scrollbars"]
        subprocess.run(base + ["--no-pdf-header-footer", "--print-to-pdf=" + saida_base + ".pdf", "file://" + h],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
        subprocess.run(base + ["--window-size=500,800", "--force-device-scale-factor=3.125", "--screenshot=" + saida_base + ".png", "file://" + h],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    from PIL import Image
    caixa = (0, 0, round(pw / 25.4 * 300), round(ph / 25.4 * 300))
    im = Image.open(saida_base + ".png").crop(caixa)
    im.save(saida_base + ".png", dpi=(300, 300))
    return saida_base + ".pdf", saida_base + ".png"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--codigo"); ap.add_argument("--nome"); ap.add_argument("--cidade")
    ap.add_argument("--fundador", action="store_true"); ap.add_argument("--destino", default="google", choices=["google", "perfil"])
    ap.add_argument("--modelo", default=None, choices=["classico", "fundador", "google", "google-claro", "futurista"], help="classico (padrão), fundador (azul-noite com coroa), google (vibrante, foco total no Google), google-claro ou futurista (escuro, HUD)")
    ap.add_argument("--numero", help="Nº do Fundador na cidade (1 a 100), só no modelo fundador")
    ap.add_argument("--verificado", action="store_true", help="imprime 'Verificada em visita pela Rede Baixada' (só se a visita aconteceu)")
    ap.add_argument("--csv"); ap.add_argument("--saida", default=None)
    ap.add_argument("--incluir-sem-dono", action="store_true", help="no CSV, imprime também as placas sem empresa (só QR e código)")
    ap.add_argument("--forcar-destino", choices=["google", "perfil"], help="ignora o destino do CSV: define a chamada de TODOS os cartões")
    ap.add_argument("--sangria", type=float, default=0, help="mm de sangria em cada lado (ex.: 2). Padrão 0 = arte exatamente do tamanho da placa")
    a = ap.parse_args()
    if a.csv:
        with open(a.csv, newline="", encoding="utf-8-sig") as f:  # utf-8-sig: o CSV da tela vem com BOM
            paginas = list(csv.DictReader(f))
        if a.modelo:
            for p in paginas:
                p["modelo"] = a.modelo
        if a.forcar_destino:
            for p in paginas:
                p["destino"] = a.forcar_destino
        if not a.incluir_sem_dono:
            sem_dono = [p for p in paginas if not (p.get("nome") or "").strip()]
            paginas = [p for p in paginas if (p.get("nome") or "").strip()]
            if sem_dono:
                print("Pulei %d placa(s) sem empresa (use --incluir-sem-dono pra imprimir o cartão só com QR e código)." % len(sem_dono))
        if not paginas:
            sys.exit("Nenhuma linha pra imprimir. Vincule as placas a empresas na tela, ou use --incluir-sem-dono.")
        saida = a.saida or os.path.splitext(a.csv)[0] + "-cartoes"
    elif a.codigo and a.nome and a.cidade:
        paginas = [{"codigo": a.codigo, "nome": a.nome, "cidade": a.cidade, "fundador": "sim" if a.fundador else "", "destino": a.destino,
                    "modelo": a.modelo or "classico", "numero": a.numero or "", "verificado": "sim" if a.verificado else ""}]
        saida = a.saida or os.path.join(RAIZ, "marketing", "placa-prototipo", "cartao-" + a.codigo.upper())
    else:
        ap.error("informe --csv, ou --codigo + --nome + --cidade")
    pdf, png = renderizar(paginas, saida, sangria=a.sangria)
    print("PDF:", pdf); print("PNG (conferência, 1ª página):", png)
    for p in paginas:
        c = p["codigo"].strip().upper()
        print("  %s -> gravar no chip NFC: %s%s?s=nfc" % (c, BASE_URL, c))


if __name__ == "__main__":
    main()

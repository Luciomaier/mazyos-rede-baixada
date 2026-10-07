#!/usr/bin/env python3
"""Gera a arte 11 x 16 cm que cobre a placa inteira (impressão em plotter, por metro).

Uso (um cartão):
  python3 scripts/gerar-cartao-placa.py --codigo RB7K3M --nome "Salão Belle Concept Ita" \
      --cidade Itanhaém --fundador --destino google

Uso (lote, direto do CSV que a tela "Placas e chips" exporta; usa codigo,nome,cidade,fundador,destino):
  python3 scripts/gerar-cartao-placa.py --csv dados/placas-piloto.csv --saida marketing/placa-prototipo/lote

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


def cartao(p, logo_uri):
    code = p["codigo"].strip().upper()
    if len(code) != 6 or not set(code) <= ALFABETO:
        sys.exit("Código inválido: %r (6 caracteres, sem 0, O, 1, I, L)" % code)
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
    ap.add_argument("--csv"); ap.add_argument("--saida", default=None)
    ap.add_argument("--incluir-sem-dono", action="store_true", help="no CSV, imprime também as placas sem empresa (só QR e código)")
    ap.add_argument("--forcar-destino", choices=["google", "perfil"], help="ignora o destino do CSV: define a chamada de TODOS os cartões")
    ap.add_argument("--sangria", type=float, default=0, help="mm de sangria em cada lado (ex.: 2). Padrão 0 = arte exatamente do tamanho da placa")
    a = ap.parse_args()
    if a.csv:
        with open(a.csv, newline="", encoding="utf-8-sig") as f:  # utf-8-sig: o CSV da tela vem com BOM
            paginas = list(csv.DictReader(f))
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
        paginas = [{"codigo": a.codigo, "nome": a.nome, "cidade": a.cidade, "fundador": "sim" if a.fundador else "", "destino": a.destino}]
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

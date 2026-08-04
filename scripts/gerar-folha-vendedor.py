#!/usr/bin/env python3
"""
Gera a folha de rua (frente e verso, A4) personalizada de um vendedor.

Por que existe: a folha v3 tinha o nome, o telefone e o QR do Lucio cravados no
HTML. Cada vendedor novo (Barça, Paulo, Gi, Elis) precisa da MESMA folha com o
crachá dele — senão a venda nasce órfã e a comissão cai no nome errado.

O QR carrega `?k=<chave da oferta>&v=<id do vendedor>`:
  · k  = OFFER_PARCEIRO_KEY, é o que libera o preço de R$77,70
  · v  = crachá do vendedor, é o que faz a venda cair na carteira dele

Os números da página 2 saem do BANCO (regra do Lucio, 27/07: número que não sai
do banco não entra na página) — passe-os por --negocios/--cidades/--anos.

Uso:
  python3 scripts/gerar-folha-vendedor.py \
      --nome "Matheus Freitas" --vendedor-id <uuid> --telefone "(13) 9xxxx-xxxx" \
      --saida marketing/folha-vendas-barca

Gera <saida>.html e <saida>.pdf.
"""
import argparse
import base64
import io
import pathlib
import re
import subprocess
import sys

import qrcode
from qrcode.constants import ERROR_CORRECT_Q

RAIZ = pathlib.Path(__file__).resolve().parent.parent
BASE = RAIZ / "marketing" / "folha-vendas-parceiro-v3.html"

# Confirmada em 01/08/2026 contra o QR real da folha v3 (comparação de matriz).
CHAVE_OFERTA = "b036e660589d546db056951c"
SITE = "https://redebaixada.com.br"


def qr_data_uri(url: str) -> str:
    """QR no mesmo padrão da v3: correção Q, sem borda extra (a moldura é CSS)."""
    qr = qrcode.QRCode(error_correction=ERROR_CORRECT_Q, border=2, box_size=12)
    qr.add_data(url)
    qr.make(fit=True)
    img = qr.make_image(fill_color="#0A141F", back_color="white")
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--nome", required=True, help="nome do vendedor como o cliente vê")
    ap.add_argument("--vendedor-id", required=True, help="uuid do perfil (o ?v= do crachá)")
    ap.add_argument("--telefone", default="", help='ex: "(13) 98155-2646" — vazio omite do rodapé')
    ap.add_argument("--negocios", default="55", help="negócios reais no portal (do banco)")
    ap.add_argument("--cidades", default="4", help="cidades com negócio cadastrado (do banco)")
    # 13 anos = desde 2013, o primeiro anúncio pago (prova no arquivo do Facebook). Decidido em
    # 04/08 pra acabar com as quatro versões que circulavam: "2016" no rodapé do site, "6 anos"
    # no template da folha, "10 anos" aqui e "13 anos" na história.
    ap.add_argument("--anos", default="13 anos", help="tempo de casa (história, não métrica)")
    ap.add_argument("--fotos", default="6", help="fotos do Plano Presença (plans.max_photos)")
    ap.add_argument("--manter-numeros", action="store_true",
                    help="não mexe nos números da pág. 2 — folha idêntica à do Lucio, só troca nome e QR")
    ap.add_argument("--saida", required=True, help="caminho de saída sem extensão")
    a = ap.parse_args()

    if not BASE.exists():
        print(f"erro: folha base não encontrada em {BASE}", file=sys.stderr)
        return 1

    html = BASE.read_text(encoding="utf-8")
    link = f"{SITE}/oferta-parceiro?k={CHAVE_OFERTA}&v={a.vendedor_id}"

    # --- 1. troca o QR (é a 2ª imagem do documento; as outras duas são a logo) ---
    blobs = list(re.finditer(r'data:image/[a-z+]*;base64,[A-Za-z0-9+/=\s]+', html))
    if len(blobs) != 3:
        print(f"erro: esperava 3 imagens na folha base, achei {len(blobs)}", file=sys.stderr)
        return 1
    qr = blobs[1]  # ordem no HTML: logo (pág 1), QR, logo (pág 2)
    html = html[: qr.start()] + qr_data_uri(link) + html[qr.end() :]

    # --- 2. nome do vendedor (linha "Apresentado por" e rodapé) ---
    html = html.replace("Apresentado por <b>Lucio Maier</b>", f"Apresentado por <b>{a.nome}</b>")
    rodape = f"<b>{a.nome}</b>"
    if a.telefone:
        rodape += f" · {a.telefone}"
    rodape += " · redebaixada.com.br"
    html = html.replace(
        "<b>Lucio Maier</b> · (13) 98155-2646 · redebaixada.com.br", rodape
    )

    # --- 3. números da pág. 2 (só com --manter-numeros desligado) ---
    # A folha do Lucio é a referência aprovada; mexer nos números dela é opcional
    # e é decisão comercial dele, não do script.
    if not a.manter_numeros:
        html = html.replace(
            '<b>5 fotos no perfil</b>', f'<b>{a.fotos} fotos no perfil</b>'
        )
        html = html.replace(
            '<div class="prova"><b>100+</b><span>empresas parceiras na Baixada</span></div>',
            f'<div class="prova"><b>{a.negocios}</b><span>negócios no portal, hoje</span></div>',
        )
        html = html.replace(
            '<div class="prova"><b>3</b><span>cidades na região</span></div>',
            f'<div class="prova"><b>{a.cidades}</b><span>cidades na Baixada</span></div>',
        )
        # Por regex, e não por string literal: o template já trocou de "6 anos" pra "13 anos" uma
        # vez (04/08), e um `replace` literal não avisa quando erra o alvo — ele só não substitui,
        # e a folha sai com o número velho sem ninguém notar.
        html = re.sub(
            r'<div class="prova"><b>[^<]*anos</b><span>conectando o comércio local</span></div>',
            f'<div class="prova"><b>{a.anos}</b><span>conectando o comércio local</span></div>',
            html,
        )
    html = html.replace(
        "<title>Folha de Vendas — Parceiro R$77,70 (v3)</title>",
        f"<title>Folha de Vendas — {a.nome} — Parceiro R$77,70</title>",
    )

    saida = pathlib.Path(a.saida)
    if not saida.is_absolute():
        saida = RAIZ / saida
    saida.parent.mkdir(parents=True, exist_ok=True)
    fhtml = saida.with_suffix(".html")
    fpdf = saida.with_suffix(".pdf")
    fhtml.write_text(html, encoding="utf-8")

    chrome = next(
        (c for c in ("chromium", "google-chrome", "chromium-browser")
         if subprocess.run(["which", c], capture_output=True).returncode == 0),
        None,
    )
    if not chrome:
        print("aviso: chromium não encontrado — só o HTML foi gerado", file=sys.stderr)
        return 0

    subprocess.run(
        [chrome, "--headless=new", "--disable-gpu", "--no-sandbox",
         "--no-pdf-header-footer", f"--print-to-pdf={fpdf}", str(fhtml)],
        capture_output=True, timeout=120,
    )
    print(f"link do vendedor: {link}")
    print(f"html: {fhtml}")
    print(f"pdf : {fpdf} ({fpdf.stat().st_size if fpdf.exists() else 0} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

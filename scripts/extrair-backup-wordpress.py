#!/usr/bin/env python3
"""Garimpa o backup do WordPress (https://77.redebaixada.com.br) — 226 empresas.

O backup guarda o que o portal novo não tem: TELEFONE e ENDEREÇO dos clientes
antigos. É a matéria-prima da reconquista por demanda (quem ainda é procurado
no Google, com o contato pra chamar no WhatsApp).

Como funciona:
  1. REST API (index.php?rest_route=/wp/v2/job-listings) pagina as 226:
     slug, título, descrição, categorias (job-types).
  2. O telefone NÃO está no REST — está no HTML: busca cada página
     (?job_listing=<slug>) e extrai tel:, wa.me e o endereço do link do Maps.
  3. Limpa os números do PRÓPRIO PORTAL (o botão de WhatsApp de toda página é
     o (13) 98155-2646 do Lucio; qualquer número presente em >40% das páginas
     é tratado como número do site, não da empresa).
  4. Salva dados/wordpress-backup-empresas.csv e .json.

Uso:  python3 scripts/extrair-backup-wordpress.py
"""

import csv
import html
import json
import re
import time
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

BASE = "https://77.redebaixada.com.br"
REST = BASE + "/index.php?rest_route="
SAIDA = Path(__file__).resolve().parent.parent / "dados"
# Números do portal (não são da empresa) — o WhatsApp genérico do site.
NUMEROS_DO_PORTAL = {"5513981552646", "13981552646", "981552646"}
# E-mails de IMPLANTADOR (contratados pra cadastrar perfis no WP antigo) — o
# Lucio confirmou em 10/08 que NÃO são de cliente. matheus assina 95 perfis,
# negueba 64, redebaixada é o portal, elis_bella é a Elis (equipe). O CSV sai
# com o campo vazio nesses casos; o e-mail real entra na ligação.
EMAILS_DE_IMPLANTADOR = {
    "matheus.silvac137@gmail.com",
    "negueba013.jpg@gmail.com",
    "redebaixada@gmail.com",
    "elis_bella@hotmail.com",
}
CIDADES = [
    "Praia Grande", "Mongaguá", "Mongagua", "Itanhaém", "Itanhaem",
    "Peruíbe", "Peruibe", "São Vicente", "Sao Vicente", "Santos",
    "Guarujá", "Guaruja", "Cubatão", "Cubatao", "Bertioga",
]


def buscar(url: str, tentativas: int = 3) -> str:
    for i in range(tentativas):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "RedeBaixada-garimpo/1.0"})
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.read().decode("utf-8", errors="replace")
        except Exception:
            if i == tentativas - 1:
                raise
            time.sleep(2 * (i + 1))
    return ""


def so_digitos(tel: str) -> str:
    return re.sub(r"\D", "", tel)


def rest_json(rota: str):
    return json.loads(buscar(REST + urllib.parse.quote(rota, safe="/&=?")))


def listar_empresas():
    """Pagina o REST até esgotar (X-WP-Total dizia 226)."""
    todas = []
    pagina = 1
    while True:
        lote = rest_json(f"/wp/v2/job-listings&per_page=100&page={pagina}")
        if not isinstance(lote, list) or not lote:
            break
        todas.extend(lote)
        if len(lote) < 100:
            break
        pagina += 1
    return todas


def mapa_categorias():
    try:
        cats = rest_json("/wp/v2/job-types&per_page=100")
        return {c["id"]: c["name"] for c in cats}
    except Exception:
        return {}


def extrair_pagina(slug: str) -> dict:
    """O que só o HTML tem: telefone, whatsapp e endereço."""
    pagina = buscar(f"{BASE}/?job_listing={urllib.parse.quote(slug)}")

    telefones = []
    for t in re.findall(r'href="tel:([^"]+)"', pagina):
        d = so_digitos(t)
        if d and d not in telefones:
            telefones.append(d)

    whats = []
    for w in re.findall(r'href="[^"]*(?:wa\.me/|api\.whatsapp\.com/send/?\?phone=)(\d+)', pagina):
        if w not in whats:
            whats.append(w)

    # O 1º link maps.google.com/maps?q=... é o endereço da EMPRESA
    # (o do rodapé é google.com/maps/place/Portal+RedeBaixada — outro formato).
    endereco = ""
    m = re.search(r'href="https://maps\.google\.com/maps\?q=([^"&]+)', pagina)
    if m:
        endereco = urllib.parse.unquote_plus(html.unescape(m.group(1)))

    email = ""
    m = re.search(r'href="mailto:([^"?]+)', pagina)
    if m:
        email = html.unescape(m.group(1)).strip()
        if email.lower() in EMAILS_DE_IMPLANTADOR:
            email = ""

    return {"telefones": telefones, "whatsapps": whats, "endereco": endereco, "email": email}


def cidade_do_endereco(endereco: str) -> str:
    for c in CIDADES:
        if c.lower() in endereco.lower():
            return {"Mongagua": "Mongaguá", "Itanhaem": "Itanhaém",
                    "Peruibe": "Peruíbe", "Sao Vicente": "São Vicente",
                    "Guaruja": "Guarujá", "Cubatao": "Cubatão"}.get(c, c)
    return ""


def main():
    SAIDA.mkdir(exist_ok=True)
    cats = mapa_categorias()
    empresas = listar_empresas()
    print(f"REST devolveu {len(empresas)} empresas; garimpando as páginas…")

    resultado = {}
    with ThreadPoolExecutor(max_workers=6) as pool:
        futuros = {pool.submit(extrair_pagina, e["slug"]): e for e in empresas}
        feitos = 0
        for fut in as_completed(futuros):
            e = futuros[fut]
            feitos += 1
            try:
                extra = fut.result()
            except Exception as err:
                extra = {"telefones": [], "whatsapps": [], "endereco": "", "email": "", "erro": str(err)}
            descricao = re.sub(r"<[^>]+>", " ", e.get("content", {}).get("rendered", ""))
            descricao = re.sub(r"\s+", " ", html.unescape(descricao)).strip()
            resultado[e["slug"]] = {
                "slug": e["slug"],
                "nome": html.unescape(e["title"]["rendered"]),
                "categorias": [cats.get(i, str(i)) for i in e.get("job-types", [])],
                "telefones": extra["telefones"],
                "whatsapps": extra["whatsapps"],
                "endereco": extra["endereco"],
                "cidade": cidade_do_endereco(extra["endereco"]),
                "email": extra.get("email", ""),
                "descricao": descricao[:500],
                "url_backup": f"{BASE}/?job_listing={e['slug']}",
                "url_morta_google": f"https://redebaixada.com.br/litoral-sp/{e['slug']}/",
            }
            if feitos % 40 == 0:
                print(f"  {feitos}/{len(empresas)}…")

    # Números que aparecem em >40% das páginas são do SITE, não da empresa.
    contagem = {}
    for r in resultado.values():
        for n in set(r["telefones"] + r["whatsapps"]):
            contagem[n] = contagem.get(n, 0) + 1
    limite = max(3, int(len(resultado) * 0.4))
    do_site = {n for n, q in contagem.items() if q >= limite} | NUMEROS_DO_PORTAL
    for r in resultado.values():
        r["telefones"] = [n for n in r["telefones"] if n not in do_site]
        r["whatsapps"] = [n for n in r["whatsapps"] if n not in do_site]
    print(f"números do site descartados: {sorted(do_site)}")

    (SAIDA / "wordpress-backup-empresas.json").write_text(
        json.dumps(list(resultado.values()), ensure_ascii=False, indent=1))
    with open(SAIDA / "wordpress-backup-empresas.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["slug", "nome", "cidade", "categorias", "telefones",
                    "whatsapps", "email", "endereco", "url_backup"])
        for r in sorted(resultado.values(), key=lambda x: (x["cidade"], x["nome"])):
            w.writerow([r["slug"], r["nome"], r["cidade"], " | ".join(r["categorias"]),
                        " | ".join(r["telefones"]), " | ".join(r["whatsapps"]),
                        r["email"], r["endereco"], r["url_backup"]])

    com_tel = sum(1 for r in resultado.values() if r["telefones"] or r["whatsapps"])
    print(f"\nPRONTO: {len(resultado)} empresas · {com_tel} com telefone próprio")
    print(f"  → {SAIDA/'wordpress-backup-empresas.csv'}")
    print(f"  → {SAIDA/'wordpress-backup-empresas.json'}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Auditoria da conta Asaas — quem está sendo cobrado AGORA, e por quê.

Nasceu do caso Giovani (07/08/2026): cliente Fundador, pagou em julho, e uma cobrança
gêmea pendente ficou no Asaas levando a régua padrão — semanas de "Não registramos o
pagamento" assinado por REDE PUBLICIDADE E TECNOLOGIA, um nome que ele nunca viu.

O que o script responde:
  1. Quantas cobranças pendentes/vencidas existem, de qual negócio cada uma é
     (Rede Baixada × UniMasso × link manual do painel), há quantos dias, de quem.
  2. 🚨 Quais são GÊMEAS — o cliente JÁ PAGOU essa mesma referência e a pendente
     sobrou viva cobrando ele. É o padrão Giovani. Essas se apagam sem dó.
  3. Quais clientes estão com a régua de notificação do Asaas LIGADA
     (notificationDisabled=false) — ou seja, quem o Asaas cobra sozinho.

Uso:
  ASAAS_API_KEY="$(cat ~/.asaas-key)" python3 scripts/auditoria-asaas.py
  python3 scripts/auditoria-asaas.py --chave-arquivo ~/.asaas-key

  Ações (nunca rodam sozinhas — o relatório imprime os comandos prontos):
    --apagar pay_x pay_y        apaga cobranças específicas (mata a régua delas na hora)
    --silenciar cus_x cus_y     desliga TODA notificação Asaas desses clientes
                                (PUT notificationDisabled=true — quem fala com o cliente
                                passa a ser só a gente, via Resend)

Só a leitura é automática. Toda escrita exige ID explícito na linha de comando.
A chave NUNCA deve ir pro git — guarde fora do repositório (ex: ~/.asaas-key).
"""

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime

BASE_URL = os.environ.get("ASAAS_BASE_URL", "https://api.asaas.com/v3")

# Slugs de plano que identificam cobrança da Rede Baixada mesmo nas referências
# antigas (v1/v2, sem o campo `unit` no fim).
PLANOS_RB = {"presenca", "destaque", "movimento", "basico", "premium"}

VIVAS = ("PENDING", "OVERDUE")
PAGAS = ("RECEIVED", "CONFIRMED", "RECEIVED_IN_CASH")


def req(chave: str, path: str, method: str = "GET", body: dict | None = None) -> dict:
    url = f"{BASE_URL}{path}"
    dados = json.dumps(body).encode() if body is not None else None
    r = urllib.request.Request(url, data=dados, method=method)
    r.add_header("access_token", chave)
    r.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(r, timeout=30) as resp:
            return json.loads(resp.read().decode())
    except urllib.error.HTTPError as e:
        corpo = e.read().decode(errors="replace")
        raise SystemExit(f"Asaas {e.code} em {method} {path}: {corpo[:500]}")


def listar_pagamentos(chave: str, status: str) -> list[dict]:
    """Pagina /payments até o fim para um status."""
    tudo, offset = [], 0
    while True:
        pagina = req(chave, f"/payments?status={status}&limit=100&offset={offset}")
        tudo.extend(pagina.get("data", []))
        if not pagina.get("hasMore"):
            return tudo
        offset += 100


def origem_de(p: dict) -> str:
    ref = p.get("externalReference") or ""
    desc = (p.get("description") or "").lower()
    if "|" in ref:
        partes = ref.split("|")
        if (len(partes) > 3 and partes[3] == "rede_baixada") or (
            len(partes) > 1 and partes[1] in PLANOS_RB
        ):
            return "Rede Baixada"
        return f"Outro sistema (ref: {ref[:40]})"
    if "rede baixada" in desc:
        return "Rede Baixada"
    if "unimasso" in desc:
        return "UniMasso"
    if p.get("paymentLink"):
        return "Link de pagamento (painel)"
    return "Manual / sem referência"


def dias_desde(iso: str | None) -> int | None:
    if not iso:
        return None
    try:
        return (date.today() - datetime.strptime(iso, "%Y-%m-%d").date()).days
    except ValueError:
        return None


def moeda(v) -> str:
    return f"R$ {float(v or 0):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--chave-arquivo", help="arquivo contendo a ASAAS_API_KEY (alternativa à env var)")
    ap.add_argument("--apagar", nargs="+", metavar="PAY_ID", help="apaga cobranças específicas")
    ap.add_argument("--silenciar", nargs="+", metavar="CUS_ID",
                    help="desliga a régua Asaas desses clientes (notificationDisabled=true)")
    ap.add_argument("--calibrar", nargs="+", metavar="CUS_ID",
                    help="cirúrgico: desliga só os PAYMENT_OVERDUE (mantém aviso de vencimento e recibo)")
    args = ap.parse_args()

    chave = os.environ.get("ASAAS_API_KEY", "").strip()
    if args.chave_arquivo:
        chave = open(os.path.expanduser(args.chave_arquivo)).read().strip()
    if not chave:
        sys.exit("Falta a chave: exporte ASAAS_API_KEY ou passe --chave-arquivo ~/.asaas-key")

    # ── Ações explícitas ─────────────────────────────────────────────────────────────
    if args.apagar:
        for pid in args.apagar:
            r = req(chave, f"/payments/{pid}", "DELETE")
            print(f"  apagar {pid}: {'✅ apagada (régua morta)' if r.get('deleted') else r}")
        return
    if args.silenciar:
        for cid in args.silenciar:
            r = req(chave, f"/customers/{cid}", "PUT", {"notificationDisabled": True})
            ok = r.get("notificationDisabled") is True
            print(f"  silenciar {cid} ({r.get('name', '?')}): {'✅ régua desligada' if ok else r}")
        return
    if args.calibrar:
        # A régua da casa: some a cobrança de atraso (PAYMENT_OVERDUE offset 0 e offset 7 —
        # a de 7 repete pra sempre e a de 0 aciona robô de voz). Ficam de pé o aviso de
        # vencimento, o link da cobrança e o recibo — o que o cliente quer receber.
        for cid in args.calibrar:
            notifs = req(chave, f"/customers/{cid}/notifications").get("data", [])
            atrasos = [n for n in notifs if n.get("event") == "PAYMENT_OVERDUE" and n.get("enabled")]
            if not atrasos:
                print(f"  calibrar {cid}: já estava sem cobrança de atraso")
                continue
            req(chave, "/notifications/batch", "PUT", {
                "customer": cid,
                "notifications": [{"id": n["id"], "enabled": False} for n in atrasos],
            })
            print(f"  calibrar {cid}: ✅ {len(atrasos)} PAYMENT_OVERDUE desligados "
                  f"(aviso de vencimento e recibo mantidos)")
        return

    # ── Relatório ────────────────────────────────────────────────────────────────────
    print(f"Conta: {BASE_URL}\n")
    vivas = [p for s in VIVAS for p in listar_pagamentos(chave, s)]
    pagas = [p for s in PAGAS for p in listar_pagamentos(chave, s)]
    refs_pagas = {p.get("externalReference") for p in pagas if p.get("externalReference")}
    clientes_que_pagaram = {p.get("customer") for p in pagas}

    clientes: dict[str, dict] = {}

    def cliente(cid: str) -> dict:
        if cid not in clientes:
            clientes[cid] = req(chave, f"/customers/{cid}")
        return clientes[cid]

    gemeas, restantes = [], []
    for p in vivas:
        ref = p.get("externalReference")
        # Padrão Giovani: a MESMA referência já tem pagamento confirmado → esta é gêmea.
        (gemeas if ref and ref in refs_pagas else restantes).append(p)

    total = sum(float(p.get("value") or 0) for p in vivas)
    print(f"═══ {len(vivas)} cobranças vivas (pendentes+vencidas) somando {moeda(total)} ═══\n")

    if gemeas:
        print(f"🚨 GÊMEAS DE PAGAMENTO JÁ FEITO — {len(gemeas)} (o padrão Giovani; apagar sem dó):")
        for p in gemeas:
            c = cliente(p["customer"])
            atraso = dias_desde(p.get("dueDate"))
            regua = "régua LIGADA 🔔" if not c.get("notificationDisabled") else "régua desligada"
            print(f"  {p['id']}  {moeda(p.get('value'))}  {c.get('name', '?')}  "
                  f"venc. {p.get('dueDate')} ({atraso}d)  [{origem_de(p)}]  {regua}")
        ids = " ".join(p["id"] for p in gemeas)
        print(f"\n  → python3 scripts/auditoria-asaas.py --apagar {ids}\n")

    if restantes:
        print(f"⏳ DEMAIS VIVAS — {len(restantes)} (avaliar uma a uma: abandono de checkout × dívida real):")
        for p in sorted(restantes, key=lambda x: x.get("dueDate") or ""):
            c = cliente(p["customer"])
            atraso = dias_desde(p.get("dueDate"))
            idade = f"{atraso}d vencida" if atraso and atraso > 0 else "no prazo"
            ja_pagou_outra = "  (cliente TEM outro pgto pago)" if p["customer"] in clientes_que_pagaram else ""
            regua = "🔔" if not c.get("notificationDisabled") else "🔕"
            print(f"  {regua} {p['id']}  {moeda(p.get('value'))}  {c.get('name', '?')} <{c.get('email', '?')}>  "
                  f"venc. {p.get('dueDate')} ({idade})  [{origem_de(p)}]{ja_pagou_outra}")
        print()

    barulhentos = [c for c in clientes.values() if not c.get("notificationDisabled")]
    if barulhentos:
        print(f"🔔 CLIENTES COM A RÉGUA DO ASAAS LIGADA — {len(barulhentos)} "
              f"(o Asaas fala com eles em nome da conta):")
        for c in barulhentos:
            print(f"  {c['id']}  {c.get('name', '?')} <{c.get('email', '?')}>")
        ids = " ".join(c["id"] for c in barulhentos)
        print(f"\n  → recomendado (cirúrgico): python3 scripts/auditoria-asaas.py --calibrar {ids}")
        print(f"  → nuclear (zero e-mail do Asaas): python3 scripts/auditoria-asaas.py --silenciar {ids}")
        print("  ⚠️ Calibrar só apaga a COBRANÇA DE ATRASO. Aviso de vencimento e recibo continuam.")
        print("  ⚠️ Vale só pra cobranças criadas DEPOIS: o Asaas agenda as notificações no")
        print("     nascimento da cobrança e não cancela agendamento. Cobrança viva → apagar.")

    if not vivas:
        print("✅ Nenhuma cobrança viva — ninguém está sendo cobrado pela régua agora.")


if __name__ == "__main__":
    main()

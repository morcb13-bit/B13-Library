"""
b13_arith.py ― 平衡N進の掛け算と割り算を足し算だけで組む
==========================================================
第1章の add / neg / sign だけを使う。

  掛け算：b の各桁 d について、a を桁の位置だけずらしたものを |d| 回足す（d が負なら裏返して足す）。
          平衡13進では桁が −6…+6 なので、一桁あたり足すのは多くて 6 回。
  割り算：上の位から、ずらした b を足すか引くかして、余りを b の半分以内へ寄せる。
          足した・引いた回数がその位の商の桁になる。
          最後の余りは |余り| ≤ |b|/2 。商は「一番近い商」、余りは残渣。

ずらすのは、桁の列の下に 0 を並べるだけ（掛け算ではない）。
"""
from __future__ import annotations
from typing import List, Tuple
from b13_balanced import Digits, add, neg, sign, trim, from_decimal, to_int, show, dec

Log = List[str]


def shift(a: Digits, k: int) -> Digits:
    """N^k の位へずらす：下に 0 を k 個並べる。"""
    return trim([0] * k + list(a))


def mul(a: Digits, b: Digits, N: int, log: Log | None = None) -> Tuple[Digits, int]:
    """掛け算。戻り値は (積, 足した回数)。"""
    acc: Digits = [0]
    adds = 0
    for k, d in enumerate(b):
        if d == 0:
            continue
        part = shift(a, k) if d > 0 else neg(shift(a, k))
        for _ in range(abs(d)):
            acc = add(acc, part, N)
            adds += 1
        if log is not None:
            log.append(f"{N}^{k} の位：a を {'+' if d > 0 else '−'}{abs(d)} 回")
    return acc, adds


def _more_than_half(r: Digits, s: Digits, N: int) -> bool:
    """|r| が |s| の半分より大きいか（r と s は同じ向き）を、r+r−s の符号で見る。"""
    return sign(add(add(r, r, N), neg(s), N)) == sign(s)


def divide(a: Digits, b: Digits, N: int, log: Log | None = None) -> Tuple[Digits, Digits, int]:
    """割り算。戻り値は (商, 余り, 足した回数)。a = 商×b + 余り、|余り| ≤ |b|/2。"""
    if sign(b) == 0:
        raise ZeroDivisionError("b = 0")
    r = list(a)
    q: Digits = [0] * (len(a) + 2)
    adds = 0
    for k in range(len(a) + 1, -1, -1):
        s = shift(b, k)
        while sign(r) != 0:
            if sign(r) == sign(s) and _more_than_half(r, s, N):
                r = add(r, neg(s), N)
                q[k] += 1
            elif sign(r) == -sign(s) and _more_than_half(neg(r), s, N):
                r = add(r, s, N)
                q[k] += -1
            else:
                break
            adds += 1
        if log is not None and q[k] != 0:
            log.append(f"{N}^{k} の位：商の桁 {q[k]:+d}")
    return trim(q), trim(r), adds


if __name__ == "__main__":
    N = 13
    print("== 掛け算（平衡13進）")
    for x, y in (("2026", "13"), ("2026", "-7"), ("123", "456"), ("-89", "144")):
        a, b = from_decimal(x, N), from_decimal(y, N)
        p, n = mul(a, b, N)
        print(f"{dec(int(x))} × {dec(int(y))}：{show(a, N)} × {show(b, N)} → {show(p, N)} = {dec(to_int(p, N))}   足した回数 {n}")
    print()
    print("== 割り算（平衡13進、商は一番近い商、余りは |余り| ≤ |b|/2）")
    for x, y in (("2026", "13"), ("2026", "7"), ("2026", "-7"), ("56088", "123"), ("100", "8"), ("-100", "8")):
        a, b = from_decimal(x, N), from_decimal(y, N)
        q, r, n = divide(a, b, N)
        print(f"{dec(int(x))} ÷ {dec(int(y))}：商 {show(q, N)} = {dec(to_int(q, N))}  余り {show(r, N)} = {dec(to_int(r, N))}   足した回数 {n}")
    print()
    print("== 同じ割り算を平衡5進で")
    for x, y in (("2026", "7"), ("100", "8")):
        a, b = from_decimal(x, 5), from_decimal(y, 5)
        q, r, n = divide(a, b, 5)
        print(f"{dec(int(x))} ÷ {dec(int(y))}：商 {show(q, 5)} = {dec(to_int(q, 5))}  余り {show(r, 5)} = {dec(to_int(r, 5))}")

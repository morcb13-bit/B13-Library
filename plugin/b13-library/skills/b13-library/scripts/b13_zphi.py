"""
b13_zphi.py ― Z[φ]：整数の組 a + bφ の算術・ノルム・単数・φ倍
===============================================================
数は整数の組 (a, b) ＝ a + bφ。約束は φ² = φ + 1 の一つだけ（第2章）。

  足す：   (a, b) + (c, d) = (a + c, b + d)
  掛ける： (a, b)(c, d) = (ac + bd, ad + bc + bd)        ← φ² を φ + 1 に置き換えただけ
  φ 倍：   (a, b) → (b, a + b)        φ で割る：(a, b) → (b − a, a)
  共役：   φ を 1 − φ に取り替える：(a, b) → (a + b, −b)
  ノルム： 自分と共役の積 N(a, b) = a² + ab − b²（整数）

ノルムが ±1 の数が単数。単数は ±φ^k だけで、φ^k = F(k−1) + F(k)φ。

整数どうしの掛け算は第4章で足し算に戻したので、ここでは整数の掛け算をそのまま使う。
既存の在処：Paper 2026-02-26-phi-ntt（φ 算術）、B13/Bp のノルム形 x² − xy − y²。
"""
from __future__ import annotations
from typing import Dict, List, Tuple

Z = Tuple[int, int]


def add(u: Z, v: Z) -> Z:
    return (u[0] + v[0], u[1] + v[1])


def neg(u: Z) -> Z:
    return (-u[0], -u[1])


def mul(u: Z, v: Z) -> Z:
    a, b = u
    c, d = v
    return (a * c + b * d, a * d + b * c + b * d)


def times_phi(u: Z) -> Z:
    return (u[1], u[0] + u[1])


def div_phi(u: Z) -> Z:
    return (u[1] + -u[0], u[0])


def conj(u: Z) -> Z:
    return (u[0] + u[1], -u[1])


def norm(u: Z) -> int:
    a, b = u
    return a * a + a * b + -(b * b)


def phi_pow(k: int) -> Z:
    u: Z = (1, 0)
    for _ in range(abs(k)):
        u = times_phi(u) if k > 0 else div_phi(u)
    return u


def show(u: Z) -> str:
    a, b = u
    sa = ("−" if a < 0 else "") + str(abs(a))
    return f"{sa} {'−' if b < 0 else '+'} {abs(b)}φ"


def units_in_box(R: int) -> List[Z]:
    """|a|, |b| ≤ R でノルムが ±1 の組を全部。"""
    return [(a, b) for a in range(-R, R + 1) for b in range(-R, R + 1) if norm((a, b)) in (1, -1)]


def norms_in_box(R: int, top: int) -> Dict[int, List[Z]]:
    """|a|, |b| ≤ R で、ノルムの絶対値が top 以下になる組を、ノルムごとに。"""
    out: Dict[int, List[Z]] = {}
    for a in range(-R, R + 1):
        for b in range(-R, R + 1):
            n = norm((a, b))
            if n != 0 and -top <= n <= top:
                out.setdefault(n, []).append((a, b))
    return out


if __name__ == "__main__":
    print("== φ の累乗（単数）とノルム")
    for k in range(-4, 9):
        u = phi_pow(k)
        print(f"φ^{k:>2} = {show(u):<12} ノルム {norm(u):+d}")
    print()
    print("== 掛け算とノルム（ノルムは掛け算をそのまま写す）")
    for u, v in (((2, 1), (3, 1)), ((3, 1), (3, 1)), ((4, -1), (1, 2)), ((7, 3), (5, -2))):
        w = mul(u, v)
        print(f"({show(u)}) × ({show(v)}) = {show(w):<12} ノルム {norm(u)} × {norm(v)} = {norm(w)}")
    print()
    print("== φ 倍はノルムの符号を裏返す")
    u: Z = (3, 1)
    for _ in range(6):
        print(f"{show(u):<12} ノルム {norm(u):+d}")
        u = times_phi(u)
    print()
    print("== 単数を箱の中で探す（|a|, |b| ≤ 60）")
    us = units_in_box(60)
    pw = {phi_pow(k) for k in range(-12, 13)} | {neg(phi_pow(k)) for k in range(-12, 13)}
    print(f"ノルム ±1 の組 {len(us)} 個。すべて ±φ^k か → {all(u in pw for u in us)}")
    print()
    print("== ノルムになれる数（1〜31、|a|, |b| ≤ 60 で探す）")
    nb = norms_in_box(60, 31)
    print("なれる  :", [n for n in range(1, 32) if n in nb])
    print("なれない:", [n for n in range(1, 32) if n not in nb])
    for n in (5, 11, 19, 29, 31):
        a, b = min(nb[n], key=lambda t: (t[0] < 0 or t[1] < 0, abs(t[0]) + abs(t[1])))
        print(f"{n} = N({show((a, b))})")

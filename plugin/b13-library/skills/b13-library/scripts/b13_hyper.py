"""
b13_hyper.py ― 双曲関数と双曲回転
==================================
  cosh と sinh：cos・sin と同じ級数で、項の符号を裏返さない
                 項 ← 項 × t² ÷ ((2k − 1)(2k))
  双曲回転：     (x, y) → (C·x + S·y, S·x + C·y)。円の回転とは符号が一つ違うだけ
                 x² − y² が変わらない（円は x² + y²）
  整数の双曲回転：Z[φ] で φ² を掛ける (a, b) → (a + b, a + 2b)。ノルム a² + ab − b² が変わらない
                 cosh にあたる量は 3/2（整数の 3 を 2 で割ったもの）。どの一歩も整数のまま
  ペルの双曲回転：x² − 2y² = 1 の解 (3, 2) で (x, y) → (3x + 4y, 2x + 3y)

既存の在処：連載「動く図で見るB13講座」その3（双曲回転）、Paper 2026-09-02-lorentz-hyperbola
"""
from __future__ import annotations
from typing import List, Tuple
from b13_explog import S, sdiv, fmul, show, exp_fx, ln_fx, fixed
from b13_roots import sqrt_digits

Pair = Tuple[int, int]


# ---------------------------------------------------------------- cosh と sinh
def cosh_sinh(t: int) -> Pair:
    t2 = fmul(t, t)
    c_term, c, k = S, S, 1
    while c_term:
        c_term = sdiv(fmul(c_term, t2), (2 * k - 1) * (2 * k))     # 符号を裏返さない
        c += c_term
        k += 1
    s_term, s, k = t, t, 1
    while s_term:
        s_term = sdiv(fmul(s_term, t2), (2 * k) * (2 * k + 1))
        s += s_term
        k += 1
    return c, s


def cos_sin(t: int) -> Pair:
    """比べるための cos・sin（第11章と同じ。項の符号を裏返す）。"""
    t2 = fmul(t, t)
    c_term, c, k = S, S, 1
    while c_term:
        c_term = -sdiv(fmul(c_term, t2), (2 * k - 1) * (2 * k))
        c += c_term
        k += 1
    s_term, s, k = t, t, 1
    while s_term:
        s_term = -sdiv(fmul(s_term, t2), (2 * k) * (2 * k + 1))
        s += s_term
        k += 1
    return c, s


def boost(v: Pair, C: int, Sh: int) -> Pair:
    x, y = v
    return (fmul(C, x) + fmul(Sh, y), fmul(Sh, x) + fmul(C, y))


def turn(v: Pair, c: int, s: int) -> Pair:
    x, y = v
    return (fmul(c, x) + -fmul(s, y), fmul(s, x) + fmul(c, y))


# ---------------------------------------------------------------- 整数の双曲回転
def phi2(u: Pair) -> Pair:
    """φ² を掛ける：(a, b) → (a + b, a + 2b)。"""
    a, b = u
    return (a + b, a + b + b)


def phi2_inv(u: Pair) -> Pair:
    """φ² で割る：(a, b) → (2a − b, b − a)。"""
    a, b = u
    return (a + a + -b, b + -a)


def norm(u: Pair) -> int:
    a, b = u
    return a * a + a * b + -(b * b)


def pell2(v: Pair) -> Pair:
    """x² − 2y² を変えない一歩：(x, y) → (3x + 4y, 2x + 3y)。"""
    x, y = v
    return (x + x + x + y + y + y + y, x + x + y + y + y)


if __name__ == "__main__":
    print("== cos と cosh：違いは項の符号だけ")
    for p, q in ((1, 2), (1, 1), (2, 1)):
        t = fixed(p, q)
        c, s = cos_sin(t)
        C, Sh = cosh_sinh(t)
        print(f"t = {p}/{q}:  cos {show(c, 15)}  sin {show(s, 15)}  |  cosh {show(C, 15)}  sinh {show(Sh, 15)}")
        print(f"         cos² + sin² = {show(fmul(c, c) + fmul(s, s), 25)}   cosh² − sinh² = {show(fmul(C, C) + -fmul(Sh, Sh), 25)}")
    print()
    print("== 双曲回転を 10 回：x² − y² が変わらない（円の回転は x² + y²）")
    C, Sh = cosh_sinh(fixed(1, 5))
    c, s = cos_sin(fixed(1, 5))
    h, r = (S, 0), (S, 0)
    for k in range(1, 11):
        h, r = boost(h, C, Sh), turn(r, c, s)
        if k in (1, 5, 10):
            print(f"{k:>2} 回  双曲 ({show(h[0], 8)}, {show(h[1], 8)})  x²−y² = {show(fmul(h[0], h[0]) + -fmul(h[1], h[1]), 20)}"
                  f"   円 ({show(r[0], 8)}, {show(r[1], 8)})  x²+y² = {show(fmul(r[0], r[0]) + fmul(r[1], r[1]), 20)}")
    print()
    print("== 整数の双曲回転：φ² を掛ける")
    u: Pair = (1, 0)
    for k in range(7):
        print(f"φ^{2 * k:<2} = ({u[0]:>5}, {u[1]:>5})  ノルム {norm(u):+d}")
        u = phi2(u)
    u = (3, 1)
    print("3 + φ から:", [(*u, norm(u)) for u in [u, phi2(u), phi2(phi2(u)), phi2_inv(u), phi2_inv(phi2_inv(u))]])
    print()
    r5 = int(sqrt_digits(5, 40).replace(".", ""))
    print("φ² 倍の cosh にあたる量 = (φ² + φ⁻²)/2 = 3/2、sinh にあたる量 = √5/2 =", show(sdiv(r5, 2), 25))
    lnphi2 = ln_fx(sdiv(S + S + S + r5, 2))                  # φ² = (3 + √5)/2
    Cp, Sp = cosh_sinh(lnphi2)
    print("ラピディティ ln φ² =", show(lnphi2, 25))
    print("cosh(ln φ²) =", show(Cp, 25), "  sinh(ln φ²) =", show(Sp, 25))
    print()
    print("== ペルの双曲回転：x² − 2y² = 1 を保つ")
    v: Pair = (1, 0)
    for _ in range(6):
        print(v, v[0] * v[0] + -(2 * v[1] * v[1]))
        v = pell2(v)

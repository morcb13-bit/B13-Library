"""
b13_explog.py ― 指数と対数を足し算だけで
==========================================
数は「目盛り S を 1 とする整数」で持つ（固定小数点）。S = 10^40。
  1.5 は 15 × 10^39、0.25 は 25 × 10^38、という整数。

  割る：     小さな整数 k で割るのは、倍々の梯子を上から引く（第6章）
  掛ける：   目盛りどうしの掛け算は、整数の積を S で割る（同じ梯子）
  e（複利）：x ← x + x÷n を n 回。n を大きくすると e に近づく
  e（級数）：項 ← 項 ÷ k を足していく（1, 1, 1/2, 1/6, …）
  指数：     項 ← 項 × x ÷ k を足していく
  2 を底とする対数：x を二乗して、2 を越えたら半分にして桁 1 を書く。越えなければ桁 0
  ln 2：     1/2 ÷ 1 + 1/4 ÷ 2 + 1/8 ÷ 3 + …（半分にしては k で割って足す）

浮動小数は使わない。
"""
from __future__ import annotations
from typing import List, Tuple

S = 10 ** 40          # 目盛りの細かさ（1 にあたる整数）


def ladder_div(a: int, m: int) -> int:
    """a ÷ m の整数部分（a ≥ 0, m > 0）。倍々の梯子を上から引く。"""
    lad = [(m, 1)]
    while lad[-1][0] + lad[-1][0] <= a:
        lad.append((lad[-1][0] + lad[-1][0], lad[-1][1] + lad[-1][1]))
    q = 0
    for s, k in reversed(lad):
        if a >= s:
            a += -s
            q += k
    return q


def sdiv(a: int, m: int) -> int:
    """符号つきの a ÷ m（m > 0）。"""
    return ladder_div(a, m) if a >= 0 else -ladder_div(-a, m)


def fmul(a: int, b: int) -> int:
    """目盛りどうしの掛け算。"""
    return sdiv(a * b, S)


def fixed(p: int, q: int = 1) -> int:
    """分数 p/q を目盛りに。"""
    return sdiv(p * S, q)


def show(x: int, places: int = 30) -> str:
    """観察者側の読み：10進の小数として表示。"""
    sign = "−" if x < 0 else ""
    x = abs(x)
    w = ladder_div(x, S)
    f = str(x + -(w * S)).rjust(40, "0")[:places]
    return f"{sign}{w}.{f}"


# ---------------------------------------------------------------- e
def e_compound(n: int) -> int:
    """(1 + 1/n)^n：x ← x + x÷n を n 回。"""
    x = S
    for _ in range(n):
        x += ladder_div(x, n)
    return x


def e_series() -> Tuple[int, int]:
    """1 + 1 + 1/2 + 1/6 + …：項を k で割っては足す。戻り値 (e, 足した項の数)。"""
    term, total, k = S, S, 1
    while term:
        term = ladder_div(term, k)
        total += term
        k += 1
    return total, k


# ---------------------------------------------------------------- 指数
def exp_fx(x: int) -> int:
    """e^x：項 ← 項 × x ÷ k を足していく。|x| が大きいときは半分にして後で二乗する。"""
    halves = 0
    while x > S or x < -S:
        x = sdiv(x, 2)
        halves += 1
    term, total, k = S, S, 1
    while term:
        term = sdiv(fmul(term, x), k)
        total += term
        k += 1
    for _ in range(halves):
        total = fmul(total, total)
    return total


# ---------------------------------------------------------------- 対数
def log2_fx(x: int, bits: int = 133) -> Tuple[int, List[int]]:
    """2 を底とする対数（x > 0）。整数部分は 2 で割れる回数、小数部分は二乗して読む桁。"""
    whole = 0
    while x >= S + S:
        x = ladder_div(x, 2)
        whole += 1
    while x < S:
        x += x
        whole += -1
    frac_bits: List[int] = []
    for _ in range(bits):
        x = fmul(x, x)
        if x >= S + S:
            x = ladder_div(x, 2)
            frac_bits.append(1)
        else:
            frac_bits.append(0)
    # 桁 b1 b2 b3 … を 1/2, 1/4, 1/8, … として足す（観察者側の目盛りへ）
    val, half = whole * S, S
    for b in frac_bits:
        half = ladder_div(half, 2)
        if b:
            val += half
    return val, frac_bits


def ln2_fx() -> int:
    """ln 2 = 1/2 + 1/(2·4) + 1/(3·8) + …：半分にしては k で割って足す。"""
    total, p, k = 0, S, 1
    while True:
        p = ladder_div(p, 2)
        t = ladder_div(p, k)
        if t == 0:
            return total
        total += t
        k += 1


def ln_fx(x: int) -> int:
    """自然対数 = log2 × ln 2。"""
    return fmul(log2_fx(x)[0], ln2_fx())


if __name__ == "__main__":
    print("== e を複利で：(1 + 1/n)^n")
    for n in (1, 2, 12, 100, 1000, 3120, 100000):
        print(f"n = {n:>6}  {show(e_compound(n), 12)}")
    e, k = e_series()
    print(f"級数（項 {k} 個）  {show(e)}")
    print()
    print("== 指数")
    for p, q in ((1, 1), (1, 2), (-1, 1), (5, 1), (1, 13)):
        print(f"e^({p}/{q}) = {show(exp_fx(fixed(p, q)))}")
    print()
    print("== 2 を底とする対数：二乗して 2 を越えたら半分、桁 1")
    for p, q in ((3, 1), (5, 1), (13, 1), (3120, 1), (3, 2)):
        v, b = log2_fx(fixed(p, q))
        print(f"log2({p}/{q}) = {show(v, 25)}   はじめの桁 {''.join(str(t) for t in b[:24])}")
    print()
    print("== 自然対数")
    print(f"ln 2  = {show(ln2_fx())}")
    for p in (3, 10, 13):
        print(f"ln {p:<3} = {show(ln_fx(fixed(p)))}")
    print()
    print("== 往復：e^(ln x)")
    for p in (2, 13, 3120):
        print(f"x = {p:<5} e^(ln x) = {show(exp_fx(ln_fx(fixed(p))), 25)}")

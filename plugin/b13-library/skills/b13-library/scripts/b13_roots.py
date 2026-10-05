"""
b13_roots.py ― √n を足し算だけで近づける：開平・連分数・ペル方程式
====================================================================
  整数の平方根：奇数 1, 3, 5, … を引けるだけ引く。引けた回数が √n の整数部分
  開平（桁ごと）：2 桁ずつ下ろし、「20 × これまでの答え + 1」から始まる奇数を引けるだけ引く
  連分数：     長方形 √n × 1 から正方形を切り取る（第6章の互除法を √n に当てる）
               整数だけの漸化式 m, d, a で回す
  近似分数：   p(k) = a(k) p(k−1) + p(k−2)、q も同じ（a(k) 回足す）
  ペル方程式：  x² − n y² = ±1 は、近似分数のうち周期の切れ目に現れる

使う操作は 足す・引く・大小の比較（掛け算は「回数だけ足す」で書く）。
"""
from __future__ import annotations
from typing import List, Tuple


def times(k: int, x: int) -> int:
    """k 回足す（k は小さい非負整数）。"""
    s = 0
    for _ in range(k):
        s += x
    return s


def ladder_div(a: int, m: int) -> Tuple[int, int]:
    """a ÷ m の商と余り（a ≥ 0, m > 0）。倍々の梯子を上から引く（第6章）。"""
    lad = [(m, 1)]
    while lad[-1][0] + lad[-1][0] <= a:
        lad.append((lad[-1][0] + lad[-1][0], lad[-1][1] + lad[-1][1]))
    q = 0
    for s, k in reversed(lad):
        if a >= s:
            a += -s
            q += k
    return q, a


# ---------------------------------------------------------------- 平方根
def isqrt_odd(n: int) -> Tuple[int, int]:
    """奇数を引けるだけ引く。戻り値 (√n の整数部分, 残り)。"""
    k, odd = 0, 1
    while n >= odd:
        n += -odd
        odd += 2
        k += 1
    return k, n


def sqrt_digits(n: int, places: int) -> str:
    """√n を小数 places 桁まで、桁ごとの開平で。各桁は奇数を引けるだけ引いた回数。"""
    s = str(n)
    if len(s) % 2:
        s = "0" + s
    pairs = [int(s[i:i + 2]) for i in range(0, len(s), 2)] + [0] * places
    p, r, digits = 0, 0, []
    for pr in pairs:
        r = times(100, r) + pr
        odd = times(20, p) + 1
        c = 0
        while r >= odd:
            r += -odd
            odd += 2
            c += 1
        p = times(10, p) + c
        digits.append(str(c))
    head = len(pairs) - places
    whole = "".join(digits[:head]).lstrip("0") or "0"
    return whole + "." + "".join(digits[head:])


# ---------------------------------------------------------------- 連分数
def cf_sqrt(n: int, terms: int) -> List[int]:
    """√n の連分数の項 a0; a1, a2, …（整数の漸化式）。"""
    a0, rest = isqrt_odd(n)
    if rest == 0:
        return [a0]
    out = [a0]
    m, d, a = 0, 1, a0
    for _ in range(terms - 1):
        m = times(a, d) + -m                       # m ← d·a − m
        q, r = ladder_div(n + -(m * m), d)         # d ← (n − m²) ÷ d（割り切れる）
        assert r == 0
        d = q
        a, _ = ladder_div(a0 + m, d)               # a ← (a0 + m) ÷ d の整数部分
        out.append(a)
    return out


def period(n: int) -> List[int]:
    """√n の連分数の、繰り返す部分（a0 の後、2·a0 で終わる一周）。"""
    a = cf_sqrt(n, 400)
    a0 = a[0]
    for k in range(1, len(a)):
        if a[k] == a0 + a0:
            return a[1:k + 1]
    return []


def convergents(cf: List[int]) -> List[Tuple[int, int]]:
    """近似分数 p/q。p(k) = a(k) p(k−1) + p(k−2)。"""
    out = []
    p0, p1 = 1, cf[0]
    q0, q1 = 0, 1
    out.append((p1, q1))
    for a in cf[1:]:
        p0, p1 = p1, times(a, p1) + p0
        q0, q1 = q1, times(a, q1) + q0
        out.append((p1, q1))
    return out


def pell_value(n: int, p: int, q: int) -> int:
    return p * p + -(n * q * q)


if __name__ == "__main__":
    print("== 奇数を引けるだけ引く")
    for n in (2, 13, 2026, 3120):
        print(f"√{n}: 整数部分 {isqrt_odd(n)[0]}, 残り {isqrt_odd(n)[1]}")
    print()
    print("== 桁ごとの開平")
    for n in (2, 3, 5, 13):
        print(f"√{n} = {sqrt_digits(n, 30)}")
    print()
    print("== 連分数（繰り返す部分）")
    for n in (2, 3, 5, 7, 13, 19, 61):
        a = cf_sqrt(n, 1)[0]
        print(f"√{n} = [{a}; {', '.join(str(x) for x in period(n))}]   一周 {len(period(n))} 項")
    print()
    print("== 近似分数と x² − n y²")
    for n in (2, 5, 13):
        cv = convergents(cf_sqrt(n, 10))
        print(f"n = {n}:", "  ".join(f"{p}/{q}({pell_value(n, p, q):+d})" for p, q in cv))
    print()
    print("== ペル方程式の一番小さい解（周期の切れ目の近似分数）")
    for n in (2, 3, 5, 7, 13, 19, 61):
        k = len(period(n))
        p, q = convergents(cf_sqrt(n, k))[k - 1]
        print(f"n = {n:>2}: {p}² − {n}·{q}² = {pell_value(n, p, q):+d}")

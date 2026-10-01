"""
b13_residue.py ― 平方剰余・ピサノ周期・篩を足し算だけで
==========================================================
  平方剰余：k² は奇数 1, 3, 5, … を k 個足したもの。足すたびに p を越えたら p を引く
  ピサノ周期：フィボナッチ数を m の輪の上で足していき、(0, 1) に戻るまでの歩数
  篩：      p から p ずつ跳んで印をつける（足し算の歩み）

使う操作は 足す・引く・大小の比較 だけ。
"""
from __future__ import annotations
from typing import Dict, List


def wrap(x: int, m: int) -> int:
    """0 ≤ x < 2m の数を 0 ≤ x < m に戻す。"""
    return x + -m if x >= m else x


# ---------------------------------------------------------------- 平方剰余
def squares_mod(p: int) -> List[int]:
    """k = 0, 1, …, p−1 の k² を p の輪で。次の平方は、今の平方に次の奇数を足したもの。"""
    out = [0]
    sq, odd = 0, 1
    for _ in range(p - 1):
        sq = sq + odd
        while sq >= p:
            sq += -p
        out.append(sq)
        odd = odd + 2
        while odd >= p:
            odd += -p
    return out


def residues(p: int) -> List[int]:
    """0 を除く平方の集まり（重複なし、小さい順）。"""
    return sorted(set(squares_mod(p)) - {0})


# ---------------------------------------------------------------- フィボナッチの輪
def pisano(m: int) -> int:
    """フィボナッチ数を m の輪で足していき、(0, 1) に戻るまでの歩数。"""
    if m == 1:
        return 1
    a, b, n = 0, 1, 0
    while True:
        a, b = b, wrap(a + b, m)
        n += 1
        if a == 0 and b == 1:
            return n


def apparition(m: int) -> int:
    """F_n が初めて m の輪の 0（m の倍数）に着地する n。"""
    a, b, n = 0, 1, 0
    while True:
        a, b = b, wrap(a + b, m)
        n += 1
        if a == 0:
            return n


def fib_ring(m: int) -> List[int]:
    """一周ぶんの F_n（m の輪）。"""
    out = []
    a, b = 0, 1
    for _ in range(pisano(m)):
        out.append(a)
        a, b = b, wrap(a + b, m)
    return out


# ---------------------------------------------------------------- 篩
def sieve(N: int) -> List[int]:
    """2 から N まで。残った数から順に、その数ずつ跳んで印をつける。"""
    hit = [False] * (N + 1)
    primes = []
    for p in range(2, N + 1):
        if hit[p]:
            continue
        primes.append(p)
        q = p + p
        while q <= N:
            hit[q] = True
            q += p
    return primes


def survivors_after(ps: List[int], N: int) -> List[int]:
    """ps の数ずつ跳んで印をつけた後、残った数（1 を含む）。"""
    hit = [False] * (N + 1)
    for p in ps:
        q = p + p
        while q <= N:
            hit[q] = True
            q += p
    return [n for n in range(1, N + 1) if not hit[n] and n not in ps]


if __name__ == "__main__":
    print("== 平方剰余（奇数を順に足して平方を作る）")
    for p in (5, 13, 29, 31):
        print(f"p={p:>2}  平方 {squares_mod(p)}")
        print(f"       0 以外の平方 {residues(p)}  （{len(residues(p))} 個）  5 は平方か → {5 in residues(p) if p != 5 else '―'}")
    print()
    print("== 5 が平方になる素数・ならない素数（p を 5 で割った余りで並べる）")
    ps = [p for p in sieve(200) if p not in (2, 5)]
    table: Dict[int, List[str]] = {1: [], 2: [], 3: [], 4: []}
    for p in ps:
        r = p
        while r >= 5:
            r += -5
        table[r].append(f"{p}{'○' if 5 in residues(p) else '×'}")
    for r in (1, 4, 2, 3):
        print(f"余り {r}: {' '.join(table[r])}")
    print()
    print("== ピサノ周期と、0 に初めて着地する歩数")
    for m in (2, 3, 5, 8, 10, 11, 13, 29, 31, 3120):
        print(f"m={m:>4}  周期 {pisano(m):>5}   0 に着地 {apparition(m):>4}")
    print("13 の輪の一周:", fib_ring(13))
    print()
    print("== 篩")
    print("100 までの素数:", sieve(100))
    print("2 と 3 で跳んだ後に残る数（60 まで）:", survivors_after([2, 3], 60))

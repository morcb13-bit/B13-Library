"""
b13_diffsum.py ― 差分と和（微分と積分）を足し算だけで
======================================================
  差分：  隣どうしを引く      d[n] = a[n+1] − a[n]
  和：    ここまでを足す      s[n] = a[0] + a[1] + … + a[n−1]
          和の差分は元の列。差分の和は「端と端の差」
  差分の表：差分を何段も取る。n² は 2 段目で 2、n³ は 3 段目で 6 に着地する
  表を戻す：表の左端の列（先頭の数）だけから、パスカルの三角形の足し算で列全体が戻る
  自分が差分になる列：2ⁿ（差分が自分）、フィボナッチ（差分が一つ前の自分）
  刻みを細かく：刻み 1/n で引いて n 倍する。x ← x + x÷n（第10章）は「差分が自分」
  柱で数える：0〜1 の x² の下を n 本の柱で数えると、3 倍した柱の和と n³ の差が五角数になる

判定は整数と加算だけ。目盛り S は第10章と同じ。
"""
from __future__ import annotations
from typing import List
from b13_explog import S, ladder_div, show


# ---------------------------------------------------------------- 差分と和
def diff(a: List[int]) -> List[int]:
    """隣どうしを引く。"""
    return [a[i + 1] + -a[i] for i in range(len(a) - 1)]


def accum(a: List[int], start: int = 0) -> List[int]:
    """ここまでを足す。先頭は start（何も足していない状態）。"""
    out = [start]
    for x in a:
        out.append(out[-1] + x)
    return out


def table(a: List[int], depth: int) -> List[List[int]]:
    """差分の表：差分を depth 段まで取る。"""
    rows = [a]
    for _ in range(depth):
        rows.append(diff(rows[-1]))
    return rows


def heads(a: List[int], depth: int) -> List[int]:
    """表の左端（各段の先頭の数）。"""
    return [r[0] for r in table(a, depth)]


def rebuild(h: List[int], length: int) -> List[int]:
    """左端の数だけから列を戻す。いちばん下の段から和を取って上がる。
    いちばん下の段は同じ数がずっと続くとみなす。"""
    row = [h[-1]] * length
    for x in reversed(h[:-1]):
        row = accum(row, x)[:length]
    return row


def pascal(rows: int) -> List[List[int]]:
    """パスカルの三角形：上の二つを足す。"""
    t = [[1]]
    for _ in range(rows - 1):
        p = t[-1]
        t.append([1] + [p[i] + p[i + 1] for i in range(len(p) - 1)] + [1])
    return t


# ---------------------------------------------------------------- 自分が差分になる列
def pow2(n: int) -> List[int]:
    a = [1]
    for _ in range(n - 1):
        a.append(a[-1] + a[-1])
    return a


def fib(n: int) -> List[int]:
    a = [0, 1]
    while len(a) < n:
        a.append(a[-1] + a[-2])
    return a[:n]


# ---------------------------------------------------------------- 刻みを細かく
def square_slope(x: int, n: int) -> int:
    """x² の、刻み 1/n の傾き：((x + 1/n)² − x²) を n 倍。x は目盛り。"""
    h = ladder_div(S, n)
    sq = lambda v: ladder_div(v * v, S)
    return (sq(x + h) + -sq(x)) * n


# ---------------------------------------------------------------- 柱で数える
def pentagonal(n: int) -> int:
    """n(3n − 1)/2：1, 5, 12, 22, …（足し算で 1 + 4 + 7 + …）。"""
    p, step = 0, 1
    for _ in range(n):
        p += step
        step += 3
    return p


def pentagonal_plus(n: int) -> int:
    """n(3n + 1)/2：2, 7, 15, 26, …（足し算で 2 + 5 + 8 + …）。"""
    p, step = 0, 2
    for _ in range(n):
        p += step
        step += 3
    return p


def columns(n: int):
    """0〜1 の x² の下を幅 1/n の柱 n 本で数える。
    柱の高さを n² 倍して整数にする：低い柱 k²（k = 0〜n−1）、高い柱 k²（k = 1〜n）。
    返す値：(低い柱の和, 高い柱の和)。面積は和 ÷ n³。"""
    low = high = sq = 0
    odd = 1
    for k in range(n):
        low += sq            # k² を足す
        sq += odd            # 次の平方（奇数を足す）
        odd += 2
        high += sq           # (k + 1)² を足す
    return low, high


if __name__ == "__main__":
    print("== 差分と和は、互いに戻す")
    a = [3, 1, 4, 1, 5, 9, 2, 6]
    print("列          ", a)
    print("差分        ", diff(a))
    print("差分の和    ", accum(diff(a), a[0]))
    print("和          ", accum(a))
    print("和の差分    ", diff(accum(a)))
    print()

    print("== 差分の表")
    for name, seq, d in [("n²", [k * k for k in range(9)], 3), ("n³", [k * k * k for k in range(9)], 4)]:
        print(name)
        for i, r in enumerate(table(seq, d)):
            print(f"  {i} 段目  ", r)
        print("  左端      ", heads(seq, d), " → 戻した列", rebuild(heads(seq, d), 9))
    print("パスカルの三角形（上の二つを足す）")
    for r in pascal(6):
        print("  ", r)
    print()

    print("== 自分が差分になる列")
    p = pow2(10)
    print("2ⁿ          ", p)
    print("差分        ", diff(p))
    f = fib(14)
    print("フィボナッチ ", f)
    print("差分        ", diff(f))
    print("和          ", accum(f)[1:13], " ← 次の次 − 1:", [f[i + 2] + -1 for i in range(12)])
    print("左端から戻す（左端 × パスカルの三角形の段を足す）")
    P = pascal(12)
    for name, seq in [("2ⁿ", pow2(12)), ("フィボナッチ", fib(12))]:
        h = heads(seq, 11)
        back = [sum(h[i] * P[n][i] for i in range(n + 1)) for n in range(12)]
        print(f"  {name:<6} 左端 {h}  戻した列 {back}  一致 {back == seq}")
    print()

    print("== 刻みを細かく：x² の x = 1 での傾き（刻み 1/n で引いて n 倍）")
    for n in (1, 2, 10, 100, 3120, 10 ** 6):
        print(f"n = {n:>7}  傾き {show(square_slope(S, n), 12)}")
    print()

    print("== 柱で数える：0〜1 の x² の下")
    print("   n   低い柱の和 L   高い柱の和 H        n³    n³ − 3L   3H − n³")
    for n in (1, 2, 3, 4, 5, 10, 13, 100, 3120):
        L, H = columns(n)
        c = n * n * n
        print(f"{n:>4}  {L:>12}  {H:>12}  {c:>12}  {c + -(L + L + L):>8}  {H + H + H + -c:>8}")
    print("n³ − 3L の並び:", [pentagonal(n) for n in range(1, 11)], "（五角数）")
    print("3H − n³ の並び:", [pentagonal_plus(n) for n in range(1, 11)])
    ok = all((lambda L, H, c: c + -(L + L + L) == pentagonal(n) and H + H + H + -c == pentagonal_plus(n))(*columns(n), n * n * n)
             for n in range(1, 2001))
    print("n = 1〜2000 で両方とも一致:", ok)

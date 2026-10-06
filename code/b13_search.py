"""
b13_search.py ― 探す：二分法・フィボナッチで探す・アメーバの最短路
==================================================================
  二分法：      幅を半分にして、目当てがどちら側にあるかを比べる。半分は倍々の梯子（第6章）で出す
  フィボナッチで探す：幅をフィボナッチ数で切る。半分にする代わりに、二つ前のフィボナッチ数を引くだけ
  アメーバ：    床（ペンローズの頂点と辺、第18章）の上で、餌の濃さを
                    D_t(i) = Σ（通れる隣 j の D_{t−1}(j)） + （i が餌なら k^t）
                で広げる。D は「餌から i へ至る、すべての道の寄与の和」。
                アメーバは、今いる番地の隣のうち、いちばん濃い番地へ移るだけ（等しければ両方へ）
  比べる相手：  壁を避けて隣をたどった最短の段数（第18章で波の先頭が沿って進んだ段数）

判定は整数と加算だけ。既存の在処：Paper 2026-09-21-plant-sun（amoeba01.md）
"""
from __future__ import annotations
from collections import deque
from typing import List, Optional, Tuple

from b13_explog import S, ladder_div, fmul, show
from b13_wave import penrose_floor


# ---------------------------------------------------------------- 二分法
def half(x: int) -> int:
    return ladder_div(x, 2)


def bisect_isqrt(n: int) -> Tuple[int, int]:
    """x·x ≤ n となる最大の x。戻り値 (x, 比べた回数)。"""
    lo, hi, steps = 0, n + 1, 0
    while hi + -lo > 1:
        mid = half(lo + hi)
        steps += 1
        if mid * mid <= n:
            lo = mid
        else:
            hi = mid
    return lo, steps


def bisect_root(f, lo: int, hi: int) -> Tuple[int, int]:
    """f(lo) < 0 < f(hi) の区間を、目盛りの最後の桁まで半分にしていく。"""
    steps = 0
    while hi + -lo > 1:
        mid = half(lo + hi)
        steps += 1
        if f(mid) < 0:
            lo = mid
        else:
            hi = mid
    return lo, steps


# ---------------------------------------------------------------- フィボナッチで探す
def fib_search(a: List[int], key: int) -> Tuple[int, int]:
    """並んだ列 a から key を探す。半分にせず、フィボナッチ数を引いて幅を縮める。
    戻り値 (見つけた位置または −1, 比べた回数)。"""
    n = len(a)
    f2, f1 = 0, 1              # F(k−2), F(k−1)
    f = f2 + f1                 # F(k)
    while f < n:
        f2, f1 = f1, f
        f = f2 + f1
    off, steps = -1, 0
    while f > 1:
        i = off + f2
        if i > n + -1:
            i = n + -1
        steps += 1
        if a[i] < key:
            f, f1 = f1, f2
            f2 = f + -f1
            off = i
        elif a[i] > key:
            f = f2
            f1 = f1 + -f2
            f2 = f + -f1
        else:
            return i, steps
    if f1 and off + 1 < n and a[off + 1] == key:
        return off + 1, steps + 1
    return -1, steps + 1


def bisect_search(a: List[int], key: int) -> Tuple[int, int]:
    lo, hi, steps = 0, len(a) + -1, 0
    while lo <= hi:
        mid = half(lo + hi)
        steps += 1
        if a[mid] < key:
            lo = mid + 1
        elif a[mid] > key:
            hi = mid + -1
        else:
            return mid, steps
    return -1, steps


# ---------------------------------------------------------------- アメーバ
WX, WY, LEVELS = 30, 20, 8


def floor():
    return penrose_floor(wx=WX, wy=WY, levels=LEVELS)


def nearest(X, Y, x, y):
    return min(range(len(X)), key=lambda v: (X[v] - x) ** 2 + (Y[v] - y) ** 2)


def walls(X, Y, kind: str) -> List[bool]:
    """壁の置き方。番地の置き場所（作図用の小数）で決める。"""
    out = []
    for x, y in zip(X, Y):
        w = False
        if kind == "隙間は上" and -1 <= x <= 0.6 and not (8 <= y <= 11):
            w = True
        if kind == "隙間は下" and -1 <= x <= 0.6 and not (-11 <= y <= -8):
            w = True
        if kind == "ジグザグ" and ((-12 <= x <= -11.4 and y > -12) or (-1 <= x <= -0.4 and y < 12) or (10 <= x <= 10.6 and y > -12)):
            w = True
        if kind == "ふさぐ" and -1 <= x <= 0.6:
            w = True
        out.append(w)
    return out


def hops(adj, wall, src) -> List[int]:
    d = [-1] * len(adj)
    d[src] = 0
    q = deque([src])
    while q:
        v = q.popleft()
        for u in adj[v]:
            if d[u] < 0 and not wall[u]:
                d[u] = d[v] + 1
                q.append(u)
    return d


def scent(adj, wall, food: int, T: int, k: int, ignore: bool = False) -> List[int]:
    """餌の濃さ D_T。ignore=True なら壁を無視して広げる（対照）。"""
    n = len(adj)
    D = [0] * n
    kt = 1
    for _ in range(T):
        N = [0] * n
        for v in range(n):
            if wall[v] and not ignore:
                continue
            s = 0
            for u in adj[v]:
                if ignore or not wall[u]:
                    s += D[u]
            N[v] = s
        N[food] += kt
        kt = kt * k
        D = N
    return D


def climb(adj, wall, D, seed: int, food: int, limit: int = 1000) -> Optional[int]:
    """いちばん濃い隣へ移る（等しければ両方へ）。餌に着いた歩数。着かなければ None。"""
    front, steps = {seed}, 0
    while food not in front:
        nxt = set()
        for v in front:
            nb = [u for u in adj[v] if not wall[u]]
            if not nb:
                continue
            m = max(D[u] for u in nb)
            if m <= D[v]:
                continue                      # 濃い隣がない：止まる
            nxt |= {u for u in nb if D[u] == m}
        if not nxt or steps >= limit:
            return None
        front, steps = nxt, steps + 1
    return steps


if __name__ == "__main__":
    print("== 二分法：x·x ≤ n の最大の x")
    for n in (2, 10 ** 6, 2 * 10 ** 60):
        x, st = bisect_isqrt(n)
        print(f"  n = {n}  x = {x}  比べた回数 {st}")
    print()

    print("== 二分法で x³ − 2x − 5 = 0 の根（目盛り S = 10⁴⁰）")
    f = lambda x: fmul(fmul(x, x), x) + -(x + x) + -(5 * S)
    r, st = bisect_root(f, 2 * S, 3 * S)
    print(f"  根 {show(r, 30)}  比べた回数 {st}")
    print()

    print("== 並んだ列から探す：二分法とフィボナッチ")
    a = [k * k for k in range(1, 1001)]          # 1, 4, 9, …, 1000000
    worst_b = worst_f = 0
    tot_b = tot_f = 0
    for key in a:
        ib, sb = bisect_search(a, key)
        jf, sf = fib_search(a, key)
        assert a[ib] == key and a[jf] == key
        worst_b, worst_f = max(worst_b, sb), max(worst_f, sf)
        tot_b, tot_f = tot_b + sb, tot_f + sf
    miss_b = bisect_search(a, 2)[0]
    miss_f = fib_search(a, 2)[0]
    print(f"  1000 個の平方数を全部探した。比べた回数の最大：二分法 {worst_b}、フィボナッチ {worst_f}")
    print(f"  比べた回数の合計：二分法 {tot_b}、フィボナッチ {tot_f}")
    print(f"  列にない数（2）を探すと：二分法 {miss_b}、フィボナッチ {miss_f}（−1 は「ない」）")
    print()

    print("== アメーバ：ペンローズの床の上で餌まで")
    X, Y, adj = floor()
    n = len(X)
    degs = {}
    for a_ in adj:
        degs[len(a_)] = degs.get(len(a_), 0) + 1
    print(f"  番地 {n}  隣の数ごとの番地数 {dict(sorted(degs.items()))}")
    food = nearest(X, Y, 24, 0)
    seeds = [nearest(X, Y, -24, y) for y in (-12, -4, 4, 12)]
    T = 160
    for kind in ("隙間は上", "隙間は下", "ジグザグ"):
        w = walls(X, Y, kind)
        d = hops(adj, w, food)
        D = scent(adj, w, food, T, 8)
        res = [climb(adj, w, D, s, food) for s in seeds]
        Di = scent(adj, w, food, T, 8, ignore=True)
        res_i = [climb(adj, w, Di, s, food) for s in seeds]
        print(f"  壁：{kind}")
        print(f"    アメーバの歩数 / 最短の段数  " + "  ".join(f"{r}/{d[s]}" for r, s in zip(res, seeds)))
        print(f"    壁を無視して広げた濃さでは  " + "  ".join("止まる" if r is None else f"{r}" for r in res_i))
    w = walls(X, Y, "ふさぐ")
    D = scent(adj, w, food, T, 8)
    print("  壁：ふさぐ（隙間なし）  アメーバ", ["止まる" if climb(adj, w, D, s, food) is None else "着く" for s in seeds],
          "  種の濃さ", [D[s] for s in seeds])
    print()

    print("== 全部の番地を種にして、最短の段数と一致した数（注ぎ足しの倍率 k を変える）")
    for kind in ("隙間は上", "ジグザグ"):
        w = walls(X, Y, kind)
        d = hops(adj, w, food)
        cells = [v for v in range(n) if not w[v] and d[v] > 0]
        row = []
        for k in (4, 5, 6, 7, 8, 9):
            D = scent(adj, w, food, T, k)
            ok = sum(1 for s in cells if climb(adj, w, D, s, food) == d[s])
            row.append(f"k={k}:{ok}")
        print(f"  {kind}（番地 {len(cells)}）  " + "  ".join(row))

"""
b13_wave.py ― 点ではなく波で：ペンローズの床のスリット
======================================================
床：ペンローズのひし形の頂点（番地）と辺（隣どうし）。
    番地の置き場所だけは作図用の小数で決め、そこから先は整数だけで動かす。

  点（玉）：源の列のどこかから（くじで選ぶ）玉を一つずつ放ち、くじ（第18章 Kuji）で「右へ進む隣」を一つ選んで進める。
            壁に当たった玉は捨て、幕に着いた玉は着地として数える。
  波：      番地ごとに整数 u を持ち、一刻ごとに
                u_next = 2·u − u_prev + (隣の u の和 − 隣の数 × u) ÷ 隣の数    （0 へ向けて切り捨て）
            と進める。源の列には、30 刻で一周する整数の cos（第11章の 3120 の表から取る）を入れる。
            床の縁では、u − u_prev に比例して少しずつ引いて、波を吸い取る。
            明るさは、最後の 120 刻の u² の和（整数）。
  先頭：    波の |u| が初めて源の振れ幅の 1/100 を越えた刻。最短の道の数（壁を避けて数えた段数）と並べる。

判定は整数と加算だけ。既存の在処：Paper 2026-10-01-statistics（electron_paths.html）
"""
from __future__ import annotations
import math
import sys
from collections import deque
from typing import List, Tuple

from b13_trig import cos_table
from b13_explog import S, sdiv
from b13_count import Kuji

PHI_F = (1 + 5 ** 0.5) / 2          # 番地の置き場所を決めるためだけ（作図用）
K = 10 ** 6                          # 源の振れ幅
P = 30                               # 30 刻で一周
WX, WY = 80, 55                      # 床の大きさ（辺の長さ 1 を単位に、中心から）
BAND = 16                            # 縁の吸い取り帯の幅
SRC_X = -WX + BAND + 2               # 源の列
WALL_X = -WX + BAND + 12             # 壁
SCREEN_X = 40                        # 幕


# ---------------------------------------------------------------- 床
def penrose_floor(square: bool = False):
    """番地の置き場所 (X, Y) と隣の表。square=True なら四角い格子（対照）。"""
    if square:
        X, Y, idx = [], [], {}
        for i in range(-WX, WX + 1):
            for j in range(-WY, WY + 1):
                idx[(i, j)] = len(X)
                X.append(float(i))
                Y.append(float(j))
        adj = [[] for _ in X]
        for (i, j), a in idx.items():
            for di, dj in ((1, 0), (0, 1)):
                b = idx.get((i + di, j + dj))
                if b is not None:
                    adj[a].append(b)
                    adj[b].append(a)
        return X, Y, adj
    tris = []
    for i in range(10):
        b = (math.cos((2 * i - 1) * math.pi / 10), math.sin((2 * i - 1) * math.pi / 10))
        c = (math.cos((2 * i + 1) * math.pi / 10), math.sin((2 * i + 1) * math.pi / 10))
        if i % 2 == 0:
            b, c = c, b
        tris.append((0, (0.0, 0.0), b, c))
    for _ in range(10):
        out = []
        for col, A, B, C in tris:
            if col == 0:
                Pp = (A[0] + (B[0] - A[0]) / PHI_F, A[1] + (B[1] - A[1]) / PHI_F)
                out += [(0, C, Pp, B), (1, Pp, C, A)]
            else:
                Q = (B[0] + (A[0] - B[0]) / PHI_F, B[1] + (A[1] - B[1]) / PHI_F)
                R = (B[0] + (C[0] - B[0]) / PHI_F, B[1] + (C[1] - B[1]) / PHI_F)
                out += [(1, R, C, A), (1, Q, R, B), (0, R, Q, A)]
        tris = out
    e = tris[0]
    s = 1 / math.hypot(e[2][0] - e[1][0], e[2][1] - e[1][1])
    idx, X, Y, E = {}, [], [], set()

    def vid(p):
        k = (round(p[0] * s * 1e3), round(p[1] * s * 1e3))
        if k not in idx:
            idx[k] = len(X)
            X.append(p[0] * s)
            Y.append(p[1] * s)
        return idx[k]

    inside = lambda p: abs(p[0] * s) <= WX and abs(p[1] * s) <= WY
    for _, A, B, C in tris:
        for Q in (B, C):
            if inside(A) and inside(Q):
                a, b = vid(A), vid(Q)
                E.add((min(a, b), max(a, b)))
    adj = [[] for _ in X]
    for a, b in E:
        adj[a].append(b)
        adj[b].append(a)
    return X, Y, adj


def tq(x: int, d: int) -> int:
    """0 へ向けて切り捨てる割り算（倍々の梯子と同じ結果）。"""
    return x // d if x >= 0 else -((-x) // d)


def walls(X, Y, slits: List[float], half: float = 1.3):
    return [(WALL_X <= X[v] <= WALL_X + 1.6) and not any(abs(Y[v] - c) <= half for c in slits) for v in range(len(X))]


# ---------------------------------------------------------------- 波
def wave(X, Y, adj, slits, T: int = 480, AVG: int = 4 * P):
    n = len(X)
    deg = [len(a) for a in adj]
    blocked = walls(X, Y, slits)
    ct = cos_table(3120)
    src_tab = [sdiv(ct[(3120 // P) * t % 3120] * K, S) for t in range(P)]
    srcs = [v for v in range(n) if abs(X[v] - SRC_X) < 0.8]
    damp = []
    for v in range(n):
        dd = min(WX - abs(X[v]), WY - abs(Y[v]))
        damp.append(0 if dd >= BAND else int((BAND - dd) ** 2 * 0.12) + 1)   # 帯の深さに応じた整数
    u, p = [0] * n, [0] * n
    bright = [0] * n
    first = [-1] * n
    for t in range(T):
        nu = [0] * n
        for v in range(n):
            if blocked[v]:
                continue
            L = -deg[v] * u[v]
            for w in adj[v]:
                L += u[w]
            a = u[v] + u[v] + -p[v] + tq(L, deg[v])
            if damp[v]:
                a += -tq((u[v] + -p[v]) * damp[v], 64)
            nu[v] = a
        for v in srcs:
            nu[v] = src_tab[t % P]
        p, u = u, nu
        for v in range(n):
            if first[v] < 0 and abs(u[v]) * 100 > K:
                first[v] = t
            if t >= T - AVG:
                bright[v] += u[v] * u[v]
    return bright, first, blocked, srcs


# ---------------------------------------------------------------- 点（玉）
def balls(X, Y, adj, slits, count: int = 20000, seed: int = 3):
    kuji = Kuji(seed)
    n = len(X)
    blocked = walls(X, Y, slits)
    right = [[w for w in adj[v] if X[w] > X[v]] for v in range(n)]
    srcs = [v for v in range(n) if abs(X[v] - SRC_X) < 0.8 and abs(Y[v]) <= WY - BAND]   # 波と同じ源の列
    land = []
    for _ in range(count):
        v = srcs[kuji.below(len(srcs))]
        while X[v] < SCREEN_X:
            nb = right[v] or adj[v]
            v = nb[kuji.below(len(nb))]
            if blocked[v] or abs(Y[v]) > WY - BAND:
                v = -1
                break
        if v >= 0:
            land.append(v)
    return land


def hops(adj, blocked, src_list):
    """壁を避けて数えた最短の段数（第19章のアメーバが数えるもの）。"""
    d = [-1] * len(adj)
    q = deque()
    for s in src_list:
        d[s] = 0
        q.append(s)
    while q:
        v = q.popleft()
        for w in adj[v]:
            if d[w] < 0 and not blocked[w]:
                d[w] = d[v] + 1
                q.append(w)
    return d


def profile(values, X, Y, verts, width: int = 4):
    """幕の上で、縦 width ずつの組にまとめた和と番地数。"""
    out = {}
    for v in verts:
        k = math.floor(Y[v] / width)
        s, c = out.get(k, (0, 0))
        out[k] = (s + values[v], c + 1)
    return out


def bar(x, mx, w=40):
    return "#" * ((x * w) // mx if mx else 0)


def rel(d, keys):
    """いちばん大きい組を 100 とした整数（表示用。100 倍して割るだけ）。"""
    mx = max(d.get(k, 0) for k in keys) or 1
    return [d.get(k, 0) * 100 // mx for k in keys]


if __name__ == "__main__":
    keys = list(range(-10, 10))
    print("幕を縦 4 ずつ 20 組に分ける（y = −40〜−37 の組から y = 36〜39 の組まで、y の小さい組から順に）")
    print()
    for floor_name, sq in [("ペンローズ", False), ("四角い格子（対照）", True)]:
        X, Y, adj = penrose_floor(square=sq)
        n = len(X)
        screen = [v for v in range(n) if SCREEN_X - 2 <= X[v] <= SCREEN_X + 2]
        degs = {}
        for a in adj:
            degs[len(a)] = degs.get(len(a), 0) + 1
        print(f"== 床：{floor_name}  番地 {n}  幕の番地 {len(screen)}  隣の数ごとの番地数 {dict(sorted(degs.items()))}")
        for name, sl in [("二つのスリット", [-14.0, 14.0]), ("一つのスリット", [0.0])]:
            br, first, blocked, srcs = wave(X, Y, adj, sl)
            pr = profile(br, X, Y, screen)
            avg = {k: pr[k][0] // pr[k][1] for k in pr}
            print(f"   波・{name}  幕の明るさ（最大を 100）")
            print("     ", rel(avg, keys))
            if not sq:
                land = balls(X, Y, adj, sl)
                cnt = {}
                for v in land:
                    k = math.floor(Y[v] / 4)
                    cnt[k] = cnt.get(k, 0) + 1
                print(f"   点・{name}  玉 20000 個のうち幕に着いた {len(land)} 個の、組ごとの個数")
                print("     ", [cnt.get(k, 0) for k in keys])
            if name == "二つのスリット":
                h = hops(adj, blocked, srcs)
                rows = {}
                for v in range(n):
                    if h[v] > 0 and first[v] >= 0 and X[v] > WALL_X + 2:
                        rows[h[v]] = min(rows.get(h[v], 10 ** 9), first[v])
                print("   最短の段数と、その段数の番地に波の先頭がいちばん早く届いた刻（壁の右側）")
                print("     " + "  ".join(f"{d}段:{rows[d]}刻" for d in range(20, 101, 10) if d in rows))
        print()

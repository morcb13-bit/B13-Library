"""
b13_quat.py ― 四元数とイコシアンを整数の組で
==============================================
四元数 q = w + x·i + y·j + z·k（i² = j² = k² = ijk = −1）。
成分は Z[φ] の数（整数の組 (a, b) = a + bφ、φ² = φ + 1）。

半分（1/2）が出ないように、この章の四元数はすべて **2 倍して** 持つ。
  2q どうしを掛けると 4pq になるので、2 で割って 2(pq) に戻す（いつも割り切れる）。

  掛け算：         ハミルトンの規則（足し算と Z[φ] の掛け算だけ）
  長さ：           N(q) = w² + x² + y² + z²。N(pq) = N(p)·N(q)
  回す：           点 v を q v q̄ で挟む。q と −q は同じ回転
  整数で閉じる 24 個：(±1, 0, 0, 0) の並べ替え 8 個と (±1/2, ±1/2, ±1/2, ±1/2) 16 個
                    戻るまでの歩数は 1, 2, 3, 4, 6
  φ を入れた 120 個：上の 24 個に (±φ, ±1, ±(φ−1), 0)/2 の偶置換 96 個を足す（単位イコシアン）
                    戻るまでの歩数は 1, 2, 3, 4, 5, 6, 10。並べた 120 点は 600 胞体の頂点

判定は整数と加算だけ。既存の在処：Paper 2026-08-15-quaternion
"""
from __future__ import annotations
from itertools import permutations
from typing import List, Tuple
import random

Z = Tuple[int, int]
Q = Tuple[Z, Z, Z, Z]
Z0: Z = (0, 0)


# ---------------------------------------------------------------- Z[φ]
def zadd(u: Z, v: Z) -> Z:
    return (u[0] + v[0], u[1] + v[1])


def zneg(u: Z) -> Z:
    return (-u[0], -u[1])


def zmul(u: Z, v: Z) -> Z:
    a, b = u
    c, d = v
    return (a * c + b * d, a * d + b * c + b * d)


def zhalf(u: Z) -> Z:
    assert u[0] % 2 == 0 and u[1] % 2 == 0, u
    return (u[0] // 2, u[1] // 2)


def zstr(u: Z) -> str:
    a, b = u
    m = lambda v: ("−" if v < 0 else "") + str(abs(v))
    if b == 0:
        return m(a)
    bb = {1: "φ", -1: "−φ"}.get(b, m(b) + "φ")
    if a == 0:
        return bb
    return f"{m(a)} {'+' if b > 0 else '−'} {'' if abs(b) == 1 else abs(b)}φ"


# ---------------------------------------------------------------- 四元数
def qmul_raw(p: Q, q: Q) -> Q:
    """ハミルトンの掛け算（そのまま）。"""
    a1, b1, c1, d1 = p
    a2, b2, c2, d2 = q
    s = lambda *t: (sum(x[0] for x in t), sum(x[1] for x in t))
    n = zneg
    return (s(zmul(a1, a2), n(zmul(b1, b2)), n(zmul(c1, c2)), n(zmul(d1, d2))),
            s(zmul(a1, b2), zmul(b1, a2), zmul(c1, d2), n(zmul(d1, c2))),
            s(zmul(a1, c2), n(zmul(b1, d2)), zmul(c1, a2), zmul(d1, b2)),
            s(zmul(a1, d2), zmul(b1, c2), n(zmul(c1, b2)), zmul(d1, a2)))


def qmul(P: Q, R: Q) -> Q:
    """2 倍して持った四元数どうしの掛け算：(2p)(2q) ÷ 2 = 2(pq)。"""
    return tuple(zhalf(c) for c in qmul_raw(P, R))


def conj(q: Q) -> Q:
    return (q[0], zneg(q[1]), zneg(q[2]), zneg(q[3]))


def norm(q: Q) -> Z:
    return zadd(zadd(zmul(q[0], q[0]), zmul(q[1], q[1])), zadd(zmul(q[2], q[2]), zmul(q[3], q[3])))


def dot(p: Q, q: Q) -> Z:
    return zadd(zadd(zmul(p[0], q[0]), zmul(p[1], q[1])), zadd(zmul(p[2], q[2]), zmul(p[3], q[3])))


def qneg(q: Q) -> Q:
    return tuple(zneg(c) for c in q)


ONE: Q = ((2, 0), Z0, Z0, Z0)          # 1 を 2 倍したもの


def order(q: Q, limit: int = 200) -> int:
    x, k = q, 1
    while x != ONE:
        x = qmul(x, q)
        k += 1
        if k > limit:
            return 0
    return k


def rotate(Q2: Q, V2: Q) -> Q:
    """点 v（2 倍して持つ）を q v q̄ で挟む。(2q)(2v)(2q̄) = 4·(2·q v q̄) なので 4 で割る。"""
    r = qmul_raw(qmul_raw(Q2, V2), conj(Q2))
    out = []
    for c in r:
        assert c[0] % 4 == 0 and c[1] % 4 == 0, c
        out.append((c[0] // 4, c[1] // 4))
    return tuple(out)


# ---------------------------------------------------------------- 24 個と 120 個（どれも 2 倍で持つ）
def parity(p) -> int:
    s, seen = 1, [False] * len(p)
    for i in range(len(p)):
        if seen[i]:
            continue
        j, ln = i, 0
        while not seen[j]:
            seen[j] = True
            j = p[j]
            ln += 1
        if ln % 2 == 0:
            s = -s
    return s


def hurwitz24() -> List[Q]:
    out = []
    for i in range(4):
        for s in (2, -2):
            v = [Z0] * 4
            v[i] = (s, 0)
            out.append(tuple(v))
    for m in range(16):
        out.append(tuple((1 if (m >> k) & 1 else -1, 0) for k in range(4)))
    return out


def icosian120(all_perms: bool = False) -> List[Q]:
    out = set(hurwitz24())
    base = [(0, 1), (1, 0), (-1, 1), Z0]                 # φ, 1, φ − 1, 0
    for p in permutations(range(4)):
        if not all_perms and parity(p) != 1:
            continue
        for m in range(8):
            signs = [1 if (m >> k) & 1 else -1 for k in range(3)] + [1]
            v = [base[i] if signs[i] > 0 else zneg(base[i]) for i in range(4)]
            out.add(tuple(v[p[i]] for i in range(4)))
    return sorted(out)


def closed(G: List[Q]) -> bool:
    """どの二つを掛けても G の中に着地するか。2 で割り切れない積が出たら、その時点で外に出ている。"""
    S = set(G)
    for a in G:
        for b in G:
            r = qmul_raw(a, b)
            if any(c[0] % 2 or c[1] % 2 for c in r):
                return False
            if tuple(zhalf(c) for c in r) not in S:
                return False
    return True


if __name__ == "__main__":
    print("== 掛け算の表（i, j, k）")
    I_ = (Z0, (2, 0), Z0, Z0)
    J_ = (Z0, Z0, (2, 0), Z0)
    K_ = (Z0, Z0, Z0, (2, 0))
    name = {ONE: "1", qneg(ONE): "−1", I_: "i", qneg(I_): "−i", J_: "j", qneg(J_): "−j", K_: "k", qneg(K_): "−k"}
    for a, an in [(I_, "i"), (J_, "j"), (K_, "k")]:
        print("  ", "  ".join(f"{an}·{bn} = {name[qmul(a, b)]:>2}" for b, bn in [(I_, "i"), (J_, "j"), (K_, "k")]))
    print("   i·j·k =", name[qmul(qmul(I_, J_), K_)])
    print()

    print("== 長さは掛け算で掛け合わされる：N(pq) = N(p)·N(q)（整数の四元数 2000 組）")
    random.seed(13)
    ok = True
    for _ in range(2000):
        p = tuple((random.randint(-9, 9), 0) for _ in range(4))
        q = tuple((random.randint(-9, 9), 0) for _ in range(4))
        ok &= norm(qmul_raw(p, q)) == zmul(norm(p), norm(q))
    print("   例 (1,2,3,4)·(5,6,7,8)：", [zstr(c) for c in qmul_raw(*[tuple((v, 0) for v in t) for t in [(1, 2, 3, 4), (5, 6, 7, 8)]])],
          " 30 × 174 =", 30 * 174, "  一致", ok)
    print()

    print("== 整数で閉じる 24 個")
    H = hurwitz24()
    print("   個数", len(H), "  長さ（2 倍で持つので 4）", sorted({zstr(norm(q)) for q in H}), "  掛け算で閉じる", closed(H))
    hist = {}
    for q in H:
        hist[order(q)] = hist.get(order(q), 0) + 1
    print("   戻るまでの歩数と個数", dict(sorted(hist.items())))
    print()

    print("== φ を入れた 120 個（単位イコシアン）")
    V = icosian120()
    print("   個数", len(V), "  長さ", sorted({zstr(norm(q)) for q in V}), "  掛け算で閉じる", closed(V))
    hist = {}
    for q in V:
        hist[order(q)] = hist.get(order(q), 0) + 1
    print("   戻るまでの歩数と個数", dict(sorted(hist.items())))
    W = icosian120(all_perms=True)
    print("   対照：偶置換でなく全部の並べ替えにすると", len(W), "個、掛け算で閉じる", closed(W))
    print()

    print("== 600 胞体として並べる")
    edge = (0, 2)                                       # 2 倍どうしの内積 4·(φ/2) = 2φ
    E = [(a, b) for a in range(120) for b in range(a + 1, 120) if dot(V[a], V[b]) == edge]
    deg = {}
    for a, b in E:
        deg[a] = deg.get(a, 0) + 1
        deg[b] = deg.get(b, 0) + 1
    near = max((dot(V[0], V[b]) for b in range(1, 120)), key=lambda u: (u[0] + u[1] * 1.618034))
    print("   いちばん近い点との内積（2 倍どうし）", zstr(near), "＝ 4 × φ/2")
    print("   辺", len(E), "本、どの点からも", sorted(set(deg.values())), "本")
    layers = {}
    for q in V:
        layers[q[0]] = layers.get(q[0], 0) + 1
    order_w = sorted(layers, key=lambda u: -(u[0] + u[1] * 1.618034))
    print("   第 1 成分で切った層（2 倍の値：個数）", [(zstr(w), layers[w]) for w in order_w])
    print("   合計", sum(layers.values()))
    print()

    print("== 回す：72° の一歩を正 20 面体の頂点に 5 回")
    q72 = next(q for q in V if order(q) == 10 and q[0] == (0, 1))
    print("   q（2 倍）=", [zstr(c) for c in q72], "  戻るまで", order(q72), "歩（回転としては q と −q が同じなので 5 回）")
    v = (Z0, Z0, (0, 1), (1, 0))                         # 正 20 面体の頂点 (0, φ, 1)/2 を 2 倍したもの
    r = v
    for n in range(1, 6):
        r = rotate(q72, r)
        print(f"   {n} 回目", [zstr(c) for c in r], "  元に戻った" if r == v else "")
    print()

    print("== 120 個で正 20 面体の 12 頂点を回す")
    ico = set()
    for s1 in (1, -1):
        for s2 in (1, -1):
            A, B = (0, s1), (s2, 0)                       # ±φ, ±1
            ico |= {(Z0, Z0, A, B), (Z0, A, B, Z0), (Z0, B, Z0, A)}
    miss = sum(1 for q in V for p in ico if rotate(q, p) not in ico)
    kinds = {tuple(rotate(q, p) for p in sorted(ico)) for q in V}
    print("   頂点", len(ico), "個 × 120 回転のうち、正 20 面体の頂点に着地しなかったもの", miss)
    print("   回転の種類", len(kinds), "（q と −q が同じ回転なので 120 ÷ 2）")
    print()

    print("== 掛けては戻すを 20000 回")
    random.seed(13)
    word = [random.randrange(120) for _ in range(20000)]
    x = ONE
    for k in word:
        x = qmul(x, V[k])
    mid = x
    for k in reversed(word):
        x = qmul(x, conj(V[k]))
    print("   途中も 120 個のどれか:", mid in set(V), "  戻した結果が 1:", x == ONE)

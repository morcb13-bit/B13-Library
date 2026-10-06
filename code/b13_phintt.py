"""
b13_phintt.py ― 十の番地を Z[φ] で回す変換（φ-NTT）
=====================================================
輪を 10 等分した番地 k（一番地 36°）で、cos と sin を Z[φ] の数（整数の組）として持つ。
  cos の側：2cos(36°·k)            → 2, φ, φ−1, 1−φ, −φ, −2, …
  sin の側：sin(36°·k) ÷ sin 36°   → 0, 1, φ, φ, 1, 0, −1, −φ, −φ, −1
  二つをつなぐ数：SIN2 = 4·sin²36° = 3 − φ

  変換（十の番地の列 x を二つの列 A, B に）：
      A[m] = Σ_k 2cos(36°·mk)·x[k]       B[m] = Σ_k (sin(36°·mk) ÷ sin 36°)·x[k]
  戻す：  40·x[k] = Σ_m 2cos(36°·mk)·A[m] + SIN2·Σ_m (sin(36°·mk) ÷ sin 36°)·B[m]
  畳み込み（十の番地を一周する畳み込み）は、変換の側で掛け算になる：
      2·A_y = A_x·A_h − SIN2·B_x·B_h      2·B_y = A_x·B_h + B_x·A_h
  偶数番と奇数番に分ける：
      A[m] = (偶数番の和) + (奇数番の和)、A[m+5] = (偶数番の和) − (奇数番の和)
  桁ごとに重ねる：10^B 番地の列を、桁ごとに（繰り上がりなしで）同じ変換にかける。2^B 本の列になる

判定は整数と加算だけ。Z[φ] の数は (a, b) = a + bφ、φ² = φ + 1。
既存の在処：Paper 2026-02-26-phi-ntt
"""
from __future__ import annotations
from typing import Dict, List, Tuple

Z = Tuple[int, int]
ZERO: Z = (0, 0)


# ---------------------------------------------------------------- Z[φ]
def zadd(u: Z, v: Z) -> Z:
    return (u[0] + v[0], u[1] + v[1])


def zneg(u: Z) -> Z:
    return (-u[0], -u[1])


def zmul(u: Z, v: Z) -> Z:
    a, b = u
    c, d = v
    return (a * c + b * d, a * d + b * c + b * d)


def zint(n: int) -> Z:
    return (n, 0)


def zsum(xs) -> Z:
    s = ZERO
    for x in xs:
        s = zadd(s, x)
    return s


def zdiv_exact(u: Z, n: int) -> Z:
    """整数 n で割る。割り切れなければ止める。"""
    a, b = u
    assert a % n == 0 and b % n == 0, (u, n)
    return (a // n, b // n)


def zstr(u: Z) -> str:
    a, b = u
    m = lambda v: ("−" if v < 0 else "") + str(abs(v))
    if b == 0:
        return m(a)
    bb = {1: "φ", -1: "−φ"}.get(b, m(b) + "φ")
    if a == 0:
        return bb
    return f"{m(a)} {'+' if b > 0 else '−'} {'' if abs(b) == 1 else abs(b)}φ"


# ---------------------------------------------------------------- 十の番地の表
PHI: Z = (0, 1)
COS2: List[Z] = [(2, 0), (0, 1), (-1, 1), (1, -1), (0, -1), (-2, 0), (0, -1), (1, -1), (-1, 1), (0, 1)]   # 2cos(36°k)
SINR: List[Z] = [(0, 0), (1, 0), (0, 1), (0, 1), (1, 0), (0, 0), (-1, 0), (0, -1), (0, -1), (-1, 0)]     # sin(36°k)/sin36°
SIN2: Z = (3, -1)                                                                                       # 4 sin²36°


def addr(m: int, k: int) -> int:
    """番地 m·k を 10 で回した場所（足し算で数える）。"""
    j = 0
    for _ in range(k):
        j += m
        while j >= 10:
            j += -10
    return j


def forward(x: List[Z]) -> Tuple[List[Z], List[Z]]:
    A = [zsum(zmul(COS2[addr(m, k)], x[k]) for k in range(10)) for m in range(10)]
    B = [zsum(zmul(SINR[addr(m, k)], x[k]) for k in range(10)) for m in range(10)]
    return A, B


def inverse(A: List[Z], B: List[Z]) -> List[Z]:
    out = []
    for k in range(10):
        c = zsum(zmul(COS2[addr(m, k)], A[m]) for m in range(10))
        s = zsum(zmul(SINR[addr(m, k)], B[m]) for m in range(10))
        out.append(zdiv_exact(zadd(c, zmul(SIN2, s)), 40))
    return out


def cyc_conv(x: List[Z], h: List[Z]) -> List[Z]:
    """十の番地を一周する畳み込み（第15章の畳み込みを輪にしたもの）。"""
    return [zsum(zmul(h[j], x[addr(1, k + (10 - j))]) for j in range(10)) for k in range(10)]


def mult(Ax, Bx, Ah, Bh):
    """変換の側での掛け算。"""
    Ay = [zdiv_exact(zadd(zmul(Ax[m], Ah[m]), zneg(zmul(SIN2, zmul(Bx[m], Bh[m])))), 2) for m in range(10)]
    By = [zdiv_exact(zadd(zmul(Ax[m], Bh[m]), zmul(Bx[m], Ah[m])), 2) for m in range(10)]
    return Ay, By


def butterfly(x: List[Z]):
    """偶数番と奇数番に分けて A[m] と A[m+5] を作る。"""
    E = [zsum(zmul(COS2[addr(m, k)], x[k]) for k in range(0, 10, 2)) for m in range(5)]
    O = [zsum(zmul(COS2[addr(m, k)], x[k]) for k in range(1, 10, 2)) for m in range(5)]
    return [zadd(E[m], O[m]) for m in range(5)] + [zadd(E[m], zneg(O[m])) for m in range(5)]


# ---------------------------------------------------------------- 桁ごとに重ねる（10^B 番地）
def digits(n: int, B: int) -> List[int]:
    d = []
    for _ in range(B):
        r = n
        q = 0
        while r >= 10:
            r += -10
            q += 1
        d.append(r)
        n = q
    return d


def undigits(d: List[int]) -> int:
    n = 0
    for v in reversed(d):
        n = n * 10 + v
    return n


def forward_B(x: List[Z], B: int) -> Dict[int, List[Z]]:
    """桁 b ごとに変換をかける。印 S（ビットの集まり）の b 番目が 1 なら sin の側。2^B 本の列になる。"""
    N = 10 ** B
    ch: Dict[int, List[Z]] = {0: list(x)}
    for b in range(B):
        new: Dict[int, List[Z]] = {}
        step = 10 ** b
        for S, v in ch.items():
            Tc, Uc = [ZERO] * N, [ZERO] * N
            for n in range(N):
                d = digits(n, B)
                if d[b] != 0:
                    continue
                line = [v[n + k * step] for k in range(10)]
                A, Bs = forward(line)
                for m in range(10):
                    Tc[n + m * step], Uc[n + m * step] = A[m], Bs[m]
            new[S] = Tc
            new[S | (1 << b)] = Uc
        ch = new
    return ch


def inverse_B(ch: Dict[int, List[Z]], B: int) -> List[Z]:
    N = 10 ** B
    for b in reversed(range(B)):
        step = 10 ** b
        new: Dict[int, List[Z]] = {}
        for S in [s for s in ch if not s & (1 << b)]:
            Tc, Uc = ch[S], ch[S | (1 << b)]
            out = [ZERO] * N
            for n in range(N):
                if digits(n, B)[b] != 0:
                    continue
                x = inverse([Tc[n + m * step] for m in range(10)], [Uc[n + m * step] for m in range(10)])
                for k in range(10):
                    out[n + k * step] = x[k]
            new[S] = out
        ch = new
    return ch[0]


def cf_conv(x: List[Z], h: List[Z], B: int) -> List[Z]:
    """繰り上がりなしの畳み込み：番地を桁ごとに引く。"""
    N = 10 ** B
    D = [digits(n, B) for n in range(N)]
    out = []
    for n in range(N):
        s = ZERO
        for m in range(N):
            if h[m] == ZERO:
                continue
            idx = undigits([(D[n][i] - D[m][i]) % 10 for i in range(B)])
            s = zadd(s, zmul(h[m], x[idx]))
        out.append(s)
    return out


def mult_B(cx: Dict[int, List[Z]], ch_: Dict[int, List[Z]], B: int) -> Dict[int, List[Z]]:
    """変換の側での掛け算（2^B 本の列どうし）。sin の側が重なった桁ごとに −SIN2 が一つ掛かる。"""
    N = 10 ** B
    out = {S: [ZERO] * N for S in cx}
    negs = zneg(SIN2)
    for S, u in cx.items():
        for T, v in ch_.items():
            R = S ^ T
            f: Z = (1, 0)
            both = S & T
            while both:
                if both & 1:
                    f = zmul(f, negs)
                both >>= 1
            for n in range(N):
                out[R][n] = zadd(out[R][n], zmul(f, zmul(u[n], v[n])))
    return {S: [zdiv_exact(w, 2 ** B) for w in vals] for S, vals in out.items()}


def label(S: int, B: int) -> str:
    return "".join("U" if S & (1 << b) else "T" for b in reversed(range(B)))


if __name__ == "__main__":
    print("== 十の番地の表（Z[φ] の数）")
    print("番地      ", list(range(10)))
    print("2cos(36°k)", [zstr(v) for v in COS2])
    print("sin比     ", [zstr(v) for v in SINR])
    print("SIN2 = 4·sin²36° =", zstr(SIN2), "  確かめ：sin 比どうしで (2cos)² + SIN2·(sin 比)² = 4 →",
          sorted({zstr(zadd(zmul(COS2[k], COS2[k]), zmul(SIN2, zmul(SINR[k], SINR[k])))) for k in range(10)}))
    print()

    print("== 変換して戻す")
    x = [zint(v) for v in [3, 1, 4, 1, 5, 9, 2, 6, 5, 3]]
    A, Bs = forward(x)
    print("x  ", [zstr(v) for v in x])
    print("A  ", [zstr(v) for v in A])
    print("B  ", [zstr(v) for v in Bs])
    print("戻す", [zstr(v) for v in inverse(A, Bs)], "  一致", inverse(A, Bs) == x)
    print()

    print("== 一つの輪だけを入れる")
    for name, sig in [("番地 0 だけ 1", [1] + [0] * 9), ("全部 1", [1] * 10), ("交互 +1 −1", [1, -1] * 5),
                      ("2cos(36°k)", None)]:
        xs = COS2 if sig is None else [zint(v) for v in sig]
        A, Bs = forward(xs)
        print(f"{name:<12} A {[zstr(v) for v in A]}")
        print(f"{'':<12} B {[zstr(v) for v in Bs]}")
    print()

    print("== 畳み込みは、変換の側で掛け算になる")
    h = [zint(v) for v in [1, 2, 0, 0, 0, 0, 0, 0, 0, -1]]
    direct = cyc_conv(x, h)
    Ax, Bx = forward(x)
    Ah, Bh = forward(h)
    Ay, By = mult(Ax, Bx, Ah, Bh)
    via = inverse(Ay, By)
    print("h        ", [zstr(v) for v in h])
    print("直接     ", [zstr(v) for v in direct])
    print("変換経由 ", [zstr(v) for v in via], "  一致", via == direct)
    print()

    print("== 偶数番と奇数番に分ける：A[m] と A[m+5] は、同じ二つの和の足し引き")
    print("分けて作る", [zstr(v) for v in butterfly(x)])
    print("そのまま  ", [zstr(v) for v in forward(x)[0]], "  一致", butterfly(x) == forward(x)[0])
    print()

    print("== 桁ごとに重ねる（10^B 番地、繰り上がりなし）")
    for B in (1, 2, 3):
        N = 10 ** B
        xs = [zint(((7 * n + 3) * (n + 1)) % 11 - 5) for n in range(N)]
        hs = [ZERO] * N
        hs[0], hs[1], hs[undigits([0] * (B - 1) + [1]) if B > 1 else 1] = zint(2), zint(-1), zint(1)
        cx = forward_B(xs, B)
        back = inverse_B(cx, B)
        cy = mult_B(cx, forward_B(hs, B), B)
        via = inverse_B(cy, B)
        ok_conv = via == cf_conv(xs, hs, B)
        print(f"B = {B}: 番地 {N}、列の本数 {len(cx)} {[label(S, B) for S in sorted(cx)]}")
        print(f"        戻すと一致 {back == xs}   畳み込みの一致 {ok_conv}")

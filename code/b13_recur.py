"""
b13_recur.py ― 漸化式と畳み込みを足し算だけで
==============================================
  二つ前から作る：s(n+2) = p·s(n+1) − q·s(n)
      フィボナッチ p=1, q=−1 ／ ペル p=2, q=−1 ／ cos の表（第11章）p=2c(1), q=1
  変わらない量：  点 (a, b) = (s(n), s(n+1)) について  b² − p·a·b + q·a²
      一歩ごとに q 倍される。q = 1 なら変わらない
  分かれ目：      D = p² − 4q の符号。負なら回る、0 ならまっすぐ、正なら開く
  整数で回るのは：q = 1 のとき p = −1, 0, 1 だけ（3, 4, 6 歩で戻る）
  五歩で戻る回転：p を Z[φ] の数（φ − 1 など）にすると出る
  畳み込み：      二つの列の「ずらして掛けて足す」。漸化式は短い列 (1, −p, q) との畳み込みで
                  元の列が先頭だけ残して消えること、と言い直せる

判定は整数と加算だけ（Z[φ] の数は整数の組 (a, b) = a + bφ）。
"""
from __future__ import annotations
from typing import List, Tuple

Pair = Tuple[int, int]


# ---------------------------------------------------------------- 二つ前から作る
def seq(p: int, q: int, a: int, b: int, n: int) -> List[int]:
    out = [a, b]
    while len(out) < n:
        out.append(p * out[-1] + -(q * out[-2]))
    return out[:n]


def form(p: int, q: int, a: int, b: int) -> int:
    """b² − p·a·b + q·a²。"""
    return b * b + -(p * a * b) + q * a * a


def disc(p: int, q: int) -> int:
    return p * p + -(4 * q)


def kind(p: int, q: int) -> str:
    d = disc(p, q)
    return "回る" if d < 0 else ("まっすぐ" if d == 0 else "開く")


def period(p: int, q: int, a: int = 0, b: int = 1, limit: int = 100) -> int:
    """(a, b) に戻るまでの歩数。戻らなければ 0。"""
    x, y = a, b
    for k in range(1, limit + 1):
        x, y = y, p * y + -(q * x)
        if (x, y) == (a, b):
            return k
    return 0


# ---------------------------------------------------------------- Z[φ] の数（a + bφ、φ² = φ + 1）
def zadd(u: Pair, v: Pair) -> Pair:
    return (u[0] + v[0], u[1] + v[1])


def zneg(u: Pair) -> Pair:
    return (-u[0], -u[1])


def zmul(u: Pair, v: Pair) -> Pair:
    a, b = u
    c, d = v
    return (a * c + b * d, a * d + b * c + b * d)


def zperiod(p: Pair, a: Pair = (0, 0), b: Pair = (1, 0), limit: int = 100) -> int:
    x, y = a, b
    for k in range(1, limit + 1):
        x, y = y, zadd(zmul(p, y), zneg(x))
        if (x, y) == (a, b):
            return k
    return 0


def zform(p: Pair, a: Pair, b: Pair) -> Pair:
    """b² − p·a·b + a²（q = 1）。"""
    return zadd(zadd(zmul(b, b), zneg(zmul(p, zmul(a, b)))), zmul(a, a))


def zshow(u: Pair) -> str:
    a, b = u
    if b == 0:
        return f"{a}".replace("-", "−")
    if a == 0:
        return {1: "φ", -1: "−φ"}.get(b, f"{b}φ")
    bs = {1: "+ φ", -1: "− φ"}.get(b, f"{'+' if b > 0 else '−'} {abs(b)}φ")
    return f"{a} {bs}".replace("-", "−")


# ---------------------------------------------------------------- 畳み込み
def conv(x: List[int], y: List[int], n: int = None) -> List[int]:
    """ずらして掛けて足す。長さ n で切る。"""
    if n is None:
        n = len(x) + len(y) - 1
    out = [0] * n
    for i, xi in enumerate(x):
        for j, yj in enumerate(y):
            if i + j < n:
                out[i + j] += xi * yj
    return out


def unroll(head: List[int], p: int, q: int, n: int) -> List[int]:
    """畳み込みを戻す：(1, −p, q) で割る。やることは漸化式そのもの。"""
    s: List[int] = []
    for k in range(n):
        v = head[k] if k < len(head) else 0
        if k >= 1:
            v += p * s[k - 1]
        if k >= 2:
            v += -(q * s[k - 2])
        s.append(v)
    return s


def carry(digits: List[int], base: int = 10) -> List[int]:
    """桁ごとの数を繰り上げて、0〜base−1 の桁にする（下の桁から）。"""
    out, c = [], 0
    for d in digits:
        v = d + c
        c = 0
        while v >= base:
            v += -base
            c += 1
        out.append(v)
    while c:
        v = c
        c = 0
        while v >= base:
            v += -base
            c += 1
        out.append(v)
    return out


def digits_low(n: int) -> List[int]:
    return [int(ch) for ch in reversed(str(n))]


if __name__ == "__main__":
    print("== 二つ前から作る：s(n+2) = p·s(n+1) − q·s(n)")
    for name, p, q, a, b in [("フィボナッチ", 1, -1, 0, 1), ("リュカ", 1, -1, 2, 1), ("ペル", 2, -1, 0, 1),
                             ("2ⁿ", 3, 2, 1, 2), ("n", 2, 1, 0, 1)]:
        s = seq(p, q, a, b, 12)
        fs = [form(p, q, s[i], s[i + 1]) for i in range(8)]
        print(f"{name:<6} p={p:>2} q={q:>2}  {s}")
        print(f"{'':<6} b²−p·ab+q·a² = {fs}")
    print()

    print("== q = 1 で p を変える：D = p² − 4 の符号と、(0, 1) に戻るまでの歩数")
    for p in range(-4, 5):
        s = seq(p, 1, 0, 1, 10)
        per = period(p, 1)
        f = sorted({form(p, 1, s[i], s[i + 1]) for i in range(9)})
        print(f"p = {p:>2}  D = {disc(p, 1):>3}  {kind(p, 1):<4}  戻る歩数 {per if per else '戻らない':<4}  変わらない量 {f}  列 {s}")
    print()

    print("== Z[φ] の p：五歩・十歩で戻る回転")
    for p in [(-1, 0), (0, 0), (1, 0), (-1, 1), (0, -1), (0, 1), (1, -1)]:
        x, y, forms = (0, 0), (1, 0), set()
        for _ in range(12):
            forms.add(zform(p, x, y))
            x, y = y, zadd(zmul(p, y), zneg(x))
        print(f"p = {zshow(p):<7} 戻る歩数 {zperiod(p):>2}   変わらない量 {[zshow(f) for f in sorted(forms)]}")
    found = {}
    for a in range(-6, 7):
        for b in range(-6, 7):
            k = zperiod((a, b), limit=60)
            if k:
                found.setdefault(k, []).append(zshow((a, b)))
    print("p = a + bφ（a, b は −6〜6）で戻るもの:", {k: found[k] for k in sorted(found)})
    x, y, out = (0, 0), (1, 0), []
    for _ in range(6):
        out.append(zshow(x))
        x, y = y, zadd(zmul((-1, 1), y), zneg(x))
    print("p = φ − 1 の列:", out)
    print()

    print("== 畳み込み：漸化式は (1, −p, q) との畳み込みで消える")
    f = seq(1, -1, 0, 1, 14)
    print("フィボナッチ            ", f)
    print("× (1, −1, −1)           ", conv(f, [1, -1, -1], 14))
    print("先頭 (0, 1) を割り戻す   ", unroll([0, 1], 1, -1, 14))
    pe = seq(2, -1, 0, 1, 10)
    print("ペル × (1, −2, −1)      ", conv(pe, [1, -2, -1], 10))
    ff = conv(f, f, 14)
    print("フィボナッチ × フィボナッチ", ff)
    k2 = conv([1, -1, -1], [1, -1, -1])
    print("  (1,−1,−1) × (1,−1,−1) =", k2, " これで消える:", conv(ff, k2, 14))
    row = [1]
    for _ in range(6):
        row = conv(row, [1, 1])
    print("(1, 1) を 6 回畳み込む   ", row)
    print()

    print("== 整数の掛け算は、桁の畳み込みと繰り上がり")
    for x, y in [(1234, 5678), (3120, 3120), (89, 144)]:
        c = conv(digits_low(x), digits_low(y))
        r = carry(c)
        val = int("".join(str(d) for d in reversed(r)))
        print(f"{x} × {y}: 桁の畳み込み（下の桁から）{c} → 繰り上げ {val}   一致 {val == x * y}")

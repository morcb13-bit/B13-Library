"""
b13_phi.py ― 平衡φ進と Zeckendorf を足し算だけで扱う
=======================================================
二つの繰り上がり規則（どちらも足し算の恒等式）だけで桁を整える。

  規則A  隣り合う二つを一つ上へ    φ^k + φ^(k+1) = φ^(k+2)       （F_k + F_(k+1) = F_(k+2)）
  規則B  同じ桁の二つを上と下へ    φ^k + φ^k    = φ^(k+1) + φ^(k-2)
  規則C  上が +1・下が −1 の組を一つ下へ   φ^(k+1) − φ^k = φ^(k-1)   （平衡φ進だけ）

平衡φ進：桁の重みは φ^k（k は負にも伸びる）、桁は −1, 0, +1。
Zeckendorf：桁の重みは 1, 2, 3, 5, 8, …（フィボナッチ数）、桁は 0, 1。

値は Z[φ] の整数の組 (a, b) ＝ a + bφ で持つ。φ を掛けるのは (a, b) → (b, a+b)。
浮動小数・割り算・剰余は使わない。

既存の在処：
  2026-06-20-BpVM/phi_base_engine.py （平衡φ進：mpmath の浮動小数で貪欲に展開）
  この版はそれを整数の組と繰り上がり規則に書き直したもの。
"""
from __future__ import annotations
from typing import Dict, List, Tuple

Pair = Tuple[int, int]          # a + bφ
PhiDigits = Dict[int, int]      # 位置 k → 桁


# ---------------------------------------------------------------- Z[φ] の組
def phi_pow(k: int) -> Pair:
    """φ^k を整数の組で。上へは (a,b)→(b,a+b)、下へは (a,b)→(b−a,a)。"""
    p: Pair = (1, 0)
    if k >= 0:
        for _ in range(k):
            p = (p[1], p[0] + p[1])
    else:
        for _ in range(-k):
            p = (p[1] + -p[0], p[0])
    return p


def pair_add(x: Pair, y: Pair) -> Pair:
    return (x[0] + y[0], x[1] + y[1])


def phi_value(d: PhiDigits) -> Pair:
    """桁の値を Z[φ] の組で。桁は ±1 なので、足すか引くかだけ。"""
    v: Pair = (0, 0)
    for k, x in d.items():
        p = phi_pow(k)
        for _ in range(abs(x)):
            v = pair_add(v, p if x > 0 else (-p[0], -p[1]))
    return v


# ---------------------------------------------------------------- 平衡φ進
def _get(d: PhiDigits, k: int) -> int:
    return d.get(k, 0)


def _put(d: PhiDigits, k: int, x: int) -> None:
    if x == 0:
        d.pop(k, None)
    else:
        d[k] = x


def phi_normalize(d: PhiDigits, log: List[str] | None = None) -> PhiDigits:
    """規則A・B・C を当てはまらなくなるまで当てる。
    出来上がり：桁は −1, 0, +1、0 でない桁は隣り合わない。"""
    d = {k: x for k, x in d.items() if x != 0}
    while True:
        fired = False
        for k in sorted(d, reverse=True):
            x = _get(d, k)
            if x == 0:
                continue
            s = 1 if x > 0 else -1
            if x * s >= 2:                                   # 規則B
                _put(d, k, x + -s - s)
                _put(d, k + 1, _get(d, k + 1) + s)
                _put(d, k - 2, _get(d, k - 2) + s)
                if log is not None:
                    log.append(f"B@{k}")
                fired = True
                break
            y = _get(d, k - 1)
            if y == x:                                       # 規則A
                _put(d, k, 0)
                _put(d, k - 1, 0)
                _put(d, k + 1, _get(d, k + 1) + s)
                if log is not None:
                    log.append(f"A@{k - 1}")
                fired = True
                break
            if y == -x:                                      # 規則C
                _put(d, k, 0)
                _put(d, k - 1, 0)
                _put(d, k - 2, _get(d, k - 2) + s)
                if log is not None:
                    log.append(f"C@{k - 1}")
                fired = True
                break
        if not fired:
            return d


def phi_add(a: PhiDigits, b: PhiDigits, log: List[str] | None = None) -> PhiDigits:
    s = dict(a)
    for k, x in b.items():
        s[k] = s.get(k, 0) + x
    return phi_normalize(s, log)


def phi_neg(a: PhiDigits) -> PhiDigits:
    return {k: -x for k, x in a.items()}


def phi_from_decimal(text: str) -> PhiDigits:
    """10進から入る：x を10回足したものに、1 をその桁の回数だけ足す。"""
    t = text.strip()
    negative = t.startswith("-")
    if negative:
        t = t[1:]
    x: PhiDigits = {}
    one: PhiDigits = {0: 1}
    for ch in t:
        y: PhiDigits = {}
        for _ in range(10):
            y = phi_add(y, x)
        x = y
        for _ in range(ord(ch) - ord("0")):
            x = phi_add(x, one)
    return phi_neg(x) if negative else x


# ---------------------------------------------------------------- Zeckendorf
# 位置 i の重みは 1, 2, 3, 5, 8, …（i = 0, 1, 2, …）
def zeck_normalize(z: List[int], log: List[str] | None = None) -> List[int]:
    z = list(z) + [0, 0, 0]
    while True:
        fired = False
        for i in range(len(z) - 1, -1, -1):
            if z[i] >= 2:                                    # 規則B（右端は形が変わる）
                z[i] += -2
                z[i + 1] += 1
                if i == 1:
                    z[0] += 1                                # 2+2 = 3+1
                elif i >= 2:
                    z[i - 2] += 1
                if log is not None:
                    log.append(f"B@{i}")
                fired = True
                break
            if i >= 1 and z[i] >= 1 and z[i - 1] >= 1:      # 規則A
                z[i] += -1
                z[i - 1] += -1
                z[i + 1] += 1
                if log is not None:
                    log.append(f"A@{i - 1}")
                fired = True
                break
        if not fired:
            while len(z) > 1 and z[-1] == 0:
                z.pop()
            return z
        if z[-1] or z[-2]:
            z += [0, 0]


def zeck_add(a: List[int], b: List[int], log: List[str] | None = None) -> List[int]:
    n = max(len(a), len(b))
    s = [(a[i] if i < len(a) else 0) + (b[i] if i < len(b) else 0) for i in range(n)]
    return zeck_normalize(s, log)


def zeck_from_count(n: int) -> List[int]:
    """0 から 1 を n 回足す。"""
    z = [0]
    for _ in range(n):
        z = zeck_add(z, [1])
    return z


def zeck_value(z: List[int]) -> int:
    v, f0, f1 = 0, 1, 2
    for x in z:
        for _ in range(x):
            v += f0
        f0, f1 = f1, f0 + f1
    return v


# ---------------------------------------------------------------- 表記
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def sgn_digit(d: int) -> str:
    return "0" if d == 0 else ("+" if d > 0 else "−") + str(abs(d))


def show_phi(d: PhiDigits) -> str:
    """例 (+1,0.0,+1)ᵩ ＝ φ + φ^(−2)。点は 1 の桁と φ^(−1) の桁のあいだ。"""
    if not d:
        return "(0)ᵩ"
    hi = max(max(d), 0)
    lo = min(min(d), 0)
    out = ""
    for k in range(hi, lo - 1, -1):
        out += sgn_digit(_get(d, k))
        if k == 0 and lo < 0:
            out += "."
        elif k != lo:
            out += ","
    return "(" + out + ")ᵩ"


def show_zeck(z: List[int]) -> str:
    return "(" + ",".join(str(x) for x in reversed(z)) + ")_F"


def show_pair(p: Pair) -> str:
    a, b = p
    sa = ("−" if a < 0 else "") + str(abs(a))
    return f"{sa} {'−' if b < 0 else '+'} {abs(b)}φ"


def dec(n: int) -> str:
    return "(" + ("−" if n < 0 else "") + str(abs(n)) + ")₁₀"


if __name__ == "__main__":
    print("== φ^k を整数の組で（a + bφ）")
    for k in (-3, -2, -1, 0, 1, 2, 3, 4):
        print(f"φ^({sgn_digit(k) if k else 0}) = {show_pair(phi_pow(k))}")
    print()
    print("== 1 を足していく（平衡φ進と Zeckendorf）")
    x: PhiDigits = {}
    z = [0]
    for n in range(1, 11):
        lx: List[str] = []
        lz: List[str] = []
        x = phi_add(x, {0: 1}, lx)
        z = zeck_add(z, [1], lz)
        print(f"{dec(n):>8}  {show_phi(x):<24} 値 {show_pair(phi_value(x)):<8} 規則 {' '.join(lx) or '―':<14}"
              f"  {show_zeck(z):<14} 規則 {' '.join(lz) or '―'}")
    print()
    print("== 符号を裏返す・足す・引く（平衡φ進）")
    a = phi_from_decimal("2026")
    b = phi_neg(a)
    c = phi_from_decimal("1000")
    print(dec(2026), "→", show_phi(a), " 値", show_pair(phi_value(a)))
    print(dec(-2026), "→", show_phi(b), " 値", show_pair(phi_value(b)))
    print(show_phi(a), "+", show_phi(b), "→", show_phi(phi_add(a, b)))
    d = phi_add(a, phi_neg(c))
    print(dec(2026), "−", dec(1000), "→", show_phi(d), " 値", show_pair(phi_value(d)))
    print()
    print("== Zeckendorf")
    for n in (100, 2026):
        zz = zeck_from_count(n)
        print(dec(n), "→", show_zeck(zz), " 値", zeck_value(zz))

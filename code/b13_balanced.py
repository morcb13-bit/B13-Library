"""
b13_balanced.py ― 平衡N進（N は奇数）を足し算だけで扱う
=========================================================
桁は -(N-1)/2 … +(N-1)/2 。平衡13進なら -6…+6、平衡5進なら -2…+2。
桁の並びは「下の桁から」（LSD first）。

使う操作は 足し算・符号の裏返し・大小の比較 だけ。
割り算・剰余・浮動小数は使わない。

既存の在処：
  b13phase_v075/phase_digits.py （BASE=3120 の非平衡・繰り上がり加算）
  この版はそれを平衡桁に書き直したもの。
"""
from __future__ import annotations
from typing import List

Digits = List[int]


def half(N: int) -> int:
    """桁の上限 h = (N-1)/2 を足し算だけで求める（h + h + 1 = N）。"""
    h = 0
    while h + h + 1 < N:
        h += 1
    if h + h + 1 != N:
        raise ValueError("N は奇数")
    return h


def trim(a: Digits) -> Digits:
    """上の桁の 0 を落とす。0 は [0] で表す。"""
    out = list(a)
    while len(out) > 1 and out[-1] == 0:
        out.pop()
    return out


def neg(a: Digits) -> Digits:
    """符号の裏返し：各桁の符号を裏返すだけ。繰り上がりは起きない。"""
    return [-d for d in a]


def add(a: Digits, b: Digits, N: int) -> Digits:
    """桁ごとに足し、はみ出したら N を一つ引いて上へ ±1 を送る。"""
    h = half(N)
    out: Digits = []
    carry = 0
    i = 0
    while i < len(a) or i < len(b) or carry != 0:
        s = carry
        if i < len(a):
            s += a[i]
        if i < len(b):
            s += b[i]
        carry = 0
        if s > h:
            s += -N
            carry = 1
        elif s < -h:
            s += N
            carry = -1
        out.append(s)
        i += 1
    return trim(out) if out else [0]


def sub(a: Digits, b: Digits, N: int) -> Digits:
    """引き算＝裏返したものを足す。"""
    return add(a, neg(b), N)


def sign(a: Digits) -> int:
    """符号は一番上の 0 でない桁の符号そのもの。"""
    for d in reversed(a):
        if d > 0:
            return 1
        if d < 0:
            return -1
    return 0


def times_small(a: Digits, k: int, N: int) -> Digits:
    """小さな非負整数 k 倍 ＝ a を k 回足す。"""
    out: Digits = [0]
    for _ in range(k):
        out = add(out, a, N)
    return out


def from_decimal(text: str, N: int) -> Digits:
    """10進の文字列から入る。x ← x を10回足したもの ＋ 次の桁（足し算だけ）。"""
    s = text.strip()
    negative = s.startswith("-")
    if negative:
        s = s[1:]
    x: Digits = [0]
    for ch in s:
        x = times_small(x, 10, N)
        for _ in range(ord(ch) - ord("0")):    # 1 桁ぶん（0〜9）は 1 をその回数足す
            x = add(x, [1], N)
    return neg(x) if negative else x


def to_int(a: Digits, N: int) -> int:
    """観察者側の読み：10進の整数に戻す（表示用）。"""
    v = 0
    for d in reversed(a):
        v = v * N + d
    return v


def cut(a: Digits, k: int) -> Digits:
    """下の k 桁を捨てる。平衡桁ではこれがそのまま「一番近い値への丸め」になる。"""
    return trim(a[k:]) if len(a) > k else [0]


SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def sgn_digit(d: int) -> str:
    return "0" if d == 0 else ("+" if d > 0 else "−") + str(abs(d))


def show(a: Digits, N: int) -> str:
    """表記：上の桁からカンマで並べ、基数を下付きで添える。例 (+1,−2,−2)₅"""
    return "(" + ",".join(sgn_digit(d) for d in reversed(a)) + ")" + str(N).translate(SUB)


def dec(n: int) -> str:
    """10進の表記。例 (13)₁₀ 、(−2026)₁₀"""
    return "(" + ("−" if n < 0 else "") + str(abs(n)) + ")₁₀"


if __name__ == "__main__":
    for N in (13, 5):
        print(f"== 平衡{N}進（桁 {sgn_digit(-half(N))}…{sgn_digit(half(N))}）")
        x = from_decimal("2026", N)
        y = from_decimal("-2026", N)
        z = from_decimal("1000", N)
        print(dec(2026), "→", show(x, N))
        print(dec(-2026), "→", show(y, N))
        print(show(x, N), "+", show(y, N), "→", show(add(x, y, N), N))
        d = sub(x, z, N)
        print(dec(2026), "−", dec(1000), "→", show(d, N), "=", dec(to_int(d, N)))
        print("符号：", sign(x), sign(y), sign([0]))
        for k in (1, 2):
            c = cut(x, k)
            print(f"下{k}桁を捨てる → {show(c, N)} の {N}^{k} 倍 = {dec(to_int(c, N) * N**k)}")
        print()

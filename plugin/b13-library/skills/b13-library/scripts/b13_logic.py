"""
b13_logic.py ― 振幅を足して半加算器を作り、5桁の加算器と計算尺へ進む
=====================================================================
半加算器：二つの源から波を送り、出口で振幅を足す。
  振幅は 3120 番地の位相を四分の一周（780）ずつ進めたもの：(1,0)→(0,1)→(−1,0)→(0,−1)。
  四分の一周進めるのは (re, im) → (−im, re)。裏返しと入れ替えだけ。
  出口は三種類：
    暗の出口  二つの源から歩数が 2 違う → 両方来ると打ち消す   … 明るければ「和」（XOR）
    明の出口  二つの源から歩数が同じ   → 一つでも来れば明るい … 「または」（OR）
    強の出口  同じく歩数が同じ         → 両方来ると振幅 2     … 「桁上がり」（AND）
  明るいかは振幅が (0,0) でないか、強いかは振幅の成分に ±2 があるかで読む。2乗は使わない。

5桁の加算器：半加算器二つと「または」一つで全加算器、それを5つ並べて桁上がりを送る。

計算尺：13 の輪。1 から倍にしていく（x+x、13 を越えたら 13 を引く）と、12 歩で 12 個の番地を一巡する。
  番地（何回倍にしたか）を目盛りにすると、13 で割った余りの掛け算が目盛りの足し算になる。

既存の在処：
  Paper 2026-09-21-plant-sun/code/ha1.py （ペンローズ担体の上の半加算器：振幅の四値と出口の選び方）
"""
from __future__ import annotations
from typing import List, Tuple

Amp = Tuple[int, int]


# ---------------------------------------------------------------- 振幅
def quarter(v: Amp) -> Amp:
    """四分の一周（780 番地）進める。"""
    return (-v[1], v[0])


def amp_after(steps: int) -> Amp:
    """源を出て steps 歩進んだ振幅。一歩が四分の一周。"""
    v: Amp = (1, 0)
    for _ in range(steps):
        v = quarter(v)
    return v


def at_outlet(sources: List[Tuple[int, int]]) -> Amp:
    """出口に届いた振幅を足す。sources は (送るか 0/1, 歩数) の並び。"""
    re, im = 0, 0
    for on, d in sources:
        if on:
            v = amp_after(d)
            re += v[0]
            im += v[1]
    return (re, im)


def bright(v: Amp) -> int:
    return 0 if v == (0, 0) else 1


def strong(v: Amp) -> int:
    return 1 if v[0] in (2, -2) or v[1] in (2, -2) else 0


# 出口までの歩数（源A, 源B）
DARK = (5, 7)     # 歩数差 2 ＝ 半周 ずれて届く
EVEN = (5, 5)     # 同じ歩数で届く


def half_adder(a: int, b: int) -> Tuple[int, int]:
    """(和, 桁上がり)"""
    s = bright(at_outlet([(a, DARK[0]), (b, DARK[1])]))
    c = strong(at_outlet([(a, EVEN[0]), (b, EVEN[1])]))
    return s, c


def either(a: int, b: int) -> int:
    """「または」：明の出口。"""
    return bright(at_outlet([(a, EVEN[0]), (b, EVEN[1])]))


def full_adder(a: int, b: int, c: int) -> Tuple[int, int]:
    s1, c1 = half_adder(a, b)
    s2, c2 = half_adder(s1, c)
    return s2, either(c1, c2)


def adder(x: List[int], y: List[int]) -> List[int]:
    """桁の列（下の桁から）を足す。桁上がりを順に送る。"""
    out = []
    c = 0
    for a, b in zip(x, y):
        s, c = full_adder(a, b, c)
        out.append(s)
    out.append(c)
    return out


def bits(n: int, k: int) -> List[int]:
    """観察者側の入口：10進の n を k 桁の 0/1 に（下の桁から）。"""
    return [(n >> i) & 1 for i in range(k)]


def from_bits(v: List[int]) -> int:
    return sum(b << i for i, b in enumerate(v))


# ---------------------------------------------------------------- 計算尺（13 の輪）
P = 13


def double(x: int) -> int:
    s = x + x
    if s >= P:
        s += -P
    return s


def scale() -> List[int]:
    """目盛り k に書く数：1 を k 回倍にしたもの。"""
    out = []
    x = 1
    for _ in range(P - 1):
        out.append(x)
        x = double(x)
    return out


SCALE = scale()
WHERE = {v: k for k, v in enumerate(SCALE)}     # 数 → 目盛り


def slide_pos(a: int, b: int) -> int:
    """a と b の目盛りを足す（12 を越えたら 12 を引く）。"""
    k = WHERE[a] + WHERE[b]
    if k >= P - 1:
        k += -(P - 1)
    return k


def slide_mul(a: int, b: int) -> int:
    return SCALE[slide_pos(a, b)]


def slide_div(a: int, b: int) -> int:
    """目盛りを引く。"""
    k = WHERE[a] + -WHERE[b]
    if k < 0:
        k += P - 1
    return SCALE[k]


if __name__ == "__main__":
    print("== 振幅（一歩ごとに四分の一周）")
    print(" ".join(f"{d}歩:{amp_after(d)}" for d in range(5)))
    print()
    print("== 半加算器（出口で振幅を足す）")
    for a in (0, 1):
        for b in (0, 1):
            vd = at_outlet([(a, DARK[0]), (b, DARK[1])])
            ve = at_outlet([(a, EVEN[0]), (b, EVEN[1])])
            s, c = half_adder(a, b)
            print(f"入力 ({a},{b})  暗の出口 {vd!s:<8} 和 {s}   明・強の出口 {ve!s:<8} 桁上がり {c}")
    print()
    print("== 5桁の加算器")
    for x, y in ((13, 7), (21, 13), (31, 31), (19, 12)):
        X, Y = bits(x, 5), bits(y, 5)
        S = adder(X, Y)
        f = lambda v: "(" + ",".join(str(t) for t in reversed(v)) + ")₂"
        print(f"{f(X)} + {f(Y)} → {f(S)}    観察者側の読み {x} + {y} = {from_bits(S)}")
    print()
    print("== 計算尺（13 の輪）")
    print("目盛り:", " ".join(f"{k}" .rjust(3) for k in range(12)))
    print("数    :", " ".join(f"{v}".rjust(3) for v in SCALE))
    for a, b in ((3, 5), (7, 8), (12, 12), (6, 11)):
        print(f"{a} × {b}：目盛り {WHERE[a]} + {WHERE[b]} → 目盛り {slide_pos(a, b)} の数 {slide_mul(a, b)}   （13 で割った余り）")
    for a, b in ((1, 5), (3, 7)):
        print(f"{a} ÷ {b}：目盛り {WHERE[a]} − {WHERE[b]} → 数 {slide_div(a, b)}")
    print("目盛り 3 刻みの組:", [[SCALE[k] for k in range(r, 12, 3)] for r in range(3)])

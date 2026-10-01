"""
b13_constants.py ― 定数 π・e・φ・√5・ln 2 を 3120 の目盛りで読む
===================================================================
定数は、これまでの章の道具で目盛り（1 = 10^40）として作る。
  π：  マチンの式（第11章）
  e：  項を k で割って足す（第10章）
  √5： 桁ごとの開平（第9章）    φ = (1 + √5) ÷ 2
  ln 2：半分にしては k で割って足す（第10章）

3120 の目盛りで読む（平衡展開）：
  残りを 3120 倍し、いちばん近い整数を桁 a(n) にとる。残り ← 残り − a(n)。
  n ≥ 2 の桁は −1560 … +1559 に収まる。足し算・3120 倍（足し算の繰り返し）・比べることだけ。

既存の在処：Paper 2026-05-18-pi-base3120（b13_pi.py、b13_constants_compare.py）
"""
from __future__ import annotations
from typing import List, Tuple
from b13_explog import S, ladder_div, sdiv, show, e_series, ln2_fx
from b13_trig import PI
from b13_roots import sqrt_digits

BASE = 3120


def nearest_div(x: int, m: int) -> Tuple[int, int]:
    """x ÷ m のいちばん近い整数 q と、残り x − q·m（−m/2 … m/2）。"""
    neg = x < 0
    if neg:
        x = -x
    q = ladder_div(x, m)
    r = x + -(q * m)
    if r + r >= m:          # 半分以上残っていたら一つ上へ
        q += 1
        r += -m
    return (-q, -r) if neg else (q, r)


def expand3120(value: int, terms: int) -> Tuple[List[int], int]:
    """目盛りの値を 3120 の平衡展開に。戻り値（桁の並び, 最後の残り）。"""
    digits = []
    r = value
    for _ in range(terms):
        r3120 = 0
        for _ in range(BASE):        # 3120 倍は 3120 回足す
            r3120 += r
        a, r = nearest_div(r3120, S)
        digits.append(a)
    return digits, r


def rebuild(digits: List[int]) -> int:
    """桁から目盛りの値へ戻す（観察者側の確かめ）。"""
    num, den = 0, 1
    for a in digits:
        num = num * BASE + a
        den = den * BASE
    return sdiv(num * S, den)


SQRT5 = int(sqrt_digits(5, 40).replace(".", ""))
PHI = sdiv(S + SQRT5, 2)
E = e_series()[0]
LN2 = ln2_fx()

CONSTANTS = [("π", PI), ("e", E), ("φ", PHI), ("√5", SQRT5), ("ln 2", LN2)]


if __name__ == "__main__":
    print("== 定数（目盛り 40 桁のうち 30 桁を表示）")
    for name, v in CONSTANTS:
        print(f"{name:<5} {show(v)}")
    print()
    print("== 3120 の目盛りで読む（平衡展開、10 段）")
    for name, v in CONSTANTS:
        d, r = expand3120(v, 10)
        print(f"{name:<5} {d}")
    print()
    print("== 段を重ねると、どれだけ近づくか（π）")
    d, _ = expand3120(PI, 10)
    for n in (1, 2, 3, 4, 6, 8, 10):
        diff = abs(rebuild(d[:n]) + -PI)
        print(f"{n:>2} 段  {show(rebuild(d[:n]), 30)}   差 {show(diff, 30)}")
    print()
    print("== 角としての π：半周は 1560 番地（割り切れている）")
    print("半周 = 1560 番地（1560 + 1560 = 3120）")

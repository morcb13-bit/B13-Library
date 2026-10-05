"""
b13_phase.py ― 一周を 3120 番地に刻む位相を足し算だけで扱う
=============================================================
位相は 0 … 3119 の番地。一周すると 0 に戻る。
  足す：      番地を足し、3120 を越えたら 3120 を一つ引く
  裏返す：    3120 から引く（鏡映、角を −角 にする）
  細かく刻む：番地の下にもう一桁（同じく 3120 刻み）をつなぎ、繰り上がりで送る

一周を n 等分する歩幅は、筆算（引けるだけ引く）で桁ごとに求める。
引き切れずに残ったものが残渣で、残渣が 0 になれば n 歩でちょうど一周に着地する。

既存の在処：
  b13phase_v075/constants.py    （BASE=3120 と歩幅の定数）
  b13phase_v075/phase_digits.py （3120 進の桁と繰り上がり加算）
"""
from __future__ import annotations
from typing import List, Tuple

BASE = 3120
HALF = 1560          # 半周
QUARTER = 780        # 四分の一周


# ---------------------------------------------------------------- 一桁の位相
def padd(a: int, b: int) -> int:
    s = a + b
    if s >= BASE:
        s += -BASE
    return s


def pneg(a: int) -> int:
    return 0 if a == 0 else BASE + -a


def psub(a: int, b: int) -> int:
    return padd(a, pneg(b))


def orbit(step: int) -> List[int]:
    """0 から step ずつ足し、0 に戻るまでの番地の列。"""
    out = [0]
    p = padd(0, step)
    while p != 0:
        out.append(p)
        p = padd(p, step)
    return out


def exact_steps() -> List[int]:
    """ちょうど一周に着地する歩幅（足していって 3120 にぴたり当たるもの）。"""
    found = []
    for s in range(1, BASE + 1):
        t = 0
        while t < BASE:
            t += s
        if t == BASE:
            found.append(s)
    return found


# ---------------------------------------------------------------- 細かく刻む（多桁）
Digits = List[int]   # 上の桁から。d[0] が番地、d[1] がその下の桁、…


def dadd(a: Digits, b: Digits) -> Digits:
    """多桁の位相を足す。下の桁から繰り上がりを送り、一番上は一周で 0 に戻る。"""
    out = [0] * len(a)
    carry = 0
    for i in range(len(a) - 1, -1, -1):
        s = a[i] + b[i] + carry
        carry = 0
        if s >= BASE:
            s += -BASE
            carry = 1
        out[i] = s
    return out


def split_turn(n: int, ndig: int) -> Tuple[Digits, int]:
    """一周を n 等分する歩幅を ndig 桁まで筆算で求める（引けるだけ引く）。
    戻り値：(歩幅の桁, 残渣)。残渣が 0 なら n 歩でちょうど一周する。"""
    digits: Digits = []
    rem = 1                     # 「一周」が 1 つ
    for _ in range(ndig):
        # rem を 3120 倍する（3120 回足す）
        r = 0
        for _ in range(BASE):
            r += rem
        q = 0
        while r >= n:           # 引けるだけ引く
            r += -n
            q += 1
        digits.append(q)
        rem = r
    return digits, rem


def walk(step: Digits, times: int) -> Digits:
    p = [0] * len(step)
    for _ in range(times):
        p = dadd(p, step)
    return p


# ---------------------------------------------------------------- 表記
SUB = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")


def show(d: Digits) -> str:
    """例 (624)₃₁₂₀、(445,2674)₃₁₂₀"""
    return "(" + ",".join(str(x) for x in d) + ")" + "3120".translate(SUB)


def degrees(p: int) -> str:
    """観察者側の読み：番地を度に直す（3 度 = 26 番地）。"""
    q, r = divmod(p * 3, 26)
    return f"{q}°" if r == 0 else f"{q}+{r}/26°"


if __name__ == "__main__":
    print("== ちょうど一周に着地する歩幅")
    ex = exact_steps()
    print(f"{len(ex)} 通り：", " ".join(str(s) for s in ex))
    print()
    print("== 歩幅ごとの、0 に戻るまでの歩数")
    for s in (624, 780, 1040, 240, 260, 52, 26, 1000, 1201):
        o = orbit(s)
        print(f"歩幅 {show([s]):<12} {degrees(s):>10}  → {len(o):>4} 歩で一周")
    print()
    print("== 裏返す")
    for p in (624, 780, 1560, 1):
        print(f"{show([p])} → {show([pneg(p)])}   足すと {show([padd(p, pneg(p))])}")
    print()
    print("== 一周を n 等分する（2 桁で筆算）")
    for n in (5, 13, 16, 7, 11):
        st, rem = split_turn(n, 2)
        end = walk(st, n)
        print(f"n={n:>2}  歩幅 {show(st):<18} 残渣 {rem:>2}   {n} 歩で着地 {show(end)}")

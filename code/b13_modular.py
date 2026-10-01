"""
b13_modular.py ― 互除法・剰余・逆元・べき乗の剰余を足し算だけで
====================================================================
  剰余：      m を倍々にした梯子（m, 2m, 4m, …、x+x で作る）を上から引けるだけ引く
  互除法：    大きい方から小さい方を引く。等しくなったところが最大公約数
              （長方形から正方形を切り取っていくのと同じ）
  逆元：      互除法で引くたびに「何を何回引いたか」の組も同じように引いておく
  べき乗の剰余：指数を 1, 2, 4, … の梯子に分け、二乗の梯子から拾って掛ける
              掛け算は「倍にして足す」（ロシア農民の掛け算）を剰余つきで

使う操作は 足す・引く（裏返して足す）・大小の比較 だけ。
"""
from __future__ import annotations
from typing import List, Tuple


# ---------------------------------------------------------------- 梯子と剰余
def ladder(x: int, limit: int) -> List[int]:
    """x, 2x, 4x, … を limit を越えない所まで（x+x で作る）。"""
    out = [x]
    while out[-1] + out[-1] <= limit:
        out.append(out[-1] + out[-1])
    return out


def rem(a: int, m: int) -> int:
    """a を m で割った余り（0 ≤ 余り < m）。a ≥ 0。"""
    for s in reversed(ladder(m, a) if a >= m else []):
        if a >= s:
            a += -s
    return a


# ---------------------------------------------------------------- 互除法
def gcd_sub(a: int, b: int, log: List[Tuple[int, int]] | None = None) -> Tuple[int, int]:
    """引き算の互除法。戻り値は (最大公約数, 引いた回数)。"""
    n = 0
    while a != b:
        if a > b:
            a += -b
        else:
            b += -a
        n += 1
        if log is not None:
            log.append((a, b))
    return a, n


def squares(a: int, b: int) -> List[Tuple[int, int]]:
    """長方形 a×b から切り取る正方形を（辺, 枚数）で。"""
    out = []
    while a != b and a and b:
        if a < b:
            a, b = b, a
        k = 0
        while a > b:
            a += -b
            k += 1
        if a == b:
            k += 1
            out.append((b, k))
            return out
        out.append((b, k))
    if a == b:
        out.append((a, 1))
    return out


# ---------------------------------------------------------------- 逆元
def inverse(a: int, m: int) -> int:
    """a × x ≡ 1 (mod m) となる x。引き算の互除法で、係数の組も一緒に引く。
    各行 (値, 係数) は「値 ≡ 係数 × a (mod m)」を保つ。"""
    r0, s0 = m, 0
    r1, s1 = rem(a, m), 1
    while r1 != 0:
        if r0 >= r1:
            r0 += -r1               # 値を引くときは
            s0 += -s1               # 係数も引く
        else:
            r0, s0, r1, s1 = r1, s1, r0, s0
    if r0 != 1:
        raise ValueError("逆元なし（最大公約数が 1 でない）")
    while s0 < 0:
        s0 += m
    return rem(s0, m)


# ---------------------------------------------------------------- 掛け算とべき乗の剰余
def split2(e: int) -> List[bool]:
    """e を 1, 2, 4, … の和に分ける（梯子を上から引けるだけ引く）。下の桁から。"""
    if e == 0:
        return []
    lad = ladder(1, e)
    used = [False] * len(lad)
    for i in range(len(lad) - 1, -1, -1):
        if e >= lad[i]:
            e += -lad[i]
            used[i] = True
    return used


def mulmod(a: int, b: int, m: int) -> int:
    """a × b を m で割った余り。b を倍にしながら、a の分け方で拾って足す。"""
    a, b = rem(a, m), rem(b, m)
    acc = 0
    for bit in split2(a):
        if bit:
            acc = rem(acc + b, m)
        b = rem(b + b, m)
    return acc


def powmod(g: int, e: int, m: int) -> int:
    """g の e 乗を m で割った余り。二乗の梯子から、e の分け方で拾って掛ける。"""
    acc = rem(1, m)
    sq = rem(g, m)
    for bit in split2(e):
        if bit:
            acc = mulmod(acc, sq, m)
        sq = mulmod(sq, sq, m)
    return acc


def order(g: int, m: int) -> int:
    """g を何回掛けると 1 に戻るか。"""
    x, k = rem(g, m), 1
    while x != 1:
        x = mulmod(x, g, m)
        k += 1
    return k


if __name__ == "__main__":
    print("== 剰余（倍々の梯子を上から引く）")
    for a, m in ((2026, 13), (2026, 3120), (10 ** 12 + 39, 13)):
        print(f"{a} を {m} で割った余り → {rem(a, m)}   梯子 {len(ladder(m, a))} 段")
    print()
    print("== 引き算の互除法")
    for a, b in ((3120, 2026), (89, 55), (2026, 13), (240, 3120)):
        g, n = gcd_sub(a, b)
        print(f"({a}, {b}) → 最大公約数 {g}   引いた回数 {n}   正方形 {squares(a, b)}")
    print()
    print("== フィボナッチ数の組は、正方形が一枚ずつ")
    print(squares(233, 144))
    print()
    print("== 逆元（13 の輪）")
    print("a     :", " ".join(f"{a:>3}" for a in range(1, 13)))
    print("逆元  :", " ".join(f"{inverse(a, 13):>3}" for a in range(1, 13)))
    print("3120 で 7 の逆元 →", inverse(7, 3120), "  確かめ", mulmod(7, inverse(7, 3120), 3120))
    print()
    print("== べき乗の剰余（13 の輪）")
    print("2 の k 乗:", [powmod(2, k, 13) for k in range(13)])
    print("5 × 5 →", mulmod(5, 5, 13), "  8 × 8 →", mulmod(8, 8, 13), "  （12 は −1）")
    print("回数（何回掛けると 1 に戻るか）:", {g: order(g, 13) for g in range(1, 13)})
    print("2 の 2026 乗を 13 で →", powmod(2, 2026, 13), "  3120 で →", powmod(2, 2026, 3120))

"""
b13_count.py ― 数える：パスカルの三角形・整数のくじ・並べ替えの判定
====================================================================
  パスカルの三角形：上の二つを足す。n 段目の数は、n 回左右に分かれる道の数
      段の和は 2ⁿ。斜めに足すとフィボナッチ数
  真ん中から一目盛り：n 段目で、真ん中から √n の半分までの道を数え、2ⁿ と比べる
      判定は「10000 × 道の数」と「3413 × 2ⁿ」の大小比べ（整数だけ）
  整数のくじ：x[n] = x[n − 24] + x[n − 55] の下の 31 桁（2 進）だけを残す
      フィボナッチの足し方を、遠い二つにしたもの。足し算と桁の切り捨てだけ
  くじで玉を落とす：くじの一桁で左右を決める。着地の個数が三角形の段に寄っていく
  並べ替えの判定：二つの組の差（割り算なしの整数）を、組の名札をくじで入れ替えた
      ときの差と比べ、実測以上の差が出た回数を数える

判定は整数と加算だけ。既存の在処：Paper 2026-10-01-statistics
"""
from __future__ import annotations
from typing import List, Tuple


# ---------------------------------------------------------------- パスカルの三角形
def pascal_row(n: int) -> List[int]:
    row = [1]
    for _ in range(n):
        row = [1] + [row[i] + row[i + 1] for i in range(len(row) - 1)] + [1]
    return row


def diag_sums(rows: int) -> List[int]:
    """斜めに足す：段 n の 0 番、段 n−1 の 1 番、段 n−2 の 2 番、…"""
    T = [pascal_row(n) for n in range(rows)]
    out = []
    for n in range(rows):
        s, k = 0, 0
        while k <= n - k:
            s += T[n - k][k]
            k += 1
        out.append(s)
    return out


def isqrt(n: int) -> int:
    """奇数を引けるだけ引く（第9章）。大きな n 用に、2 桁ずつ下ろす開平を使う。"""
    if n < 2:
        return n
    digits = []
    while n:
        digits.append(n % 100)
        n //= 100
    root, rem = 0, 0
    for d in reversed(digits):
        rem = rem * 100 + d
        x = 0
        odd = root * 20 + 1
        while rem >= odd:
            rem += -odd
            odd += 2
            x += 1
        root = root * 10 + x
    return root


def within_one(n: int) -> Tuple[int, int, int]:
    """n 段目（√n が偶数）で、真ん中から片側へ一目盛り（√n/2）までの道を数える。
    真ん中と目盛りの端は半分ずつ数える → 2 倍した数で返す。
    戻り値：(2 × 道の数, 2ⁿ, 一目盛り)"""
    row = pascal_row(n)
    w = isqrt(n) // 2
    mid = n // 2
    twice = row[mid] + row[mid + w]
    for k in range(mid + 1, mid + w):
        twice += row[k] + row[k]
    return twice, sum(row), w


# ---------------------------------------------------------------- 整数のくじ
class Kuji:
    """x[n] = x[n−24] + x[n−55] を下の 31 桁で切る。種は 1, 1 から始めるフィボナッチ数の 55 個。"""
    MASK = (1 << 31) - 1

    def __init__(self, seed: int = 0):
        a, b = 1, 1
        for _ in range(seed):
            a, b = b, (a + b) & self.MASK
        self.x = []
        for _ in range(55):
            self.x.append(a)
            a, b = b, (a + b) & self.MASK
        self.i = 0
        for _ in range(1000):                    # 種の並びが表に出ないよう、先に空回しする
            self.next()

    def next(self) -> int:
        j = self.i
        v = (self.x[(j + 31) % 55] + self.x[j]) & self.MASK    # x[n−24] + x[n−55]
        self.x[j] = v
        self.i = (j + 1) % 55
        return v

    def bit(self) -> int:
        return (self.next() >> 30) & 1             # いちばん上の桁

    def below(self, m: int) -> int:
        """0〜m−1 の整数を一つ。上の桁から必要なだけ取り、m 以上なら引き直す。"""
        k = 1
        while (1 << k) < m:
            k += 1
        while True:
            v = self.next() >> (31 - k)
            if v < m:
                return v


def drop(kuji: Kuji, n: int, balls: int, right: Tuple[int, int] = (1, 2)) -> List[int]:
    """n 段の三角形に玉を落とす。一段ごとにくじを引き、right = (p, q) なら q 通りのうち p 通りで右へ。"""
    p, q = right
    land = [0] * (n + 1)
    for _ in range(balls):
        pos = 0
        for _ in range(n):
            if q == 2:
                pos += kuji.bit()
            else:
                pos += 1 if kuji.below(q) < p else 0
        land[pos] += 1
    return land


# ---------------------------------------------------------------- 並べ替えの判定
def gap(values: List[int], labels: List[int]) -> int:
    """組 1 と組 0 の差：|和1 × 個数0 − 和0 × 個数1|（割り算なし）。"""
    s0 = s1 = n0 = n1 = 0
    for v, l in zip(values, labels):
        if l:
            s1 += v
            n1 += 1
        else:
            s0 += v
            n0 += 1
    d = s1 * n0 + -(s0 * n1)
    return d if d >= 0 else -d


def shuffle(kuji: Kuji, a: List[int]) -> List[int]:
    a = a[:]
    for i in range(len(a) - 1, 0, -1):
        j = kuji.below(i + 1)
        a[i], a[j] = a[j], a[i]
    return a


def perm_test(kuji: Kuji, values: List[int], labels: List[int], times: int = 200) -> Tuple[int, int]:
    obs = gap(values, labels)
    hit = 0
    for _ in range(times):
        if gap(values, shuffle(kuji, labels)) >= obs:
            hit += 1
    return obs, hit


def positions(kuji: Kuji, n: int, balls: int, right=(1, 2)) -> List[int]:
    """玉一つずつの着地の位置を並べる。"""
    out = []
    for _ in range(balls):
        land = drop(kuji, n, 1, right)
        out.append(land.index(1))
    return out


if __name__ == "__main__":
    print("== パスカルの三角形（上の二つを足す）")
    for n in range(7):
        r = pascal_row(n)
        print(f"  {n} 段目 {r}  和 {sum(r)}")
    print("  斜めに足す", diag_sums(14))
    print()

    print("== 真ん中から一目盛り（√n の半分）までの道の割合")
    print("     n  一目盛り  百万分率  10000×道 と 3413×2ⁿ")
    for n in (100, 400, 1600, 6400):
        twice, total, w = within_one(n)
        ppm = (twice * 1000000) // (total + total)                       # 表示用（観察者側の読み）
        left = 10000 * twice
        right = 3413 * (total + total)
        print(f"  {n:>5}  {w:>6}    {ppm:>7}   {'左が小さい' if left < right else '左が大きいか等しい'}")
    print()

    print("== 整数のくじ：x[n] = x[n−24] + x[n−55] の下の 31 桁")
    k = Kuji()
    first = [k.next() for _ in range(6)]
    print("  はじめの六つ", first)
    k = Kuji()
    ones = sum(k.bit() for _ in range(100000))
    print("  上の桁を 10 万回引いて 1 が出た回数", ones)
    k = Kuji()
    faces = [0] * 6
    for _ in range(60000):
        faces[k.below(6)] += 1
    print("  0〜5 を 6 万回引いた回数", faces)
    print()

    print("== くじで玉を落とす（10 段、玉 1024 × 64 個）")
    k = Kuji()
    land = drop(k, 10, 1024 * 64)
    row = pascal_row(10)
    print("  着地      ", land)
    print("  三角形 ×64", [v * 64 for v in row])
    print()

    print("== 並べ替えの判定（組の差を、名札を入れ替えた差と比べる。入れ替え 200 回）")
    k = Kuji(seed=7)
    a = positions(k, 10, 60)                        # 左右半々の三角形
    b = positions(k, 10, 60, right=(3, 5))          # 5 通りのうち 3 通りで右
    c = positions(k, 10, 60)                        # もう一度、左右半々
    vals, labs = a + b, [0] * 60 + [1] * 60
    obs, hit = perm_test(k, vals, labs)
    print(f"  半々 と 3/5 右：差 {obs}  入れ替えで実測以上 {hit}/200")
    vals, labs = a + c, [0] * 60 + [1] * 60
    obs, hit = perm_test(k, vals, labs)
    print(f"  半々 と 半々  ：差 {obs}  入れ替えで実測以上 {hit}/200   ← 負の対照")
    print("  組の和：半々", sum(a), " 3/5 右", sum(b), " 半々（二回目）", sum(c), "（どれも 60 個）")

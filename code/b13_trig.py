"""
b13_trig.py ― 三角関数：三角波の位相と、虚数を使わない回転
============================================================
角は第3章の番地（一周 3120）で持つ。値は第10章の目盛り（1 = 10^40）で持つ。

  三角波：     番地から 0 までの道のり d を数え、780 − d。足し算と比べることだけ
  π：         マチンの式 π/4 = 4·arctan(1/5) − arctan(1/239)。項は割って足すだけ
  cos と sin： 一番地ぶんの角 θ = 2π/3120 で、級数（項 ← −項 × θ² ÷ ((2k−1)(2k))）
  表：        cos を二つ前から作る：c(k+1) = 2·c(1)·c(k) − c(k−1)（掛け算は一回、あとは足し算）
  回転：      組 (x, y) を (c·x − s·y, s·x + c·y) へ。虚数は使わない。整数の組のまま

既存の在処：
  Paper 2026-03-27-B13-Fractal-Phase-Library/b13phase_v080.zip （三角波の位相：level0_table.py ほか）
  Paper 2026-05-18-pi-base3120 （π を 3120 で展開）
"""
from __future__ import annotations
from typing import List, Tuple
from b13_explog import S, ladder_div, sdiv, fmul, show

BASE = 3120
QUARTER = 780
HALF = 1560


# ---------------------------------------------------------------- 三角波
def tri_cos(p: int) -> int:
    """番地 p の三角波（−780…+780）。0 番地で +780、半周で −780。"""
    while p >= BASE:
        p += -BASE
    while p < 0:
        p += BASE
    d = p if p <= HALF else BASE + -p
    return QUARTER + -d


def tri_sin(p: int) -> int:
    return tri_cos(p + -QUARTER)


# ---------------------------------------------------------------- π
def arctan_inv(m: int) -> int:
    """arctan(1/m) = 1/m − 1/(3m³) + 1/(5m⁵) − …"""
    total, power, k, sign = 0, sdiv(S, m), 1, 1
    mm = m * m
    while power:
        t = ladder_div(power, k)
        total += t if sign > 0 else -t
        power = ladder_div(power, mm)
        k += 2
        sign = -sign
    return total


def pi_fx() -> int:
    a = arctan_inv(5)
    b = arctan_inv(239)
    quarter = a + a + a + a + -b
    return quarter + quarter + quarter + quarter


PI = pi_fx()


# ---------------------------------------------------------------- cos と sin
def cos_sin_rad(t: int) -> Tuple[int, int]:
    """角 t（目盛り、ラジアン）の cos と sin を級数で。"""
    t2 = fmul(t, t)
    c_term, c, k = S, S, 1
    while c_term:
        c_term = -sdiv(fmul(c_term, t2), (2 * k - 1) * (2 * k))
        c += c_term
        k += 1
    s_term, s, k = t, t, 1
    while s_term:
        s_term = -sdiv(fmul(s_term, t2), (2 * k) * (2 * k + 1))
        s += s_term
        k += 1
    return c, s


def step_angle() -> int:
    """一番地ぶんの角 2π/3120（目盛り）。"""
    return sdiv(PI + PI, BASE)


C1, S1 = cos_sin_rad(step_angle())


def cos_table(n: int = BASE) -> List[int]:
    """番地 0…n の cos。c(k+1) = 2·c(1)·c(k) − c(k−1)。"""
    out = [S, C1]
    two_c1 = C1 + C1
    for _ in range(n - 1):
        out.append(fmul(two_c1, out[-1]) + -out[-2])
    return out


# ---------------------------------------------------------------- 回転
def rotate(v: Tuple[int, int], c: int, s: int) -> Tuple[int, int]:
    x, y = v
    return (fmul(c, x) + -fmul(s, y), fmul(s, x) + fmul(c, y))


def quarter_turn(v: Tuple[int, int]) -> Tuple[int, int]:
    """780 番地（四分の一周）は入れ替えと裏返しだけ（第5章）。"""
    return (-v[1], v[0])


if __name__ == "__main__":
    print("== 三角波（番地 → −780…780）")
    print(" ".join(f"{p}:{tri_cos(p)}" for p in (0, 260, 520, 624, 780, 1040, 1560, 2340, 3120)))
    print()
    print("π      =", show(PI))
    print("一番地 =", show(step_angle()), "ラジアン")
    print()
    tab = cos_table()
    print("== cos の表（二つ前から作る）と、知っている値")
    from b13_roots import sqrt_digits
    r5 = int(sqrt_digits(5, 40).replace(".", ""))      # √5 の目盛り（第9章の開平）
    phi = sdiv(S + r5, 2)
    checks = [(0, "1", S), (260, "√3/2", None), (520, "1/2", sdiv(S, 2)),
              (624, "(φ−1)/2 = cos 72°", sdiv(phi + -S, 2)), (312, "φ/2 = cos 36°", sdiv(phi, 2)),
              (780, "0", 0), (1040, "−1/2", -sdiv(S, 2)), (1560, "−1", -S), (3120, "1（一周）", S)]
    for p, name, exact in checks:
        diff = "" if exact is None else f"  {40 + -len(str(abs(tab[p] + -exact))) if tab[p] != exact else 40} 桁一致"
        print(f"番地 {p:>4}  cos = {show(tab[p], 28)}  {name}{diff}")
    print()
    print("== 三角波と cos の、いちばん離れる所")
    worst = max(range(BASE), key=lambda p: abs(sdiv(tri_cos(p) * S, QUARTER) + -tab[p]))
    print(f"番地 {worst}: 三角波 {show(sdiv(tri_cos(worst) * S, QUARTER), 6)}  cos {show(tab[worst], 6)}")
    print()
    print("== 回す：一番地ずつ 3120 回、組のまま")
    v = (S, 0)
    for _ in range(BASE):
        v = rotate(v, C1, S1)
    print("戻ってきた組:", show(v[0], 30), show(v[1], 30))
    print("出発点との差（目盛りの整数）:", v[0] + -S, v[1])
    w = (S, 0)
    for _ in range(4):
        w = quarter_turn(w)
    print("四分の一周を 4 回:", w == (S, 0))

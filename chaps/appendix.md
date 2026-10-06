---
title: "付録　関数の索引と在処の表"
---

# 付録　関数の索引と在処の表

## A. 関数の索引

本の中で使った関数を、章ごとに並べます。どの関数も `code/` のファイルにあり、標準の Python だけで走ります。

表示のためだけの関数（10進に戻して人が読むためのもの）には「観察者側の読み」と書きました。

### 第1部　数を書く

**第1章　平衡13進と平衡5進** ― `code/b13_balanced.py`

| 関数 | すること |
|---|---|
| `half(N)` | 桁の上限 h = (N − 1)/2 を、h + h + 1 = N となる数として足し算で求める |
| `add(a, b, N)` | 桁ごとに足し、はみ出したら N を一つ引いて上の桁へ ±1 を送る |
| `neg(a)` | 各桁の符号を裏返す（繰り上がりは起きない） |
| `sub(a, b, N)` | 裏返したものを足す |
| `sign(a)` | 一番上の 0 でない桁の符号 |
| `times_small(a, k, N)` | a を k 回足す |
| `from_decimal(text, N)` | 10進の文字列から入る（x を 10 回足して次の桁を足す） |
| `cut(a, k)` | 下の k 桁を捨てる（平衡桁では、これが一番近い値への丸め） |
| `trim(a)` | 上の桁の 0 を落とす |
| `to_int`、`show`、`dec` | 観察者側の読み（10進の整数、(+1,−2,−2)₅ の表記） |

**第2章　平衡φ進と Zeckendorf** ― `code/b13_phi.py`

| 関数 | すること |
|---|---|
| `phi_pow(k)` | φ^k を整数の組で（上へは (a, b) → (b, a + b)、下へは (a, b) → (b − a, a)） |
| `phi_value(d)` | 平衡φ進の桁の値を Z[φ] の組で |
| `phi_normalize(d)` | 繰り上がりの規則を、当てはまらなくなるまで当てる |
| `phi_add(a, b)`、`phi_neg(a)` | 平衡φ進の足し算と符号の裏返し |
| `phi_from_decimal(text)` | 10進から平衡φ進へ（x を 10 回足して 1 を足す） |
| `zeck_normalize(z)`、`zeck_add(a, b)` | Zeckendorf 表記の繰り上がりと足し算 |
| `zeck_from_count(n)` | 0 から 1 を n 回足して Zeckendorf 表記にする |
| `pair_add(x, y)` | Z[φ] の組の足し算 |
| `zeck_value`、`show_phi`、`show_zeck`、`show_pair`、`dec` | 観察者側の読み |

**第3章　BASE=3120 の位相** ― `code/b13_phase.py`

| 関数 | すること |
|---|---|
| `padd(a, b)`、`pneg(a)`、`psub(a, b)` | 3120 の輪の上の足し算・裏返し・引き算 |
| `orbit(step)` | 0 から step ずつ足し、0 に戻るまでの番地の列 |
| `exact_steps()` | ちょうど一周に着地する歩幅 |
| `dadd(a, b)` | 多桁の位相の足し算（一番上の桁は一周で 0 に戻る） |
| `split_turn(n, ndig)` | 一周を n 等分する歩幅を、引けるだけ引く筆算で ndig 桁まで |
| `walk(step, times)` | 歩幅を times 回足す |
| `show`、`degrees` | 観察者側の読み（番地の表記、度） |

### 第2部　演算

**第4章　四則** ― `code/b13_arith.py`（`b13_balanced.py` を使う）

| 関数 | すること |
|---|---|
| `shift(a, k)` | N^k の位へずらす（下に 0 を k 個並べる） |
| `mul(a, b, N)` | 平衡桁の掛け算。戻り値は（積, 足した回数） |
| `divide(a, b, N)` | 平衡桁の割り算。戻り値は（商, 余り, 足した回数）、余りは \|b\|/2 以内 |

**第5章　半加算器・5桁の加算器・計算尺** ― `code/b13_logic.py`

| 関数 | すること |
|---|---|
| `quarter(v)`、`amp_after(steps)` | 四分の一周（780 番地）進める。源から steps 歩の振幅 |
| `at_outlet(sources)` | 出口に届いた振幅を足す |
| `bright(v)`、`strong(v)` | 出口が明るいか、強いかを比べる |
| `half_adder(a, b)` | 半加算器：（和, 桁上がり） |
| `either(a, b)` | 「または」の出口 |
| `full_adder(a, b, c)` | 全加算器 |
| `adder(x, y)` | 桁の列を下の桁から足し、桁上がりを順に送る |
| `double(x)`、`scale()` | 倍にする。計算尺の目盛り（1 を k 回倍にした数） |
| `slide_pos(a, b)`、`slide_mul(a, b)`、`slide_div(a, b)` | 計算尺：目盛りを足す・掛ける・引く |
| `bits`、`from_bits` | 観察者側の入口と読み（0/1 の桁と10進） |

**第6章　互除法・剰余・逆元・べき乗の剰余** ― `code/b13_modular.py`

| 関数 | すること |
|---|---|
| `ladder(x, limit)` | x, 2x, 4x, … を limit を越えない所まで（x + x で作る） |
| `rem(a, m)` | 梯子を上から引いて余りを出す |
| `gcd_sub(a, b)` | 引き算の互除法。戻り値は（最大公約数, 引いた回数） |
| `squares(a, b)` | 長方形 a × b から切り取る正方形を（辺, 枚数）で |
| `inverse(a, m)` | a × x ≡ 1 (mod m) の x を、係数の組も一緒に引いて求める |
| `split2(e)` | e を 1, 2, 4, … の和に分ける |
| `mulmod(a, b, m)`、`powmod(g, e, m)` | 倍の梯子・二乗の梯子で、掛け算とべき乗の余り |
| `order(g, m)` | g を何回掛けると 1 に戻るか |

**第7章　平方剰余・ピサノ周期・篩** ― `code/b13_residue.py`

| 関数 | すること |
|---|---|
| `wrap(x, m)` | 0 ≤ x < 2m の数を m の輪に戻す |
| `squares_mod(p)`、`residues(p)` | 奇数を足して平方を作り、p の輪で並べる。0 を除く平方の集まり |
| `pisano(m)` | フィボナッチ数を m の輪で足し、(0, 1) に戻るまでの歩数 |
| `apparition(m)` | F_n が初めて m の倍数に着地する n |
| `fib_ring(m)` | 一周ぶんの F_n（m の輪） |
| `sieve(N)`、`survivors_after(ps, N)` | その数ずつ跳んで印をつける篩。残った数 |

**第8章　Z[φ]：ノルム・単数・φ倍** ― `code/b13_zphi.py`

| 関数 | すること |
|---|---|
| `add`、`neg`、`mul` | Z[φ] の組の足し算・裏返し・掛け算（φ² = φ + 1） |
| `times_phi(u)`、`div_phi(u)` | φ を掛ける・φ で割る（組の入れ替えと足し引き） |
| `conj(u)`、`norm(u)` | 共役とノルム a² + ab − b² |
| `phi_pow(k)` | φ^k |
| `units_in_box(R)` | \|a\|, \|b\| ≤ R でノルムが ±1 の組を全部 |
| `norms_in_box(R, top)` | ノルムの絶対値が top 以下の組を、ノルムごとに |
| `show` | 観察者側の読み |

**第9章　根：√n・連分数・ペル** ― `code/b13_roots.py`

| 関数 | すること |
|---|---|
| `times(k, x)` | k 回足す |
| `ladder_div(a, m)` | 倍々の梯子を上から引く割り算（商と余り） |
| `isqrt_odd(n)` | 奇数を引けるだけ引いて √n の整数部分 |
| `sqrt_digits(n, places)` | 2 桁ずつ下ろす開平で √n を places 桁まで |
| `cf_sqrt(n, terms)`、`period(n)` | √n の連分数の項と、繰り返す部分 |
| `convergents(cf)` | 近似分数 p(k) = a(k)·p(k−1) + p(k−2) |
| `pell_value(n, p, q)` | p² − n·q² の値 |

### 第3部　関数

**第10章　指数と対数** ― `code/b13_explog.py`

| 関数 | すること |
|---|---|
| `ladder_div(a, m)`、`sdiv(a, m)` | 倍々の梯子の割り算（符号つきも） |
| `fmul(a, b)`、`fixed(p, q)` | 目盛りどうしの掛け算。分数を目盛りに |
| `e_compound(n)` | x ← x + x ÷ n を n 回 |
| `e_series()` | 項を k で割っては足す e の級数 |
| `exp_fx(x)` | e^x（項 ← 項 × x ÷ k を足す） |
| `log2_fx(x, bits)` | 2 を底とする対数（二乗して 2 を越えたら半分にし、桁を読む） |
| `ln2_fx()`、`ln_fx(x)` | ln 2 の級数と、自然対数 |
| `show` | 観察者側の読み |

**第11章　三角関数** ― `code/b13_trig.py`

| 関数 | すること |
|---|---|
| `tri_cos(p)`、`tri_sin(p)` | 番地 p の三角波 |
| `arctan_inv(m)`、`pi_fx()` | arctan(1/m) の級数と、マチンの式の π |
| `cos_sin_rad(t)` | 角 t の cos と sin を級数で |
| `step_angle()` | 一番地ぶんの角 2π/3120 |
| `cos_table(n)` | 二つ前から作る cos の表 c(k+1) = 2·c(1)·c(k) − c(k−1) |
| `rotate(v, c, s)`、`quarter_turn(v)` | 整数の組のまま回す。四分の一周は入れ替えと裏返し |

**第12章　双曲関数と双曲回転** ― `code/b13_hyper.py`

| 関数 | すること |
|---|---|
| `cosh_sinh(t)`、`cos_sin(t)` | 項の符号を裏返さない級数と、裏返す級数 |
| `boost(v, C, Sh)`、`turn(v, c, s)` | 双曲回転と円の回転 |
| `phi2(u)`、`phi2_inv(u)` | φ² を掛ける・φ² で割る（整数のままの双曲回転） |
| `norm(u)` | Z[φ] のノルム |
| `pell2(v)` | x² − 2y² を変えない一歩 |

**第13章　定数を 3120 で展開する** ― `code/b13_constants.py`

| 関数 | すること |
|---|---|
| `nearest_div(x, m)` | いちばん近い商と、残り（−m/2 … m/2） |
| `expand3120(value, terms)` | 3120 倍して近い目盛りに着地させることを繰り返す |
| `rebuild(digits)` | 桁から値へ戻す（観察者側の確かめ） |

### 第4部　変化と変換

**第14章　差分と和** ― `code/b13_diffsum.py`

| 関数 | すること |
|---|---|
| `diff(a)`、`accum(a, start)` | 隣どうしを引く。ここまでを足す |
| `table(a, depth)`、`heads(a, depth)` | 差分の表と、その左端 |
| `rebuild(h, length)` | 左端の数だけから列を戻す |
| `pascal(rows)` | パスカルの三角形（上の二つを足す） |
| `pow2(n)`、`fib(n)` | 2ⁿ とフィボナッチ数の列 |
| `square_slope(x, n)` | x² の刻み 1/n の傾き |
| `pentagonal(n)`、`pentagonal_plus(n)` | 五角数の二つの列（3 ずつ増える数の和） |
| `columns(n)` | 0〜1 の x² の下を n 本の柱で数える |

**第15章　漸化式と畳み込み** ― `code/b13_recur.py`

| 関数 | すること |
|---|---|
| `seq(p, q, a, b, n)` | s(n+2) = p·s(n+1) − q·s(n) の列 |
| `form(p, q, a, b)` | b² − p·a·b + q·a²（一歩ごとに q 倍される量） |
| `disc(p, q)`、`kind(p, q)` | p² − 4q と、回る・まっすぐ・開くの分かれ目 |
| `period(p, q, a, b)` | (a, b) に戻るまでの歩数 |
| `zadd`、`zneg`、`zmul`、`zperiod`、`zform` | p を Z[φ] の数にしたときの同じ操作 |
| `conv(x, y, n)` | 畳み込み（ずらして掛けて足す） |
| `unroll(head, p, q, n)` | 畳み込みを戻す（漸化式そのもの） |
| `carry(digits, base)`、`digits_low(n)` | 桁の畳み込みを繰り上げる |
| `zshow` | 観察者側の読み |

**第16章　φ-NTT と coneFFT** ― `code/b13_phintt.py`

| 関数 | すること |
|---|---|
| `zadd`、`zneg`、`zmul`、`zint`、`zsum`、`zdiv_exact` | Z[φ] の組の演算（割り算は割り切れるときだけ） |
| `addr(m, k)` | 番地 m·k を 10 で回した場所 |
| `forward(x)`、`inverse(A, B)` | 十の番地の変換と、40 で割って戻す |
| `cyc_conv(x, h)` | 十の番地を一周する畳み込み |
| `mult(Ax, Bx, Ah, Bh)` | 変換の側での掛け算 |
| `butterfly(x)` | 偶数番と奇数番に分けて A[m] と A[m+5] を作る |
| `digits(n, B)`、`undigits(d)` | 番地を 10進の桁に分ける・戻す |
| `forward_B`、`inverse_B` | 桁ごとに重ねた変換（2^B 本の列） |
| `cf_conv(x, h, B)` | 繰り上がりなしの畳み込み |
| `mult_B(cx, ch, B)` | 2^B 本の列どうしの掛け算 |
| `zstr`、`label` | 観察者側の読み |

### 第5部　形・数える・探す

**第17章　四元数とイコシアン** ― `code/b13_quat.py`

| 関数 | すること |
|---|---|
| `zadd`、`zneg`、`zmul`、`zhalf` | Z[φ] の組の演算（半分は割り切れるときだけ） |
| `qmul_raw(p, q)`、`qmul(P, R)` | ハミルトンの掛け算。2 倍して持った四元数どうしの掛け算 |
| `conj(q)`、`norm(q)`、`dot(p, q)`、`qneg(q)` | 共役・長さ・内積・裏返し |
| `order(q)` | 何回掛けると 1 に戻るか |
| `rotate(Q, V)` | 点を q v q̄ で挟んで回す |
| `parity(p)` | 並べ替えの偶奇 |
| `hurwitz24()`、`icosian120()` | 整数で閉じる 24 個と、φ を入れた 120 個 |
| `closed(G)` | どの二つを掛けても G に着地するか |
| `zstr` | 観察者側の読み |

**第18章　数える** ― `code/b13_count.py`、`code/b13_wave.py`

| 関数 | すること |
|---|---|
| `pascal_row(n)`、`diag_sums(rows)` | パスカルの三角形の段と、斜めの和 |
| `isqrt(n)` | 2 桁ずつ下ろす開平の整数平方根 |
| `within_one(n)` | 真ん中から一目盛りまでの道を数える |
| `Kuji` | x[n] = x[n − 24] + x[n − 55] の下の 31 桁で作るくじ（`next`、`bit`、`below`） |
| `drop(kuji, n, balls, right)`、`positions(…)` | くじで玉を落とす。玉ごとの着地の位置 |
| `gap(values, labels)` | 割り算なしの組の差 |
| `shuffle(kuji, a)`、`perm_test(…)` | 名札をくじで入れ替える。並べ替えの判定 |
| `penrose_floor(square, wx, wy, levels)` | ペンローズの床（番地と隣の表）。四角い格子も |
| `tq(x, d)` | 0 へ向けて切り捨てる割り算 |
| `walls(X, Y, slits)` | 壁とスリット |
| `wave(X, Y, adj, slits)` | 整数の波を進め、明るさと先頭が届いた刻を出す |
| `balls(X, Y, adj, slits)` | 点（玉）を右へ進める |
| `hops(adj, blocked, src)` | 壁を避けた最短の段数 |
| `profile`、`rel`、`bar` | 観察者側の読み（幕の上の組ごとの和、最大を 100 とした整数） |

**第19章　探す** ― `code/b13_search.py`（`b13_explog.py`、`b13_wave.py` を使う）

| 関数 | すること |
|---|---|
| `half(x)` | 倍々の梯子で半分にする |
| `bisect_isqrt(n)` | 二分法で x·x ≤ n の最大の x |
| `bisect_root(f, lo, hi)` | 二分法で f の根を目盛りの最後の桁まで |
| `bisect_search(a, key)` | 並んだ列から二分法で探す |
| `fib_search(a, key)` | 並んだ列からフィボナッチ数を引いて探す |
| `floor()`、`nearest(…)`、`walls(…)` | 床と、番地の選び方と、壁の置き方 |
| `hops(adj, wall, src)` | 壁を避けた最短の段数 |
| `scent(adj, wall, food, T, k)` | 餌の濃さ D_t = Σ 通れる隣 + (餌なら k^t) |
| `climb(adj, wall, D, seed, food)` | いちばん濃い隣へ移って餌に着くまでの歩数 |

## B. 在処の表

| 章 | この章のコード（`code/`） | 動く図（`HTML/`） | 元の研究・道具（Paper） |
|---|---|---|---|
| 1 | `b13_balanced.py` | `ch01_balanced_dials.html` | `2026-03-27-B13-Fractal-Phase-Library`（`phase_digits.py`） |
| 2 | `b13_phi.py` | `ch02_phi_carry.html` | 第2章の在処の節を参照 |
| 3 | `b13_phase.py` | `ch03_phase_ring.html` | `2026-03-27-B13-Fractal-Phase-Library`（`constants.py`、`phase_digits.py`） |
| 4 | `b13_arith.py` | `ch04_long_arith.html` | `2026-03-27-B13-Fractal-Phase-Library`（`phase_digits.py`） |
| 5 | `b13_logic.py` | `ch05_half_adder.html`、`ch05_slide_rule.html` | `2026-09-21-plant-sun`（`code/ha1.py`）、`2026-03-27-B13-Fractal-Phase-Library`（`constants.py`） |
| 6 | `b13_modular.py` | `ch06_euclid.html` | `2026-03-27-B13-Fractal-Phase-Library`（`constants.py`） |
| 7 | `b13_residue.py` | `ch07_pisano_ring.html`、`ch07_sieve.html` | ― |
| 8 | `b13_zphi.py` | `ch08_phi_lattice.html` | `2026-02-26-phi-ntt` |
| 9 | `b13_roots.py` | `ch09_sqrt_rect.html` | ― |
| 10 | `b13_explog.py` | `ch10_exp_log.html` | `2026-02-19-Nature-Knows` |
| 11 | `b13_trig.py` | `ch11_rotate.html` | `2026-03-27-B13-Fractal-Phase-Library`、`2026-02-19-Nature-Knows` |
| 12 | `b13_hyper.py` | `ch12_hyperbolic.html` | `2026-09-02-lorentz-hyperbola`、`2026-09-09-relativity` |
| 13 | `b13_constants.py` | `ch13_constants_3120.html` | `2026-05-18-pi-base3120`、`2026-03-27-B13-Fractal-Phase-Library`（`constants.py`） |
| 14 | `b13_diffsum.py` | `ch14_diff_sum.html` | `2026-02-19-Nature-Knows` |
| 15 | `b13_recur.py` | `ch15_recur_conv.html` | 第11章の `cos_table` |
| 16 | `b13_phintt.py` | `ch16_phi_ntt.html` | `2026-02-26-phi-ntt`、`2026-03-06-Cone-FFT`、`2026-03-08-cone-FFT`、`2026-03-09-coneFFT-Verification` |
| 17 | `b13_quat.py` | `ch17_icosian.html` | `2026-08-15-quaternion`（`code/quat_exact.py`、`code/cell600.py`） |
| 18 | `b13_count.py`、`b13_wave.py` | `ch18_kuji.html`、`ch18_wave_slit.html` | `2026-10-01-statistics`（`statistics01.md`、`code/chi_penrose.py`、`code/electron_paths.html`） |
| 19 | `b13_search.py` | `ch19_amoeba.html` | `2026-09-21-plant-sun`（`amoeba01.md`、`code/amoeba_path_sum.html`） |

## C. コードどうしのつながり

ほかのファイルを使うものだけを並べます。矢印の先が、使われる側です。

```
b13_arith      → b13_balanced
b13_trig       → b13_explog, b13_roots（実行例の中だけ）
b13_hyper      → b13_explog, b13_roots
b13_constants  → b13_explog, b13_roots, b13_trig
b13_diffsum    → b13_explog
b13_wave       → b13_trig, b13_explog, b13_count
b13_search     → b13_explog, b13_wave
```

ほかのファイル（`b13_balanced`、`b13_phi`、`b13_phase`、`b13_logic`、`b13_modular`、`b13_residue`、`b13_zphi`、`b13_roots`、`b13_explog`、`b13_recur`、`b13_phintt`、`b13_quat`、`b13_count`）は、一本だけで走ります。

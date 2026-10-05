---
name: b13-library
description: B13 ライブラリ（本『Nature Knows Only Addition ― 動く図で読む足し算だけの数学 ―』のコード）で、整数と足し算と比較だけで計算するためのスキル。平衡13進・平衡5進・平衡φ進・Zeckendorf・3120番地の位相・足し算だけの四則・半加算器・計算尺・互除法・剰余・逆元・べき乗の剰余・平方剰余・ピサノ周期・篩・Z[φ]・ノルム・単数・φ倍・√n・連分数・ペル方程式・指数と対数・三角関数・虚数を使わない回転・双曲関数・双曲回転・π/e/φ/√5/ln2 の3120展開、と言われたとき、「足し算だけで計算して」「浮動小数を使わずに」「B13ライブラリで」「本の第N章のコード」と頼まれたとき、またはB13の記事や本の実行例・数値を出すときに使う。
---

# B13 ライブラリ

本『Nature Knows Only Addition ― 動く図で読む足し算だけの数学 ―』の 13 章ぶんのコードを `scripts/` に、各章の本文を `references/` に置いてある。数値を出すときはここのコードを走らせて出す。暗算や浮動小数の電卓で出した数を本の数として書かない。

## 約束（必ず守る）

1. **整数**だけで計算する。浮動小数は使わない。
2. **足し算**だけで組む。引き算は「符号を裏返して足す」、掛け算は「足すのを繰り返す」。
3. **比べる**（どちらが大きいか、端を越えたか）は使ってよい。
4. 割り算・剰余・べき乗・10進表示は**観察者側の読み**（人が確かめるための表示）に限る。書くときは「観察者側の読み」とラベルする。
5. 進数の表記は丸括弧＋基数の下付き：(13)₁₀・(+1,−2,−2)₅・(+1,0)₁₃・(1,0,1)_F。
6. 帰属を分ける：スクリプトが出した数は [計算]、知識として参照しただけのものは [知識]、未検証の読みは [見立て]。ユーザーの発話と計算を混ぜない。
7. 既存の学説を越える・置き換えるとは書かない。「足し算だけで書く別の視点」「離散化しただけ」の範囲に留める。

## 走らせ方

```bash
cd ${CLAUDE_PLUGIN_ROOT}/skills/b13-library/scripts
python3 b13_arith.py          # 各モジュールは単独で走らせると実行例を出す
python3 -c "from b13_zphi import norm; print(norm((5,1)))"
```

- どのモジュールも `b13_balanced.py`（平衡N進の add / neg / sign）を土台に組んである。同じディレクトリから走らせる。
- 実行例を本や記事に載せるときは、出力をそのまま貼る。丸めない。

## 章・コード・図の対応

| 章 | 主題 | コード | 主な関数 | 動く図（b13-moving-figures） |
|---|---|---|---|---|
| 序章 | 足し算だけで書くという約束 | ― | ― | ― |
| 1 | 平衡13進と平衡5進 | b13_balanced.py | add neg sub sign times_small from_decimal to_int cut show | ch01_balanced_dials |
| 2 | 平衡φ進と Zeckendorf | b13_phi.py | phi_add phi_normalize phi_from_decimal zeck_add zeck_from_count zeck_value | ch02_phi_carry |
| 3 | BASE=3120 の位相 | b13_phase.py | padd pneg psub orbit exact_steps split_turn walk degrees | ch03_phase_ring |
| 4 | 四則 | b13_arith.py | shift mul divide | ch04_long_arith |
| 5 | 半加算器・5桁の加算器・計算尺 | b13_logic.py | half_adder full_adder adder slide_pos slide_mul slide_div | ch05_half_adder・ch05_slide_rule |
| 6 | 互除法・剰余・逆元・べき乗の剰余 | b13_modular.py | gcd_sub rem inverse mulmod powmod order | ch06_euclid |
| 7 | 平方剰余・ピサノ周期・篩 | b13_residue.py | residues pisano apparition fib_ring sieve survivors_after | ch07_pisano_ring・ch07_sieve |
| 8 | Z[φ]：ノルム・単数・φ倍 | b13_zphi.py | add mul times_phi div_phi conj norm phi_pow units_in_box | ch08_phi_lattice |
| 9 | 根：√n・連分数・ペル | b13_roots.py | isqrt_odd sqrt_digits cf_sqrt period convergents pell_value | ch09_sqrt_rect |
| 10 | 指数と対数 | b13_explog.py | e_compound e_series exp_fx log2_fx ln_fx | ch10_exp_log |
| 11 | 三角関数・虚数を使わない回転 | b13_trig.py | tri_cos tri_sin pi_fx cos_sin_rad rotate quarter_turn | ch11_rotate |
| 12 | 双曲関数と双曲回転 | b13_hyper.py | cosh_sinh boost turn phi2 norm pell2 | ch12_hyperbolic |
| 13 | 定数 π・e・φ・√5・ln2 の3120展開 | b13_constants.py | expand3120 rebuild nearest_div | ch13_constants_3120 |

章の本文は `references/` の同名ファイル（intro.md, ch01-balanced.md … ch13-constants.md）。各章は「B13 の言葉で → 動く図 → コード → 実行例 → 在処」の順で書いてある。新しい章や記事を書くときもこの順に揃える。

## 使い方の手順

1. 頼まれた計算がどの章に当たるかを上の表で決める。
2. 迷ったら該当章の `references/` を読み、使う関数と表記を確かめる（全章を読み直さない）。
3. スクリプトを走らせて数を出す。出た数だけを [計算] として書く。
4. 表にない演算が要るときは、既存モジュールの add / neg / sign / 比較の上に足し算だけで組む。新しく組んだ部分には事前に「何が出たら合格か」を書いてから走らせる。
5. 動く図が要るときは b13-moving-figures スキルに渡す。

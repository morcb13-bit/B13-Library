# B13 ライブラリー

Zennの本『Nature Knows Only Addition ― 動く図で読む足し算だけの数学 ―  B13ライブラリー』のコンテンツやコード類を保存します。

- 本：[Zenn（morc_b13）](https://zenn.dev/morc_b13)

この本のコードは、**整数・足し算・比べる**の三つだけで書いています。浮動小数は使いません。割り算や10進の表示は、人が確かめるための「観察者側の読み」に限ります。

## 中身

| フォルダ | 内容 |
|---|---|
| `chaps/` | 本の本文（序章、第1〜19章、付録） |
| `code/` | 各章の Python コード（20本）。単独で走らせると実行例を出します |
| `HTML/` | 動く図（28枚：本文の章の図22枚、別冊付録6枚）。HTML 一枚で動き、外部の読み込みはありません |
| `plugin/b13-library/` | Claude 用のプラグイン（上の三つをまとめたもの） |

### 章とコード

| 部 | 章 | 主題 | コード |
|---|---|---|---|
| 第1部　数を書く | 1 | 平衡13進と平衡5進 | b13_balanced.py |
| | 2 | 平衡φ進と Zeckendorf | b13_phi.py |
| | 3 | BASE=3120 の位相 | b13_phase.py |
| 第2部　演算 | 4 | 四則 | b13_arith.py |
| | 5 | 半加算器・5桁の加算器・計算尺 | b13_logic.py |
| | 6 | 互除法・剰余・逆元・べき乗の剰余 | b13_modular.py |
| | 7 | 平方剰余・ピサノ周期・篩 | b13_residue.py |
| | 8 | Z[φ]：ノルム・単数・φ倍 | b13_zphi.py |
| | 9 | 根：√n・連分数・ペル | b13_roots.py |
| 第3部　関数 | 10 | 指数と対数 | b13_explog.py |
| | 11 | 三角関数：虚数を使わない回転 | b13_trig.py |
| | 12 | 双曲関数と双曲回転 | b13_hyper.py |
| | 13 | 定数 π・e・φ・√5・ln2 を3120で展開 | b13_constants.py |
| 第4部　変化と変換 | 14 | 差分と和（微分と積分） | b13_diffsum.py |
| | 15 | 漸化式と畳み込み | b13_recur.py |
| | 16 | φ-NTT と coneFFT | b13_phintt.py |
| 第5部　形・数える・探す | 17 | 四元数とイコシアン | b13_quat.py |
| | 18 | 数える：パスカルの三角形・整数のくじ・並べ替えの判定 | b13_count.py、b13_wave.py |
| | 19 | 探す：二分法と最短路（アメーバ） | b13_search.py |
| 付録 | | 関数の索引と在処の表 | |

```bash
cd code
python3 b13_arith.py
```

### 別冊付録の動く図（6枚）

本文の章とは別に、`HTML/` に入れてある動く図です。

| ファイル | 題 |
|---|---|
| calabi_yau_25.html | 整数番地のカラビ・ヤウ |
| checkerboard_wave.html | 市松の波動関数 |
| dimension_ladder.html | 点から600胞体の先へ |
| hive_center.html | ハチ型配送センター |
| lorenz_integer.html | 整数のローレンツ・アトラクタ |
| quadric_shells.html | 整数殻の二次曲面 |

## Claude のプラグインとして使う

このリポジトリは Claude のプラグインの配布元（マーケットプレイス）を兼ねています。入れると、Claude が本のコードを走らせて足し算だけで計算し、動く図を出せるようになります。

### Claude Code

```bash
claude plugin marketplace add morcb13-bit/B13-Library
claude plugin install b13-library@morc-b13
```

新しい版を受け取るとき：

```bash
claude plugin update b13-library@morc-b13
```

### Claude のアプリ（有料プラン）

`plugin/b13-library` フォルダを zip にまとめ、Customize → Plugins から自作のプラグインとしてアップロードします。

### 頼み方の例

- 「B13ライブラリで 2026 ÷ 7 を足し算だけで計算して」
- 「100 を Zeckendorf で表して」
- 「2 の 2026 乗を 13 で割った余りを、足し算だけで」
- 「第7章の篩の動く図を出して」
- 「第19章のアメーバの動く図を出して」

## ライセンス

MIT License（`LICENSE` を参照）

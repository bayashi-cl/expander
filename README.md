# expander

Pythonのソースコードをオンラインジャッジに提出可能な単一ソースのものに変換します。

## 注意

* **CodeForcesの難読化禁止の規定に触れる可能性があります。確認が取れるまではCodeForcesには提出しないでください**
* まだバグが存在する可能性があります。コンテスト中に使用する場合は正しく実行できるかを確認してから提出してください

## オリジナル

<https://github.com/not522/ac-library-python/blob/master/atcoder/__main__.py>


**変更点**

* 指定されたモジュールを展開可能に
* `__future__` 系を正しくimportできるように
* ソース内でエスケープ（改行文字とか）を使用可能に

## できないこと

* インデントされているimportは壊れる
* import文を使わない(importlibとか)と壊れる

## パフォーマンス

Library Checkerで検証

Problem: [Shortest Path](https://judge.yosupo.jp/problem/shortest_path)

|CPython  |Submission                                 |Time   |
|:--------|:------------------------------------------|:------|
|expander |<https://judge.yosupo.jp/submission/79094> |2745 ms|
|pure     |<https://judge.yosupo.jp/submission/79093> |2970 ms|

|PyPy     |Submission                                 |Time   |
|:--------|:------------------------------------------|:------|
|expander |<https://judge.yosupo.jp/submission/79096> |913 ms |
|pure     |<https://judge.yosupo.jp/submission/79097> |918 ms |

## インストール

```
pip install git+https://github.com/bayashi-cl/expander
```

## 実行コマンド

```
python -m expander <source file> [-o <output file>] [-m <expand module names...>]
```

出力先の指定がない場合は標準出力に出力される

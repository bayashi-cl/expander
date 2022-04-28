# expander

[![pytest](https://github.com/bayashi-cl/expander/actions/workflows/pytest.yml/badge.svg)](https://github.com/bayashi-cl/expander/actions/workflows/pytest.yml)

[English Version](https://github.com/bayashi-cl/expander/blob/main/README-en.md)

Pythonのソースコードをオンラインジャッジに提出可能な単一ソースのものに変換します。

[このツールを使った提出](https://atcoder.jp/contests/past202012-open/submissions/30913394)

<details>
<summary>展開前のコード</summary>

```python
from byslib.core.config import procon_setup
from byslib.core.const import IINF, MOD
from byslib.core.fastio import debug, int1, readline, sinput
from byslib.graph.breadth_first_search import breadth_first_search
from byslib.graph.edge import AdjacencyList


@procon_setup
def main(**kwargs) -> None:
    n, m, k = map(int, readline().split())
    h = list(map(int, readline().split()))
    c = list(map(int1, readline().split()))
    graph = AdjacencyList.init(n)
    for _ in range(m):
        a, b = map(int1, readline().split())
        if h[a] > h[b]:
            a, b = b, a
        graph.add_edge(a, b, 1)

    cost, _ = breadth_first_search(graph, c)
    print(*map(lambda x: -1 if x == IINF else x, cost), sep="\n")


if __name__ == "__main__":
    t = 1
    # t = int(readline())
    main(t)
```

</details>

## 注意

* **CodeForcesの[難読化禁止の規定](https://codeforces.com/blog/entry/4088)に触れる可能性があります。確認が取れるまではCodeForcesには提出しないでください**
* まだバグが存在する可能性があります。コンテスト中に使用する場合は正しく実行できるかを確認してから提出してください

## オリジナル

<https://github.com/not522/ac-library-python/blob/master/atcoder/__main__.py>

**変更点**

* 指定されたモジュールを展開可能に
* `__future__` 系を正しくimportできるように
* ソース内でエスケープ（改行文字とか）を使用可能に
* 必要そうならライセンスを挿入するように
* .pycファイルが作成されるように

## パフォーマンス

Library Checkerで検証

Problem: [Shortest Path](https://judge.yosupo.jp/problem/shortest_path)

|CPython  |Submission                                 |Time   |
|:--------|:------------------------------------------|:------|
|expander |<https://judge.yosupo.jp/submission/87683> |1800 ms|
|pure     |<https://judge.yosupo.jp/submission/87687> |1821 ms|

|PyPy     |Submission                                 |Time   |
|:--------|:------------------------------------------|:------|
|expander |<https://judge.yosupo.jp/submission/87684> |974 ms |
|pure     |<https://judge.yosupo.jp/submission/87685> |928 ms |

## インストール

```sh
pip install git+https://github.com/bayashi-cl/expander
```

## 実行コマンド

```sh
python -m expander <source file> [-o <output file>] [-m <expand module names...>]
```

例:

```sh
python -m expander main.py -o out.py -m yourlib
```

出力先の指定がない場合は標準出力に出力される

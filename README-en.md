# expander

[![pytest](https://github.com/bayashi-cl/expander/actions/workflows/pytest.yml/badge.svg)](https://github.com/bayashi-cl/expander/actions/workflows/pytest.yml)

Convert Python source code into a single source that can be submitted to online judges.

[Submission using this tool.](https://github.com/bayashi-cl/expander/blob/main/README-en.md)

<details>
<summary>Before expand.</summary>

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

## Attention

* **Submission may violate CodeForces' [no obfuscation policy](https://codeforces.com/blog/entry/4088). Please do not submit to CodeForces until you have confirmation.**
* There may still be bugs present. If you want to use it during the contest, please make sure that it runs correctly before submitting it.

## Original

<https://github.com/not522/ac-library-python/blob/master/atcoder/__main__.py>

**Modifications**

* Make the specified module expandable.
* Allow `__future__` modules to be imported correctly.
* Allow escaping in the source (such as newline characters).
* Generate .pyc file if able.

## Performance

Verified with Library Checker.

Problem: [Shortest Path](https://judge.yosupo.jp/problem/shortest_path)

|CPython  |Submission                                 |Time   |
|:--------|:------------------------------------------|:------|
|expander |<https://judge.yosupo.jp/submission/79094> |2745 ms|
|pure     |<https://judge.yosupo.jp/submission/79093> |2970 ms|

|PyPy     |Submission                                 |Time   |
|:--------|:------------------------------------------|:------|
|expander |<https://judge.yosupo.jp/submission/79096> |913 ms |
|pure     |<https://judge.yosupo.jp/submission/79097> |918 ms |

## How to install

```sh
pip install git+https://github.com/bayashi-cl/expander
```

## Usage

```sh
python -m expander <source file> [-o <output file>] [-m <expand module names...>]
```

Example:

```sh
python -m expander main.py -o out.py -m yourlib
```

If no output destination is specified, the output will be sent to standard output.

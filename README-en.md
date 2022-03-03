[![pytest](https://github.com/bayashi-cl/expander/actions/workflows/pytest.yml/badge.svg)](https://github.com/bayashi-cl/expander/actions/workflows/pytest.yml)

# expander

Convert Python source code into a single source that can be submitted to online judges.

[Submission using this tool.](https://atcoder.jp/contests/abc238/submissions/29410034)

<details>
<summary>Before expand.</summary>

```python
import sys

from byslib.core import IINF, MOD, debug, sinput
from byslib.data.union_find import UnionFindTree


def main() -> None:
    n, q = map(int, sinput().split())
    uft = UnionFindTree(n + 1)
    for _ in range(q):
        l, r = map(int, sinput().split())
        uft.union(l - 1, r)
    print("Yes" if uft.same(0, n) else "No")


if __name__ == "__main__":
    sys.setrecursionlimit(10**6)
    main()
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

## What you can't do

* Indented imports will be broken.
* If you don't use import statements (like importlib), it will break.

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

```
pip install git+https://github.com/bayashi-cl/expander
```

## Usage

```
python -m expander <source file> [-o <output file>] [-m <expand module names...>]
```

Example:
```
python -m expander main.py -o out.py -m yourlib
```


If no output destination is specified, the output will be sent to standard output.

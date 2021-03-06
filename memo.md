# MEMO

現状の問題点に対応するためのメモ

## 研究

### inspect

* inspect.getsource はファイルが空だと落ちる？
* inspect.getsourcefileは空でも動く
* -> `module.__file__`でよかった

### modulefinder

```python
from modulefinder import ModuleFinder
finder = ModuleFinder()
finder.run_script("path/to/source.py")
finder.modules
```

で読み込まれているmoduleの一覧が取れる。

できること

* 行きがけ順っぽい
* それならモジュール生成部分に使える
* ロードされるファイルすべてを含む

できないこと

* そのままだと標準ライブラリとか関係ないライブラリも含まれてる
* 依存関係はわからない
* 自力で解決する

### ast, astor

* `ast.parse("")`で作成して`.body`に追加していく
* 最後に`ast.fix_missing_locations()`
* 3.8以前だとastからコードに戻すにはastorが必要（一応[公式](https://github.com/python/cpython/blob/3.7/Tools/parser/unparse.py)にもある）
* -> この方法は使わない

* ast nodeからどこまでがモジュール名かを判定するやつ

```python
try:
    if importlib.util.find_spec(name) is None:
        # from module import (class|function|...)
        import_from = module_name
    else:
        # from module import submodule
        import_from = name
except ModuleNotFoundError:
    # from module import (class|function|...)
    import_from = module_name
```

### importのast表現からの変換

大文字がモジュール、小文字がモジュールの要素(関数, クラス, 変数...)

|import                  |asname|name |import from|
|:-----------------------|:-----|:----|:----------|
|`import A.B`            |A.B   |A.B  |A.B        |
|`import A.B as C`       |C     |A.B  |A.B        |
|`from A.B import C`     |C     |A.B.C|A.B.C      |
|`from A.B import C as D`|D     |A.B.C|A.B.C      |
|`from A.B import f`     |f     |A.B.f|A.B        |
|`from A.B import f as g`|g     |A.B.f|A.B        |
|`from A.B import *`     |*     |A.B.*|A.B        |

### パフォーマンス

* Cpythonはクラス定義をグローバルに置かなくなったからか少し速くなった
* PyPyはほぼ変化なし

### パッケージの情報

* 基本的にモジュール名からパッケージの情報は取得できなさそう
* インストールされたパッケージ一覧から該当するモジュール名を探す

## 方針

### ModuleInfo作成パート

* modulefinderで展開するファイルを列挙 これがグラフの頂点になる
* ModuleFinder順でModuleInfo作成
* 依存関係全体の情報は隣接リスト形式 Dict[str, ModuleInfo] で持つ
* 依存関係はDAGになってるはず
* ここでは再帰的な探索は不要

#### ModuleInfoクラス

* モジュール名 `a.b.c`
* ModuleType文字列 `a.b.c = ModuleType("a.b.c")`
* 展開先の文字列

```python
_code_a_b_c = """
import sys
# import a.b.d
# import p as q
# from a.b import f
...
# エスケープを適切にやる
"""
a.b.c.__dict__["a.b.d"] = a.b.d
a.b.c.__dict__["q"] = p
a.b.c.__dict__["f"] = a.b.f
exec(_code_a_b_c, a.b.c.__dict__)
```

* 依存先
`{"a.b.d", "p", "a.b"}`

#### 展開先文字列作成

* code, asname, exec の3つ
* code
    1. inspect.getsourcefileでパスを取得 -> 読み込み
    1. astを探索してimportの位置を記録 -> 依存先に追加
    1. importの行をコメントアウト
    1. `"""` と `\`をエスケープ
    1. `code_a_b_c = """\n{code}"""\n`

* asname\
    各importについて `a_b_c.__dict__["{asname}"] = {name}`

* exec\
    `exec(_code_a_b_c, a.b.c.__dict__)`

### import探索パート

#### ワイルドカードインポートへの対処

* `__all__` が定義されている場合はその中にあるもののみimport
* その他の場合は`_`始まりのもの以外を全てimport

#### 相対インポートへの対処

* `node.level != 0` なら相対インポート
* 今見てるモジュールの絶対名はわかってる
* `importlib.util.resolve_name`で解決
* `from . import ...`の場合はmoduleが`None`になるので注意

### コード追加パート

* `from __future__ import ...`を先頭に持ってくる必要がある
* 結果はastで持つとコメントが消えるので文字列で持つ
* それまでに何を展開したのかを持っておく
* インデントされているimportは壊れる
* import文を使わない(importlibとか)と壊れる

1. astを探索して指定されたパッケージのimportを探す
1. 見つかったらモジュール名とソースコード上の位置を記録 (開始位置, 終了位置, モジュール名, asname...)
1. コードを一行ずつresultに追加
1. 展開するimport文に到達したら、まずはimport文をコメントアウト
1. import文が終わったら展開を始める
1. モジュール名が`a.b.c`だったら`a` -> `a.b` -> `a.b.c` の順にそれぞれを根としたDFSをする
1. pre-orderでModuleType追加、post-orderでコード追加
1. asnameの処理

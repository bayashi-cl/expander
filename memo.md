# MEMO

現状の問題点に対応するためのメモ

## 研究

### inspect

* inspect.getsource はファイルが空だと落ちる？
* inspect.getsourcefileは空でも動く

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
* 自力で解決するしかなさそう？

### ast, astor

* `ast.parse("")`で作成して`.body`に追加していく
* 最後に`ast.fix_missing_locations()`
* 3.8以前だとastからコードに戻すにはastorが必要（一応[公式](https://github.com/python/cpython/blob/3.7/Tools/parser/unparse.py)にもある）

ast nodeからどこまでがモジュール名かを判定するやつ

```python
if import_from is None:
        module_name = name
    else:
        try:
            module_name = import_from + "." + name
            importlib.import_module(module_name)
        except ImportError:
            module_name = import_from
```

### パフォーマンス

* Cpythonだと少し遅くなった （50msくらい？）
* PyPyだと逆に速くなった（なんで？）

## 方針
### モジュール作成パート

* `atcoder = types.ModuleType("atcoder")`みたいなやつ
* modulefinderで展開するファイルを列挙 これが頂点
* ModuleFinder順でModuleType作成

### グラフ探索パート

* 依存関係はDAGになってるはず
* 全頂点からDFSで探索 帰りがけに追加していく
* importは無効化してmoduleの辞書に追加`{now_module}[{asname}] = {module_name}.{asname}`


相対インポートへの対処

* `level != 0` なら相対インポート
* 今見てるモジュールの絶対名はわかってる
* モジュール名の後ろから`level`個削ったあと名前を付け足す

### コード追加パート

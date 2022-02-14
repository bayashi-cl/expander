# expander

Pythonのソースコードをオンラインジャッジに提出可能な単一ソースのものに変換します。

## オリジナル

<https://github.com/not522/ac-library-python/blob/master/atcoder/__main__.py>


**変更点**

* 指定されたモジュールのファイルを展開可能に
* `__future__` 系を最初にimportするように
* ソース内でエスケープ（改行文字とか）を使用可能に
* ソース内の三重引用符はダブルクォーテーションに置き換える


## 注意
* `__init__.py` に何か書かれていないと壊れる
* ソースの中にの三重引用符のネストがあると壊れる

## インストール

```
pip install git+https://github.com/bayashi-cl/expander
```

## 実行コマンド

```
python -m expander <source file> [-o <output file>] [-m <expand module names...>]
```

出力先の指定がない場合は標準出力に出力される。

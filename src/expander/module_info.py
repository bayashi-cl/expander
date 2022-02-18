import importlib
import inspect
import pathlib
from typing import List, Set, cast

from .import_info import ImportInfo, search_import


class ModuleInfo:
    def __init__(self, name: str, expand_module: List[str]) -> None:
        self.name = name
        self.code_valname = f'_code_{name.replace(".", "_")}'
        self.module_type = f'{self.name} = ModuleType("{self.name}")\n'
        self.expand_module = expand_module
        self.dependance: Set[str] = set()

        self.expand_to = ""
        self.expand_to += self.make_code()
        self.expand_to += self.make_aliase()
        self.expand_to += self.make_exec()

    def make_code(self) -> str:
        module = importlib.import_module(self.name)
        module_file = pathlib.Path(cast(str, inspect.getsourcefile(module)))
        code = module_file.read_text()

        # importを探索
        if hasattr(module, "__path__"):  # __init__.py
            self.imports = search_import(code, self.name + ".", self.expand_module)
        else:  # other
            self.imports = search_import(code, self.name, self.expand_module)
        import_lines = set()
        for info in self.imports:
            for lineno in range(info.lineno - 1, cast(int, info.end_lineno)):
                import_lines.add(lineno)
            self.dependance.add(info.import_from)

        # エスケープ処理
        code = code.replace("\\", "\\\\")
        code = code.replace('"""', '\\"""')

        # コメントアウト
        code_lines = code.splitlines()
        for lineno, code_str in enumerate(code_lines):
            if lineno in import_lines:
                code_lines[lineno] = "# " + code_str

        res = f'{self.code_valname} = """\n'
        res += "\n".join(code_lines)
        res += '\n"""\n'
        return res

    def make_aliase(self) -> str:
        res = ""
        for info in self.imports:
            res += f'{self.name}.__dict__["{info.asname}"] = {info.name}\n'
        return res

    def make_exec(self) -> str:
        return f"exec({self.code_valname}, {self.name}.__dict__)\n\n"

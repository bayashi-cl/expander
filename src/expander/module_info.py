import importlib
import importlib.metadata
import inspect
import pathlib
from pkg_resources import Environment
from typing import List, Set, cast, Dict, Optional

from .import_info import search_import

module_to_pkg_name: Dict[str, str] = dict()
pkg_license: Dict[str, Optional[str]] = dict()
for pkg_name, env in Environment()._distmap.items():  # type:ignore
    for dist in env:
        try:
            pkg_license[pkg_name] = dist._provider.get_metadata("LICENSE")
        except Exception:
            pkg_license[pkg_name] = None
        try:
            for top in dist._provider.get_metadata_lines("top_level.txt"):
                module_to_pkg_name[top] = pkg_name
        except Exception:
            pass


class ModuleInfo:
    def __init__(self, name: str, expand_module: List[str]) -> None:
        self.name = name
        self.code_valname = f'_code_{name.replace(".", "_")}'
        self.module_type = (
            self.make_metadata() + f'{self.name} = ModuleType("{self.name}")\n'
        )
        self.expand_module = expand_module
        self.dependance: Set[str] = set()

        self.expand_to = ""
        self.expand_to += self.make_code()
        self.expand_to += self.make_aliase()
        self.expand_to += self.make_exec()

    def make_metadata(self) -> str:
        res = []
        if self.name in module_to_pkg_name:
            pkg_name = module_to_pkg_name[self.name]
            meta = importlib.metadata.metadata(pkg_name)
            res.append(f'# Package infomation of {meta["Name"]}\n')
            res.append(f'# Version: {meta["Version"]}\n')
            if "Author" in meta:
                res.append(f'# Author : {meta["Author"]}\n')
            res.append(f'# License: {meta["License"]}\n')
            if meta["License"] not in {"CC0"}:
                license_text = pkg_license[pkg_name]
                if license_text is not None:
                    res.append("#\n")
                    for line in license_text.splitlines():
                        res.append(f"# {line}\n")
            res.append("\n")
        return "".join(res)

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

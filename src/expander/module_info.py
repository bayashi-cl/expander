import importlib
import importlib.metadata
import pathlib
import textwrap
from logging import getLogger
from typing import Dict, List, Optional, Set, cast

from pkg_resources import Environment

from .import_info import search_import

logger = getLogger(__name__)

# モジュール名 -> パッケージ名の辞書を作成(e.g. sklearn -> scikit-learn)
module_to_pkg_name: Dict[str, str] = dict()
pkg_license: Dict[str, Optional[str]] = dict()
for pkg_name, env in Environment()._distmap.items():  # type: ignore
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
        self.module_type = f'{self.name} = ModuleType("{self.name}")\n'
        self.expand_module = expand_module
        self.dependance: Set[str] = set()
        self.imported: Set[str] = set()
        self.has_all = False

        self.expand_to = ""
        self.expand_to += self.make_code()
        self.expand_to += self.make_aliase()
        self.expand_to += self.make_exec()
        self.metadata = self.make_metadata()

        self.dependance = set(sorted(list(self.dependance)))

    def make_metadata(self) -> Optional[str]:
        res = []
        if self.name in module_to_pkg_name:
            pkg_name = module_to_pkg_name[self.name]
            meta = importlib.metadata.metadata(pkg_name)
            res.append(f'# {meta["Name"]}\n')
            for field in ["Version", "Author", "Home-page", "License"]:
                if field in meta:
                    res.append(f"#   {field:<9s}: {meta[field]}\n")
            if meta["License"] not in {"CC0"}:
                license_text = pkg_license[pkg_name]
                if license_text is not None:
                    res.append("#\n")
                    for line in license_text.splitlines():
                        res.append(f"#   {line}\n")
            return "".join(res)
        else:
            return None

    def make_code(self) -> str:
        module = importlib.import_module(self.name)
        self.has_all = hasattr(module, "__all__")
        code = pathlib.Path(cast(str, module.__file__)).read_text()

        # importを探索
        self.imports = search_import(
            code, cast(str, module.__package__), self.expand_module
        )

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
            if info.import_from == info.name == info.asname:
                sep = info.name.split(".")
                for i in range(len(sep)):
                    module_name = ".".join(sep[: i + 1])
                    if module_name in self.imported:
                        continue
                    self.imported.add(module_name)
                    res += f'{self.name}.__dict__["{module_name}"] = {module_name}\n'

            if info.asname == "*":
                if hasattr(importlib.import_module(info.name), "__all__"):
                    res += textwrap.dedent(
                        f"""\
                        for _name in {info.name}.__all__:
                            {self.name}.__dict__[_name] = {info.name}.__dict__[_name]
                        """
                    )
                else:
                    res += textwrap.dedent(
                        f"""\
                        for _name in {info.name}.__dict__:
                            if not _name.startswith("_"):
                                {self.name}.__dict__[_name] = {info.name}.__dict__[_name]
                        """
                    )

            elif info.asname not in self.imported:
                res += f'{self.name}.__dict__["{info.asname}"] = {info.name}\n'

        return res

    def make_exec(self) -> str:
        return f"exec({self.code_valname}, {self.name}.__dict__)\n\n"

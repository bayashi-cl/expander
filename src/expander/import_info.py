import ast
import importlib.util
from dataclasses import dataclass
from typing import Any, List, Optional, cast

import sys


@dataclass
class ImportInfo:
    name: str
    asname: str
    import_from: str
    lineno: int
    end_lineno: Optional[int]

    def __post_init__(self):
        if self.end_lineno is None:
            self.end_lineno = self.lineno


class ImportVisitor(ast.NodeVisitor):
    def __init__(
        self, now_module: str, expand_module: Optional[List[str]] = None
    ) -> None:
        self.now_module = now_module
        if expand_module is None:
            self.expand_module = []
        else:
            self.expand_module = expand_module
        self.info: List[ImportInfo] = []

    def visit_Import(self, node: ast.Import) -> Any:
        for alias in node.names:
            name = alias.name
            if name.split(".")[0] in self.expand_module:
                if alias.asname is None:
                    asname = name
                else:
                    asname = alias.asname
                self.info.append(
                    ImportInfo(name, asname, name, node.lineno, node.end_lineno)
                )

    def visit_ImportFrom(self, node: ast.ImportFrom) -> Any:
        if node.module is None:
            module_name = ""
        else:
            module_name = node.module
        if node.level != 0:
            base = ".".join(self.now_module.split(".")[: -node.level])
            if module_name:
                module_name = base + "." + module_name
            else:
                module_name = base

        if module_name.split(".")[0] in self.expand_module:
            for alias in node.names:
                if alias.name == "*":
                    print("cannot expand wildcard import", file=sys.stderr)
                    raise NotImplementedError
                name = module_name + "." + alias.name
                try:
                    if importlib.util.find_spec(name) is None:
                        import_from = module_name
                    else:
                        import_from = name
                except ModuleNotFoundError:
                    import_from = module_name

                if alias.asname is None:
                    asname = alias.name
                else:
                    asname = alias.asname
                self.info.append(
                    ImportInfo(name, asname, import_from, node.lineno, node.end_lineno)
                )


def search_import(code: str, now: str, expand_module: List[str]) -> List[ImportInfo]:
    tree = ast.parse(code)
    visitor = ImportVisitor(now, expand_module)
    visitor.visit(tree)
    return visitor.info

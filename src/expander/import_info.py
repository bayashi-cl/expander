import ast
import importlib.util
import sys
from dataclasses import dataclass
from typing import Any, List, Optional


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
    def __init__(self, now_pkg: str, expand_module: Optional[List[str]] = None) -> None:
        self.now_pkg = now_pkg
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
            # resolve relative import
            dot_module = "." * node.level + module_name
            module_name = importlib.util.resolve_name(dot_module, self.now_pkg)

        if module_name.split(".")[0] in self.expand_module:
            for alias in node.names:
                if alias.name == "*":
                    print("cannot expand wildcard import", file=sys.stderr)
                    raise NotImplementedError
                name = module_name + "." + alias.name
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

                if alias.asname is None:
                    asname = alias.name
                else:
                    asname = alias.asname
                self.info.append(
                    ImportInfo(name, asname, import_from, node.lineno, node.end_lineno)
                )


def search_import(code: str, pkg: str, expand_module: List[str]) -> List[ImportInfo]:
    tree = ast.parse(code)
    visitor = ImportVisitor(pkg, expand_module)
    visitor.visit(tree)
    return visitor.info

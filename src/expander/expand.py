import logging
import pathlib
import textwrap
from collections import defaultdict
from modulefinder import ModuleFinder
from typing import DefaultDict, Dict, List, Set, cast

from .import_info import ImportInfo, search_import
from .module_info import ModuleInfo

logger = logging.getLogger(__name__)
ATCODER_MODULES = [
    "Cython",
    "cython",
    "decorator",
    "easy_install",
    "joblib",
    "llvmlite",
    "networkx",
    "numba",
    "numpy",
    "pkg_resources",
    "pyximport",
    "scipy",
    "setuptools",
    "sklearn",
]


class ModuleImporter:
    def __init__(self, modules: Dict[str, ModuleInfo]) -> None:
        self.modules = modules
        self.imported_modules: Set[str] = set()
        self.pkg_info: List[str] = []

    def expand(self, module_info_: ModuleInfo) -> str:
        module_types = ""
        if not self.imported_modules:
            module_types += "from types import ModuleType\n\n"
        body = ""

        def dfs(module_info: ModuleInfo) -> None:
            if module_info.name in self.imported_modules:
                return
            logger.info(module_info.name)
            self.imported_modules.add(module_info.name)
            if module_info.metadata is not None:
                self.pkg_info.append(module_info.metadata)

            nonlocal module_types, body
            module_types += module_info.module_type
            for dep in module_info.dependance:
                dep_split = dep.split(".")
                for i in range(len(dep_split)):
                    dfs(self.modules[".".join(dep_split[: i + 1])])
            body += module_info.expand_to

        module_info_split = module_info_.name.split(".")
        for i in range(len(module_info_split)):
            dfs(self.modules[".".join(module_info_split[: i + 1])])
        if len(module_types) > 0 or len(body) > 0:
            return module_types + "\n" + body
        else:
            return module_types + body


def expand(source: pathlib.Path, expand_module: List[str]) -> str:
    """expand modules

    Args:
        source (pathlib.Path): source to expand
        expand (List[str]): List of expand module names.

    Returns:
        str: expanded code

    Note:
        This module is intended to be used in competition programming.

    """
    # 展開するモジュールを探索
    finder = ModuleFinder(excludes=ATCODER_MODULES)
    finder.run_script(str(source))
    modules: Dict[str, ModuleInfo] = dict()
    for module in finder.modules.values():
        if cast(str, module.__name__).split(".")[0] in expand_module:  # type:ignore
            modulename = cast(str, module.__name__)  # type: ignore
            logger.info(f"load {module.__file__}")  # type:ignore
            modules[modulename] = ModuleInfo(modulename, expand_module)
    logger.info(f"{len(modules)} modules found.")

    # src内のimportを探索
    logger.info("expand start")
    code: str = source.read_text()
    imports = search_import(code, "", expand_module)
    import_lines = set()
    expand_lines: DefaultDict[int, List[ImportInfo]] = defaultdict(list)
    for info in imports:
        for lineno in range(info.lineno - 1, cast(int, info.end_lineno)):
            import_lines.add(lineno)
        expand_lines[cast(int, info.end_lineno) - 1].append(info)

    # コード生成
    code_lines = code.splitlines(keepends=True)
    importer = ModuleImporter(modules)
    result: List[str] = []

    for lineno, line_str in enumerate(code_lines):
        if lineno in import_lines:
            result.append("# " + line_str)
        else:
            result.append(line_str)

        if lineno in expand_lines:
            for importinfo in expand_lines[lineno]:
                moduleinfo = modules[importinfo.import_from]
                result.append(importer.expand(moduleinfo))
                if importinfo.asname == "*":
                    if moduleinfo.has_all:
                        importall = textwrap.dedent(
                            f"""
                            for _name in {importinfo.name}.__all__:
                                locals()[_name] = {importinfo.name}.__dict__[_name]
                            """
                        )
                    else:
                        importall = textwrap.dedent(
                            f"""
                            for _name in {importinfo.name}.__dict__:
                                if not _name.startswith("_"):
                                    locals()[_name] = {importinfo.name}.__dict__[_name]
                            """
                        )
                    result.append(importall)

                elif importinfo.asname != importinfo.name:
                    result.append(f"{importinfo.asname} = {importinfo.name}\n")

    if importer.pkg_info:
        result.append("\n\n# package infomations\n")
        for meta in importer.pkg_info:
            result.append("# " + "-" * 74 + "\n")
            result.append(meta)
        result.append("# " + "-" * 74 + "\n")

    return "".join(result)

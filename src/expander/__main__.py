"""\
source expander
"""

import argparse
import logging
import pathlib
import sys
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


def setup_logger(verbose: bool = False) -> None:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)-8s%(message)s")
    handler.setFormatter(formatter)
    if verbose:
        logging.basicConfig(level=logging.DEBUG, handlers=[handler])
    else:
        logging.basicConfig(level=logging.INFO, handlers=[handler])


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


def main() -> None:
    setup_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=pathlib.Path, help="Source path")
    parser.add_argument("-o", "--output", type=pathlib.Path, help="output path")
    parser.add_argument("-m", "--modules", nargs="*", help="list of expand module")
    args = parser.parse_args()
    expand_module: List[str] = args.modules

    # 展開するモジュールを探索
    finder = ModuleFinder(excludes=ATCODER_MODULES)
    finder.run_script(str(args.src))
    modules: Dict[str, ModuleInfo] = dict()
    for module in finder.modules.values():
        if cast(str, module.__name__).split(".")[0] in expand_module:  # type:ignore
            modulename = cast(str, module.__name__)  # type: ignore
            logger.info(f"load {module.__file__}")  # type:ignore
            modules[modulename] = ModuleInfo(modulename, expand_module)

    # 展開するものがないとき
    if len(modules) == 0:
        logger.info("no module to expand")
        if args.output is None:
            print(args.src.read_text())
        else:
            args.output.write_text(args.src.read_text())
        sys.exit(0)
    else:
        logger.info(f"{len(modules)} modules found.")

    # src内のimportを探索
    logger.info("expand start")
    code: str = args.src.read_text()
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

    # 出力
    if args.output is None:
        print("".join(result), end="")
    else:
        args.output.write_text("".join(result))


if __name__ == "__main__":
    main()

"""\
source expander
"""

import argparse
import pathlib
import sys
from collections import defaultdict
from modulefinder import ModuleFinder
from typing import DefaultDict, Dict, List, Set, cast

from .import_info import ImportInfo, search_import
from .module_info import ModuleInfo


class ModuleImporter:
    imported_modules: Set[str]
    modules: Dict[str, ModuleInfo]

    def __init__(self, modules: Dict[str, ModuleInfo]) -> None:
        self.modules = modules
        self.imported_modules = set()

    def expand(self, module_info_: ModuleInfo) -> str:
        module_types = ""
        if not self.imported_modules:
            module_types += "from types import ModuleType\n\n"
        body = ""

        def dfs(module_info: ModuleInfo) -> None:
            if module_info.name in self.imported_modules:
                return
            self.imported_modules.add(module_info.name)

            nonlocal module_types, body
            module_types += module_info.module_type
            for dep in module_info.dependance:
                dfs(self.modules[dep])
            body += module_info.expand_to

        module_info_split = module_info_.name.split(".")
        for i in range(len(module_info_split)):
            dfs(self.modules[".".join(module_info_split[: i + 1])])
        return module_types + "\n" + body


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=pathlib.Path, help="Source path")
    parser.add_argument("-o", "--output", type=pathlib.Path, help="output path")
    parser.add_argument("-m", "--modules", nargs="*", help="list of expand module")
    args = parser.parse_args()
    expand_module: List[str] = args.modules

    # 展開するモジュールを探索
    finder = ModuleFinder()
    finder.run_script(str(args.src))
    imported_modules: List[str] = []
    for module in finder.modules.values():
        if cast(str, module.__name__).split(".")[0] in expand_module:  # type:ignore
            imported_modules.append(module.__name__)  # type:ignore
    #
    modules: Dict[str, ModuleInfo] = dict()
    for modulename in imported_modules:
        modules[modulename] = ModuleInfo(modulename, expand_module)

    # 展開するものがないとき
    print(f"{len(imported_modules)} modules found.", file=sys.stderr)
    print(*imported_modules, sep="\n", file=sys.stderr)
    if not imported_modules:
        print("no module to expand", file=sys.stderr)
        if args.output is None:
            print(args.src.read_text())
        else:
            args.output.write_text(args.src.read_text())
        sys.exit(0)

    # src内のimportを探索
    code: str = args.src.read_text()
    imports = search_import(code, __name__, expand_module)
    import_lines = set()
    expand_lines: DefaultDict[int, List[ImportInfo]] = defaultdict(list)
    for info in imports:
        for lineno in range(info.lineno - 1, cast(int, info.end_lineno)):
            import_lines.add(lineno)
        expand_lines[cast(int, info.end_lineno) - 1].append(info)

    # コード生成
    code_lines = code.splitlines(keepends=True)
    importer = ModuleImporter(modules)
    result = ""

    for lineno, line_str in enumerate(code_lines):
        if lineno in import_lines:
            result += "# " + line_str
        else:
            result += line_str

        if lineno in expand_lines:
            for importinfo in expand_lines[lineno]:
                result += importer.expand(modules[importinfo.import_from])
                if importinfo.asname != importinfo.name:
                    result += f"{importinfo.asname} = {importinfo.name}\n"

    # 出力
    if args.output is None:
        print(result)
    else:
        args.output.write_text(result)


if __name__ == "__main__":
    main()

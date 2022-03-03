import pathlib
import subprocess
import sys
from typing import Tuple

TESTSDIR = pathlib.Path.cwd() / "tests"
SRCDIR = TESTSDIR / "src"
OUTDIR = TESTSDIR / "out"


def run_python_file(path: pathlib.Path, stdin: str = "") -> str:
    res = subprocess.run(
        args=[sys.executable, path],
        stdout=subprocess.PIPE,
        input=stdin,
        text=True,
        check=True,
    )
    return res.stdout


def expand(name: str) -> Tuple[pathlib.Path, pathlib.Path]:
    subprocess.run(
        args=[
            "python",
            "-m",
            "expander",
            SRCDIR / name,
            "-o",
            OUTDIR / name,
            "-m",
            "testlib_a",
            "testlib_b",
        ],
        check=True,
    )
    return SRCDIR / name, OUTDIR / name


class TestExpandNormal:
    def test_normal(self):
        src, out = expand("normal.py")
        assert run_python_file(src) == run_python_file(out)

    def test_import_as(self):
        src, out = expand("import_as.py")
        assert run_python_file(src) == run_python_file(out)

    def test_import_func_as(self):
        src, out = expand("import_func_as.py")
        assert run_python_file(src) == run_python_file(out)

    def test_import_func(self):
        src, out = expand("import_func.py")
        assert run_python_file(src) == run_python_file(out)


class TestExpandRelative:
    def test_relative_from_samedir(self):
        src, out = expand("relative_from_samedir.py")
        assert run_python_file(src) == run_python_file(out)

    def test_relative_from_parentdir(self):
        src, out = expand("relative_from_parentdir.py")
        assert run_python_file(src) == run_python_file(out)

    def test_relative_from_childdir(self):
        src, out = expand("relative_from_childdir.py")
        assert run_python_file(src) == run_python_file(out)


class TestExpandMisc:
    def test_expand_only_std(self):
        src, out = expand("only_std.py")
        assert run_python_file(src) == run_python_file(out)

    def test_expand_otherlib(self):
        src, out = expand("otherlib.py")
        assert run_python_file(src) == run_python_file(out)

    def test_expand_from_init(self):
        src, out = expand("from_init.py")
        assert run_python_file(src) == run_python_file(out)


class TestExpandWildcard:
    def test_wildcard_module_all(self):
        src, out = expand("wildcard_module_all.py")
        assert run_python_file(src) == run_python_file(out)

    def test_wildcard_module(self):
        src, out = expand("wildcard_module.py")
        assert run_python_file(src) == run_python_file(out)

    def test_wildcard_main_all(self):
        src, out = expand("wildcard_main_all.py")
        assert run_python_file(src) == run_python_file(out)

    def test_wildcard_main(self):
        src, out = expand("wildcard_main.py")
        assert run_python_file(src) == run_python_file(out)


class TestFuture:
    def test_input(self):
        src, out = expand("input.py")
        assert run_python_file(src, "5") == run_python_file(out, "5")

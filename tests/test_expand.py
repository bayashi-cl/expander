import pathlib
import subprocess
import sys

import pytest

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


def expand(name: str) -> tuple[pathlib.Path, pathlib.Path]:
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


class TestExpand:
    @pytest.mark.parametrize(
        "path",
        [
            "normal.py",
            "import_as.py",
            "import_func_as.py",
            "import_func.py",
        ],
    )
    def test_normal(self, path: str) -> None:
        src, out = expand(path)
        assert run_python_file(src) == run_python_file(out)

    @pytest.mark.parametrize(
        "path",
        [
            "relative_from_samedir.py",
            "relative_from_parentdir.py",
            "relative_from_childdir.py",
        ],
    )
    def test_relative(self, path: str) -> None:
        src, out = expand(path)
        assert run_python_file(src) == run_python_file(out)

    @pytest.mark.parametrize(
        "path",
        [
            "wildcard_module_all.py",
            "wildcard_module.py",
            "wildcard_main_all.py",
            "wildcard_main.py",
        ],
    )
    def test_wildcard(self, path: str) -> None:
        src, out = expand(path)
        assert run_python_file(src) == run_python_file(out)

    def test_input(self) -> None:
        src, out = expand("input.py")
        assert run_python_file(src, "5") == run_python_file(out, "5")

    @pytest.mark.parametrize(
        "path",
        [
            "only_std.py",
            "otherlib.py",
            "from_init.py",
            "abs_name.py",
            "future.py",
        ],
    )
    def test_misc(self, path: str) -> None:
        src, out = expand(path)
        assert run_python_file(src) == run_python_file(out)

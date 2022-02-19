import pathlib
import subprocess
from typing import Tuple

TESTSDIR = pathlib.Path.cwd() / "tests"
SRCDIR = TESTSDIR / "src"
OUTDIR = TESTSDIR / "out"


def run_python_file(path: pathlib.Path, stdin: str = "") -> str:
    res = subprocess.run(
        args=["python", path],
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


def test_expand_normal():
    src, out = expand("normal.py")
    assert run_python_file(src) == run_python_file(out)


def test_expand_import_as():
    src, out = expand("import_as.py")
    assert run_python_file(src) == run_python_file(out)


def test_expand_import_func_as():
    src, out = expand("import_func_as.py")
    assert run_python_file(src) == run_python_file(out)


def test_expand_import_func():
    src, out = expand("import_func.py")
    assert run_python_file(src) == run_python_file(out)


def test_expand_only_std():
    src, out = expand("only_std.py")
    assert run_python_file(src) == run_python_file(out)


def test_expand_relative_from_samedir():
    src, out = expand("relative_from_samedir.py")
    assert run_python_file(src) == run_python_file(out)


def test_expand_relative_from_parentdir():
    src, out = expand("relative_from_parentdir.py")
    assert run_python_file(src) == run_python_file(out)


def test_expand_relative_from_childdir():
    src, out = expand("relative_from_childdir.py")
    assert run_python_file(src) == run_python_file(out)


def test_expand_otherlib():
    src, out = expand("otherlib.py")
    assert run_python_file(src) == run_python_file(out)


def test_expand_from_init():
    src, out = expand("from_init.py")
    assert run_python_file(src) == run_python_file(out)


def test_feature_input():
    src, out = expand("input.py")
    assert run_python_file(src, "5") == run_python_file(out, "5")

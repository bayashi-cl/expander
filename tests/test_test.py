import os
import pathlib
import subprocess

srcdir = pathlib.Path.cwd() / "tests" / "src"
outdir = pathlib.Path.cwd() / "tests" / "out"


def test_env_pythonpath() -> None:
    assert os.environ["PYTHONPATH"] == str(pathlib.Path.cwd() / "tests" / "testlib")


def test_testlib_import() -> None:
    subprocess.run(["python", srcdir / "normal.py"], check=True)  # noqa: S603, S607


def test_testlib_expand() -> None:
    subprocess.run(
        args=[
            "python",
            "-m",
            "expander",
            srcdir / "normal.py",
            "-o",
            outdir / "normal_test_expand.py",
            "-m",
            "testlib_a",
        ],
        check=True,
    )
    assert (outdir / "normal_test_expand.py").exists()

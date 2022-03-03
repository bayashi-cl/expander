import expander
import os
import pathlib
import subprocess

srcdir = pathlib.Path.cwd() / "tests" / "src"
outdir = pathlib.Path.cwd() / "tests" / "out"


def test_version():
    assert expander.__version__ == "0.2.2"


def test_env_pythonpath():
    assert os.environ["PYTHONPATH"] == str(pathlib.Path.cwd() / "tests" / "testlib")


def test_testlib_import():
    try:
        subprocess.run(["python", srcdir / "normal.py"], check=True)
    except subprocess.CalledProcessError as e:
        assert False, e


def test_testlib_expand():
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

import pytest
from unittest import mock
import os
import pathlib


@pytest.fixture(scope="session", autouse=True)
def set_pythonpath():
    testlib_path = pathlib.Path.cwd() / "tests" / "testlib"
    with mock.patch.dict(os.environ, {"PYTHONPATH": str(testlib_path)}):
        yield

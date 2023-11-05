import os
import pathlib
from collections.abc import Generator
from unittest import mock

import pytest


@pytest.fixture(scope="session", autouse=True)
def _set_pythonpath() -> Generator[None, None, None]:
    testlib_path = pathlib.Path.cwd() / "tests" / "testlib"
    with mock.patch.dict(os.environ, {"PYTHONPATH": str(testlib_path)}):
        yield

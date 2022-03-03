import re
from setuptools import setup, find_packages

with open("src/expander/__init__.py", "r") as fd:
    version = re.search(  # type: ignore
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', fd.read(), re.MULTILINE
    ).group(1)

setup(
    name="expander",
    version=version,
    author="Masaki Kobayashi",
    author_email="bayashi.cl@gmail.com",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    license="CC0",
)

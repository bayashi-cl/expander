"""source expander

Note:
    usage: __main__.py [-h] [-o OUTPUT] [-m [MODULES [MODULES ...]]] src

    positional arguments:
    src                   Source path

    optional arguments:
    -h, --help            show this help message and exit
    -o OUTPUT, --output OUTPUT
                            output path
    -m [MODULES [MODULES ...]], --modules [MODULES [MODULES ...]]
                            list of expand module
"""
import argparse
import logging
import pathlib
import sys

from .bundle_importer import importer_expand

logger = logging.getLogger(__name__)


def setup_logger(*, verbose: bool = False) -> None:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(levelname)-8s%(message)s")
    handler.setFormatter(formatter)
    if verbose:
        logging.basicConfig(level=logging.DEBUG, handlers=[handler])
    else:
        logging.basicConfig(level=logging.INFO, handlers=[handler])


def main() -> None:
    setup_logger()
    parser = argparse.ArgumentParser()
    parser.add_argument("src", type=pathlib.Path, help="Source path")
    parser.add_argument("-o", "--output", type=pathlib.Path, help="output path")
    parser.add_argument("-m", "--modules", nargs="*", help="list of expand module")
    args = parser.parse_args()

    result = importer_expand(args.src, args.modules)

    if args.output is None:
        sys.stdout.write(result)
    else:
        args.output.write_text(result)


if __name__ == "__main__":
    main()

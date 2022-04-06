"""\
source expander
"""

import argparse
import logging
import pathlib
import sys

from .expand import expand

logger = logging.getLogger(__name__)


def setup_logger(verbose: bool = False) -> None:
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

    result = expand(args.src, args.modules)

    # 出力
    if args.output is None:
        sys.stdout.write(result)
    else:
        args.output.write_text(result)


if __name__ == "__main__":
    main()

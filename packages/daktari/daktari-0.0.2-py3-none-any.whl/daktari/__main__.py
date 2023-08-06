from daktari.config import read_config
from daktari.check_runner import run_checks
from daktari.options import argument_parser
import sys
import logging
from pyfiglet import Figlet


def print_logo(title: str):
    figlet = Figlet(font="slant")
    print(figlet.renderText(title))


def main():
    args = argument_parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)
    config = read_config(args.config_path)

    if config.title:
        print_logo(config.title)
    all_passed = run_checks(config.checks)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

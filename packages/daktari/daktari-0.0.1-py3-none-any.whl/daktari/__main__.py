from daktari.git_checks import (
    GitCryptInstalledCheck,
    GitInstalledCheck,
    GitLfsCheck,
    GitLfsFilesDownloadedCheck,
    GitLfsSetUpForUserCheck,
)
from daktari.check_runner import run_checks
import sys
import argparse
import logging
from pyfiglet import Figlet

parser = argparse.ArgumentParser(description="Check developer environment configuration.")
parser.add_argument("--debug", default=False, action="store_true", help="turn on debug logging")


def print_logo():
    figlet = Figlet(font="slant")
    print(figlet.renderText("Doctor"))


checks = [
    GitInstalledCheck(),
    GitLfsCheck(),
    GitLfsSetUpForUserCheck(),
    GitLfsFilesDownloadedCheck(),
    GitCryptInstalledCheck(),
]


def main():
    args = parser.parse_args()
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)

    print_logo()

    all_passed = run_checks(checks)
    return 0 if all_passed else 1


if __name__ == "__main__":
    sys.exit(main())

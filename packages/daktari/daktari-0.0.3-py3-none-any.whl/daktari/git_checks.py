import logging
from daktari.os import OS
from daktari.check import Check, CheckResult
from daktari.command_utils import can_run_command, get_stdout


class GitInstalledCheck(Check):
    check_name = "git.installed"

    suggestions = {
        OS.OS_X: "<cmd>brew install git</cmd>",
        OS.UBUNTU: "<cmd>sudo apt install git</cmd>",
        OS.GENERIC: "Install Git from https://git-scm.com/downloads",
    }

    def check(self) -> CheckResult:
        if can_run_command("git version"):
            return self.passed("Git is installed")
        else:
            return self.failed("Could not find git on the path")


class GitLfsCheck(Check):
    check_name = "git.lfs.installed"
    depends_on = [GitInstalledCheck]

    suggestions = {
        OS.OS_X: "<cmd>brew install git-lfs</cmd>",
        OS.UBUNTU: "<cmd>sudo apt install git-lfs</cmd>",
        OS.GENERIC: "Install Git LFS (https://github.com/git-lfs/git-lfs/wiki/Installation)",
    }

    def check(self) -> CheckResult:
        if can_run_command("git lfs version"):
            return self.passed("Git LFS is installed")
        else:
            return self.failed("Git LFS is not installed")


class GitLfsSetUpForUserCheck(Check):
    check_name = "git.lfs.setUpForUser"
    depends_on = [GitLfsCheck]

    suggestions = {
        OS.GENERIC: """Set up Git LFS for your user account:
                       <cmd>git lfs install</cmd>"""
    }

    def check(self) -> CheckResult:
        output = get_stdout("git lfs env")
        if output and "git config filter.lfs" in output:
            return self.passed("Git LFS is set up for the current user")
        else:
            return self.failed("Git LFS is not set up for the current user")


class GitLfsFilesDownloadedCheck(Check):
    check_name = "git.lfs.filesDownloaded"
    depends_on = [GitLfsSetUpForUserCheck]

    suggestions = {
        OS.GENERIC: """Download all Git LFS files and update working copy with the downloaded content:
                       <cmd>git lfs pull</cmd>"""
    }

    def check(self) -> CheckResult:
        output = get_stdout("git lfs ls-files") or ""
        files_not_downloaded = [line.split()[2] for line in output.splitlines() if line.split()[1] == "-"]
        for file in files_not_downloaded:
            logging.info(f"Git LFS file not downloaded: {file}")
        if files_not_downloaded:
            return self.failed("Git LFS files have not been downloaded")
        else:
            return self.passed("Git LFS files have been downloaded")


class GitCryptInstalledCheck(Check):
    check_name = "git.crypt.installed"
    depends_on = [GitInstalledCheck]

    suggestions = {
        OS.OS_X: "<cmd>brew install git-crypt</cmd>",
        OS.UBUNTU: "<cmd>sudo apt install git-crypt</cmd>",
        OS.GENERIC: "Install git-crypt (https://www.agwa.name/projects/git-crypt/",
    }

    def check(self) -> CheckResult:
        if can_run_command("git crypt version"):
            return self.passed("git-crypt is installed")
        else:
            return self.failed("git-crypt is not installed")


def is_ascii(path: str) -> bool:
    file_output = get_stdout(["file", path]) or ""
    parts = file_output.strip().split(": ")
    return parts[1] == "ASCII text"

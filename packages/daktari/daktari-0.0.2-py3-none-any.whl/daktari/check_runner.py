from daktari.check_sorter import sort_checks
import logging
from typing import List
from daktari.check import Check, CheckStatus
from daktari.result_printer import print_check_result
from colors import yellow


def run_checks(checks: List[Check]):
    CheckRunner().run(checks)


class CheckRunner:
    def __init__(self):
        self.all_passed = True
        self.checks_passed = set()

    def run(self, checks: List[Check]) -> bool:
        for check in sort_checks(checks):
            self.try_run_check(check)
        return self.all_passed

    def try_run_check(self, check: Check):
        dependencies_met = all([dependency.name in self.checks_passed for dependency in check.depends_on])
        if dependencies_met:
            logging.info(f"Running check {check.name}")
            result = check.check()
            print_check_result(result)
            if result.status == CheckStatus.PASS:
                self.checks_passed.add(check.name)
            else:
                self.all_passed = False
        else:
            print(f"⚠️  [{yellow(check.name)}] skipped due to previous failures")

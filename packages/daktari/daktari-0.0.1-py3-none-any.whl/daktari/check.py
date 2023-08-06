import abc
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Type


class CheckStatus(Enum):
    PASS = "PASS"
    FAIL = "FAIL"


@dataclass
class CheckResult:
    check_name: str
    status: CheckStatus
    summary: str
    suggestions: Dict[str, str]


class Check:
    check_name: str
    depends_on: List[Type] = []
    suggestions: Dict[str, str] = {}

    def passed(self, message: str) -> CheckResult:
        return CheckResult(self.check_name, CheckStatus.PASS, message, self.suggestions)

    def failed(self, message: str) -> CheckResult:
        return CheckResult(self.check_name, CheckStatus.FAIL, message, self.suggestions)

    @abc.abstractmethod
    def check(self) -> CheckResult:
        raise NotImplementedError("check must be implemented")

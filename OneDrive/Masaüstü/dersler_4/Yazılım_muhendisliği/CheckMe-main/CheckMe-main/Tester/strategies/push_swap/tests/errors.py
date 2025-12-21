from .base import BaseTest
from typing import List, Tuple, Any

class ErrorManagementTest(BaseTest):
    """Base class for error management tests."""

    def validate(self, output: str, stderr: str, exit_code: int) -> Tuple[bool, str, Any]:
        if "Error" in stderr:
            return True, "Correctly detected error", None
        return False, f"Expected 'Error' in stderr, got: {stderr.strip()}", None

class DuplicateTest(ErrorManagementTest):
    def generate_args(self) -> List[str]:
        return ["1", "2", "3", "2", "5"]

    def get_name(self) -> str:
        return "Error: Duplicates"

class MaxMinTest(ErrorManagementTest):
    def generate_args(self) -> List[str]:
        # Testing values just outside integer limits
        return ["2147483648", "-2147483649"]

    def get_name(self) -> str:
        return "Error: Max/Min Limits"

class OverflowTest(ErrorManagementTest):
    def generate_args(self) -> List[str]:
        # Testing values that definitely overflow standard integer types
        return ["999999999999999999"]

    def get_name(self) -> str:
        return "Error: Overflow"

class InvalidInputTest(ErrorManagementTest):
    def generate_args(self) -> List[str]:
        return ["1", "two", "3"]

    def get_name(self) -> str:
        return "Error: Invalid Input"

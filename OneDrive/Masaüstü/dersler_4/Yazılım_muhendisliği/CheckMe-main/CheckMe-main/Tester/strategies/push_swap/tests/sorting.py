from .base import BaseTest
from typing import List, Tuple, Any
# Import NumberGenerator from utils.
# Since we are in Tester/strategies/push_swap/tests/,
# utils is in Tester/utils/
# So it is ...utils.number_generator
# But python relative imports can be tricky if not run as module.
# Assuming the runner sets up path correctly or we use absolute imports if needed.
# The user context shows Tester/utils/number_generator.py exists.
# Let's try relative import.
try:
    from ...utils.number_generator import NumberGenerator
except ImportError:
    # Fallback for when running tests directly or different path structure
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
    from utils.number_generator import NumberGenerator

class SortingTest(BaseTest):
    """Base class for sorting tests."""

    def __init__(self):
        self.generator = NumberGenerator()
        self.args = []

    def validate(self, output: str, stderr: str, exit_code: int) -> Tuple[bool, str, Any]:
        if exit_code != 0:
            return False, f"Program exited with code {exit_code}", None
        if stderr:
            return False, f"Unexpected stderr: {stderr}", None
        return True, "Execution successful", None

class IdentityTest(SortingTest):
    def generate_args(self) -> List[str]:
        self.args = ["1", "2", "3", "4", "5"]
        return self.args

    def get_name(self) -> str:
        return "Sorting: Identity (Already Sorted)"

class ReverseTest(SortingTest):
    def generate_args(self) -> List[str]:
        self.args = ["5", "4", "3", "2", "1"]
        return self.args

    def get_name(self) -> str:
        return "Sorting: Reverse Sorted"

class RandomTest(SortingTest):
    def __init__(self, count: int):
        super().__init__()
        self.count = count

    def generate_args(self) -> List[str]:
        nums = self.generator.generate_random_numbers(self.count)
        self.args = nums.split()
        return self.args

    def get_name(self) -> str:
        return f"Sorting: Random {self.count}"

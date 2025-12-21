from .base import BaseTest
from typing import List, Tuple, Any
try:
    from ...utils.number_generator import NumberGenerator
except ImportError:
    import sys
    import os
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
    from utils.number_generator import NumberGenerator

class PerformanceTest(BaseTest):
    """Base class for performance tests."""

    def __init__(self, count: int, limit: int):
        self.generator = NumberGenerator()
        self.count = count
        self.limit = limit
        self.args = []

    def generate_args(self) -> List[str]:
        nums = self.generator.generate_random_numbers(self.count)
        self.args = nums.split()
        return self.args

    def validate(self, output: str, stderr: str, exit_code: int) -> Tuple[bool, str, Any]:
        if exit_code != 0:
            return False, f"Program exited with code {exit_code}", None
        if stderr:
            return False, f"Unexpected stderr: {stderr}", None

        moves = len(output.strip().split('\n')) if output.strip() else 0

        if moves <= self.limit:
            score = 100
            msg = f"OK: {moves} moves (Limit: {self.limit})"
            return True, msg, {"moves": moves, "score": score}
        else:
            score = 0
            msg = f"FAIL: {moves} moves (Limit: {self.limit})"
            return False, msg, {"moves": moves, "score": score}

    def get_name(self) -> str:
        return f"Performance: {self.count} numbers"

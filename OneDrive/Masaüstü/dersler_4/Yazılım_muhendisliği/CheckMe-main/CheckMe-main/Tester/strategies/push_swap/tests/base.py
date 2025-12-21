from abc import ABC, abstractmethod
from typing import List, Tuple, Any

class BaseTest(ABC):
    """Abstract base class for all push_swap tests."""

    @abstractmethod
    def generate_args(self) -> List[str]:
        """Returns input arguments for the test."""
        pass

    @abstractmethod
    def validate(self, output: str, stderr: str, exit_code: int) -> Tuple[bool, str, Any]:
        """
        Validates the result.
        Returns: (is_success, message, extra_data)
        """
        pass

    @abstractmethod
    def get_name(self) -> str:
        """Returns test name."""
        pass

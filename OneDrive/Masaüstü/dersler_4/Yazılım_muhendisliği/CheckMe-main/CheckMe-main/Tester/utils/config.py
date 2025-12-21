"""
Configuration module for Push_Swap Logic Tester.
"""

import os
from pathlib import Path

# Paths
PROJECT_ROOT = Path(__file__).parent.parent
TESTER_DIR = PROJECT_ROOT / "Tester"
STORAGE_DIR = os.getenv("TESTER_STORAGE", str(PROJECT_ROOT / "Storage"))

# Ensure storage directory exists
os.makedirs(STORAGE_DIR, exist_ok=True)

# Push_Swap executable name
PUSH_SWAP_EXECUTABLE = "push_swap"

# Checker executables
CHECKER_NAMES = ["checker_linux", "checker_darwin", "checker_OS", "checker"]

# Performance thresholds
PERFORMANCE_THRESHOLDS = {
    100: {
        "excellent": 700,
        "good": 1500,
    },
    500: {
        "excellent": 5500,
        "good": 11500,
    }
}

# Test configuration
TEST_CONFIG = {
    "quick": {
        "test_cases": [3, 5, "edge_limits"],
        "timeout": 10,
        "description": "Quick validation test"
    },
    "full": {
        "test_cases": [3, 5, 100, 500, "edge_negative", "edge_positive", "edge_limits", "edge_mixed"],
        "timeout": 60,
        "description": "Comprehensive test suite"
    },
    "performance": {
        "test_cases": [100, 500],
        "timeout": 30,
        "description": "Performance-focused tests"
    }
}

# Valgrind settings
VALGRIND_SETTINGS = {
    "enabled": True,
    "leak_check": "full",
    "show_leak_kinds": "all",
    "track_origins": "yes",
    "verbose": False
}

# Logging
LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "standard": {
            "format": "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
        },
    },
    "handlers": {
        "default": {
            "level": "INFO",
            "class": "logging.StreamHandler",
            "formatter": "standard",
        },
    },
    "loggers": {
        "": {
            "handlers": ["default"],
            "level": "INFO",
            "propagate": True
        }
    }
}

# Error messages
ERROR_MESSAGES = {
    "executable_not_found": "Push_swap executable not found",
    "checker_not_found": "Checker utility not found",
    "compilation_failed": "Compilation failed",
    "invalid_input": "Invalid input format",
    "timeout": "Test execution timeout",
    "memory_error": "Memory allocation error",
}

# Grading thresholds
GRADING_SCALE = {
    "A": {
        "pass_rate": 100,
        "memory_safe_rate": 100,
        "description": "Excellent"
    },
    "B": {
        "pass_rate": 90,
        "memory_safe_rate": 90,
        "description": "Good"
    },
    "C": {
        "pass_rate": 80,
        "memory_safe_rate": 80,
        "description": "Acceptable"
    },
    "D": {
        "pass_rate": 70,
        "memory_safe_rate": 50,
        "description": "Needs Improvement"
    },
    "F": {
        "pass_rate": 0,
        "memory_safe_rate": 0,
        "description": "Failed"
    }
}

# Valid moves in push_swap
VALID_MOVES = [
    "sa", "sb", "ss",  # swap
    "pa", "pb",        # push
    "ra", "rb", "rr",  # rotate
    "rra", "rrb", "rrr"  # reverse rotate
]

# Print configuration on import
if __name__ == "__main__":
    print(f"Storage Directory: {STORAGE_DIR}")
    print(f"Push_Swap Executable: {PUSH_SWAP_EXECUTABLE}")
    print(f"Checker Names: {CHECKER_NAMES}")
    print(f"Performance Thresholds: {PERFORMANCE_THRESHOLDS}")

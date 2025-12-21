"""
Comprehensive test example and documentation for LogicTester.
This module demonstrates the complete testing workflow.
"""

import json
from typing import Dict, List

# Example test output structure
EXAMPLE_TEST_RESULT = {
    "input": "3 2 1 4 5",
    "test_name": "small_5",
    "number_count": 5,
    "expected": "OK",
    "output": "sa\nrra\npb\nrb\npa\n",
    "stderr": "",
    "moves": 5,
    "error": False,
    "status": "OK",
    "leak": True,  # True means no leaks (memory safe)
    "validation": {
        "validated": True,
        "status": "OK",
        "message": "OK",
        "result": "OK"
    },
    "memory_details": {
        "checked": True,
        "has_leaks": False,
        "message": "No leaks detected",
        "details": "==1234== HEAP SUMMARY:\n==1234==     in use at exit: 0 bytes in 0 blocks\n==1234==   total heap usage: 123 allocs, 123 frees, 45,678 bytes allocated\n==1234==\n==1234== All heap blocks were freed -- no leaks are possible\n"
    },
    "performance": {
        "status": "Excellent",
        "points": 5,
        "threshold": 700  # For 100 numbers
    }
}

EXAMPLE_FULL_TEST_RESPONSE = {
    "test_type": "full",
    "summary": {
        "total_tests": 8,
        "passed_tests": 7,
        "failed_tests": 1,
        "memory_safe": 7,
        "pass_rate": 87.5
    },
    "results": [
        # Multiple test results like EXAMPLE_TEST_RESULT
    ]
}

# Test scenarios documentation
TEST_SCENARIOS = {
    "quick": {
        "description": "Quick validation test (3 test cases)",
        "test_cases": ["small_3", "small_5", "edge_limits"],
        "duration": "~5-10 seconds",
        "use_case": "CI/CD pipelines, quick validation"
    },
    "full": {
        "description": "Comprehensive test suite (8 test cases)",
        "test_cases": [
            "small_3",       # 3 random numbers
            "small_5",       # 5 random numbers
            "medium_100",    # 100 random numbers
            "large_500",     # 500 random numbers
            "edge_negative", # All negative numbers
            "edge_positive", # All positive numbers
            "edge_limits",   # INT_MIN/MAX boundaries
            "edge_mixed"     # Mixed positive/negative/zero
        ],
        "duration": "~30-60 seconds",
        "use_case": "Full validation, grading"
    },
    "performance": {
        "description": "Performance-focused tests",
        "test_cases": ["perf_100", "perf_500"],
        "duration": "~10-20 seconds",
        "use_case": "Algorithm efficiency evaluation"
    }
}

# API Endpoint documentation
API_ENDPOINTS = {
    "POST /test": {
        "description": "Clone repository and run compilation tests",
        "request": {
            "repo_url": "https://github.com/user/push_swap.git"
        },
        "response": {
            "test_id": "abc12345",
            "result": {"project": "push_swap", "status": "SUCCESS"},
            "steps": [
                {"id": 1, "status": "OK", "msg": "Clone successful"},
                {"id": 2, "status": "OK", "msg": "Makefile found"},
                # ... more steps
            ]
        }
    },
    "POST /test/logic": {
        "description": "Run comprehensive logic tests",
        "request": {
            "repo_path": "/app/storage/test_abc12345",
            "test_type": "full",  # or 'quick', 'performance'
            "seed": None  # Optional: for reproducible tests
        },
        "response": {
            "test_type": "full",
            "summary": {
                "total_tests": 8,
                "passed_tests": 8,
                "failed_tests": 0,
                "memory_safe": 8,
                "pass_rate": 100.0
            },
            "results": [
                # List of test results
            ]
        }
    },
    "POST /test/custom": {
        "description": "Run a custom test with specific numbers",
        "request": {
            "repo_path": "/app/storage/test_abc12345",
            "numbers": "3 2 1 4 5",
            "test_name": "my_custom_test"
        },
        "response": {
            "test_name": "my_custom_test",
            "result": {
                "input": "3 2 1 4 5",
                "moves": 5,
                "status": "OK",
                "leak": True,
                "validation": {"status": "OK"},
                "performance": {"status": "Excellent", "points": 5}
            },
            "success": True
        }
    },
    "GET /test/generate/{count}": {
        "description": "Generate test numbers",
        "parameters": {
            "count": "Number of integers (e.g., 3, 5, 100, 500)",
            "edge_case": "Optional: negative, positive, limits, mixed, duplicates"
        },
        "response": {
            "test_type": "random_100",
            "numbers": "42 -17 89 -23 ...",
            "count": 100
        }
    },
    "GET /health": {
        "description": "Check service health",
        "response": {
            "status": "ok",
            "service": "push_swap-tester"
        }
    }
}

# Performance thresholds
PERFORMANCE_CRITERIA = {
    "100_numbers": {
        "excellent": {"limit": 700, "points": 5},
        "good": {"limit": 1500, "points": 1},
        "fail": {"limit": float('inf'), "points": 0}
    },
    "500_numbers": {
        "excellent": {"limit": 5500, "points": 5},
        "good": {"limit": 11500, "points": 1},
        "fail": {"limit": float('inf'), "points": 0}
    }
}

# Validation criteria
VALIDATION_CRITERIA = {
    "move_count": "Must be able to sort array",
    "checker_validation": "Must output 'OK' from checker utility",
    "memory_safety": "Must have no memory leaks detected by valgrind",
    "error_handling": "Must output 'Error' for invalid input",
    "edge_cases": "Must handle negative, positive, and INT_MIN/MAX values"
}

def print_documentation():
    """Print comprehensive documentation."""
    print("=" * 80)
    print("PUSH_SWAP LOGIC TESTER - API DOCUMENTATION")
    print("=" * 80)
    
    print("\n[TEST SCENARIOS]")
    for scenario, details in TEST_SCENARIOS.items():
        print(f"\n  {scenario.upper()}")
        print(f"    Description: {details['description']}")
        print(f"    Duration: {details['duration']}")
        print(f"    Test cases: {', '.join(details['test_cases'])}")
        print(f"    Use case: {details['use_case']}")
    
    print("\n\n[PERFORMANCE CRITERIA]")
    for count, criteria in PERFORMANCE_CRITERIA.items():
        print(f"\n  {count}:")
        for level, threshold in criteria.items():
            print(f"    {level}: < {threshold['limit']} moves = {threshold['points']} points")
    
    print("\n\n[VALIDATION CRITERIA]")
    for criterion, description in VALIDATION_CRITERIA.items():
        print(f"  • {criterion}: {description}")
    
    print("\n" + "=" * 80)

if __name__ == "__main__":
    print_documentation()

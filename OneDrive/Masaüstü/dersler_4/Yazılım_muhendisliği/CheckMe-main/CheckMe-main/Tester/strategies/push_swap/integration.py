"""
Integration test runner combining compilation and logic tests.
MOVED FROM: tester/utils/integration_tester.py
"""

from typing import Dict, List
from utils.compiler import Compiler
# Changed import to relative import within the strategy
from .logic import PushSwapLogicTester
from utils.number_generator import NumberGenerator


class PushSwapIntegrationTester:
    """Runs complete test pipeline: compilation -> logic tests -> performance analysis."""

    def __init__(self, repo_path: str):
        """
        Initialize integration tester.

        Args:
            repo_path: Path to cloned repository
        """
        self.repo_path = repo_path
        self.compiler = Compiler()
        # Use renamed class
        self.logic_tester = PushSwapLogicTester(repo_path)
        self.number_generator = NumberGenerator()

    def run_complete_test(self, test_type: str = "full", seed: int = None) -> Dict:
        """
        Run complete test pipeline.

        Args:
            test_type: Type of test ('quick', 'full', 'performance')
            seed: Optional seed for reproducibility

        Returns:
            Complete test results with all phases
        """
        self.number_generator = NumberGenerator(seed=seed)

        results = {
            "compilation": None,
            "logic_tests": None,
            "summary": {
                "overall_status": "PENDING",
                "total_score": 0,
                "max_score": 0
            }
        }

        # Phase 1: Compilation
        compilation_result = self.compiler.check_all(self.repo_path, "push_swap")
        results["compilation"] = {
            "status": "OK" if all(s["status"] == "OK" for s in compilation_result) else "KO",
            "details": compilation_result
        }

        if results["compilation"]["status"] == "KO":
            results["summary"]["overall_status"] = "COMPILATION_FAILED"
            return results

        # Phase 2: Logic Tests
        # test_cases = self._get_test_cases(test_type)
        # logic_results = self.logic_tester.run_test_suite(test_cases)
        logic_results = self.logic_tester.run_modular_tests(test_type)

        results["logic_tests"] = {
            "test_type": test_type,
            "total": len(logic_results),
            "passed": sum(1 for r in logic_results if r["status"] == "OK"),
            "failed": sum(1 for r in logic_results if r["status"] != "OK"),
            "memory_safe": sum(1 for r in logic_results if r["leak"] is True),
            "results": logic_results
        }

        # Calculate overall status
        pass_rate = (results["logic_tests"]["passed"] / results["logic_tests"]["total"]) * 100

        if results["logic_tests"]["failed"] == 0 and results["logic_tests"]["memory_safe"] == results["logic_tests"]["total"]:
            results["summary"]["overall_status"] = "SUCCESS"
        elif results["logic_tests"]["passed"] == 0:
            results["summary"]["overall_status"] = "COMPLETE_FAILURE"
        else:
            results["summary"]["overall_status"] = "PARTIAL_SUCCESS"

        results["summary"]["pass_rate"] = pass_rate
        results["summary"]["memory_safe_rate"] = (results["logic_tests"]["memory_safe"] / results["logic_tests"]["total"]) * 100 if results["logic_tests"]["total"] > 0 else 0

        # Calculate score from performance tests
        total_points = 0
        max_points = 0
        for result in logic_results:
            if result.get("performance"):
                perf = result["performance"]
                total_points += perf.get("points", 0)
                if result["number_count"] in [100, 500]:
                    max_points += 5

        results["summary"]["total_score"] = total_points
        results["summary"]["max_score"] = max_points

        return results

    def _get_test_cases(self, test_type: str) -> Dict[str, str]:
        """Get test cases based on type."""
        if test_type == "quick":
            return {
                "small_3": self.number_generator.generate_random_numbers(3),
                "small_5": self.number_generator.generate_random_numbers(5),
                "edge_limits": self.number_generator.generate_edge_case_numbers("limits"),
            }

        elif test_type == "full":
            return {
                "small_3": self.number_generator.generate_random_numbers(3),
                "small_5": self.number_generator.generate_random_numbers(5),
                "medium_100": self.number_generator.generate_random_numbers(100),
                "large_500": self.number_generator.generate_random_numbers(500),
                "edge_negative": self.number_generator.generate_edge_case_numbers("negative"),
                "edge_positive": self.number_generator.generate_edge_case_numbers("positive"),
                "edge_limits": self.number_generator.generate_edge_case_numbers("limits"),
                "edge_mixed": self.number_generator.generate_edge_case_numbers("mixed"),
            }

        elif test_type == "performance":
            return {
                "perf_100": self.number_generator.generate_random_numbers(100),
                "perf_500": self.number_generator.generate_random_numbers(500),
            }

        else:
            return {}

    def get_grade(self, results: Dict) -> Dict:
        """
        Calculate grade based on test results.

        Args:
            results: Complete test results

        Returns:
            Grade information
        """
        compilation = results.get("compilation", {}).get("status") == "OK"
        logic = results.get("logic_tests", {})

        if not compilation:
            return {
                "grade": "F",
                "reason": "Compilation failed",
                "points": 0,
                "max_points": 100
            }

        total_tests = logic.get("total", 0)
        passed = logic.get("passed", 0)
        memory_safe = logic.get("memory_safe", 0)
        score = results.get("summary", {}).get("total_score", 0)
        max_score = results.get("summary", {}).get("max_score", 0)

        # Calculate base grade
        pass_rate = (passed / total_tests * 100) if total_tests > 0 else 0

        if pass_rate == 100 and memory_safe == total_tests:
            if max_score > 0 and (score / max_score * 100) >= 80:
                grade = "A"
            elif pass_rate >= 90:
                grade = "B"
            else:
                grade = "C"
        elif pass_rate >= 80:
            grade = "D"
        else:
            grade = "F"

        return {
            "grade": grade,
            "pass_rate": pass_rate,
            "memory_safe_rate": logic.get("memory_safe_rate", 0),
            "performance_score": f"{score}/{max_score}" if max_score > 0 else "N/A",
            "reason": self._grade_reason(grade, pass_rate, memory_safe, total_tests)
        }

    def _grade_reason(self, grade: str, pass_rate: float, memory_safe: int, total: int) -> str:
        """Generate human-readable grade reason."""
        reasons = {
            "A": f"Excellent! {pass_rate:.1f}% tests passed, {memory_safe}/{total} memory safe",
            "B": f"Good! {pass_rate:.1f}% tests passed, {memory_safe}/{total} memory safe",
            "C": f"Acceptable. {pass_rate:.1f}% tests passed, {memory_safe}/{total} memory safe",
            "D": f"Needs improvement. {pass_rate:.1f}% tests passed, {memory_safe}/{total} memory safe",
            "F": f"Failed. {pass_rate:.1f}% tests passed, {memory_safe}/{total} memory safe"
        }
        return reasons.get(grade, "Unknown result")

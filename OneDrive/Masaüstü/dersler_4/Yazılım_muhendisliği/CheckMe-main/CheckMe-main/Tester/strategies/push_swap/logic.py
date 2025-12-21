"""
Logic Tester for push_swap project.
Handles execution, validation, and performance checking of push_swap.
MOVED FROM: tester/utils/logic_tester.py
"""

import subprocess
import os
import shutil
from typing import Dict, List, Optional, Tuple
from .tests.base import BaseTest
from .tests.errors import DuplicateTest, MaxMinTest, OverflowTest, InvalidInputTest, ErrorManagementTest
from .tests.sorting import IdentityTest, ReverseTest, RandomTest, SortingTest
from .tests.performance import PerformanceTest

class PushSwapLogicTester:
    """Tests push_swap logic including execution, validation, and performance."""

    def __init__(self, repo_path: str):
        """
        Initialize the logic tester.

        Args:
            repo_path: Path to the cloned push_swap repository
        """
        self.repo_path = repo_path
        self.push_swap_path = os.path.join(repo_path, "push_swap")
        self.checker_path = None
        self._locate_checker()

    def _locate_checker(self):
        """Locate the checker executable in the system or repo."""
        # Try common locations
        common_paths = [
            # In repo root or subdirectories
            os.path.join(self.repo_path, "checker_linux"),
            os.path.join(self.repo_path, "checker_darwin"),
            os.path.join(self.repo_path, "checker_OS"),
            os.path.join(self.repo_path, "checker"),
            # In subdirectories
            os.path.join(self.repo_path, "checkers", "checker_linux"),
            os.path.join(self.repo_path, "checkers", "checker_darwin"),
            os.path.join(self.repo_path, "checkers", "checker_OS"),
            # In system paths
            "/usr/local/bin/checker_linux",
            "/usr/bin/checker_linux",
            shutil.which("checker_linux") if shutil.which("checker_linux") else None,
        ]

        for path in common_paths:
            if path and os.path.isfile(path):
                if os.access(path, os.X_OK):
                    self.checker_path = path
                    return
                else:
                    # Try to make it executable
                    try:
                        os.chmod(path, 0o755)
                        self.checker_path = path
                        return
                    except:
                        pass

        # If not found, log a warning but continue
        self.checker_path = None

    def _run_command(self, cmd: List[str], cwd: str = None) -> Tuple[int, str, str]:
        """
        Run a shell command and return result.

        Args:
            cmd: Command as list of strings
            cwd: Working directory (default: self.repo_path)

        Returns:
            Tuple of (returncode, stdout, stderr)
        """
        if cwd is None:
            cwd = self.repo_path

        try:
            result = subprocess.run(
                cmd,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=10
            )
            return result.returncode, result.stdout, result.stderr
        except subprocess.TimeoutExpired:
            return -1, "", "Command timeout"
        except Exception as e:
            return -1, "", str(e)

    def _count_moves(self, output: str) -> int:
        """
        Count the number of moves from push_swap output.

        Args:
            output: Output from push_swap (list of moves)

        Returns:
            Number of moves
        """
        if not output:
            return 0

        lines = [line.strip() for line in output.strip().split('\n') if line.strip()]
        valid_moves = ['sa', 'sb', 'ss', 'pa', 'pb', 'ra', 'rb', 'rr', 'rra', 'rrb', 'rrr']

        count = 0
        for line in lines:
            if line in valid_moves:
                count += 1

        return count

    def _check_error(self, output: str) -> bool:
        """
        Check if output indicates an error.

        Args:
            output: Output from push_swap

        Returns:
            True if error, False otherwise
        """
        error_indicators = ["Error", "error", "ERROR", "invalid", "Invalid"]
        return any(indicator in output for indicator in error_indicators)

    def execute_push_swap(self, numbers: str) -> Dict:
        """
        Execute push_swap with given numbers.

        Args:
            numbers: Space-separated numbers

        Returns:
            Dictionary with execution results
        """
        if not os.path.isfile(self.push_swap_path) or not os.access(self.push_swap_path, os.X_OK):
            return {
                "success": False,
                "error": "push_swap executable not found",
                "moves": 0,
                "output": ""
            }

        returncode, stdout, stderr = self._run_command([self.push_swap_path] + numbers.split())

        result = {
            "success": returncode == 0 and not self._check_error(stdout + stderr),
            "returncode": returncode,
            "output": stdout,
            "stderr": stderr,
            "moves": self._count_moves(stdout),
            "error": self._check_error(stdout + stderr)
        }

        return result

    def validate_with_checker(self, numbers: str, output: str) -> Dict:
        """
        Validate push_swap output using checker.

        Args:
            numbers: Space-separated numbers
            output: Output from push_swap (moves)

        Returns:
            Dictionary with validation result
        """
        if not self.checker_path:
            return {
                "validated": False,
                "status": "SKIP",
                "message": "Checker not found",
                "result": None
            }

        # Pipe push_swap output to checker
        try:
            # Create push_swap command output
            push_swap_proc = subprocess.Popen(
                [self.push_swap_path] + numbers.split(),
                stdout=subprocess.PIPE,
                cwd=self.repo_path,
                text=True
            )

            # Pipe to checker
            checker_proc = subprocess.Popen(
                [self.checker_path] + numbers.split(),
                stdin=push_swap_proc.stdout,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.repo_path,
                text=True
            )

            push_swap_proc.stdout.close()
            stdout, stderr = checker_proc.communicate(timeout=10)

            result = stdout.strip()

            # Debugging: If result is empty, check stderr
            if not result:
                if stderr:
                    result = f"Error: {stderr.strip()}"
                else:
                    result = f"Empty output (Exit: {checker_proc.returncode})"

            return {
                "validated": True,
                "status": "OK" if result == "OK" else "KO",
                "message": result,
                "result": result
            }
        except subprocess.TimeoutExpired:
             return {
                "validated": False,
                "status": "KO",
                "message": "Checker Timeout",
                "result": None
            }
        except Exception as e:
            return {
                "validated": False,
                "status": "ERROR",
                "message": f"Exception: {str(e)}",
                "result": None
            }

    def check_memory_leaks(self, numbers: str) -> Dict:
        """
        Check for memory leaks using valgrind.

        Args:
            numbers: Space-separated numbers

        Returns:
            Dictionary with memory check result
        """
        # Check if valgrind is available
        valgrind_check = self._run_command(["which", "valgrind"])
        if valgrind_check[0] != 0:
            return {
                "checked": False,
                "has_leaks": None,
                "message": "Valgrind not available",
                "details": ""
            }

        cmd = ["valgrind", "--leak-check=full", "--show-leak-kinds=all", self.push_swap_path] + numbers.split()

        returncode, stdout, stderr = self._run_command(cmd)

        # Check for the success message
        leak_summary = stderr if stderr else stdout
        no_leaks = "All heap blocks were freed -- no leaks are possible" in leak_summary

        return {
            "checked": True,
            "has_leaks": not no_leaks,
            "message": "No leaks detected" if no_leaks else "Potential leaks detected",
            "details": leak_summary
        }

    def evaluate_performance(self, moves: int, number_count: int) -> Dict:
        """
        Evaluate performance based on move count and number count.

        Args:
            moves: number of moves execution
            number_count: Number of input numbers

        Returns:
            Dictionary with performance evaluation
        """
        if number_count == 100:
            if moves < 700:
                return {"status": "Excellent", "points": 5, "threshold": 700}
            elif moves < 1500:
                return {"status": "Good", "points": 1, "threshold": 1500}
            else:
                return {"status": "Fail", "points": 0, "threshold": 1500}

        elif number_count == 500:
            if moves < 5500:
                return {"status": "Excellent", "points": 5, "threshold": 5500}
            elif moves < 11500:
                return {"status": "Good", "points": 1, "threshold": 11500}
            else:
                return {"status": "Fail", "points": 0, "threshold": 11500}

        else:
            return {"status": "N/A", "points": 0, "threshold": None}

    def run_single_test(self, numbers: str, test_name: str = "unnamed") -> Dict:
        """
        Run a single comprehensive test case.

        Args:
            numbers: Space-separated numbers
            test_name: Name of the test

        Returns:
            Dictionary with complete test results
        """
        number_count = len(numbers.split())

        # Execute push_swap
        exec_result = self.execute_push_swap(numbers)

        # Prepare base result
        result = {
            "input": numbers,
            "test_name": test_name,
            "number_count": number_count,
            "expected": "OK",
            "output": exec_result.get("output", ""),
            "stderr": exec_result.get("stderr", ""),
            "moves": exec_result.get("moves", 0),
            "error": exec_result.get("error", False),
            "status": "OK" if exec_result.get("success") else "KO",
            "leak": None,
            "validation": None,
            "performance": None
        }

        # Skip further tests if push_swap itself failed
        if not exec_result.get("success"):
            return result

        # Validate with checker
        validation_result = self.validate_with_checker(numbers, exec_result.get("output", ""))
        result["validation"] = validation_result
        if validation_result.get("status") != "OK":
            result["status"] = validation_result.get("status", "KO")

        # Check memory leaks
        memory_result = self.check_memory_leaks(numbers)
        result["leak"] = not memory_result.get("has_leaks", True)
        result["memory_details"] = memory_result

        # Evaluate performance (for larger test cases)
        perf_result = self.evaluate_performance(result["moves"], number_count)
        result["performance"] = perf_result

        return result

    def run_modular_tests(self, test_type: str = "full") -> List[Dict]:
        """
        Run tests using the modular test suite.

        Args:
            test_type: Type of test ('quick', 'full', 'performance')

        Returns:
            List of test results
        """
        tests: List[BaseTest] = []

        # Register tests based on type
        if test_type in ["quick", "full"]:
            tests.extend([
                IdentityTest(),
                ReverseTest(),
                RandomTest(3),
                RandomTest(5),
                DuplicateTest(),
                MaxMinTest(),
                OverflowTest(),
                InvalidInputTest()
            ])

        if test_type == "full":
            tests.extend([
                RandomTest(100),
                RandomTest(500),
                PerformanceTest(100, 700),
                PerformanceTest(500, 5500)
            ])

        if test_type == "performance":
            tests.extend([
                PerformanceTest(100, 700),
                PerformanceTest(500, 5500)
            ])

        results = []
        for test in tests:
            args = test.generate_args()
            args_str = " ".join(args)

            # Execute
            exec_result = self.execute_push_swap(args_str)

            # Validate
            is_success, msg, extra = test.validate(
                exec_result["output"],
                exec_result["stderr"],
                exec_result["returncode"]
            )

            status = "OK" if is_success else "KO"
            validation_details = {"message": msg}

            # Run checker for non-Error tests if they passed basic validation
            if is_success and not isinstance(test, ErrorManagementTest):
                checker_res = self.validate_with_checker(args_str, exec_result["output"])
                if checker_res["status"] != "OK":
                    status = "KO"
                    msg = f"Checker failed: {checker_res['message']}"
                validation_details.update(checker_res)

            # Memory check
            memory_res = self.check_memory_leaks(args_str)

            # Construct result dict
            res_dict = {
                "input": args_str,
                "test_name": test.get_name(),
                "number_count": len(args),
                "expected": "Error" if isinstance(test, ErrorManagementTest) else "OK",
                "output": exec_result["output"],
                "stderr": exec_result["stderr"],
                "moves": exec_result["moves"],
                "error": exec_result["error"],
                "status": status,
                "leak": not memory_res["has_leaks"],
                "memory_details": memory_res,
                "validation": validation_details,
                "performance": None
            }

            # If PerformanceTest, use the score from extra
            if isinstance(test, PerformanceTest) and extra:
                res_dict["performance"] = {
                    "status": "OK" if status == "OK" else "Fail",
                    "points": 5 if status == "OK" else 0,
                    "threshold": test.limit
                }
            # For RandomTest(100/500), we also want performance evaluation
            elif isinstance(test, RandomTest) and test.count in [100, 500]:
                 res_dict["performance"] = self.evaluate_performance(exec_result["moves"], test.count)

            results.append(res_dict)

        return results

    def run_test_suite(self, test_cases: Dict[str, str]) -> List[Dict]:
        """
        Run multiple test cases.

        Args:
            test_cases: Dictionary of test_name -> numbers

        Returns:
            List of test results
        """
        results = []

        for test_name, numbers in test_cases.items():
            result = self.run_single_test(numbers, test_name)
            results.append(result)

        return results

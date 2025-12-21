#!/usr/bin/env python3
"""
Test runner script for push_swap logic testing.
Can be used for manual testing or CI/CD integration.
"""

import sys
import json
import argparse
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from strategies.push_swap.integration import PushSwapIntegrationTester
from utils.number_generator import NumberGenerator
from strategies.push_swap.logic import PushSwapLogicTester


def print_section(title: str):
    """Print a formatted section header."""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}\n")


def print_test_result(result: dict, name: str):
    """Print a formatted test result."""
    print(f"Test: {name}")
    print(f"  Status: {result['status']}")
    print(f"  Moves: {result['moves']}")
    if result.get('leak') is not None:
        print(f"  Memory Safe: {'Yes' if result['leak'] else 'No'}")
    if result.get('validation'):
        print(f"  Validation: {result['validation'].get('status', 'N/A')}")
    if result.get('performance'):
        print(f"  Performance: {result['performance']['status']} ({result['performance'].get('points', 0)} points)")
    print()


def test_number_generator():
    """Test the number generator."""
    print_section("Testing Number Generator")
    
    gen = NumberGenerator(seed=42)
    
    test_cases = {
        "3 random": gen.generate_random_numbers(3),
        "5 random": gen.generate_random_numbers(5),
        "100 random": gen.generate_random_numbers(100),
        "500 random": gen.generate_random_numbers(500),
        "edge_negative": gen.generate_edge_case_numbers("negative"),
        "edge_positive": gen.generate_edge_case_numbers("positive"),
        "edge_limits": gen.generate_edge_case_numbers("limits"),
        "edge_mixed": gen.generate_edge_case_numbers("mixed"),
    }
    
    for name, numbers in test_cases.items():
        count = len(numbers.split())
        print(f"✓ {name}: {count} numbers generated")
    
    print(f"\nTotal test cases generated: {len(test_cases)}")


def test_single_repo(repo_path: str, test_type: str = "quick"):
    """Test a single repository."""
    print_section(f"Testing Repository: {repo_path}")
    
    try:
        tester = PushSwapIntegrationTester(repo_path)
        results = tester.run_complete_test(test_type=test_type, seed=42)
        
        # Print compilation results
        comp_status = results.get("compilation", {}).get("status", "UNKNOWN")
        print(f"Compilation: {comp_status}")
        
        if comp_status == "KO":
            print("\n❌ Compilation failed. Skipping logic tests.")
            return results
        
        # Print logic test results
        logic = results.get("logic_tests", {})
        print(f"\nLogic Tests ({test_type}):")
        print(f"  Total: {logic.get('total', 0)}")
        print(f"  Passed: {logic.get('passed', 0)}")
        print(f"  Failed: {logic.get('failed', 0)}")
        print(f"  Memory Safe: {logic.get('memory_safe', 0)}")
        print(f"  Pass Rate: {results['summary'].get('pass_rate', 0):.1f}%")
        
        # Print grade
        grade = results.get("grade", {})
        print(f"\n📊 Grade: {grade.get('grade', 'N/A')}")
        print(f"   Reason: {grade.get('reason', 'N/A')}")
        
        # Print detailed results if requested
        if test_type == "quick":
            print(f"\nDetailed Results:")
            for result in logic.get("results", []):
                print_test_result(result, result.get("test_name", "unnamed"))
        
        return results
    
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None


def export_results(results: dict, output_file: str):
    """Export test results to JSON file."""
    try:
        with open(output_file, "w") as f:
            json.dump(results, f, indent=2)
        print(f"✓ Results exported to {output_file}")
    except Exception as e:
        print(f"❌ Failed to export results: {str(e)}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Push_Swap Logic Tester - Manual test runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Test number generator
  python test_runner.py --test-generator
  
  # Test a repository with quick validation
  python test_runner.py --repo /path/to/push_swap --type quick
  
  # Test with full suite and export results
  python test_runner.py --repo /path/to/push_swap --type full --output results.json
  
  # Test with specific seed for reproducibility
  python test_runner.py --repo /path/to/push_swap --seed 12345
        """
    )
    
    parser.add_argument(
        "--test-generator",
        action="store_true",
        help="Test the number generator"
    )
    
    parser.add_argument(
        "--repo",
        type=str,
        help="Path to push_swap repository"
    )
    
    parser.add_argument(
        "--type",
        choices=["quick", "full", "performance"],
        default="quick",
        help="Test type (default: quick)"
    )
    
    parser.add_argument(
        "--seed",
        type=int,
        default=None,
        help="Random seed for reproducibility"
    )
    
    parser.add_argument(
        "--output",
        type=str,
        help="Export results to JSON file"
    )
    
    parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print verbose output"
    )
    
    args = parser.parse_args()
    
    # Test number generator if requested
    if args.test_generator:
        test_number_generator()
        return 0
    
    # Test repository if path provided
    if args.repo:
        results = test_single_repo(args.repo, test_type=args.type)
        
        if results and args.output:
            export_results(results, args.output)
        
        return 0 if results and results.get("grade", {}).get("grade") != "F" else 1
    
    # Show help if no arguments
    if not sys.argv[1:]:
        parser.print_help()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

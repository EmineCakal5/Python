"""
Random number generator for push_swap testing.
Generates unique random numbers for various test scenarios.
"""

import random
from typing import List, Tuple
import sys

class NumberGenerator:
    """Generates random unique numbers for push_swap testing."""
    
    def __init__(self, seed: int = None):
        """
        Initialize the number generator.
        
        Args:
            seed: Optional seed for reproducibility
        """
        if seed is not None:
            random.seed(seed)
    
    def generate_random_numbers(self, count: int) -> str:
        """
        Generate 'count' unique random numbers as a space-separated string.
        
        Args:
            count: Number of unique integers to generate
            
        Returns:
            Space-separated string of unique integers
        """
        if count <= 0:
            return ""
        
        # Use a safe range to ensure uniqueness
        min_val = -2147483648  # INT_MIN
        max_val = 2147483647   # INT_MAX
        range_size = max_val - min_val + 1
        
        if count > range_size:
            raise ValueError(f"Cannot generate {count} unique numbers in valid range")
        
        numbers = random.sample(range(min_val, max_val + 1), count)
        return " ".join(str(n) for n in numbers)
    
    def generate_edge_case_numbers(self, scenario: str = "mixed") -> str:
        """
        Generate edge case numbers based on scenario.
        
        Args:
            scenario: Type of edge case ('negative', 'positive', 'mixed', 'limits')
            
        Returns:
            Space-separated string of test numbers
        """
        if scenario == "negative":
            # All negative numbers
            numbers = random.sample(range(-1000, 0), 5)
            return " ".join(str(n) for n in numbers)
        
        elif scenario == "positive":
            # All positive numbers
            numbers = random.sample(range(1, 1001), 5)
            return " ".join(str(n) for n in numbers)
        
        elif scenario == "limits":
            # Testing INT_MIN and INT_MAX boundaries
            numbers = [
                -2147483648,  # INT_MIN
                -2147483647,
                0,
                2147483646,
                2147483647   # INT_MAX
            ]
            return " ".join(str(n) for n in numbers)
        
        elif scenario == "mixed":
            # Mix of negative, positive, and zero
            neg = random.sample(range(-100, 0), 2)
            pos = random.sample(range(1, 101), 2)
            zero = [0]
            numbers = neg + [zero[0]] + pos
            return " ".join(str(n) for n in numbers)
        
        elif scenario == "zeros":
            # Edge case: only zeros (should fail - duplicates)
            return "0 0 0"
        
        elif scenario == "duplicates":
            # Edge case: duplicate numbers (should fail)
            return "5 10 5 15 20"
        
        else:
            raise ValueError(f"Unknown scenario: {scenario}")
    
    def generate_test_cases(self) -> dict:
        """
        Generate a comprehensive set of test cases.
        
        Returns:
            Dictionary with test cases of different sizes
        """
        return {
            "small": self.generate_random_numbers(3),
            "medium": self.generate_random_numbers(5),
            "large": self.generate_random_numbers(100),
            "extra_large": self.generate_random_numbers(500),
            "edge_negative": self.generate_edge_case_numbers("negative"),
            "edge_positive": self.generate_edge_case_numbers("positive"),
            "edge_limits": self.generate_edge_case_numbers("limits"),
            "edge_mixed": self.generate_edge_case_numbers("mixed"),
            "error_duplicates": self.generate_edge_case_numbers("duplicates"),
        }


# Convenience functions
def generate_numbers(count: int, seed: int = None) -> str:
    """
    Generate count unique random numbers as a string.
    
    Args:
        count: Number of unique integers to generate
        seed: Optional seed for reproducibility
        
    Returns:
        Space-separated string of unique integers
    """
    gen = NumberGenerator(seed=seed)
    return gen.generate_random_numbers(count)


def generate_edge_case(scenario: str, seed: int = None) -> str:
    """
    Generate edge case numbers.
    
    Args:
        scenario: Type of edge case test
        seed: Optional seed for reproducibility
        
    Returns:
        Space-separated string of test numbers
    """
    gen = NumberGenerator(seed=seed)
    return gen.generate_edge_case_numbers(scenario)

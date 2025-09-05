#!/usr/bin/env python3
"""
Test Runner

Comprehensive test runner for the RocketReach Python SDK.
"""

import sys
import os
import subprocess
import time
from typing import List, Dict, Any

# Add the src directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))


class TestRunner:
    """Test runner for the RocketReach Python SDK."""
    
    def __init__(self):
        self.test_categories = [
            "unit",
            "integration", 
            "e2e",
            "live"
        ]
        self.results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
    
    def run_tests(self, category: str = None, verbose: bool = True) -> Dict[str, Any]:
        """
        Run tests for a specific category or all categories.
        
        Args:
            category: Test category to run (unit, integration, e2e, live)
            verbose: Whether to show verbose output
            
        Returns:
            Dict containing test results
        """
        if category:
            categories = [category]
        else:
            categories = self.test_categories
        
        print("=" * 60)
        print("RocketReach Python SDK Test Runner")
        print("=" * 60)
        print()
        
        for cat in categories:
            print(f"Running {cat} tests...")
            result = self._run_category_tests(cat, verbose)
            self.results[cat] = result
            
            if result['success']:
                print(f"✅ {cat} tests passed: {result['passed']}/{result['total']}")
            else:
                print(f"❌ {cat} tests failed: {result['failed']}/{result['total']}")
            
            self.total_tests += result['total']
            self.passed_tests += result['passed']
            self.failed_tests += result['failed']
            print()
        
        self._print_summary()
        return self.results
    
    def _run_category_tests(self, category: str, verbose: bool) -> Dict[str, Any]:
        """Run tests for a specific category."""
        test_dir = f"tests/{category}"
        
        if not os.path.exists(test_dir):
            return {
                'success': True,
                'total': 0,
                'passed': 0,
                'failed': 0,
                'message': f"No {category} tests found"
            }
        
        cmd = [
            sys.executable, "-m", "pytest",
            test_dir,
            "-v" if verbose else "",
            "--tb=short",
            "--cov=rocketreach" if category == "unit" else "",
            "--cov-report=term-missing" if category == "unit" else "",
            "--cov-fail-under=100" if category == "unit" else "",
        ]
        
        # Remove empty strings
        cmd = [arg for arg in cmd if arg]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )
            
            # Parse pytest output to get test counts
            passed = 0
            failed = 0
            total = 0
            
            if result.returncode == 0:
                # Count passed tests
                for line in result.stdout.split('\n'):
                    if ' PASSED ' in line:
                        passed += 1
                    elif ' FAILED ' in line:
                        failed += 1
                total = passed + failed
                success = failed == 0
            else:
                # Count failed tests
                for line in result.stdout.split('\n'):
                    if ' FAILED ' in line:
                        failed += 1
                    elif ' PASSED ' in line:
                        passed += 1
                total = passed + failed
                success = False
            
            return {
                'success': success,
                'total': total,
                'passed': passed,
                'failed': failed,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }
            
        except subprocess.TimeoutExpired:
            return {
                'success': False,
                'total': 0,
                'passed': 0,
                'failed': 0,
                'message': f"{category} tests timed out"
            }
        except Exception as e:
            return {
                'success': False,
                'total': 0,
                'passed': 0,
                'failed': 0,
                'message': f"Error running {category} tests: {str(e)}"
            }
    
    def _print_summary(self):
        """Print test summary."""
        print("=" * 60)
        print("TEST SUMMARY")
        print("=" * 60)
        print(f"Total Tests: {self.total_tests}")
        print(f"Passed: {self.passed_tests}")
        print(f"Failed: {self.failed_tests}")
        
        if self.total_tests > 0:
            success_rate = (self.passed_tests / self.total_tests) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        
        print()
        
        if self.failed_tests == 0:
            print("🎉 ALL TESTS PASSED!")
            print("✅ The Python SDK is ready for production use.")
        else:
            print("⚠️  Some tests failed. Please review the output above.")
        
        print("=" * 60)
    
    def run_loop(self, max_iterations: int = 10) -> bool:
        """
        Run tests in a loop until all pass or max iterations reached.
        
        Args:
            max_iterations: Maximum number of iterations
            
        Returns:
            True if all tests pass, False otherwise
        """
        print("Starting test loop...")
        print(f"Maximum iterations: {max_iterations}")
        print()
        
        for iteration in range(1, max_iterations + 1):
            print(f"Iteration {iteration}/{max_iterations}")
            print("-" * 40)
            
            results = self.run_tests(verbose=False)
            
            if self.failed_tests == 0:
                print(f"\n🎉 All tests passed after {iteration} iteration(s)!")
                return True
            
            print(f"\n⚠️  {self.failed_tests} tests failed. Retrying...")
            print()
            
            # Reset counters for next iteration
            self.total_tests = 0
            self.passed_tests = 0
            self.failed_tests = 0
        
        print(f"\n❌ Tests failed after {max_iterations} iterations.")
        return False


def main():
    """Main function."""
    import argparse
    
    parser = argparse.ArgumentParser(description="RocketReach Python SDK Test Runner")
    parser.add_argument("--category", choices=["unit", "integration", "e2e", "live"], 
                       help="Test category to run")
    parser.add_argument("--loop", action="store_true", 
                       help="Run tests in a loop until all pass")
    parser.add_argument("--max-iterations", type=int, default=10,
                       help="Maximum iterations for loop mode")
    parser.add_argument("--verbose", action="store_true",
                       help="Verbose output")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.loop:
        success = runner.run_loop(args.max_iterations)
        sys.exit(0 if success else 1)
    else:
        results = runner.run_tests(args.category, args.verbose)
        
        # Exit with error code if any tests failed
        if runner.failed_tests > 0:
            sys.exit(1)
        else:
            sys.exit(0)


if __name__ == "__main__":
    main()

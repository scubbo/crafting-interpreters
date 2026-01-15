#!/usr/bin/env python3
"""
Test harness for lox interpreter implementations.

Usage:
    python run_tests.py [test_directory]

Test files are Python modules that define test cases. Each test case specifies
a .lox file to run and assertions to make against the output.
"""

import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Callable


@dataclass
class ExecutionResult:
    """Result of running a lox file through the interpreter."""
    stdout: str
    stderr: str
    exit_code: int


@dataclass
class TestCase:
    """A single test case."""
    name: str
    lox_file: Path
    assertions: Callable[[ExecutionResult], None]


class LoxRunner:
    """Runs lox files through an interpreter."""

    def __init__(self, interpreter_cmd: list[str]):
        self.interpreter_cmd = interpreter_cmd

    def run(self, lox_file: Path) -> ExecutionResult:
        """Execute a lox file and capture the result."""
        result = subprocess.run(
            self.interpreter_cmd + [str(lox_file)],
            capture_output=True,
            text=True
        )
        return ExecutionResult(
            stdout=result.stdout,
            stderr=result.stderr,
            exit_code=result.returncode
        )


class TestHarness:
    """Runs test cases and reports results."""

    def __init__(self, runner: LoxRunner):
        self.runner = runner
        self.passed = 0
        self.failed = 0
        self.failures: list[tuple[str, str]] = []

    def run_test(self, test: TestCase) -> bool:
        """Run a single test case. Returns True if passed."""
        result = self.runner.run(test.lox_file)
        try:
            test.assertions(result)
            self.passed += 1
            print(f"  PASS: {test.name}")
            return True
        except AssertionError as e:
            self.failed += 1
            self.failures.append((test.name, str(e)))
            print(f"  FAIL: {test.name}")
            print(f"        {e}")
            return False

    def run_tests(self, tests: list[TestCase]) -> bool:
        """Run all test cases. Returns True if all passed."""
        for test in tests:
            self.run_test(test)
        return self.failed == 0

    def summary(self) -> str:
        """Return a summary of test results."""
        total = self.passed + self.failed
        return f"\n{self.passed}/{total} tests passed"


def main():
    # Default interpreter path - can be overridden
    project_root = Path(__file__).parent.parent
    jlox_jar = project_root / "jlox" / "src" / "main" / "java" / "target" / "lox-1.0-SNAPSHOT.jar"

    runner = LoxRunner(["java", "-jar", str(jlox_jar)])
    harness = TestHarness(runner)

    # Import and run tests from test modules
    # For now, just run the example tests
    from example_tests import TESTS

    print("Running tests...")
    harness.run_tests(TESTS)
    print(harness.summary())

    sys.exit(0 if harness.failed == 0 else 1)


if __name__ == "__main__":
    main()

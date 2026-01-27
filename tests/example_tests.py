"""
Example test cases demonstrating the test harness.
"""

from pathlib import Path
from run_tests import TestCase, ExecutionResult

LOX_FILES = Path(__file__).parent / "lox_files"


def test_hello(result: ExecutionResult):
    assert result.exit_code == 0, f"Expected exit code 0, got {result.exit_code}"
    assert "hello world" in result.stdout, f"Expected 'hello world' in output, got: {result.stdout}"


def test_arithmetic(result: ExecutionResult):
    assert result.exit_code == 0, f"Expected exit code 0, got {result.exit_code}"
    assert "3" in result.stdout, "Expected 3 (1+2) in output"
    assert "7" in result.stdout, "Expected 7 (10-3) in output"
    assert "6" in result.stdout, "Expected 6 (2*3) in output"

def test_variable_declaration(result: ExecutionResult):
    assert result.exit_code == 0, f"Expected exit code 0, got {result.exit_code}"
    assert result.stdout.strip() == "4", f"Expected output to be `4`, was {result.stdout}"

def test_variables_and_scope(result: ExecutionResult):
    output = result.stdout.strip()
    expected = '''inner a
outer b
global c
outer a
outer b
global c
global a
global b
global c'''
    assert output == expected, f"Expected {expected} but got {output}"

def parse_test_case(file_path: Path) -> TestCase:
    file_name = file_path.name
    with file_path.open() as r:
        name = r.readlines()[0].replace('// Name: ', '')
    return TestCase(
        name=name,
        lox_file=file_path,
        assertions=globals()[f'test_{file_name.replace(".lox", "")}']
    )

TESTS = map(parse_test_case, Path(LOX_FILES).iterdir())

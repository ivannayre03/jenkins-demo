"""Tests for the Jenkins Demo Calculator (run by the Jenkins 'Test' stage)."""

from app import add, subtract, multiply, divide, calculate

passed = 0


def check(name, actual, expected):
    global passed
    assert actual == expected, f"FAIL {name}: expected {expected}, got {actual}"
    print(f"  PASS  {name}")
    passed += 1


def check_error(name, func, *args):
    global passed
    try:
        func(*args)
    except ValueError:
        print(f"  PASS  {name}")
        passed += 1
        return
    raise AssertionError(f"FAIL {name}: expected ValueError")


print("Running tests...")

check("add", add(2, 3), 5)
check("subtract", subtract(10, 4), 6)
check("multiply", multiply(6, 7), 42)
check("divide", divide(9, 3), 3)
check("calculate with text input", calculate("2", "3", "+"), 5)
check("calculate decimals", calculate("1.5", "2", "×"), 3)
check_error("divide by zero is rejected", divide, 1, 0)
check_error("non-number input is rejected", calculate, "abc", "1", "+")

print(f"All tests passed ({passed} tests)")

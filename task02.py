"""
Given a cell with "it's a fib sequence" from slideshow,
    please write function "check_fib", which accepts a Sequence of integers, and
    returns if the given sequence is a Fibonacci sequence

We guarantee, that the given sequence contain >= 0 integers inside.

"""
from collections.abc import Sequence


def check_fibonacci(data: Sequence) -> bool:
    if len(data) < 2: return False

    for i in range(2, len(data)):
        if data[i] != data[i - 1] + data[i - 2]: return False

    return True






print(check_fibonacci([0, 1, 1, 2, 3, 5]))
print(check_fibonacci([0, 1, 1, 2, 4, 5]))
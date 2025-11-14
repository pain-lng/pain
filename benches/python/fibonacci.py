#!/usr/bin/env python3
"""Fibonacci benchmark for Python"""

def fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

def main():
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
    result = fib(n)
    print(result)

if __name__ == "__main__":
    main()


#!/usr/bin/env python3
"""Factorial benchmark for Python"""

def fact(n: int) -> int:
    if n <= 1:
        return 1
    return n * fact(n - 1)

def main():
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 15
    result = fact(n)
    print(result)

if __name__ == "__main__":
    main()


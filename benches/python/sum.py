#!/usr/bin/env python3
"""Sum benchmark for Python"""

def sum_n(n: int) -> int:
    result = 0
    i = 0
    while i <= n:
        result = result + i
        i = i + 1
    return result

def main():
    import sys
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 10000
    result = sum_n(n)
    print(result)

if __name__ == "__main__":
    main()


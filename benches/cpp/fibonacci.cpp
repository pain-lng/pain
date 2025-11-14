// Fibonacci benchmark for C++

#include <iostream>
#include <cstdlib>
#include <cstdint>

int64_t fib(int64_t n) {
    if (n <= 1) {
        return n;
    }
    return fib(n - 1) + fib(n - 2);
}

int main(int argc, char* argv[]) {
    int64_t n = argc > 1 ? std::atoll(argv[1]) : 20;
    int64_t result = fib(n);
    std::cout << result << std::endl;
    return 0;
}


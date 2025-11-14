// Factorial benchmark for C++

#include <iostream>
#include <cstdlib>
#include <cstdint>

int64_t fact(int64_t n) {
    if (n <= 1) {
        return 1;
    }
    return n * fact(n - 1);
}

int main(int argc, char* argv[]) {
    int64_t n = argc > 1 ? std::atoll(argv[1]) : 15;
    int64_t result = fact(n);
    std::cout << result << std::endl;
    return 0;
}


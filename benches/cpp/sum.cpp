// Sum benchmark for C++

#include <iostream>
#include <cstdlib>
#include <cstdint>

int64_t sum_n(int64_t n) {
    int64_t result = 0;
    int64_t i = 0;
    while (i <= n) {
        result = result + i;
        i = i + 1;
    }
    return result;
}

int main(int argc, char* argv[]) {
    int64_t n = argc > 1 ? std::atoll(argv[1]) : 10000;
    int64_t result = sum_n(n);
    std::cout << result << std::endl;
    return 0;
}


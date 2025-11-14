# Pain Benchmarks

Benchmark suite for the Pain programming language.

## Running Benchmarks

### Criterion Benchmarks (Detailed Analysis)

```bash
# Run all benchmarks
cargo bench

# Run specific benchmark
cargo bench --bench fibonacci
cargo bench --bench sum
cargo bench --bench factorial
```

Results are saved in `target/criterion/` directory. Open `target/criterion/*/index.html` in a browser to view detailed reports.

### Cross-Language Comparison

Compare Pain performance with Python, Rust, and C++:

```bash
# Compare all benchmarks (default: 10 iterations, 3 warmup)
python benches/compare.py all

# Compare with custom iterations and warmup
python benches/compare.py all 20 5

# Compare specific benchmark
python benches/compare.py fibonacci 10 3
python benches/compare.py factorial 10 3
python benches/compare.py sum 10 3
```

**Prerequisites:**
- Python 3.x
- Rust toolchain (for Rust benchmarks)
- C++ compiler (optional, for C++ benchmarks):
  - **Windows**: Install MinGW-w64 (recommended) or Visual Studio Build Tools
    - MinGW-w64: Download from https://www.mingw-w64.org/downloads/ or install via MSYS2 (https://www.msys2.org/)
    - After installation, add `C:\msys64\mingw64\bin` (or your MinGW path) to PATH
  - **Linux/Mac**: Usually pre-installed (g++ or clang++)

**Setup:**
```bash
# Build Rust benchmarks
cd benches/rust
cargo build --release
cd ../..

# Build C++ benchmarks
cd benches/cpp
make
cd ../..
```

## Current Benchmarks

### Phase 1: Basic Infrastructure ✅
- **fibonacci**: Recursive Fibonacci calculation
- **sum**: Sum of numbers from 0 to n (using while loop)
- **factorial**: Recursive factorial calculation

### Phase 2: Numerical Benchmarks (Planned)
- Matrix multiplication
- Vector operations
- Basic linear algebra

### Phase 3: ML Benchmarks (Planned)
- Neural network forward pass
- Gradient computation
- Data preprocessing

### Phase 4: HPC Benchmarks (Planned)
- N-body simulation
- Stencil computations
- Advanced reductions

### Phase 5: Cross-Language Comparison ✅
- Automated comparison with Python/Rust/C++
- Performance regression detection
- Detailed timing reports

## Benchmark Structure

```
benches/
├── README.md              # This file
├── compare.py             # Cross-language comparison script
├── fibonacci.rs           # Criterion benchmark
├── factorial.rs           # Criterion benchmark
├── sum.rs                 # Criterion benchmark
├── pain/                  # Pain source files
│   ├── fibonacci.pain
│   ├── factorial.pain
│   └── sum.pain
├── python/                # Python implementations
│   ├── fibonacci.py
│   ├── factorial.py
│   └── sum.py
├── rust/                  # Rust implementations
│   ├── Cargo.toml
│   ├── fibonacci.rs
│   ├── factorial.rs
│   └── sum.rs
└── cpp/                   # C++ implementations
    ├── Makefile
    ├── fibonacci.cpp
    ├── factorial.cpp
    └── sum.cpp
```

## Notes

- Currently benchmarks measure interpreter performance
- Compiled benchmarks (LLVM IR -> executable) will be added when compilation pipeline is complete
- Cross-language comparison uses Python as baseline (1.0x speedup)
- All benchmarks use the same algorithm for fair comparison


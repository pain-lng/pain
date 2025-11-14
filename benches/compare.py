#!/usr/bin/env python3
"""
Benchmark comparison script for Pain vs Python/Rust/C++

Usage:
    python compare.py [benchmark_name] [iterations] [warmup]

Examples:
    python compare.py fibonacci 10 3
    python compare.py all 20 5
    python compare.py all  # Uses defaults: 10 iterations, 3 warmup
"""

import subprocess
import sys
import time
import os
import platform
from pathlib import Path
from typing import Dict, List, Tuple

BENCHMARKS = {
    "fibonacci": {"pain_n": 20, "python_n": 20, "rust_n": 20, "cpp_n": 20},
    "factorial": {"pain_n": 15, "python_n": 15, "rust_n": 15, "cpp_n": 15},
    "sum": {"pain_n": 10000, "python_n": 10000, "rust_n": 10000, "cpp_n": 10000},
}

def run_command(cmd: List[str], input_data: str = None, capture_output: bool = True) -> Tuple[float, str]:
    """Run command and measure execution time"""
    start = time.perf_counter()
    try:
        result = subprocess.run(
            cmd,
            input=input_data,
            capture_output=capture_output,
            text=True,
            check=True,
            timeout=300,
            creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" and capture_output else 0
        )
        elapsed = time.perf_counter() - start
        output = result.stdout.strip() if capture_output else ""
        return elapsed, output
    except subprocess.TimeoutExpired:
        return float('inf'), "TIMEOUT"
    except subprocess.CalledProcessError as e:
        error_msg = e.stderr.strip() if e.stderr else str(e)
        return float('inf'), f"ERROR: {error_msg}"

def benchmark_pain(benchmark: str, n: int, iterations: int, warmup: int = 2) -> List[float]:
    """Benchmark Pain interpreter"""
    times = []
    source_file = Path(f"benches/pain/{benchmark}.pain")
    
    # Update source file with correct n value
    if benchmark == "fibonacci":
        source = f"""
fn fib(n: int) -> int:
    if n <= 1:
        return n
    return fib(n - 1) + fib(n - 2)

fn main() -> int:
    return fib({n})
"""
    elif benchmark == "factorial":
        source = f"""
fn fact(n: int) -> int:
    if n <= 1:
        return 1
    return n * fact(n - 1)

fn main() -> int:
    return fact({n})
"""
    elif benchmark == "sum":
        source = f"""
fn sum(n: int) -> int:
    var result = 0
    var i = 0
    var limit = n
    while i <= limit:
        result = result + i
        i = i + 1
    return result

fn main() -> int:
    return sum({n})
"""
    else:
        return []
    
    source_file.parent.mkdir(parents=True, exist_ok=True)
    source_file.write_text(source)
    
    # Try to use compiled binary first, fallback to cargo run
    exe_ext = ".exe" if platform.system() == "Windows" else ""
    exe_path = Path(f"target/release/pain-compiler{exe_ext}")
    if not exe_path.exists():
        exe_path = Path(f"target/debug/pain-compiler{exe_ext}")
    
    cmd = [str(exe_path.absolute()), "run", "--input", str(source_file.absolute())] if exe_path.exists() else [
        "cargo", "run", "--release", "--bin", "pain-compiler", "--",
        "run", "--input", str(source_file.absolute())
    ]
    
    # Warmup runs
    for _ in range(warmup):
        run_command(cmd, capture_output=False)
    
    # Actual benchmark runs
    for _ in range(iterations):
        elapsed, _ = run_command(cmd)
        if elapsed != float('inf'):
            times.append(elapsed)
    
    return times

def benchmark_python(benchmark: str, n: int, iterations: int, warmup: int = 2) -> List[float]:
    """Benchmark Python"""
    times = []
    script = Path(f"benches/python/{benchmark}.py")
    
    if not script.exists():
        print(f"    Warning: Python script not found at {script}")
        return []
    
    cmd = ["python", str(script.absolute()), str(n)]
    
    # Warmup runs
    for _ in range(warmup):
        run_command(cmd, capture_output=False)
    
    # Actual benchmark runs
    for _ in range(iterations):
        elapsed, _ = run_command(cmd)
        if elapsed != float('inf'):
            times.append(elapsed)
    
    return times

def benchmark_rust(benchmark: str, n: int, iterations: int, warmup: int = 2) -> List[float]:
    """Benchmark Rust"""
    times = []
    bin_name = benchmark
    
    # Build if needed
    build_cmd = ["cargo", "build", "--release", "--manifest-path", "benches/rust/Cargo.toml", "--bin", bin_name]
    result = subprocess.run(
        build_cmd,
        capture_output=True,
        text=True,
        creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
    )
    if result.returncode != 0:
        print(f"    Warning: Failed to build Rust benchmark: {result.stderr[:200]}")
        return []
    
    exe_ext = ".exe" if platform.system() == "Windows" else ""
    # Try multiple possible locations
    possible_paths = [
        Path(f"benches/rust/target/release/{bin_name}{exe_ext}"),
        Path(f"target/release/{bin_name}{exe_ext}"),
        Path(f"benches/rust/target/release/{bin_name}"),  # Without extension
    ]
    
    exe_path = None
    for path in possible_paths:
        if path.exists():
            exe_path = path
            break
    
    if exe_path is None:
        print(f"    Warning: Rust executable not found. Tried: {[str(p) for p in possible_paths]}")
        return []
    
    cmd = [str(exe_path.absolute()), str(n)]
    
    # Warmup runs
    for _ in range(warmup):
        run_command(cmd, capture_output=False)
    
    # Actual benchmark runs
    for _ in range(iterations):
        elapsed, _ = run_command(cmd)
        if elapsed != float('inf'):
            times.append(elapsed)
    
    return times

def find_compiler(compilers: List[str]) -> str:
    """Find available C++ compiler"""
    for compiler in compilers:
        try:
            # Check if compiler exists by trying to get version
            if compiler == "cl":
                # MSVC uses different flag
                result = subprocess.run(
                    [compiler],
                    capture_output=True,
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
                )
            else:
                result = subprocess.run(
                    [compiler, "--version"],
                    capture_output=True,
                    timeout=5,
                    creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
                )
            if result.returncode == 0 or (compiler == "cl" and result.returncode != 9009):
                return compiler
        except (FileNotFoundError, subprocess.TimeoutExpired, OSError):
            continue
    return None

def benchmark_cpp(benchmark: str, n: int, iterations: int, warmup: int = 2) -> List[float]:
    """Benchmark C++"""
    times = []
    exe_ext = ".exe" if platform.system() == "Windows" else ""
    exe_path = Path(f"benches/cpp/{benchmark}{exe_ext}")
    
    # Build if needed
    if not exe_path.exists():
        cpp_file = Path(f"benches/cpp/{benchmark}.cpp")
        if not cpp_file.exists():
            print(f"    Warning: C++ source file not found at {cpp_file}")
            return []
        
        if platform.system() == "Windows":
            # On Windows, try to find available compiler
            compiler = find_compiler(["g++", "clang++", "cl"])
            if compiler is None:
                print(f"    Warning: No C++ compiler found (tried g++, clang++, cl). Skipping C++ benchmark.")
                return []
            
            if compiler == "cl":
                # MSVC compiler
                compile_cmd = [
                    compiler, "/O2", "/EHsc", f"/Fe:{exe_path}", str(cpp_file)
                ]
            else:
                # g++ or clang++
                compile_cmd = [
                    compiler, "-O3", "-std=c++17", "-o", str(exe_path), str(cpp_file)
                ]
            
            try:
                result = subprocess.run(
                    compile_cmd,
                    capture_output=True,
                    text=True,
                    timeout=60,
                    creationflags=subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0
                )
                if result.returncode != 0:
                    print(f"    Warning: Failed to compile C++ benchmark: {result.stderr[:200] if result.stderr else result.stdout[:200]}")
                    return []
            except (FileNotFoundError, subprocess.TimeoutExpired, OSError) as e:
                print(f"    Warning: Failed to run C++ compiler: {e}")
                return []
            
            if not exe_path.exists():
                print(f"    Warning: C++ compilation succeeded but executable not found at {exe_path}")
                return []
        else:
            # Unix-like systems: use make
            make_cmd = ["make", "-C", "benches/cpp", benchmark]
            result = subprocess.run(make_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print(f"    Warning: Failed to build C++ benchmark: {result.stderr[:200]}")
                return []
    
    if exe_path.exists():
        cmd = [str(exe_path.absolute()), str(n)]
        
        # Warmup runs
        for _ in range(warmup):
            run_command(cmd, capture_output=False)
        
        # Actual benchmark runs
        for _ in range(iterations):
            elapsed, _ = run_command(cmd)
            if elapsed != float('inf'):
                times.append(elapsed)
    else:
        print(f"    Warning: C++ executable not found at {exe_path}")
    
    return times

def format_time(seconds: float) -> str:
    """Format time in appropriate units"""
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2f} ns"
    elif seconds < 1e-3:
        return f"{seconds * 1e6:.2f} μs"
    elif seconds < 1.0:
        return f"{seconds * 1e3:.2f} ms"
    else:
        return f"{seconds:.2f} s"

def print_results(benchmark: str, results: Dict[str, List[float]]):
    """Print benchmark results"""
    print(f"\n{'='*60}")
    print(f"Benchmark: {benchmark}")
    print(f"{'='*60}")
    print(f"{'Language':<15} {'Mean':<15} {'Min':<15} {'Max':<15} {'Speedup':<15}")
    print(f"{'-'*60}")
    
    # Calculate baseline (Python)
    python_times = results.get("Python", [])
    if python_times:
        baseline_mean = sum(python_times) / len(python_times)
    else:
        baseline_mean = 1.0
    
    for lang in ["Pain", "Python", "Rust", "C++"]:
        times = results.get(lang, [])
        if not times:
            print(f"{lang:<15} {'N/A':<15} {'N/A':<15} {'N/A':<15} {'N/A':<15}")
            continue
        
        mean_time = sum(times) / len(times)
        min_time = min(times)
        max_time = max(times)
        speedup = baseline_mean / mean_time if mean_time > 0 else 0
        
        print(f"{lang:<15} {format_time(mean_time):<15} {format_time(min_time):<15} {format_time(max_time):<15} {speedup:.2f}x")

def main():
    if len(sys.argv) < 2:
        print("Usage: python compare.py [benchmark_name] [iterations] [warmup]")
        print("Available benchmarks:", ", ".join(BENCHMARKS.keys()))
        sys.exit(1)
    
    benchmark_name = sys.argv[1].lower()
    iterations = int(sys.argv[2]) if len(sys.argv) > 2 else 10
    warmup = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    
    if benchmark_name == "all":
        benchmarks_to_run = list(BENCHMARKS.keys())
    elif benchmark_name in BENCHMARKS:
        benchmarks_to_run = [benchmark_name]
    else:
        print(f"Unknown benchmark: {benchmark_name}")
        print("Available benchmarks:", ", ".join(BENCHMARKS.keys()))
        sys.exit(1)
    
    for bench in benchmarks_to_run:
        config = BENCHMARKS[bench]
        results = {}
        
        print(f"\nRunning {bench} benchmark ({iterations} iterations, {warmup} warmup)...")
        
        # Pain
        print("  Running Pain...", end="", flush=True)
        pain_times = benchmark_pain(bench, config["pain_n"], iterations, warmup)
        results["Pain"] = pain_times
        print(f" Done ({len(pain_times)} successful runs)")
        
        # Python
        print("  Running Python...", end="", flush=True)
        python_times = benchmark_python(bench, config["python_n"], iterations, warmup)
        results["Python"] = python_times
        print(f" Done ({len(python_times)} successful runs)")
        
        # Rust
        print("  Running Rust...", end="", flush=True)
        rust_times = benchmark_rust(bench, config["rust_n"], iterations, warmup)
        results["Rust"] = rust_times
        print(f" Done ({len(rust_times)} successful runs)")
        
        # C++
        print("  Running C++...", end="", flush=True)
        cpp_times = benchmark_cpp(bench, config["cpp_n"], iterations, warmup)
        results["C++"] = cpp_times
        print(f" Done ({len(cpp_times)} successful runs)")
        
        print_results(bench, results)

if __name__ == "__main__":
    main()


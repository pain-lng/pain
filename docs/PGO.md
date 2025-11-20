# Profile-Guided Optimization (PGO) Guide

Profile-Guided Optimization (PGO) is a compiler optimization technique that uses runtime profiling data to improve code performance. Pain compiler supports PGO for LLVM-generated executables.

## Overview

PGO works in two phases:

1. **Profile Generation**: Build your program with profiling instrumentation, run it with representative workloads, and collect profile data.
2. **Profile Use**: Rebuild your program using the collected profile data to optimize hot paths and improve performance.

## Quick Start

### Step 1: Build with Profile Generation

```bash
pain build --input main.pain --executable --pgo generate
```

This creates an executable instrumented for profiling. When you run it, profile data files (`.profraw`) will be generated in the current directory.

### Step 2: Run Your Program

Execute your program with representative workloads:

```bash
./main
# or on Windows
main.exe
```

This generates profile data files (e.g., `default.profraw`).

### Step 3: Merge Profile Data (Optional)

If you have multiple profile files, merge them:

```bash
pain pgo-merge --input "*.profraw" --output default.profdata
```

The `--input` flag supports glob patterns (e.g., `*.profraw`, `profile-*.profraw`) and multiple files:

```bash
pain pgo-merge --input "*.profraw" --input "profile-*.profraw" --output default.profdata
```

Or use `llvm-profdata` directly:

```bash
llvm-profdata merge -o default.profdata *.profraw
```

### Step 4: Rebuild with Profile Data

```bash
pain build --input main.pain --executable --pgo use --pgo-profile default.profdata
```

This creates an optimized executable using the profile data.

## Automated PGO Pipeline

For convenience, you can use the automated PGO pipeline command that handles all steps:

```bash
pain pgo-pipeline --input main.pain --output main_optimized
```

This command automatically:
1. Builds with profile generation
2. Runs the executable to collect profile data
3. Merges profile files
4. Rebuilds with profile data

You can customize the collection step:

```bash
# Use custom command for profile collection
pain pgo-pipeline --input main.pain --collect-command "./main --test-data large.dat"

# Specify profile directory
pain pgo-pipeline --input main.pain --profile-dir ./profiles
```

## Collecting Profile Data

To collect profile data from multiple runs of an instrumented executable:

```bash
# Run executable 5 times with different arguments
pain pgo-collect --executable ./main --args "40" --runs 5

# Run with multiple arguments
pain pgo-collect --executable ./main --args "40" --args "50" --runs 3
```

This is useful when you want to collect profiles from multiple representative workloads before merging.

## Command-Line Options

### `--pgo <mode>`

Specify PGO mode:
- `generate`: Build with profile generation instrumentation
- `use`: Build using existing profile data

### `--pgo-profile <path>`

Specify profile data path:
- For `generate` mode: Directory where profile data will be written (default: current directory)
- For `use` mode: Path to profile data file (e.g., `default.profdata`)

If not specified in `use` mode, the compiler will look for `default.profdata` in the current directory.

## Example Workflows

### Manual Workflow

```bash
# 1. Build with profiling
pain build --input fibonacci.pain --executable --pgo generate -o fib

# 2. Run with representative input (multiple times for better coverage)
./fib 40
./fib 50
./fib 60

# 3. Merge profile data
pain pgo-merge --input "*.profraw" --output default.profdata

# 4. Rebuild with optimization
pain build --input fibonacci.pain --executable --pgo use --pgo-profile default.profdata -o fib_optimized

# 5. Compare performance
time ./fib 40
time ./fib_optimized 40
```

### Automated Pipeline Workflow

```bash
# Single command does everything
pain pgo-pipeline --input fibonacci.pain --output fib_optimized

# Or with custom collection command
pain pgo-pipeline --input fibonacci.pain --collect-command "./fib 40" --output fib_optimized
```

### Advanced Workflow with Multiple Runs

```bash
# 1. Build with profiling
pain build --input fibonacci.pain --executable --pgo generate -o fib

# 2. Collect profiles from multiple runs
pain pgo-collect --executable ./fib --args "40" --runs 5
pain pgo-collect --executable ./fib --args "50" --runs 3

# 3. Merge all collected profiles
pain pgo-merge --input "*.profraw" --output default.profdata

# 4. Rebuild with optimization
pain build --input fibonacci.pain --executable --pgo use --pgo-profile default.profdata -o fib_optimized
```

## Best Practices

1. **Use Representative Workloads**: Run your program with inputs that represent typical usage patterns.
2. **Multiple Runs**: Run your program multiple times with different inputs to get better profile coverage.
3. **Merge Profiles**: If you have multiple profile files, merge them before the final build.
4. **Keep Intermediate Files**: Use `--keep-intermediates` to debug PGO issues.

## Requirements

- LLVM/Clang with PGO support (LLVM 10+)
- `llvm-profdata` tool for merging profiles (usually included with LLVM)

## Troubleshooting

### Profile data not found

If you get an error about missing profile data:
- Ensure you've run the instrumented executable at least once
- Check that profile files (`.profraw`) were generated
- Merge profile files if you have multiple runs

### Performance not improved

- Ensure you're using representative workloads during profiling
- Run the program multiple times with different inputs
- Check that you're using the optimized executable (built with `--pgo use`)

## PGO Commands Reference

### `pain pgo-merge`

Merge multiple profile data files into a single profile.

**Options:**
- `--input <pattern>`: Input profile files (supports glob patterns like `*.profraw`)
- `--output <path>`: Output profile data file (e.g., `default.profdata`)

**Examples:**
```bash
pain pgo-merge --input "*.profraw" --output default.profdata
pain pgo-merge --input "profile-*.profraw" --input "test-*.profraw" --output merged.profdata
```

### `pain pgo-pipeline`

Run complete PGO pipeline: generate, collect, merge, and rebuild.

**Options:**
- `--input <path>`: Input source file (required)
- `--output <path>`: Output executable file (optional, defaults to input name + `_optimized`)
- `--collect-command <cmd>`: Custom command to run for profile collection (optional)
- `--profile-dir <path>`: Profile data directory (optional, defaults to current directory)
- `--keep-intermediates`: Keep intermediate files (IR, object files)

**Examples:**
```bash
pain pgo-pipeline --input main.pain
pain pgo-pipeline --input main.pain --output optimized_main --collect-command "./main --test"
```

### `pain pgo-collect`

Collect profile data by running instrumented executable multiple times.

**Options:**
- `--executable <path>`: Executable to run (required)
- `--args <arg>`: Command arguments (can be specified multiple times)
- `--runs <n>`: Number of runs (default: 1)
- `--profile-dir <path>`: Profile data directory (optional, defaults to current directory)

**Examples:**
```bash
pain pgo-collect --executable ./main --runs 5
pain pgo-collect --executable ./main --args "40" --args "50" --runs 3
```

## Limitations

- PGO currently only works with LLVM backend (not MLIR)
- Requires LLVM/Clang installation
- Profile data is platform-specific


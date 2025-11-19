# Pain Programming Language

A modern, high-performance programming language designed for scientific computing and data science workloads.

## Features

### Core Language
- **Indentation-based syntax** - Clean, Python-like syntax with proper block parsing
- **Static type system** - Type inference and type checking
- **Functions and classes** - Support for functions, classes, and methods
- **Rich type system** - Integers, floats, strings, booleans, lists, arrays, maps, and user-defined types
- **Doc comments** - Python-style doc comments with automatic documentation generation

### Compiler
- **Lexer and Parser** - Complete lexer and parser with indentation-based block parsing
- **Type Checker** - Full type checking with type inference
- **IR Generation** - Intermediate representation (IR) builder
- **Code Generation** - LLVM IR and MLIR code generation
- **Optimizations** - SSA transformation, constant folding, dead code elimination
- **Interpreter** - Runtime interpreter for testing and development

### Developer Tools
- **LSP Server** - Language Server Protocol implementation with:
  - Diagnostics and error reporting
  - Code completion with context-aware suggestions
  - Hover tooltips with doc comments
  - Function location finding
- **VS Code Extension** - Full VS Code integration with syntax highlighting and LSP support
- **Code Formatter** - Automatic code formatting
- **Documentation Generator** - Generate documentation from source code

### Package Management
- **painpkg** - Package manager with:
  - Dependency resolution (semver)
  - Package installation from local/remote sources (file://, git://)
  - `pain.toml` dependency management
  - Local file-based registry with indexing

### Runtime
- **Memory Management** - Bump allocator and garbage collector
- **Object Model** - Runtime object representation for lists, arrays, and user-defined types

### Standard Library
- **Math functions**: `abs`, `min`, `max`, `sqrt`, `pow`, `sin`, `cos`, `floor`, `ceil`
- **String functions**: `len`, `concat`, `substring`, `contains`, `starts_with`, `ends_with`, `trim`, `to_int`, `to_float`, `to_string`
- **List/Array functions**: `len` (indexing and literals supported)
- **I/O functions**: `print`

## Installation

### Prerequisites
- Rust toolchain (install from [rustup.rs](https://rustup.rs/))
- LLVM (optional, for LLVM backend)

### Build from Source

```bash
# Clone the repository
git clone --recursive https://github.com/pain-lng/pain.git
cd pain

# Build all components
cargo build --release

# Build specific components
cargo build --release --package pain-compiler
cargo build --release --package pain-lsp
cargo build --release --package painpkg
```

## Quick Start

### Running a Pain Program

```bash
# Run a Pain source file
cargo run --package pain-compiler -- run --input example.pain

# Or use the installed binary
pain run example.pain
```

### Building a Pain Program

```bash
# Generate LLVM IR
pain build --input example.pain --output example.ll

# Build executable
pain build --input example.pain --executable

# Use MLIR backend
pain build --input example.pain --backend mlir --output example.mlir
```

## Usage Examples

- **Check**: `pain check --input path/to/file.pain` — parse + type-check without running.
- **Format**: `pain format --input src/main.pain --stdout` — pretty-print to stdout or overwrite file.
- **Run via interpreter**: `pain run --input examples/loop.pain`.
- **Build optimized binary**: `pain build --input examples/app.pain --executable --backend llvm`.
- **Generate docs**: `pain doc --input src/lib.pain --output docs/lib.md` or `pain doc --stdlib`.
- **Package manager**: `painpkg init demo && painpkg install && painpkg run`.

### Example Program

```pain
fn main():
    print("I love Pain!")
    
    let x = 10
    let y = 20
    let sum = x + y
    print(sum)
```

## Project Structure

This is a workspace containing multiple crates:

- **pain-compiler** - Main compiler implementation
- **pain-lsp** - Language Server Protocol server
- **pain-runtime** - Runtime library (allocator, GC, object model)
- **painpkg** - Package manager

## Documentation

- High-level guides live in [`docs/`](docs/):
  - [`docs/quickstart.md`](docs/quickstart.md) – installation, running programs, `painpkg`.
  - [`docs/stdlib.md`](docs/stdlib.md) – summary of built-in APIs.
  - [`docs/examples.md`](docs/examples.md) – ready-to-run snippets.
- Generate fresh API docs from source:

```bash
cargo run -p pain-compiler -- doc --stdlib
cargo run -p pain-compiler -- doc --input source.pain
```

## Benchmarks

Run benchmarks to compare performance:

```bash
# Run all benchmarks
cargo bench

# Compare with Python/Rust/C++
cd benches
python compare.py all
```

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see the project structure and submit pull requests to the appropriate submodule repositories.

## Links

- **Compiler**: [pain-compiler](https://github.com/pain-lng/pain-compiler)
- **LSP Server**: [pain-lsp](https://github.com/pain-lng/pain-lsp)
- **Runtime**: [pain-runtime](https://github.com/pain-lng/pain-runtime)
- **Package Manager**: [painpkg](https://github.com/pain-lng/painpkg)


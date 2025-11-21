# Quick Start Guide

This guide walks through installing the toolchain, compiling your first Pain program, and using the bundled package manager.

## 1. Prerequisites

- Rust (via [rustup.rs](https://rustup.rs/)).
- LLVM toolchain for LLVM/MLIR backends (optional for interpreter-only workflows).
- `git` for fetching dependencies.

Check versions:

```bash
rustc --version
cargo --version
llvm-config --version   # optional
```

## 2. Clone & Build

```bash
git clone --recursive https://github.com/pain-lng/pain.git
cd pain
cargo build --release       # entire workspace
# or focus on the compiler:
cargo build -p pain-compiler
```

Artifacts live in `target/{debug,release}`. On Windows, binaries end with `.exe`.

## 3. Command Cheat Sheet

| Task | Command |
| --- | --- |
| Interactive REPL | `pain repl` |
| Interpret & print result | `pain run --input path/to/app.pain` |
| Build IR / executable | `pain build --input app.pain [--backend mlir|llvm] [--executable]` |
| Type-check only | `pain check --input app.pain` |
| Format source | `pain format --input app.pain --stdout` |
| Generate docs | `pain doc --input app.pain --output docs/app.md` |
| Stdlib docs | `pain doc --stdlib --output docs/stdlib.md` |

Invoke via the installed `pain` binary or through `cargo run -p pain-compiler -- <subcommand>` during development.

## 4. Run a Program

Create `examples/hello.pain`:

```pain
fn main():
    print("Hello, Pain!")
```

Execute it:

```bash
pain run --input examples/hello.pain
# before installing binaries:
cargo run -p pain-compiler -- run --input examples/hello.pain
```

## 5. Interactive REPL

Start the interactive REPL for quick testing:

```bash
pain repl
# or during development:
cargo run -p pain-compiler -- repl
```

REPL features:
- Multi-line input support
- Command history (persisted to `~/.pain/repl_history.txt`)
- Debug commands:
  - `:vars` - show all variables
  - `:funcs` - show all functions
  - `:classes` - show all classes

Example session:
```pain
>>> let x = 10
>>> let y = 20
>>> x + y
30
>>> :vars
x: int = 10
y: int = 20
```

## 6. Build & Optimize

```bash
# Generate LLVM IR
pain build --input examples/hello.pain --backend llvm --output hello.ll

# Run full pipeline with optimizations
pain build --input examples/loop.pain --opt-level 2
```

## 7. Package Management (`painpkg`)

Initialize a project:

```bash
cargo run -p painpkg -- init my_app
cd my_app
```

Add a dependency to `pain.toml`:

```toml
[dependencies]
linear-algebra = "0.2"
```

Install dependencies:

```bash
cargo run -p painpkg -- install
```

## 8. Lint, Test, Benchmark

```bash
# Lint compiler code
cargo clippy -p pain-compiler

# Run integration tests
cargo test -p pain-compiler --test integration_test

# Run language benchmarks
cargo bench
```

## 9. Next Steps

- Explore API details in [`stdlib.md`](stdlib.md).
- Copy ready-to-run snippets from [`examples.md`](examples.md).
- Use the LSP server (`pain-lsp`) inside VS Code for hover docs, completion, and diagnostics.


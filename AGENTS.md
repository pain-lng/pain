# Pain — guide for AI agents

Pain is an experimental programming language with Python-like syntax and static types.
The toolchain is written in Rust: a compiler with a tree-walking interpreter and an
LLVM backend, a language server, a runtime and a package manager.

This file is the entry point for coding agents (Claude Code, Cursor, Codex, ...).
Each submodule has its own `AGENTS.md` with the details of that crate.

## Layout

This repository is a Cargo workspace whose members are **git submodules**, each with
its own GitHub repository and history:

| Path | What it is | Guide |
| --- | --- | --- |
| `pain-compiler/` | Lexer, parser, type checker, interpreter, IR, optimizer, LLVM codegen. Binary: `pain` | `pain-compiler/AGENTS.md` |
| `pain-lsp/` | Language server (tower-lsp) built on the compiler crate | `pain-lsp/AGENTS.md` |
| `pain-runtime/` | Runtime values, allocator, GC used by the interpreter | `pain-runtime/AGENTS.md` |
| `painpkg/` | Package manager CLI (`pain.toml`, registry client) | `painpkg/AGENTS.md` |
| `docs/` | User documentation: language examples, stdlib, PML, development flow | |
| `benches/` | Cross-language benchmark programs and `compare.py` | |
| `.github/workflows/` | CI (`ci.yml`) and release builds (`release.yml`) | |

`pain-vscode/` and `pain-registry/` are separate repositories; if present locally they
are ignored by git here.

## Commands

Run from the workspace root. These are the checks CI runs:

```bash
cargo build --release --all
cargo fmt --all -- --check
cargo clippy --all-targets -- -D warnings
cargo test --lib
cargo test --test integration_test
cargo test --test full_pipeline_integration   # native builds, needs LLVM (see below)
cargo test --test property_tests
cargo test --test performance_regression
(cd pain-lsp && cargo test --tests)
```

Running Pain code:

```bash
cargo run --bin pain -- run   --input file.pain          # interpreter
cargo run --bin pain -- check --input file.pain          # parse + type check
cargo run --bin pain -- build --input file.pain --executable -o file.exe   # native
```

## Working with submodules

- A change inside `pain-compiler/` (or another member) is a commit in **that**
  repository. Commit and push it there first, then commit the updated submodule
  pointer in this repository. A root commit that points at an unpushed submodule
  commit breaks CI and every fresh clone.
- Branch flow is described in `docs/DEVELOPMENT.md`: `feature/*` → `develop` → `main`.
  Use the same branch name in the submodule and in the root when a change spans both.
- CI checks out submodules recursively and runs on pushes and PRs to `main` and `develop`.

## Rules for AI contributions

- Do not invent or add language syntax without the maintainer's approval. When docs,
  tests and the parser disagree, the parser is the reference; ask before changing it.
- Do not change the core architecture, the IR format or public APIs unless the task
  says so. Propose optimizations; implement them only when asked.
- One responsibility per commit, with tests. There is no line limit on a change;
  split it into commits that can be reviewed one by one.
- Do not restructure the repository or add stray files. Avoid `unsafe` Rust unless
  it is necessary.
- If the task is unclear, ask.

## Things that are easy to get wrong

- **CI uses the latest stable Rust.** An older local toolchain misses newer clippy
  lints. Before pushing, run clippy with a current toolchain
  (`rustup update stable`, or `cargo +<version> clippy ...`).
- **Native builds need LLVM tools on `PATH`** (`clang`, `llc`; on Windows
  `C:\Program Files\LLVM\bin`). Without them the `full_pipeline_integration` tests
  skip the native part instead of failing — a green run without LLVM proves nothing
  about the backend.
- **Verify native code against the interpreter.** The interpreter is the reference
  implementation; run the same program with `pain run` and as an executable and
  compare the output.
- `*.pain` files are git-ignored everywhere except `benches/pain/`. Put test programs
  into Rust tests as strings, not into loose files.
- Objects are created with `new Name(args)`; arguments fill the fields in declaration
  order. There is no `fn new` constructor: `new` is a keyword.
- The type checker does not convert implicitly: `int` is not accepted where `float64`
  is declared.

# Changelog

All notable changes to the Pain programming language will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.2.0] - 2025-01-XX

### Added

#### PML (Pain Markup Language) v0.1
- **PML Parser** - Complete lexer and parser implementation for PML format
  - Tab-based indentation parsing (1 TAB = 1 level)
  - Support for SCALAR, MAP, and LIST node types
  - Comment parsing with `#` syntax
  - String, int, float, bool, and null value types
  - Escape sequence support (`\n`, `\t`, `\r`, `\\`, `\"`, `\'`)
  - Comprehensive error handling with detailed error messages
- **PML Standard Library** - Runtime functions for PML integration
  - `pml_load_file(path: str) -> dynamic` - Load and parse PML files
  - `pml_parse(source: str) -> dynamic` - Parse PML strings
- **PML Documentation** - Complete specification and examples
  - PML v0.1 specification document (`docs/PML_SPEC.md`)
  - PML examples and usage guide (`docs/examples_pml.md`)
  - 40+ unit tests covering edge cases (Unicode, long strings, deep nesting, etc.)
  - 5 integration tests for stdlib functions
  - Performance benchmarks (10 benchmarks documented)

#### VS Code Extension Enhancements
- **PML Language Support** - Full syntax highlighting for `.pml` files
  - TextMate grammar for PML syntax
  - Language configuration for PML
  - PML file association and recognition
- **Custom File Icons** - Visual file type identification
  - Custom PNG icons for `.pain` files
  - Custom PNG icons for `.pml` files
  - Icon theme configuration for VS Code/Cursor
- **Extension Distribution** - Ready for VSIX distribution via repository

### Changed
- Improved error handling in PML parser with Display trait for `PmlParseError`
- Enhanced code quality (clippy, fmt) - all checks passing
- Performance profiling and analysis document created (`.pain_dev_docs/PML_PERFORMANCE.md`)

### Testing
- Expanded PML parser test coverage (40 unit tests)
- Added PML integration tests (5 tests for stdlib functions)
- Edge case testing (15+ edge cases: Unicode, long strings, deep nesting, etc.)
- Performance benchmarking suite (10 benchmarks)

[0.2.0]: https://github.com/pain-lng/pain/releases/tag/v0.2.0

## [0.1.0] - 2025-11-20

### Added

#### Core Language
- Indentation-based syntax with proper block parsing
- Static type system with type inference
- Functions and classes with methods
- Rich type system: integers, floats, strings, booleans, lists, arrays, maps, and user-defined types
- Python-style doc comments with automatic documentation generation

#### Compiler
- Complete lexer and parser with indentation-based block parsing
- Full type checking with type inference
- Intermediate representation (IR) builder
- LLVM IR code generation (stable)
- MLIR code generation (experimental IR dump)
- SSA transformation, constant folding, dead code elimination
- Runtime interpreter for testing and development
- JIT compilation engine with runtime code generation (optional, requires LLVM 21+)
- On-stack replacement (OSR) support for function recompilation

#### Developer Tools
- LSP Server with diagnostics, code completion, hover tooltips, and function location finding
- VS Code Extension with syntax highlighting and LSP support
- Code formatter
- Documentation generator
- Interactive REPL with:
  - Multi-line input support
  - Command history (persisted to ~/.pain/repl_history.txt)
  - Debug commands (`:vars`, `:funcs`, `:classes`)

#### Package Management
- `painpkg` package manager with:
  - Dependency resolution (semver)
  - Package installation from local sources (`file://`) and experimental Git sources (`git://`, `git+`)
  - `pain.toml` dependency management
  - Local file-based registry with indexing

#### Runtime
- Bump allocator and garbage collector
- Runtime object representation for lists, arrays, and user-defined types

#### Standard Library
- Math functions: `abs`, `min`, `max`, `sqrt`, `pow`, `sin`, `cos`, `floor`, `ceil`
- String functions: `len`, `concat`, `substring`, `contains`, `starts_with`, `ends_with`, `trim`, `to_int`, `to_float`, `to_string`
- List/Array functions: `len` with indexing and literals support
- I/O functions: `print`

#### CI/CD
- Automated testing on Windows/Linux/macOS
- Multi-platform builds with GitHub Actions
- Release automation with multi-platform binaries
- Code formatting checks (rustfmt)
- Linting checks (clippy)

#### Documentation
- README with usage examples
- Quick Start Guide
- API documentation for stdlib
- Example programs
- JIT setup guide

[0.1.0]: https://github.com/pain-lng/pain/releases/tag/v0.1.0


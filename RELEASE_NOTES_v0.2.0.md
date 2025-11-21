# Pain v0.2.0 Release Notes

**Release Date:** January 2025  
**Release Type:** Feature Release (Alpha)

## Overview

Pain v0.2.0 introduces **PML (Pain Markup Language)** v0.1, a minimalistic declarative data format designed for UI structures, configurations, and tree data. This release also includes significant enhancements to the VS Code/Cursor extension with PML support and custom file icons.

## 🎉 Major Features

### PML (Pain Markup Language) v0.1

PML is a YAML-inspired but simplified markup language with strict rules for predictability, ease of parsing, and high performance.

**Key Features:**
- **Tab-based indentation** - Strict 1 TAB = 1 level rule
- **Three node types**: SCALAR, MAP, LIST
- **Type support**: strings, integers, floats, booleans, null
- **Comment support** with `#` syntax
- **Escape sequences** for strings (`\n`, `\t`, `\r`, `\\`, `\"`, `\'`)
- **Simple syntax**: `key: value` for maps, `- item` for lists

**Standard Library Functions:**
- `pml_load_file(path: str) -> dynamic` - Load and parse PML files
- `pml_parse(source: str) -> dynamic` - Parse PML strings

**Example Usage:**
```pain
fn main():
    let config = pml_load_file("config.pml")
    let app_name = config.app.name
    print("Starting " + app_name)
```

**Documentation:**
- Complete specification: [`docs/PML_SPEC.md`](docs/PML_SPEC.md)
- Examples and usage: [`docs/examples_pml.md`](docs/examples_pml.md)

### VS Code/Cursor Extension Enhancements

**PML Language Support:**
- Full syntax highlighting for `.pml` files
- TextMate grammar for PML syntax
- Language configuration and file associations

**Custom File Icons:**
- Custom PNG icons for `.pain` files
- Custom PNG icons for `.pml` files
- Icon theme configuration for better visual identification

**Distribution:**
- Extension ready for VSIX distribution via repository
- Version 0.2.0 with PML support

## 📊 Testing & Quality

- **40+ unit tests** for PML parser covering edge cases
- **5 integration tests** for PML stdlib functions
- **15+ edge cases** tested: Unicode, long strings, deep nesting, etc.
- **10 performance benchmarks** documented
- All code quality checks passing (clippy, fmt)

## 📚 Documentation

- PML v0.1 specification document
- PML examples and usage guide
- Performance analysis document (`.pain_dev_docs/PML_PERFORMANCE.md`)

## 🔧 Technical Details

**PML Parser Implementation:**
- ~250-350 lines of parser code
- Comprehensive error handling with detailed messages
- High-performance parsing with minimal allocations
- Support for deeply nested structures (tested up to 10+ levels)

**Performance:**
- Fast parsing of simple maps: < 1μs
- Efficient handling of large structures (100+ keys/items)
- Optimized for common use cases (UI configs, app settings)

## 🚀 Migration Guide

No breaking changes from v0.1.0. This is a purely additive release.

**To use PML:**
1. Create `.pml` files with your data structures
2. Use `pml_load_file()` or `pml_parse()` in your Pain code
3. Access parsed data as dynamic objects

**VS Code Extension:**
- Update to v0.2.0 to get PML syntax highlighting
- Custom icons will appear automatically for `.pain` and `.pml` files

## 📦 What's Next

**Planned for v0.3.0:**
- PML v0.2: inline strings, extended escape sequences, nullable values
- Tensor support for ML workloads
- Python bridge for data science workflows

## 🙏 Acknowledgments

Thanks to all contributors and testers who helped make this release possible!

---

**Full Changelog:** See [CHANGELOG.md](CHANGELOG.md) for complete list of changes.


# Active Tasks (≤7)

## Priority 1: Critical for v0.2.0 release

1. **PML v0.1 — Pain Markup Language** ✅ **COMPLETED**
   - ✅ Design PML AST structure (PmlNode with SCALAR/MAP/LIST)
   - ✅ Implement PML lexer (tab-based indentation, comments, key-value parsing)
   - ✅ Implement PML parser (build PmlNode tree from tokens)
   - ✅ Add PML stdlib module (`pml_load_file`, `pml_parse`)
   - ✅ Write PML specification document (`docs/PML_SPEC.md`)
   - ✅ Add PML examples and tests (`docs/examples_pml.md`, unit tests)
   - **Status**: Core functionality implemented and tested. Ready for v0.2.0-alpha release.

2. **VS Code Extension: Enhancements** ✅ **COMPLETED**
   - ✅ PML syntax highlighting (TextMate grammar, language configuration)
   - ✅ Custom file icons for `.pain` and `.pml` files (PNG icons, icon theme)
   - ✅ Extension ready for VSIX distribution (marketplace publication postponed)
   - **Status**: Extension enhanced with PML support and custom icons. VSIX will be distributed via repository.

3. **Release preparation** ✅ **COMPLETED**
   - ✅ Final testing and bug fixes (126 unit tests passing, 5 LLVM integration tests need environment setup)
   - ✅ Update CHANGELOG.md with v0.2.0 changes
   - ✅ Prepare release notes (RELEASE_NOTES_v0.2.0.md)
   - ✅ Update version to 0.2.0 in Cargo.toml
   - ⏳ Tag v0.2.0 release (pending git tag creation)

## Priority 2: Important for v0.2.0 release

4. **Documentation updates** (1 week)
   - ⏳ Update main README with v0.2.0 features
   - ⏳ Add PML documentation and examples
   - ⏳ Update quickstart guide
   - ⏳ Review and update all user-facing docs

5. **Stability and polish** (1-2 weeks) ✅ **COMPLETED**
   - ✅ Expanded PML parser tests (40 unit tests covering edge cases)
   - ✅ Added PML integration tests (5 tests for stdlib functions)
   - ✅ Improved error handling (Display trait for PmlParseError)
   - ✅ Code quality improvements (clippy, fmt) - all checks passing
   - ✅ Performance profiling (10 benchmarks, results documented)
   - ✅ Edge case testing (15+ edge cases: Unicode, long strings, deep nesting, etc.)
   - ✅ Performance analysis document created (`.pain_dev_docs/PML_PERFORMANCE.md`)

## Priority 3: Future features (v0.3.0+)

6. Tensor support: add tensor operations for ML workloads
7. Python bridge: implement Python interop for data science workflows

## Future Tasks

- Kernel DSL: implement @kernel(device="gpu") support with MLIR backend
- Profiler: CPU, GC, GPU profiling tools
- Tracing GC: generational/concurrent garbage collector
- PML v0.2: inline strings, escape sequences, nullable values
- PML v0.3: anchors, mini-templates, include directives

## Notes

**PML v0.1 Specification:**
- Tab-based indentation (1 TAB = 1 level)
- SCALAR, MAP, LIST node types
- Simple syntax: `key: value`, `- item` for lists
- Comments with `#`
- String, int, float, bool, null types
- No multiline strings, inline lists/maps, YAML references
- Target: ~250-350 lines parser implementation

**VS Code/Cursor Extension:**
- ✅ Extension moved to separate repository (`pain-vscode`) - https://github.com/pain-lng/pain-vscode
- ✅ PML syntax highlighting and language support added
- ✅ Custom file icons for `.pain` and `.pml` files implemented
- ✅ VSIX distribution via repository (marketplace publication postponed)

**Documentation:**
- ✅ LSP server ready - can show doc comments in hover tooltips
- ✅ Standard library ready - have API to document
- ✅ Doc comments syntax and auto-documentation generation - completed

**Performance Benchmarks:**
- Phase 1: ✅ Basic infrastructure after code generation (completed)
- Phase 2: ✅ Numerical benchmarks after stdlib (completed)
- Phase 3: ML benchmarks after tensor support
- Phase 4: HPC benchmarks after optimization passes
- Phase 5: ✅ Comparison suite with Python/Rust/C++ (completed)

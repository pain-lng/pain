# Active Tasks (≤7)

## Priority 1: Critical for v0.2.0 release

1. **PML v0.1 — Pain Markup Language** (2-3 weeks)
   - ⏳ Design PML AST structure (PmlNode with SCALAR/MAP/LIST)
   - ⏳ Implement PML lexer (tab-based indentation, comments, key-value parsing)
   - ⏳ Implement PML parser (build PmlNode tree from tokens)
   - ⏳ Add PML stdlib module (`pml.load_file`, `pml.parse`, node accessors)
   - ⏳ Write PML specification document
   - ⏳ Add PML examples and tests
   - **Goals**: Minimalist declarative format for UI/configs, simpler than YAML, easy to parse in Pain

2. **VS Code Extension: Marketplace publication** (1 week)
   - ⏳ Finalize extension metadata and assets
   - ⏳ Prepare marketplace listing (description, screenshots, changelog)
   - ⏳ Publish to VS Code marketplace
   - ⏳ Update installation documentation

3. **Release preparation** (1 week)
   - ⏳ Final testing and bug fixes
   - ⏳ Update CHANGELOG.md with v0.2.0 changes
   - ⏳ Prepare release notes
   - ⏳ Tag v0.2.0 release

## Priority 2: Important for v0.2.0 release

4. **Documentation updates** (1 week)
   - ⏳ Update main README with v0.2.0 features
   - ⏳ Add PML documentation and examples
   - ⏳ Update quickstart guide
   - ⏳ Review and update all user-facing docs

5. **Stability and polish** (1-2 weeks)
   - ⏳ Fix any critical bugs found during testing
   - ⏳ Improve error messages where needed
   - ⏳ Performance profiling and optimizations
   - ⏳ Code quality improvements (clippy, fmt)

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
- ⏳ Ready for marketplace publication

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

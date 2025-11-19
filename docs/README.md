# Pain Documentation

This directory hosts user-facing documentation shipped with the main repository.  
Every guide stays close to the code so that feature and doc updates evolve together.

## Contents

- [`quickstart.md`](quickstart.md) – install prerequisites, run the compiler, use `painpkg`.
- [`stdlib.md`](stdlib.md) – high-level API reference for the bundled standard library.
- [`examples.md`](examples.md) – runnable snippets that exercise common Pain features.

## Regenerating API Docs

Use the compiler’s built-in generator to refresh doc comments when stdlib changes:

```bash
cargo run -p pain-compiler -- doc --stdlib
```

Artifacts can live next to the relevant crate (e.g. `pain-compiler/docs/`) or be published via CI/CD.  
For now we keep curated Markdown sources here; generated HTML/JSON output should remain in `target/` or release assets.

## Contributing

1. Keep docs in sync with code changes—reference concrete commands, file paths, and flags.
2. Prefer short runnable samples; add links back to source files when duplication would be large.
3. Validate shell commands on at least one OS in the CI matrix (Windows, Linux, or macOS).
4. If documentation grows substantially (tutorials, website), revisit whether a separate repo is needed.



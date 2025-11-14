# Pain Language VS Code Extension

VS Code extension for Pain programming language.

## Features

- ✅ Syntax highlighting
- ✅ LSP integration (diagnostics, completion, hover)
- ✅ Error checking
- ✅ Language configuration (comments, brackets, auto-closing)

## Installation

### Development Setup

1. Install dependencies:
```bash
cd pain-vscode
npm install
```

2. Build the extension:
```bash
npm run compile
```

3. Run in VS Code:
   - Open `pain-vscode` folder in VS Code
   - Press F5 to open Extension Development Host
   - Open a `.pain` file to test

### Building LSP Server

The extension requires the `pain-lsp` executable. Build it first:

```bash
# From workspace root
cargo build --package pain-lsp

# Or for release
cargo build --release --package pain-lsp
```

The extension will automatically detect the LSP server in:
- `target/debug/pain-lsp` (development)
- `target/release/pain-lsp` (release)
- Or use `pain.lsp.path` setting to specify custom path

## Configuration

Set `pain.lsp.path` in VS Code settings to specify custom path to LSP server executable.

## Package and Install

To create a distributable package:

```bash
npm install -g vsce
vsce package
```

This creates a `.vsix` file that can be installed in VS Code.

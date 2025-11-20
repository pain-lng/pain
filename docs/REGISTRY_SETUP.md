# Pain Registry Setup Guide

This guide explains how to initialize the `pain-registry` repository for the first time.

## Quick Start

The `pain-registry` repository is already created at: https://github.com/pain-lng/pain-registry

To initialize it with the proper structure:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/pain-lng/pain-registry.git
   cd pain-registry
   ```

2. **Create directory structure**:
   ```bash
   mkdir -p index packages
   touch index/.gitkeep packages/.gitkeep
   ```

3. **Copy template files** from the Pain repository:
   - The registry structure is already initialized in `pain-registry/` directory
   - If needed, copy files from `pain-registry/` to your cloned repository

4. **Commit and push**:
   ```bash
   git add .
   git commit -m "Initial registry structure"
   git push origin main
   ```

## Alternative: Manual Setup

If you prefer to set up manually:

1. **Create directories**:
   ```
   index/
   packages/
   ```

2. **Create README.md** (see `pain-registry/README.md`)

3. **Create .gitignore** (see `pain-registry/.gitignore`)

4. **Add .gitkeep files** to keep empty directories in git:
   ```
   index/.gitkeep
   packages/.gitkeep
   ```

## Verification

After setup, verify the structure:

```bash
painpkg search test
```

This should work without errors (even if no packages are found).

## Next Steps

Once the registry is initialized:

- Users can publish packages with `painpkg publish`
- Users can install packages with `painpkg install`
- Users can search packages with `painpkg search`

See [docs/REGISTRY.md](REGISTRY.md) for detailed usage instructions.


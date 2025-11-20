# Pain Package Registry

The Pain Package Registry is a GitHub-based package registry for the Pain programming language. It provides a simple, decentralized way to discover and install packages.

## Registry Structure

The registry follows a hierarchical structure similar to Cargo's crates.io:

```
pain-registry/
├── index/           # Hierarchical index for fast package lookup
│   └── p/
│       └── pa/
│           └── pain-math
├── packages/        # Package metadata files
│   └── pain-math/
│       ├── 0.1.0.toml
│       └── 0.2.0.toml
└── README.md
```

### Index Structure

The index uses a hierarchical path structure based on package names:
- 1 character: `index/p/`
- 2 characters: `index/p/pa/`
- 4 characters: `index/p/pa/pain/`
- Full name: `index/p/pa/pain/pain-math`

Each index file contains one version per line (newest first).

### Package Metadata Format

Package metadata is stored in TOML format at `packages/{name}/{version}.toml`:

```toml
name = "pain-math"
version = "0.1.0"
description = "Mathematical functions for Pain"
repository = "https://github.com/user/pain-math.git"
license = "MIT OR Apache-2.0"
authors = ["Author Name <author@example.com>"]

[dependencies]
pain-std = "^0.1.0"
```

## Publishing Packages

### Prerequisites

1. Your package must be in a Git repository
2. The repository must have a `pain.toml` manifest file
3. You must have git configured with credentials for pushing to GitHub

### Publishing Process

1. **Prepare your package**:
   ```bash
   cd your-package
   # Ensure pain.toml is valid
   painpkg publish
   ```

2. **The publish command will**:
   - Validate your `pain.toml` manifest
   - Clone/update the registry repository
   - Create package metadata file
   - Update the index
   - Create a new branch
   - Commit and push changes
   - Provide a link to create a PR

3. **Create a Pull Request**:
   - Follow the link provided by `painpkg publish`
   - Or manually create a PR at: https://github.com/pain-lng/pain-registry/pulls
   - Wait for review and merge

### Manual Publishing

If you prefer to publish manually:

```bash
# Clone the registry
git clone https://github.com/pain-lng/pain-registry.git
cd pain-registry

# Create package metadata
# (Use painpkg publish to generate this automatically)

# Create index entry
# (Use painpkg publish to generate this automatically)

# Commit and push
git checkout -b publish-my-package-0.1.0
git add packages/my-package/0.1.0.toml index/...
git commit -m "Add my-package v0.1.0"
git push -u origin publish-my-package-0.1.0

# Create PR on GitHub
```

## Installing Packages

Packages are installed from their Git repositories:

```bash
# Install a package
painpkg add pain-math

# Install specific version
painpkg add pain-math --version "^0.1.0"

# Install all dependencies
painpkg install
```

The package manager will:
1. Clone the registry to find package metadata
2. Read the repository URL from metadata
3. Clone the package repository
4. Checkout the appropriate version tag (e.g., `v0.1.0`)
5. Install the package to `.pain/packages/`

## Searching Packages

Search for packages by name or description:

```bash
painpkg search math
painpkg search "linear algebra"
```

## Versioning

Packages must follow [Semantic Versioning](https://semver.org/):
- **MAJOR.MINOR.PATCH** (e.g., `1.2.3`)
- Version tags in Git should be prefixed with `v` (e.g., `v1.2.3`)

## Best Practices

1. **Use meaningful descriptions**: Help users find your package
2. **Tag releases**: Always create Git tags for published versions
3. **Keep dependencies up to date**: Update your package's dependencies regularly
4. **Follow naming conventions**: Use lowercase with hyphens (e.g., `pain-math`)
5. **Include a README**: Add a README.md to your repository

## Registry Maintenance

The registry is maintained by the Pain Language team. PRs are reviewed for:
- Valid package metadata
- Proper versioning
- Repository accessibility
- License compliance

## Limitations

- **No automatic updates**: You must manually publish new versions
- **No package hosting**: Packages are stored in their own Git repositories
- **No version deletion**: Once published, versions cannot be removed (yanked versions may be added in the future)

## Future Improvements

- Automated PR creation via GitHub API
- Package yanking (marking versions as deprecated)
- Package statistics and download counts
- Web interface for browsing packages
- Package verification and security scanning

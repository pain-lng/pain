# Development Flow

This repository now follows a lightweight Git Flow:

1. `main`
   - Stable only; releases are tagged here.
   - Protected: PR + status checks required before merge; no direct pushes.
2. `develop`
   - Integration branch. All feature branches merge here after CI passes.
3. `feature/<topic>`
   - Branch off `develop` for each task/issue. Merge via PR → `develop`.

CI expectations:

| Branch pattern | Jobs (current) | Notes |
| --- | --- | --- |
| `feature/*` | fmt, clippy, tests (Linux/Windows/macOS) | No release artifacts |
| `develop` | same as feature | Acts as gate before `main` |
| `main` | same as develop (plus future release steps) | Publish artifacts when ready |

## Branch Protection Checklist

In GitHub → Settings → Branches → Branch protection rules (for `main`):

1. ✅ Require pull request reviews before merging (min 1).
2. ✅ Require status checks to pass before merging — select the CI jobs (e.g. `ci-linux`, `ci-windows`, `ci-macos`).
3. ✅ (Optional but recommended) Restrict direct pushes to admins only.

Repeat the status-check requirement for `develop` once it is the primary integration branch in PRs to `main`.

## Working on a Feature

```bash
git checkout develop
git pull
git checkout -b feature/<short-name>
# ... work, commit ...
git push -u origin feature/<short-name>
# Open PR: feature → develop
```

After `develop` is ready for release:

```bash
git checkout develop
git pull
git checkout main
git merge --no-ff develop
git tag vX.Y.Z
git push origin main vX.Y.Z
```

CI must be green on the target branch before merging at every step.


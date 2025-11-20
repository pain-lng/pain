# JIT Compilation Setup

## Requirements

For JIT compilation to work, you need:

1. **LLVM 21+ installed** in `C:\Program Files\LLVM` (Windows) or standard system paths
2. **Environment variable** `LLVM_SYS_211_PREFIX` pointing to LLVM installation directory
3. **Build with JIT feature**: `cargo build --features jit`

## Windows Setup

### Option 1: Pre-built Binaries from GitHub (Recommended)

1. Download LLVM from [GitHub releases](https://github.com/llvm/llvm-project/releases):
   - Go to the [LLVM 21.1.0 release page](https://github.com/llvm/llvm-project/releases/tag/llvmorg-21.1.0) (or latest 21.x)
   - **Important**: For developing software that uses LLVM (like JIT compilation), you need the **`clang+llvm-` archive**, NOT the `LLVM-` installer
   - Download: `clang+llvm-21.1.0-x86_64-pc-windows-msvc.tar.xz` (archive - this is what's available, there's no .exe installer for clang+llvm)
   - The `clang+llvm-` package includes libraries and development files needed for embedding LLVM

2. Extract LLVM archive:
   - Extract `clang+llvm-21.1.0-win64.zip` to a directory like `C:\LLVM` or `C:\Program Files\LLVM`
   - The archive contains a folder (usually `clang+llvm-21.1.0-win64`) - extract its contents or use the folder itself
   - **Note**: The `clang+llvm-` package contains development files (headers, libs, cmake) that the regular `LLVM-` installer does not include

3. Verify extraction has dev files:
   ```powershell
   # Adjust path if you extracted to a different location
   $llvmPath = "C:\LLVM\clang+llvm-21.1.0-win64"  # or wherever you extracted
   Test-Path "$llvmPath\include\llvm"  # Should be True
   Test-Path "$llvmPath\lib\cmake\llvm\LLVMConfig.cmake"  # Should be True
   ```

4. Set environment variable (permanent):
   ```powershell
   $llvmPath = "C:\LLVM\clang+llvm-21.1.0-win64"  # adjust to your path
   [System.Environment]::SetEnvironmentVariable("LLVM_SYS_211_PREFIX", $llvmPath, "User")
   ```

   Or temporarily for current session:
   ```powershell
   $env:LLVM_SYS_211_PREFIX = "C:\LLVM\clang+llvm-21.1.0-win64"  # adjust to your path
   ```

5. Build with JIT feature:
   ```bash
   cargo build --features jit
   ```

### Option 2: Using llvmenv (Alternative)

If pre-built binaries don't include dev files, use `llvmenv`:

```powershell
cargo install llvmenv
llvmenv build-entry
# This will download and build LLVM with all dev files
```

### Option 3: Using vcpkg

```powershell
vcpkg install llvm:x64-windows
$env:LLVM_SYS_211_PREFIX = "C:\vcpkg\installed\x64-windows"
```

## Linux/macOS Setup

1. Install LLVM 21+:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install llvm-21-dev
   
   # macOS
   brew install llvm@21
   ```

2. Set environment variable:
   ```bash
   export LLVM_SYS_211_PREFIX=/usr/lib/llvm-21  # Adjust path as needed
   ```

3. Build with JIT feature:
   ```bash
   cargo build --features jit
   ```

## Verification

After installation, verify that dev files are present:

```powershell
# Check for CMake config (required by llvm-sys)
Test-Path "C:\Program Files\LLVM\lib\cmake\llvm\LLVMConfig.cmake"  # Should be True

# Check for C++ headers
Test-Path "C:\Program Files\LLVM\include\llvm"  # Should be True

# Check for static libraries
Get-ChildItem "C:\Program Files\LLVM\lib\*.lib" | Select-Object -First 5
```

If these checks fail, you have a runtime-only installation and need to install the `clang+llvm-` package instead.

## Current Status

- ✅ Basic JIT engine structure with function caching
- ✅ LLVM IR generation and extraction
- ✅ Runtime code generation (compiles LLVM IR to shared libraries and loads them dynamically)
- ✅ On-stack replacement (OSR) - basic support for recompiling functions with optimizations

## Troubleshooting

If `llvm-sys` cannot find LLVM:

1. **Verify LLVM installation has development files:**
   ```bash
   clang --version  # Should show LLVM version
   ```
   
   On Windows, the standard LLVM installer may not include development files.
   You need:
   - `include/llvm/` directory with headers
   - `lib/cmake/llvm/` directory with CMake files
   - `lib/` directory with `.lib` files (Windows) or `.a` files (Unix)

2. **Check that `LLVM_SYS_211_PREFIX` points to correct directory:**
   ```bash
   echo $LLVM_SYS_211_PREFIX  # Linux/macOS
   echo $env:LLVM_SYS_211_PREFIX  # Windows PowerShell
   ```

3. **Ensure LLVM cmake files exist:**
   ```bash
   ls $LLVM_SYS_211_PREFIX/lib/cmake/llvm  # Should list cmake files
   ```
   
   If missing, you may need to:
   - Install LLVM with development files (not just runtime)
   - Use `llvmenv` to build LLVM from source
   - Or use pre-built LLVM with dev files

4. **Use `llvmenv` to manage LLVM versions (recommended):**
   ```bash
   cargo install llvmenv
   llvmenv build-entry
   ```
   
   This will download and build LLVM with all necessary development files.

5. **Alternative: Use LLVM from vcpkg (Windows):**
   ```powershell
   vcpkg install llvm:x64-windows
   $env:LLVM_SYS_211_PREFIX = "C:\vcpkg\installed\x64-windows"
   ```

## Important Notes

### Package Selection for Windows

According to the [LLVM 21.1.0 release notes](https://github.com/llvm/llvm-project/releases/tag/llvmorg-21.1.0):

> "Where `LLVM-*.exe` is an installer intended for using LLVM as a toolchain and the archive `clang+llvm-` contains the contents of the installer, plus libraries and tools not normally used in a toolchain. You most likely want the `LLVM-` installer, **unless you are developing software which itself uses LLVM**, in which case choose `clang+llvm-`."

**For JIT compilation, you MUST use the `clang+llvm-*.zip` archive**, not the regular `LLVM-*.exe` installer! The archive is the only option for `clang+llvm-` on Windows.

### LLVM Version Compatibility

- `llvm-sys = "211"` requires LLVM 21.1.x
- If you have LLVM 18.x, use `llvm-sys = "180"` instead
- Check your LLVM version: `clang --version`

### Development Files Required

The standard LLVM installer on Windows may include only runtime files. For JIT compilation, you need:
- Headers: `include/llvm/` directory
- CMake configs: `lib/cmake/llvm/` directory  
- Static libraries: `lib/*.lib` files

### If Pre-built Binaries Don't Include Dev Files

1. **Use llvmenv** (recommended for automatic setup)
2. **Build from source** using CMake (see LLVM documentation)
3. **Use vcpkg** package manager
4. **Temporarily disable JIT** feature until dev files are available

For more information, see the [LLVM download page](https://releases.llvm.org/download.html) and check GitHub releases for packages with development files.


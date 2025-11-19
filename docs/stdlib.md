# Standard Library Overview

Pain ships with a batteries-included stdlib implemented inside `pain-compiler/src/stdlib.rs`.  
This document summarizes the public surface area grouped by category. All functions are available
without imports inside Pain source files.

## Notation

- `int`, `float64`, `bool`, `str`, `list[T]`, `array[T]`, `map[K, V]` follow Pain’s type names.
- `dynamic` indicates runtime-dispatched values.

## Math

| Function | Signature | Description |
| --- | --- | --- |
| `abs` | `fn abs(x: int) -> int` | Integer absolute value |
| `abs` | `fn abs(x: float64) -> float64` | Floating-point absolute value |
| `min`, `max` | `fn min(a: int, b: int) -> int` | Choose smaller/greater integer |
| `sqrt` | `fn sqrt(x: float64) -> float64` | Square root (expects non-negative) |
| `pow` | `fn pow(base: float64, exp: float64) -> float64` | Exponentiation |
| `sin`, `cos` | `fn sin(x: float64) -> float64` | Trigonometry in radians |
| `floor`, `ceil` | `fn floor(x: float64) -> float64` | Rounds down/up |

## Strings

| Function | Signature | Description |
| --- | --- | --- |
| `len` | `fn len(s: str) -> int` | Number of code units in a string |
| `concat` | `fn concat(a: str, b: str) -> str` | Equivalent to `a + b` |
| `substring` | `fn substring(s: str, start: int, end: int) -> str` | End index is exclusive |
| `contains` | `fn contains(s: str, needle: str) -> bool` | Substring test |
| `starts_with`, `ends_with` | `fn starts_with(s: str, prefix: str) -> bool` | Prefix/suffix checks |
| `trim` | `fn trim(s: str) -> str` | Removes leading/trailing whitespace |
| `to_int` | `fn to_int(s: str) -> int` | Parses decimal integer |
| `to_float` | `fn to_float(s: str) -> float64` | Parses decimal float |
| `to_string` | `fn to_string(x: int) -> str` | Integer → string |

Example:

```pain
fn normalize(username: str) -> str:
    let trimmed = trim(username)
    if len(trimmed) == 0:
        return "anonymous"
    return to_string(len(trimmed)) + ":" + trimmed
```

## Collections

| Function | Signature | Description |
| --- | --- | --- |
| `len` | `fn len(items: list[dynamic]) -> int` | Works for lists |
| `len` | `fn len(items: array[dynamic]) -> int` | Works for arrays |

Currently mutation helpers (`push`, `pop`) are wired in the runtime but not yet exposed through `StdlibFunction`; add them here once implemented.

## I/O

| Function | Signature | Description |
| --- | --- | --- |
| `print` | `fn print(value: dynamic) -> dynamic` | Sends textual representation to stdout |

## Extending the Stdlib

1. Modify `pain-compiler/src/stdlib.rs`.
2. Document the new API (doc comments + this file) and add integration coverage.
3. Regenerate machine docs if needed: `pain doc --stdlib --output docs/generated-stdlib.md`.

All stdlib values piggyback on `pain-runtime`, so keep types aligned (e.g., prefer `Type::Float64` over ad-hoc enums). When adding categories, expand this file with new tables so users can discover capabilities without reading Rust sources.


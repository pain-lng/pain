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

### Lists and Arrays

Lists (`list[T]`) are dynamic, growable collections. Arrays (`array[T]`) are fixed-size collections (currently implemented similarly to lists in the runtime).

| Function | Signature | Description |
| --- | --- | --- |
| `len` | `fn len(items: list[dynamic]) -> int` | Returns the length of a list |
| `len` | `fn len(items: array[dynamic]) -> int` | Returns the length of an array |

**List/Array Literals:**
```pain
let numbers = [1, 2, 3, 4, 5]  # list[int]
let names = ["Alice", "Bob"]    # list[str]
```

**Indexing:**
```pain
let first = numbers[0]          # Access element at index
numbers[0] = 10                 # Modify element (if mutable)
```

**Note:** Mutation helpers (`push`, `pop`) are recognized by the type checker but not yet fully implemented in stdlib. They will be added in a future release.

## Classes and Objects

Classes are user-defined types with fields and methods. They are part of the language syntax, not stdlib functions.

**Class Definition:**
```pain
class Point:
    let x: int
    let y: int
    
    fn distance() -> float64:
        return sqrt(x * x + y * y)
```

**Object Creation:**
```pain
let p = new Point(10, 20)  # Create instance
let x = p.x                 # Access field
p.x = 30                    # Modify field (if mutable)
let d = p.distance()        # Call method
```

**Class Features:**
- Fields: typed member variables (`let name: type`)
- Methods: functions associated with the class
- Constructors: use `new ClassName(...)` syntax
- `self` keyword: reference to the current instance in methods

See [`examples.md`](examples.md) for complete class examples.

## I/O

| Function | Signature | Description |
| --- | --- | --- |
| `print` | `fn print(value: dynamic) -> dynamic` | Sends textual representation to stdout |

## PML (Pain Markup Language)

PML is a minimalistic declarative data format for configurations, UI structures, and tree data. PML files use tab-based indentation and support SCALAR, MAP, and LIST node types.

| Function | Signature | Description |
| --- | --- | --- |
| `pml_load_file` | `fn pml_load_file(path: str) -> dynamic` | Loads and parses a PML file, returns parsed tree as dynamic object |
| `pml_parse` | `fn pml_parse(source: str) -> dynamic` | Parses PML string, returns parsed tree as dynamic object |

**Example:**
```pain
fn main():
    # Load PML file
    let config = pml_load_file("config.pml")
    let app_name = config.app.name
    let port = config.app.port
    
    # Parse PML string
    let pml_source = "title: \"Hello\"\nwidth: 400"
    let doc = pml_parse(pml_source)
    let title = doc.title
```

**PML File Example (config.pml):**
```pml
app:
	name: "My Application"
	version: "1.0.0"
	debug: false
	port: 8080
```

See [`PML_SPEC.md`](PML_SPEC.md) for complete PML syntax specification and [`examples_pml.md`](examples_pml.md) for more usage examples.

## Extending the Stdlib

1. Modify `pain-compiler/src/stdlib.rs`.
2. Document the new API (doc comments + this file) and add integration coverage.
3. Regenerate machine docs if needed: `pain doc --stdlib --output docs/generated-stdlib.md`.

All stdlib values piggyback on `pain-runtime`, so keep types aligned (e.g., prefer `Type::Float64` over ad-hoc enums). When adding categories, expand this file with new tables so users can discover capabilities without reading Rust sources.


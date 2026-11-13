# Example Programs

Use these snippets as starting points for demos, regression tests, or onboarding new users.  
Every example is self-contained; copy into `examples/*.pain` and run with `pain run`.

## 1. I love Pain

```pain
fn main():
    print("I love Pain!")
```

Run:

```bash
pain run --input examples/hello.pain
```

## 2. Fibonacci (Iterative)

```pain
fn fibonacci(n: int) -> int:
    if n <= 1:
        return n

    let a = 0
    let b = 1
    let i = 2

    while i <= n:
        let temp = a + b
        a = b
        b = temp
        i = i + 1

    return b

fn main() -> int:
    return fibonacci(10)
```

Demonstrates loops, mutation, and return values.

## 3. Classes & Methods

```pain
class Counter:
    let value: int

    fn increment():
        self.value = self.value + 1

    fn get() -> int:
        return self.value

fn main() -> int:
    let counter = new Counter(0)
    counter.increment()
    counter.increment()
    return counter.get()
```

Shows class fields, methods, and object creation: `new Counter(0)` fills the fields in declaration order.

## 4. Lists and Arrays

```pain
fn main() -> int:
    let numbers = [1, 2, 3, 4, 5]  # list[int]
    let sum = 0
    let i = 0
    
    while i < len(numbers):
        sum = sum + numbers[i]
        i = i + 1
    
    return sum
```

Demonstrates list literals, indexing, and iteration.

## 5. Full Pipeline Smoke Test

```pain
fn sum(n: int) -> int:
    let total = 0
    let i = 0
    while i <= n:
        total = total + i
        i = i + 1
    return total

fn main() -> int:
    return sum(10)
```

Exercise parsing, type checking, IR, optimization, and codegen:

```bash
# LLVM IR
pain build --input examples/sum.pain --backend llvm --output sum.ll

# MLIR
pain build --input examples/sum.pain --backend mlir --output sum.mlir
```

## 6. painpkg Workspace

```bash
painpkg init demo_app
cd demo_app
cat > src/main.pain <<'EOF'
fn main():
    print("demo")
EOF
painpkg install
painpkg run
```

Uses the package manager to scaffold, resolve dependencies, and execute the entrypoint.

## Modules

A program can be split into files. A module is a file; `import` lists the names it
takes from a module, and only items marked `pub` can be imported.

`combat.pain`:

```pain
pub class Unit:
    let hp: int
    let attack: int

pub fn strike(attacker: Unit, seed: int) -> int:
    return clamp(attacker.attack + seed, 1, 99)

fn clamp(value: int, low: int, high: int) -> int:
    if value < low:
        return low
    if value > high:
        return high
    return value
```

`main.pain`:

```pain
import combat: strike, Unit

fn main() -> int:
    var knight = new Unit(40, 9)
    return strike(knight, 5)
```

Rules:

- There is one import form: `import module: name, name`. Every imported name is
  listed; there are no wildcards and no aliases.
- `import ai.target: pick` reads `ai/target.pain`. Paths start at the directory of
  the file you run, or at `src/` inside a package with `pain.toml`.
- Imports come first in a file, before functions and classes.
- `clamp` above has no `pub`, so it is private: importing it is an error, and
  another file may define its own `clamp`.
- Import cycles are errors.

```bash
pain run --input main.pain                       # loads combat.pain as well
pain query callers strike --input main.pain      # call sites in every file
```

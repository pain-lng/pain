# Example Programs

Use these snippets as starting points for demos, regression tests, or onboarding new users.  
Every example is self-contained; copy into `examples/*.pain` and run with `pain-compiler run`.

## 1. I love Pain

```pain
fn main():
    print("I love Pain!")
```

Run:

```bash
pain-compiler run --input examples/hello.pain
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

    fn new(start: int) -> Counter:
        let c = Counter()
        c.value = start
        return c

    fn increment():
        self.value = self.value + 1

    fn get() -> int:
        return self.value

fn main() -> int:
    let counter = Counter.new(0)
    counter.increment()
    counter.increment()
    return counter.get()
```

Shows class fields, methods, and constructors.

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
pain-compiler build --input examples/sum.pain --backend llvm --output sum.ll

# MLIR
pain-compiler build --input examples/sum.pain --backend mlir --output sum.mlir
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


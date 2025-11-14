use criterion::{black_box, criterion_group, criterion_main, Criterion};
use pain_compiler::{parse, type_check_program, Interpreter, IrBuilder, CodeGenerator, Optimizer};

fn factorial_interpreter(n: i64) -> i64 {
    let source = format!(
        r#"
fn fact(n: int) -> int:
    if n <= 1:
        return 1
    return n * fact(n - 1)

fn main() -> int:
    return fact({})
"#,
        n
    );

    let program = parse(&source).unwrap();
    type_check_program(&program).unwrap();
    
    let mut interpreter = Interpreter::new().unwrap();
    match interpreter.interpret(&program).unwrap() {
        pain_runtime::Value::Int(result) => result,
        _ => panic!("Expected integer result"),
    }
}

fn factorial_compiled(n: i64) -> i64 {
    let source = format!(
        r#"
fn fact(n: int) -> int:
    if n <= 1:
        return 1
    return n * fact(n - 1)

fn main() -> int:
    return fact({})
"#,
        n
    );

    let program = parse(&source).unwrap();
    type_check_program(&program).unwrap();
    
    let ir_builder = IrBuilder::new();
    let mut ir = ir_builder.build(&program);
    ir = Optimizer::optimize(ir);
    
    let codegen = CodeGenerator::new(ir);
    let _llvm_ir = codegen.generate();
    
    // TODO: Compile LLVM IR to executable and run
    0 // Placeholder
}

fn benchmark_factorial(c: &mut Criterion) {
    let mut group = c.benchmark_group("factorial");
    
    // Benchmark interpreter
    group.bench_function("interpreter_n10", |b| {
        b.iter(|| factorial_interpreter(black_box(10)))
    });
    
    group.bench_function("interpreter_n15", |b| {
        b.iter(|| factorial_interpreter(black_box(15)))
    });
    
    // Benchmark compiled (when available)
    // group.bench_function("compiled_n10", |b| {
    //     b.iter(|| factorial_compiled(black_box(10)))
    // });
    
    group.finish();
}

criterion_group!(benches, benchmark_factorial);
criterion_main!(benches);


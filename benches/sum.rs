use criterion::{black_box, criterion_group, criterion_main, Criterion};
use pain_compiler::{parse, type_check_program, Interpreter, IrBuilder, CodeGenerator, Optimizer};

fn sum_interpreter(n: i64) -> i64 {
    let source = format!(
        r#"
fn sum(n: int) -> int:
    var result = 0
    var i = 0
    while i <= n:
        result = result + i
        i = i + 1
    return result

fn main() -> int:
    return sum({})
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

fn sum_compiled(n: i64) -> i64 {
    let source = format!(
        r#"
fn sum(n: int) -> int:
    var result = 0
    var i = 0
    while i <= n:
        result = result + i
        i = i + 1
    return result

fn main() -> int:
    return sum({})
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

fn benchmark_sum(c: &mut Criterion) {
    let mut group = c.benchmark_group("sum");
    
    // Benchmark interpreter
    group.bench_function("interpreter_n1000", |b| {
        b.iter(|| sum_interpreter(black_box(1000)))
    });
    
    group.bench_function("interpreter_n10000", |b| {
        b.iter(|| sum_interpreter(black_box(10000)))
    });
    
    // Benchmark compiled (when available)
    // group.bench_function("compiled_n1000", |b| {
    //     b.iter(|| sum_compiled(black_box(1000)))
    // });
    
    group.finish();
}

criterion_group!(benches, benchmark_sum);
criterion_main!(benches);


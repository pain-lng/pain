// Sum benchmark for Rust

fn sum_n(n: i64) -> i64 {
    let mut result = 0;
    let mut i = 0;
    while i <= n {
        result = result + i;
        i = i + 1;
    }
    result
}

fn main() {
    let n = std::env::args()
        .nth(1)
        .and_then(|s| s.parse().ok())
        .unwrap_or(10000);
    let result = sum_n(n);
    println!("{}", result);
}


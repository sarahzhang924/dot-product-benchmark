// 第04讲：Scaled Dot-Product 三语言对比
// 用法：OnlineGDB 语言选 Rust，粘进去点 Run
// 输出：每个规模一行，含校验和与 5 轮中位数耗时

use std::time::Instant;

const ROUNDS: usize = 5;

fn gen_data(n: usize) -> (Vec<f64>, Vec<f64>) {
    let mut a = vec![0.0f64; n];
    let mut b = vec![0.0f64; n];
    let mut seed: u64 = 42;
    let m: u64 = 2147483648;
    for i in 0..n {
        seed = (1103515245u64.wrapping_mul(seed).wrapping_add(12345)) % m;
        a[i] = seed as f64 / 2147483648.0;
        seed = (1103515245u64.wrapping_mul(seed).wrapping_add(12345)) % m;
        b[i] = seed as f64 / 2147483648.0;
    }
    (a, b)
}

fn dot(a: &[f64], b: &[f64]) -> f64 {
    let mut s = 0.0f64;
    for i in 0..a.len() {
        s += a[i] * b[i];
    }
    s
}

fn main() {
    for &n in &[10000usize, 100000, 1000000] {
        let (a, b) = gen_data(n);

        let mut res = dot(&a, &b); // 预热

        let mut t: Vec<f64> = Vec::with_capacity(ROUNDS);
        for _ in 0..ROUNDS {
            let t0 = Instant::now();
            res = dot(&a, &b);
            t.push(t0.elapsed().as_secs_f64());
        }
        t.sort_by(|x, y| x.partial_cmp(y).unwrap());

        println!("Rust    N={:<8} checksum={:.9} median={:.6}s", n, res, t[ROUNDS / 2]);
    }
}

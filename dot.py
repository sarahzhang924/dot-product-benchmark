# 第04讲：Scaled Dot-Product 三语言对比
# 用法：OnlineGDB 选 Python 3，粘进去点 Run
# 输出：每个规模一行，含校验和与 5 轮中位数耗时

import time
import statistics

N_LIST = (10000, 100000, 1000000)
ROUNDS = 5


def gen_data(n):
    """固定种子的线性同余生成器：三种语言用同一个算法，数组逐位相同。"""
    a = [0.0] * n
    b = [0.0] * n
    seed = 42
    M = 2147483648
    for i in range(n):
        seed = (1103515245 * seed + 12345) % M
        a[i] = seed / M
        seed = (1103515245 * seed + 12345) % M
        b[i] = seed / M
    return a, b


def dot(a, b):
    """显式循环，和 C / Rust 的写法保持同一口径，方便比较。"""
    s = 0.0
    n = len(a)
    for i in range(n):
        s += a[i] * b[i]
    return s


def main():
    for n in N_LIST:
        a, b = gen_data(n)
        dot(a, b)                      # 预热：先把缓存和分支预测喂热，结果丢掉

        times = []
        for _ in range(ROUNDS):
            t0 = time.perf_counter()
            res = dot(a, b)
            times.append(time.perf_counter() - t0)

        med = statistics.median(times)
        print(f"Python  N={n:<8d} checksum={res:.9f} median={med:.6f}s")


if __name__ == "__main__":
    main()

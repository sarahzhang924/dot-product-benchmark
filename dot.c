/* 第04讲：Scaled Dot-Product 三语言对比
 * 用法：OnlineGDB 语言选 C，点顶部齿轮把 Compiler Options 设成 -O2，再 Run
 * 输出：每个规模一行，含校验和与 5 轮中位数耗时
 */
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define ROUNDS 5

static void gen_data(int n, double *a, double *b) {
    long long seed = 42;
    const long long M = 2147483648LL;
    for (int i = 0; i < n; i++) {
        seed = (1103515245LL * seed + 12345) % M;
        a[i] = (double)seed / 2147483648.0;
        seed = (1103515245LL * seed + 12345) % M;
        b[i] = (double)seed / 2147483648.0;
    }
}

static double dot(const double *a, const double *b, int n) {
    double s = 0.0;
    for (int i = 0; i < n; i++) {
        s += a[i] * b[i];
    }
    return s;                     /* 结果必须返回并打印，否则 -O2 会删掉整段循环 */
}

static int cmp_double(const void *x, const void *y) {
    double a = *(const double *)x, b = *(const double *)y;
    return (a > b) - (a < b);
}

int main(void) {
    int sizes[3] = {10000, 100000, 1000000};

    for (int s = 0; s < 3; s++) {
        int n = sizes[s];
        double *a = malloc(n * sizeof(double));
        double *b = malloc(n * sizeof(double));
        gen_data(n, a, b);

        double res = dot(a, b, n);          /* 预热一轮，结果丢掉 */

        double t[ROUNDS];
        for (int k = 0; k < ROUNDS; k++) {
            clock_t t0 = clock();
            res = dot(a, b, n);
            t[k] = (double)(clock() - t0) / CLOCKS_PER_SEC;
        }

        qsort(t, ROUNDS, sizeof(double), cmp_double);
        printf("C       N=%-8d checksum=%.9f median=%.6fs\n", n, res, t[ROUNDS / 2]);

        free(a);
        free(b);
    }
    return 0;
}

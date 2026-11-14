# 第04讲：5 个边界用例
# 用法：OnlineGDB 选 Python 3，粘进去点 Run，把输出截图放进报告第四部分

import math


def dot(a, b):
    if len(a) != len(b):
        raise ValueError("两个向量长度不一致")
    s = 0.0
    for x, y in zip(a, b):
        s += x * y
    return s


def check(name, ok, detail=""):
    print(f"[{'PASS' if ok else 'FAIL'}] {name}{('  ' + detail) if detail else ''}")
    return ok


def main():
    all_ok = True

    # 1. n = 0：空向量，点积应为 0
    all_ok &= check("n=0 空向量", dot([], []) == 0.0, "得到 0.0")

    # 2. n = 1：单元素
    all_ok &= check("n=1 单元素", abs(dot([3.0], [4.0]) - 12.0) < 1e-12, "3*4=12")

    # 3. 长度不匹配：必须抛异常，而不是悄悄算一半
    try:
        dot([1.0, 2.0], [1.0])
        all_ok = check("长度不匹配", False, "没有抛异常")
    except ValueError:
        all_ok &= check("长度不匹配", True, "正确抛出 ValueError")

    # 4. 全零向量：结果必须是 0，不能是 NaN
    all_ok &= check("全零向量", dot([0.0] * 10, [1.0] * 10) == 0.0, "得到 0.0")

    # 5. 含 NaN：结果应为 NaN，且不崩溃
    r = dot([float("nan"), 1.0], [1.0, 1.0])
    all_ok &= check("含 NaN 输入", math.isnan(r), "结果为 NaN，程序未崩溃")

    print()
    print("全部通过" if all_ok else "存在失败用例")


if __name__ == "__main__":
    main()

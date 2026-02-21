def f_rec(n):
    if n == 0 or n == 1:
        return 1
    return n * f_rec(n-1)


def f_it(n):
    res = 1
    for i in range(2, n+1):
        res *= i

    return res


from itertools import accumulate
import operator
from collections import deque


def f_acc(n):
    res = 1
    for j in accumulate(range(2, n+1), operator.mul):
        res = j

    return res


def f_acc_fast(n):
    return deque(accumulate(range(2, n+1), operator.mul), maxlen=1)[0] if n >= 2 else 1


if __name__ == "__main__":
    n = int(input().strip())   # reads from CPH "Input" box
    print(f_acc_fast(n))
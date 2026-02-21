# n = 4
# 4 = 1 + 1 + 1 + 1
# 4 = 1 + 1 + 2
# 4 = 1 + 2 + 1
# 4 = 2 + 1 + 1
# 4 = 2 + 2

# 1 + 1 + 2
# 2 + 2

# 1 + 1 + 1 + 1
# 1 + 2 + 1
# 2 + 1 + 1

def f_rec(n):
    if n < 0:
        return 0
    elif n == 0:
        return 1
    else:
        return f_rec(n-1) + f_rec(n-2) + f_rec(n-5)


from functools import lru_cache

@lru_cache(maxsize=128)
def f_memo(n):
    if n < 0:
        return 0
    elif n == 0:
        return 1
    else:
        return f_memo(n-1) + f_memo(n-2) + f_memo(n-5)


def f_it(n):
    dp = [0] * (n + 2)
    dp[0] = 0
    dp[1] = 1

    for i in range(2, n + 2):
        dp[i] = dp[i-1] + dp[max(0, i-2)] + dp[max(0, i-5)]

    return dp[n+1]


if __name__ == "__main__":
    n = int(input().strip())   # reads from CPH "Input" box
    print(f_it(n))

'''
PROBLEM:
Factorize large N into 2 close prime p and q (N = pq):
      |p - q| < c * N^(1/4)
Let A = (p + q) / 2
      A - sqrt(N) = (A^2 - N)/(A + sqrt(N)
                  < c^2 / 8
=> A = sqrt(N) + y
          (If c <= 2 -> y = 1)
p = A - x, q = A + x, x in Z
N = pq = (A - x)(A + x)
=> x = sqrt(A^2 - N)
y satisfy: A^2 - N is true square
'''

import gmpy2 as gmp

def factor(N: int, c: int = 2) -> tuple[int, int]:
    A = gmp.isqrt(N) + 1
    for _ in range(1 + (c * c >> 3)):
        if gmp.is_square(A * A - N):
            x = gmp.isqrt(A * A - N)
            return A - x, A + x
        A += 1
    return 1, 1
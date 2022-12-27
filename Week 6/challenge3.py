'''
PROBLEM:
Factorize large N into 2 close prime p and q (N = pq):
      1 < |a.p - b.q| < c * N^(1/4)
where a, b, c are constants

Let A = (a.p + b.q) / 2, B = ab.N
-> A >= B
-> A - sqrt(B) = (A^2 - B)/(A + sqrt(B))
      <= (ap - bq)^2 / 8(sqrt(B))
      < c^2 / 8sqrt(ab)
=> A = B + y
          (If c <= 2 -> y = 1)

When: (a.p + b.q) not even, A = (a.p + b.q - 1) / 2, also satisfy:
A - sqrt(B) < c^2 / 8sqrt(ab)

If ap < bq:
ap = A - x, bq = A + 1 + x, x in Z
B = ap.bq = (A - x)(A + 1 + x)
=> x^2 + x + (B - A^2 - A) = 0
=> x = (-1 + sqrt(1 + 4(A^2 + A - B))) / 2
y satisfy: 1 + 4(A^2 + A - B)) is true square (always odd)
'''
import gmpy2 as gmp

def factor(N: int, a: int, b: int, c: int) -> tuple[int, int]:
    B = a * b * N
    A = gmp.isqrt(B)
    
    for _ in range(1 + (c * c >> 3)):
        t = 1 + 4 * (A * A + A - B)
        if gmp.is_square(t):
            x = gmp.divexact(gmp.isqrt(t) - 1, 2)
            if gmp.is_divisible(A - x, a):
                p = gmp.divexact(A - x, a)
                q = gmp.divexact(A + x + 1, b)
            elif gmp.is_divisible(A - x, b):
                p = gmp.divexact(A - x, b)
                q = gmp.divexact(A + x + 1, a)
            else:
                continue
            return min(p, q), max(p, q)
        A += 1
    return 1, 1
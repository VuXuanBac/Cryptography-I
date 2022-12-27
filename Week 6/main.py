from gmpy2 import mpz
import challenge2, challenge3, challenge4
# GMPY2 Documents:
# 1. gcd(...), lcm(...)
# 2. f_mod(x, m)                x mod m
# 3. gg.invert(x, m)            x ^ -1
# 4. gg.powmod(x, y, m)         x ^ y mod m
# 5. gg.divm(x, y, m)           x * y^-1 mod m
# 6. gg.is_congruent(x, y, m)
# 7. gg.gcdext(x, y)            gcd, a, b

with open('./nums.txt', 'r') as file:
    N1 = mpz(file.readline())
    N2 = mpz(file.readline())
    N3 = mpz(file.readline())
    cipher4 = mpz(file.readline())

print('====== Challenge 1 ======')
p, q = challenge2.factor(N1, 2)
print(f'p = {p}\nq = {q}')

print('====== Challenge 2 ======')
p, q = challenge2.factor(N2, 1 << 11)
print(f'p = {p}\nq = {q}')

print('====== Challenge 3 ======')
p, q = challenge3.factor(N3, 3, 2, 1)
print(f'p = {p}\nq = {q}')

print('====== Challenge 4 ======')
plain = challenge4.decrypt(N1, challenge2.factor, 65537, cipher4, 0x00)
print(f'Decrypted Text = {plain}')



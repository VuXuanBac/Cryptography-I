import gmpy2 as gmp
from gmpy2 import mpz
import time
# GMPY2 Documents:
# 1. gcd(...), lcm(...)
# 2. f_mod(x, m)                x mod m
# 3. gg.invert(x, m)            x ^ -1
# 4. gg.powmod(x, y, m)         x ^ y mod m
# 5. gg.divm(x, y, m)           x * y^-1 mod m
# 6. gg.is_congruent(x, y, m)
# 7. gg.gcdext(x, y)            gcd, a, b

with open('./nums.txt', 'r') as file:
    p = mpz(file.readline())
    g = mpz(file.readline())
    h = mpz(file.readline())
    x_max_bit = mpz(file.readline()) >> 1

B = count = 1 << x_max_bit
gB = gmp.powmod(g, B, p)
ig = gmp.invert(g, p)

# Equalization Problem: (gB)^x_0 = h * (ig)^x_1   mod p

left = h
right = 1
vdict = {h : 0}

# Left: Build dictionary
start = time.time()
print('...Build Dictionary')
for i in range(1, count):
    left = gmp.f_mod(left * ig, p)
    vdict[left] = i
print(f'Done [{(time.time() - start)} seconds]')

# Right: Find
start = time.time()
print('... Finding')
for x0 in range(count):
    try:
        x1 = vdict[right]
        x = (x0 << x_max_bit) | x1
        print(f'Found: x0 = {x0}, x1 = {x1} -> x = {x} [{(time.time() - start)} seconds]')
        break
    except:
        pass
    right = gmp.f_mod(right * gB, p)

    




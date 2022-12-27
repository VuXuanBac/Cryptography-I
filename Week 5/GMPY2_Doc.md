# GMPY2.MPZ Documents

[Document](https://gmpy2.readthedocs.io/en/latest/mpz.html)

```Python
import gmpy2 as gmp
from gmpy2 import mpz
```

Supported type for big integer, efficient than Python builtins when the integer's precision _exceeds 20 to 50 digits_.

## Basic

### Initialization

```Python
a = mpz(999233)
# 999233
b = mpz('999233', 16)
# 0x10064435
```

### Convert to Bytes

```Python
a = mpz(1234)
byte_array = gmp.to_binary(a)
```

In LE architecture like Windows, the result `byte_array` has the following format:

```Python
b'\x01\x01<reversed_result>'
```

`b'\x01\x01'` is 2-byte headers for MPZ type.
`<reversed_result>` is the reverse of actual byte array (Little-Endian).

For example:

```Python
>>> gmp.to_binary(mpz(0x01020304))
b'\x01\x01\x04\x03\x02\x01'
```

### Builtin Functions

Notes: From `gmpy2` module

#### Basic arithmetic

Return the result of basic math operator.

```Python
add(x, y)
subtract(x, y)
mul(x, y)
div(x, y)
divexact(x, y)      # require: y | x
```

#### Division and Remainder

Return the quotient and remainder of $x$ divided by $y$

```Python
*_divmod(x, y)
*_divmod_2exp(x, n)     # y = 2**n
```

Where `*` is:

- `c_`: Quotient is ceiling rounded (toward $+\inf$). Remainder has _opposite_ sign of $y$.
- `f_`: Quotient is flooring rounded (toward $-\inf$). Remainder has _same_ sign as $y$.
- `t_`: Quotient is truncating rounded (toward 0). Remainder has same sign as $x$.

**Similar**:

```Python
*_div(x, y)
*_div_2exp(x, n)
*_mod(x, y)
*_mod_2exp(x, n)
...
```

#### Modulus

##### gcd(...) and lcm(...)

Return GCD and LCM of many integers.

##### gcdext(x, y)

Return $g, a, b$:
$$\bold{g} = \gcd(x, y)$$$$\bold{a}*x+\bold{b}*y = \bold{g}$$

##### f_mod(x, m)

Return ($x \ \text{mod} \ m$) that has same sign as $m$.

##### invert(x, m)

Return $a$ or 0:
$$\bold{a} * x == 1 \left(\text{mod} \ m\right)$$

##### powmod(x, y, m)

Return ($x^y \ \text{mod} \ m$)
When $y\lt0$, if not exists inverse of $x$ in $\mathbb{Z}_m$, raise ValueError.

##### divm(x, y, m)

Return $a \in \mathbb{Z}_m$:
$$y * \bold{a} = x \left(mod \ m\right)$$If not exists inverse of $y$ in $\mathbb{Z}_m$ ($\gcd(y, m)\gt1$), raise ZeroDivisionError.

##### is_congruent(x, y, m)

Return True if $x = y \left(mod \ m\right)$

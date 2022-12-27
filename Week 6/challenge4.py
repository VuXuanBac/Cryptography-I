import gmpy2 as gmp

def mpz2bytes(number) -> bytes:
    temp = gmp.to_binary(number)
    # to_binary return: 2 bytes header || reverse(hex_value)
    result = bytearray()
    for b in reversed(temp[2:]):
        result.append(b)
    return bytes(result)

def decrypt(N: int, factoror, e: int, cipher: int, pkcs_separator: int) -> str:
    p, q = factoror(N)
    phiN = (p - 1) * (q - 1)
    d = gmp.invert(e, phiN)
    rsa_plain = gmp.powmod(cipher, d, N)
    result = mpz2bytes(rsa_plain)
    for i in range(len(result)):
        if result[i] == pkcs_separator:
            return result[i + 1:]
    return result


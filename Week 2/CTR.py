def xor(a: bytes, b: bytes) -> bytes:
    length = min(len(a), len(b))
    return bytes([x ^ y for x, y in zip(a[:length], b[:length])])

def _CTR_Block(encrypt, input: bytes, IV: bytes) -> bytes:
    return xor(input, encrypt(IV))

def Encrypt(encryptor, plain: bytes, IV: bytes, block_size: int = 16) -> bytes:
    iv_int = int.from_bytes(IV, 'big')
    iv_length = len(IV)
    block_count = len(plain) // block_size + 1 - (len(plain) % block_size == 0)
    result = bytearray(IV)
    for i in range(block_count):
        iv = (iv_int + i).to_bytes(iv_length, 'big')
        start = i * block_size
        end = start + block_size if i + 1 < block_count else len(plain)
        cipher = _CTR_Block(encryptor.encrypt, plain[start:end], iv)
        result.extend(cipher)

    return bytes(result)

def Decrypt(decryptor, cipher: bytes, IV: bytes, block_size: int = 16) -> bytes:
    iv_int = int.from_bytes(IV, 'big')
    iv_length = len(IV)
    block_count = len(cipher) // block_size + 1 - (len(cipher) % block_size == 0)
    result = bytearray()
    for i in range(block_count):
        iv = (iv_int + i).to_bytes(iv_length, 'big')
        start = i * block_size
        end = start + block_size if i + 1 < block_count else len(cipher)
        plain = _CTR_Block(decryptor.encrypt, cipher[start:end], iv)
        result.extend(plain)

    return bytes(result)
def xor(a: bytes, b: bytes) -> bytes:
    length = min(len(a), len(b))
    return bytes([x ^ y for x, y in zip(a[:length], b[:length])])

def PKCS5_Padding(message: bytes, block_size: int) -> bytes:
    temp = bytearray(message)
    padd_len = (block_size - len(message) % block_size) % 256
    temp.extend(bytes([padd_len] * padd_len))
    return bytes(temp)

def Encrypt(encryptor, plain: bytes, IV: bytes, block_size: int = 16) -> bytes:
    result = bytearray(IV)
    # encryptor = AES.new(key, AES.MODE_ECB)
    iv = IV
    padded_plain = PKCS5_Padding(plain, block_size)
    for start in range(0, len(padded_plain), block_size):
        enc_inp = xor(iv, padded_plain[start:start + block_size])
        enc_out = encryptor.encrypt(enc_inp)
        result.extend(enc_out)
        iv = enc_out

    return bytes(result)

def Decrypt(decryptor, cipher: bytes, IV: bytes, block_size: int = 16) -> bytes:
    if len(cipher) % block_size != 0:
        return

    result = bytearray()
    iv = IV
    for start in range(0, len(cipher), block_size):
        dec_inp = cipher[start:start + block_size]
        dec_out = decryptor.decrypt(dec_inp)
        result.extend(xor(iv, dec_out))
        iv = dec_inp

    padd_len = int(result[-1])
    return bytes(result[:len(result) - padd_len])
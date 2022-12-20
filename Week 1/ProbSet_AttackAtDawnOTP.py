plain1 = 'attack at dawn'
plain2 = 'attack at dusk'
cipher1_hex = '6c73d5240a948c86981bc294814d'
encoding = 'ascii'

plain1_bytes = plain1.encode(encoding)
plain2_bytes = plain2.encode(encoding)
cipher1_bytes = bytes.fromhex(cipher1_hex)

def xor(a, b):
    result = bytearray()
    for i in range(len(a)):
        result.append(a[i] ^ b[i])
    return result

key = xor(plain1_bytes, cipher1_bytes)

print(key.hex())
print(xor(key, plain2_bytes).hex())
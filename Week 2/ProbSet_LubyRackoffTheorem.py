z = [('9f970f4e 932330e4', '1792d21d b645c008'), 
    ('5f67abaf 5210722b', '325032a9 c5e2364b'), 
    ('4af53267 1351e2e1', '87a40cfa 8dd39154'), 
    ('2d1cfa42 c0b1d266', 'eea6e3dd b2146dd0')]

def xor(a : bytes, b : bytes) -> bytes:
    result = bytearray()
    for i in range(len(a)):
        result.append(a[i] ^ b[i])
    return bytes(result)

def fun(hex_list):
    for hex_tuple in hex_list:
        bytes1 = bytes.fromhex(hex_tuple[0])
        bytes2 = bytes.fromhex(hex_tuple[1])
        print(xor(bytes1, bytes2).hex())

fun(z)
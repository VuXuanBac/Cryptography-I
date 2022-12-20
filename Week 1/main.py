def read_bytes(path: str) -> list[bytes]:
    lines = []
    with open(path, 'r') as file:
        for l in file.readlines():
            lines.append(bytes.fromhex(l))

    return lines

inputs = read_bytes('./input.txt')

target_len = len(inputs[-1])
inputs_count = len(inputs)

def xor(a: bytes, b: bytes, length: int) -> list[int]:
    '''
        XOR two byte-strings [a] and [b]
        [length]: The length of the output, just XOR [length] byte in [a] and [b].
                        [length] must be less than both len([a]) and len([b])
    '''
    minlen = min(len(a), len(b))
    if length > minlen or length < 0:
        length = minlen
    return [x ^ y for x, y in zip(a[:length], b[:length])]

xored_ciphers = {(c1, c2): xor(inputs[c1], inputs[c2], target_len) \
                        for c1 in range(inputs_count) \
                            for c2 in range(c1 + 1, inputs_count)}

def calculate_space_possibilities(xored_pairs: list[bytes], ciphers_count: int, length: int):
    '''
        Give 'space' score for all ciphertexts in each position based on xored value between each pair of them.
        [length] The maximum position need to calculate score.
    '''
    def has_space(v: int) -> bool:
        return ord('A') <= v <= ord('Z') or ord('a') <= v <= ord('z')

    space_poss = [[0] * ciphers_count for _ in range(length)]
    # space_poss[i][j] = v: Space possibilities for cipher j at index i is v

    for c1 in range(ciphers_count):
        for c2 in range(c1 + 1, ciphers_count):
            for pos in range(length):
                if has_space(xored_pairs[c1, c2][pos]):
                    space_poss[pos][c1] += 1
                    space_poss[pos][c2] += 1
    
    return space_poss

space_possibilities = calculate_space_possibilities(xored_ciphers, inputs_count, target_len)

def predict_space(space_possibilities: list[list[int]]):
    '''
        Based on [space_possibilities], create a mapping between a position and the plaintext that
        has the highest possibilities on holding a space character at that position
        [Return] A lookup_table for the mappings that can be used for decoding.
    '''
    lookup_table = {}

    ciphers_count = len(space_possibilities[0])
    for pos in range(len(space_possibilities)):
        P = space_possibilities[pos] # list[int]

        max_index = max(range(ciphers_count), key = P.__getitem__)
        max_poss = P[max_index]

        if max_poss > 0:
            lookup_table[pos] = (max_index, ' ')

    return lookup_table

def load_custom_lookup_table(path: str, existing_lookup_table: dict, length: int):
    '''
        Read from file custom decoded mappings added manually for correctness the decoded result
        [path] Path to file
        [length] Ignore records that the position value is greater than [length]
        [existing_lookup_table] Append read records to this.
    '''
    if existing_lookup_table == None:
        existing_lookup_table = {}

    with open(path, 'r') as file:
        for line in file.readlines():
            parts = line.split(' ', 3)
            pos = int(parts[0])
            index = int(parts[1])
            value = str(' ' if len(parts[2]) == 0 else parts[2][0])
            if pos < length:
                existing_lookup_table[pos] = (index, value)

    return existing_lookup_table

lookup_table = load_custom_lookup_table('./custom-mapping.txt', predict_space(space_possibilities), target_len)

def decode(ciphers: list[bytes], xored_pairs: dict, lookup_table: dict, length: int) -> list[bytes]:
    '''
        Perform Decoding using a [lookup_table] and [xored_pairs]
        [ciphers]: Ciphertexts need to be decoded
        [lookup_table]: A dictionary with the [key] is the position and the [value] is a tuple of ciphertext and the decoded character for that position.
        [xored_pairs]: Xored string between 2 ciphers that used for decoding other ciphertexts not in the mapping at a specific position.
        [length]: The number of characters need to be decoded in all ciphertextes.
    '''
    if length < 0:
        length = min([len(c) for c in ciphers])

    ciphers_count = len(ciphers)
    plains = [['*'] * length for c in ciphers]
    # plains[i][j]: decode value for character at j in ciphers text at i

    for plain_pos, (cipher_index, value) in lookup_table.items():
        plains[cipher_index][plain_pos] = value

        for ci in range(ciphers_count):
            if ci != cipher_index:
                index_tuple = (ci, cipher_index) if cipher_index > ci else (cipher_index, ci)
                c = chr(ord(value) ^ xored_pairs[index_tuple][plain_pos])
                if c.isascii():
                    plains[ci][plain_pos] = c

    return plains

plaintextes = decode(inputs, xored_ciphers, lookup_table, target_len)

def write_result(result, output_path : str):
    '''
        Write decoded result to file
    '''
    with open(output_path, 'w') as file:
        for i in range(inputs_count):
            file.write(f'{i} : ' + ''.join(result[i]) + '\n')

write_result(plaintextes, '.__temp-result.txt')

# def write_xored_ciphers(output_path : str, ciphers: list[bytes], length: int):
#     '''
#         Write XOR value between 2 ciphers to file
#     '''
#     count = len(ciphers)
#     with open(output_path, 'w') as file:
#         file.write('    ' + ''.join([f'{i % 10:3}' for i in range(length)]) + '\n')
#         for i in range(count):
#             file.write(f'========== Cipher {i} ==========\n')
#             for j in range(count):
#                 if i != j:
#                     file.write(f'{j:2} : ' + bytes(xor(ciphers[i], ciphers[j], length)).hex(' ', 1) + '\n')

# write_xored_ciphers('.__xored-ciphers.txt', inputs, target_len)

# def write_space_poss(output_path : str, space_poss: list[list[int]]):
#     '''
#         Write space possibilities to file
#     '''
#     with open(output_path, 'w') as file:
#         for i in range(len(space_poss)):
#             file.write(f'{i:3} : {space_poss[i]}\n')

# write_space_poss('.__space-possibilities.txt', space_possibilities)
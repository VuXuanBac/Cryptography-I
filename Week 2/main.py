from Crypto.Cipher import AES
import CTR
import CBC

########## CTR ##########
CTR_keys = bytes.fromhex('36f18357be4dbd77f050515c73fcf9f2')
CTR_ciphertexts = (
    bytes.fromhex('69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329'),
    bytes.fromhex('770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451')
)

for c in CTR_ciphertexts:
    AES_cipher = AES.new(CTR_keys, AES.MODE_ECB)
    plain = CTR.Decrypt(AES_cipher, c[16:], c[:16])
    print(plain)
    cipher = CTR.Encrypt(AES_cipher, plain, c[:16])
    print(cipher.hex(), '->', cipher == c)

########## CBC ##########
CBC_keys = bytes.fromhex('140b41b22a29beb4061bda66b6747e14')
CBC_ciphertexts = (
    bytes.fromhex('4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81'),
    bytes.fromhex('5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253')
)

for c in CBC_ciphertexts:
    AES_cipher = AES.new(CBC_keys, AES.MODE_ECB)
    plain = CBC.Decrypt(AES_cipher, c[16:], c[:16])
    print(plain)
    cipher = CBC.Encrypt(AES_cipher, plain, c[:16])
    print(cipher.hex(), '->', cipher == c)
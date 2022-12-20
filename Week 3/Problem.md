Suppose a web site hosts large video file FF that anyone can download. Browsers who download the file need to make sure the file is authentic before displaying the content to the user. One approach is to have the web site hash the contents of FF using a collision resistant hash and then distribute the resulting short hash value h\=H(F)h = H(F) to users via some authenticated channel (later on we will use digital signatures for this). Browsers would download the entire file FF, check that H(F)H(F) is equal to the authentic hash value hh and if so, display the video to the user. Unfortunately, this means that the video will only begin playing after the \*entire\* file FF has been downloaded.

Our goal in this project is to build a file authentication system that lets browsers authenticate and play video chunks as they are downloaded without having to wait for the entire file. Instead of computing a hash of the entire file, the web site breaks the file into 1KB blocks (1024 bytes). It computes the hash of the last block and appends the value to the second to last block. It then computes the hash of this augmented second to last block and appends the resulting hash to the third block from the end. This process continues from the last block to the first as in the following diagram:

![](https://d3c33hcgiwev3.cloudfront.net/imageAssetProxy.v1/ueCUoSdTEeWpFArPV6NvgQ_90610d1864b116c0992e91c144f9c056_Screen-Shot-2015-07-10-at-3.33.04-PM.png?expiry=1670025600000&hmac=MmbwLYxBrwjMgS_UUIX4NAR4ceaOSmZcI9WSNt3xPJk)

The final hash value h0h\_0 – a hash of the first block with its appended hash – is distributed to users via the authenticated channel as above.

Now, a browser downloads the file FF one block at a time, where each block includes the appended hash value from the diagram above. When the first block (B0 ∥ h1)(B\_0 \\ \\big\\|\\ h\_1) is received the browser checks that H(B0 ∥ h1)H(B\_0\\ \\big\\|\\ h\_1) is equal to h0h\_0 and if so it begins playing the first video block. When the second block (B1 ∥ h2)(B\_1\\ \\big\\|\\ h\_2) is received the browser checks that H(B1 ∥ h2)H(B\_1\\ \\|\\ h\_2) is equal to h1h\_1 and if so it plays this second block. This process continues until the very last block. This way each block is authenticated and played as it is received and there is no need to wait until the entire file is downloaded.

It is not difficult to argue that if the hash function HH is collision resistant then an attacker cannot modify any of the video blocks without being detected by the browser. Indeed, since h0\=H(B0 ∥ h1)h\_0 = H(B\_0 \\ \\big\\|\\ h\_1) an attacker cannot find a pair (B0′,h1′)≠(B0,h1)(B\_0',h\_1') \\neq (B\_0,h\_1) such that h0\=H(B0′ ∥ h1′)h\_0 = H(B\_0' \\ \\big\\|\\ h\_1') since this would break collision resistance of HH. Therefore after the first hash check the browser is convinced that both B0B\_0 and h1h\_1 are authentic. Exactly the same argument proves that after the second hash check the browser is convinced that both B1B\_1 and h2h\_2 are authentic, and so on for the remaining blocks.

In this project we will be using SHA256 as the hash function. For an implementation of SHA256 use an existing crypto library such as [PyCrypto](https://www.dlitz.net/software/pycrypto/) (Python), [Crypto++](http://www.cryptopp.com/) (C++), or any other.

When appending the hash value to each block, please append it as binary data, that is, as 32 unencoded bytes (which is 256 bits). If the file size is not a multiple of 1KB then the very last block will be shorter than 1KB, but all other blocks will be exactly 1KB.

Your task is to write code to compute the hash h0h\_0 of a given file FF and to verify blocks of FF as they are received by the client.

In the box below please enter the (hex encoded) hash h0h\_0 for [this video file](https://crypto.stanford.edu/~dabo/onlineCrypto/6.1.intro.mp4_download).

You can check your code by using it to hash a different file. In particular, the hex encoded h0h\_0 for [this video file](https://crypto.stanford.edu/~dabo/onlineCrypto/6.2.birthday.mp4_download) is:

_**03c08f4ee0b576fe319338139c045c89c3e8e9409633bea29442e21425006ea8**_
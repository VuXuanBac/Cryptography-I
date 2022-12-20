# Programming Problem [Week 1]
## PROBLEM
**Decode a ciphertext that encoded with Many Time Pad.**  

- _**Input**: 11 hexa ciphertexts that encoded using OTP with the same key_  
- _**Output**: Plaintext for the last ciphertext (that has the shortest length)._

## IDEA

```
    cipher_1 (+) cipher_2 = plain_1 (+) plain_2
```
_Denotes (+) for XOR operator_

See that, a normal message mainly contains [A-Za-z] and `space` (' ' / 0x20). And we have:  
```
    [A-Z] (+) 0x20 = [a-z]
    [a-z] (+) 0x20 = [A-Z]
```
If the xored 2 characters value in range ([a-zA-Z]), we can claim (_with high possibility_) that **_one of them is a `space` and the other is a letter_**.

So we can decode the target ciphertext by finding `space`s in all ciphertexts. Almost the ciphers will be clear and meaningful. After that, we correct the incorrect decoding manually.

## IMPLEMENTATION

#### Step 1: Xoring 2 ciphers

With 11 ciphers, we have 55 xored string, enough to predict the `space`s

Note that: **These 55 xored strings are xored value between each pair of plaintexts**

#### Step 2: Predict which cipher hold the `space`

Based on 55 xored strings, for each `position` (_from 0 to target cipher length_) we give a cipher `1` point for each pair it belong to and the pair's xored `position` character is in `[A-Za-z]`

At one `position`, which cipher has a highest score, we assume that the `position` plaintext for that cipher is a `space`.

#### Step 3: Decoding

If we know at a `position`, a plaintext `X` for a cipher `Y` hold the `space`, based on xored string with all other ciphers, we can decode the `position` character at these cipher.

However not all our space predictions is correct and not all characters are decoded with these predictions.
 So, after automatic decoding, we need to fill the remaining `position` and correcting the wrong space predictions based on syntax and meaning of current decoded strings.

## CODE EXPLAINATION

**[1]**, I read 11 ciphertexts from file [input.txt](./input.txt) and store them as global variable `inputs`. I also get the length for the target ciphertext (also the length for the answer plaintext) for limiting the number of characters need to be decoded.

**[2]**, I XOR each pairs of ciphers in `inputs` and store the result as `xored_ciphers`, a dictionary with [key] is the index of two ciphers (smaller one come first) and the [value] is the xored value (in byte-string)

**[3]**, Based on `xored_ciphers`, I calculate the space possibilities which a cipher can hold a `space` at a specicfic position. With one xored string between cipher `X` and cipher `Y`, if at position `p`, the xored character is in `[A-Za-z]`, I give `X` one point and `Y` one point at that position. After all (55) xored string, for a specific position, which cipher has the largest score, then it has a highest possibility for holding a `space` at that position.  
The overall score stored in `space_possibilities`, a 2D array, that the row represent the position, the column represent the ciphertext, so `space_possibilities[i][j] = v` means the score for the ciphertext `j` at position `i` is `v`.

**[4]**, With space possibilities, I create a mapping between a position and a ciphertext that has the highest score for that position (choose arbitrarily if has many), stored them on a `lookup_table`, a dictionary with the [key] is the position and the [value] is a tuple of ciphertext and the decoded character for that position (in here, the decoded character is `space`).  
So `lookup_table[p] = (x, m)` means we decoded the character at position `p` in ciphertext `x` by character `m`.

**[5]**, With `lookup_table`, I carry out the decoding. At position `p`, the decoded character for ciphertext `x` is `m` if we has `lookup_table[p] = (x, m)`, for other ciphertexts `y`, the decoded character is:
```
    xored_ciphers[x, y][p] (+) m
```

**[6]**, At this time, I have decoded almost the characters for all ciphertexts, but at some positions the space prediction is not correct, so I perform decoding manually by inserting some records in `lookup_table` based on the syntax and meanings of incomplete words.  
The hand-craft records are appended on file [custom-mapping](./custom-mapping.txt) after each correctness.

## RUNNING
- Inputs (ciphertexts) need to be saved in [input.txt](./input.txt).  
- Custom records for correcting automatic decoding need to be saved in [custom-mapping.txt](./custom-mapping.txt) 

In current directory, perform
```
    py main.py
```
If have no error, the result will appear in the last row in created file [__temp_result.txt](./)

## RESULT
Message: 
`The secret message is: When using a stream cipher, never use the key more than once`

#### [Vũ Xuân Bắc - 20194230]
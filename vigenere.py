from alphabet import Alphabet


def encrypt(text, key, alphabet=Alphabet()):
    if not key:
        raise ValueError("Key must be non-empty")
    ptr = 0
    result = ''
    for c in text:
        if c in alphabet.get_alphabet():
            c = alphabet.shift(c, alphabet.ord(key[ptr]))
            ptr += 1
            if ptr == len(key):
                ptr = 0
        result += c
    return result


def decrypt(text, key, alphabet=Alphabet()):
    return encrypt(text, alphabet.anti_word(key), alphabet)
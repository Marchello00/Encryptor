from alphabet import Alphabet


def encrypt(text, key, alphabet=Alphabet()):
    result = ''
    for c in text:
        if c in alphabet.get_alphabet():
            c = alphabet.shift(c, key)
        result += c
    return result


def decrypt(text, key, alphabet=Alphabet()):
    return encrypt(text, -key, alphabet)
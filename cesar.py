from alphabet import Alphabet


def shift(text, k, alphabet = Alphabet()):
    result = ''
    for c in text:
        if c in alphabet.get_alphabet():
            c = alphabet.shift(c, k)
        result += c
    return result
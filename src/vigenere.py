from src.alphabet import Alphabet


def encrypt(text, key, alphabet=Alphabet()):
    if not key:
        raise ValueError("Key must be non-empty")
    ptr = 0
    result = []
    for letter in text:
        if letter in alphabet.get_alphabet():
            try:
                letter = alphabet.shift(letter, alphabet.ord(key[ptr]))
            except ValueError:
                raise ValueError(
                    'Key can contain only symbols from your alphabet')
            ptr += 1
            if ptr == len(key):
                ptr = 0
        result.append(letter)
    return ''.join(result)


def decrypt(text, key, alphabet=Alphabet()):
    try:
        return encrypt(text, alphabet.anti_word(key), alphabet)
    except ValueError:
        raise ValueError(
            'Key can contain only symbols from your alphabet')

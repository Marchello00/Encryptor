from src.alphabet import Alphabet


def encrypt(text, key, alphabet=Alphabet()):
    result = []
    for letter in text:
        if letter in alphabet.get_alphabet():
            letter = alphabet.shift(letter, key)
        result.append(letter)
    return ''.join(result)


def decrypt(text, key, alphabet=Alphabet()):
    return encrypt(text, -key, alphabet)


def hack(text, trained, alphabet=Alphabet()):
    variant = []
    for key in range(len(alphabet)):
        here = decrypt(text, key, alphabet)
        variant.append((
            trained.get_analyse(here),
            key
        ))
    good_key = max(variant)[1]
    return decrypt(text, good_key, alphabet)

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


def hack(text, trained, alphabet=Alphabet()):
    variant = []
    for k in range(len(alphabet)):
        here = decrypt(text, k, alphabet)
        variant.append((
            trained.get_analyse(here),
            k
        ))
    good_k = max(variant)[1]
    return decrypt(text, good_k, alphabet)

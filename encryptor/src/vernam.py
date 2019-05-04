from encryptor.src.alphabet import Alphabet
from encryptor.src import vigenere
import math


def __int_log(n):
    return math.ceil(math.log(n, 2))


def text_to_binary(text, alphabet=Alphabet()):
    k = __int_log(len(alphabet))
    result = ''
    for c in text:
        result += '{bits:0>{num}}'.format(bits=bin(alphabet.ord(c))[2:], num=k)
    return result


def binary_to_text(binary, alphabet=Alphabet()):
    k = __int_log(len(alphabet))
    result = ''
    for i in range(0, len(binary), k):
        result += alphabet.chr(int(binary[i:i + k], 2))
    return result


def encrypt(text, key, alphabet=Alphabet()):
    k = __int_log(len(alphabet))
    try:
        if len(key) == k * len(text):
            text = text_to_binary(text, alphabet)
        elif len(text) == k * len(key):
            key = text_to_binary(key, alphabet)
        else:
            key = text_to_binary(key, alphabet)
            text = text_to_binary(text, alphabet)
    except ValueError:
        raise ValueError('For vernam cipher all symbols must be from alphabet')
    if len(key) != len(text):
        raise ValueError('Key must be as long as message, '
                         'message len is {mes} and key len is {key}'.format(
                            mes=len(text) // k, key=len(key) // k))
    return vigenere.encrypt(text, key, Alphabet('01'))


def decrypt(text, key, alphabet=Alphabet(), raw=False):
    result = encrypt(text, key, alphabet)
    if not raw:
        result = binary_to_text(result, alphabet)
    return result

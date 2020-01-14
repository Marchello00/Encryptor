import math
from src.alphabet import Alphabet
from src import vigenere


def __int_log(num):
    return math.ceil(math.log(num, 2))


def text_to_binary(text, alphabet=Alphabet()):
    num_bits = __int_log(len(alphabet))
    result = []
    for letter in text:
        result.append(
            '{bits:0>{num}}'.format(bits=bin(alphabet.ord(letter))[2:],
                                    num=num_bits))
    return ''.join(result)


def binary_to_text(binary, alphabet=Alphabet()):
    num_bits = __int_log(len(alphabet))
    result = []
    for i in range(0, len(binary), num_bits):
        result.append(alphabet.chr(int(binary[i:i + num_bits], 2)))
    return ''.join(result)


def encrypt(text, key, alphabet=Alphabet()):
    num_bits = __int_log(len(alphabet))
    try:
        if len(key) == num_bits * len(text):
            text = text_to_binary(text, alphabet)
        elif len(text) == num_bits * len(key):
            key = text_to_binary(key, alphabet)
        else:
            key = text_to_binary(key, alphabet)
            text = text_to_binary(text, alphabet)
    except ValueError:
        raise ValueError('For vernam cipher all symbols must be from alphabet')
    if len(key) != len(text):
        raise ValueError('Key must be as long as message, '
                         'message len is {mes} and key len is {key}'.format(
                            mes=len(text) // num_bits,
                            key=len(key) // num_bits))
    return vigenere.encrypt(text, key, Alphabet('01'))


def decrypt(text, key, alphabet=Alphabet(), raw=False):
    result = encrypt(text, key, alphabet)
    if not raw:
        result = binary_to_text(result, alphabet)
    return result

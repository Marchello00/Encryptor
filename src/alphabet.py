import string
import functools
from src.takes import takes


def _letter_range(start, end):
    return ''.join(map(chr, range(ord(start), ord(end) + 1)))


RUSSIAN_ALPHABET = ''.join(
    [_letter_range('а', 'е'), 'ё', _letter_range('ж', 'я')])
RUSSIAN_ALPHABET += RUSSIAN_ALPHABET.upper()


class Alphabet:
    @staticmethod
    def __check_for_consecutive(text):
        for need, have in zip(text,
                              range(ord(text[0]), ord(text[0]) + len(text))):
            if need != chr(have):
                return False
        return True

    @takes(object, str)
    def set_alphabet(self, new_alphabet):
        if not new_alphabet:
            raise ValueError("Alphabet can't be empty")
        self.__alphabet = new_alphabet
        self.__consecutive = self.__check_for_consecutive(new_alphabet)

    def set_big_letters_alphabet(self):
        self.set_alphabet(string.ascii_uppercase)

    def set_letters_alphabet(self):
        self.set_alphabet(string.ascii_letters)

    def set_punctuation_alphabet(self):
        self.set_alphabet(string.ascii_letters + string.punctuation)

    def set_russian_alphabet(self):
        self.set_alphabet(RUSSIAN_ALPHABET)

    def set_all(self):
        self.set_alphabet(string.ascii_letters +
                          RUSSIAN_ALPHABET + string.punctuation +
                          string.whitespace)

    def set_binary_alphabet(self):
        self.set_alphabet('01')

    def set_hexdigits_alphabet(self):
        self.set_alphabet(string.hexdigits)

    def get_alphabet(self):
        return self.__alphabet

    def __len__(self):
        return len(self.__alphabet)

    def __str__(self):
        return self.__alphabet

    @functools.lru_cache(10)
    def ord(self, letter):
        if self.__consecutive:
            code = ord(letter) - ord(self.__alphabet[0])
        else:
            code = self.__alphabet.find(letter)
        if code < 0 or len(self.__alphabet) <= code:
            raise ValueError("Symbol must be from alphabet")
        return code

    def chr(self, code):
        if code < 0 or len(self.__alphabet) < code:
            raise ValueError("Wrong code(it's not in your alphabet)")
        return self.__alphabet[code]

    def shift(self, letter, steps):
        code = self.ord(letter)
        alph_len = len(self.__alphabet)
        steps = (steps % alph_len + alph_len) % alph_len
        return self.__alphabet[(code + steps) % alph_len]

    @takes(object, str)
    def anti_word(self, word):
        new_word = []
        for letter in word:
            if letter not in self.__alphabet:
                raise ValueError("Word can contain only symbols from alphabet")
            new_word.append(self.__alphabet[-self.ord(letter)])
        return ''.join(new_word)

    def __init__(self, alphabet=string.ascii_letters):
        self.__alphabet = None
        self.__consecutive = None
        self.set_alphabet(alphabet)

from takes import takes
import string
import functools

# Without 'ёЁ'
russian_alphabet = ''.join(map(chr, range(ord('а'), ord('я') + 1))) + \
                   ''.join(map(chr, range(ord('А'), ord('Я') + 1)))


class Alphabet:
    @staticmethod
    def __check_for_consecutive(text):
        for need, have in zip(text,
                              range(ord(text[0]), ord(text[0]) + len(text))):
            if need != chr(have):
                return False
        return True

    @takes(object, str)
    def set_alphabet(self, new_alph):
        if not new_alph:
            raise ValueError("Alphabet can't be empty")
        self.__alphabet = new_alph
        self.__consecutive = self.__check_for_consecutive(new_alph)

    def set_big_letters_alphabet(self):
        self.set_alphabet(string.ascii_uppercase)

    def set_letters_alphabet(self):
        self.set_alphabet(string.ascii_letters)

    def set_punctuation_alphabet(self):
        self.set_alphabet(string.ascii_letters + string.punctuation)

    def set_russian_alphabet(self):
        self.set_alphabet(russian_alphabet)

    def set_all(self):
        self.set_alphabet(string.ascii_letters +
                          russian_alphabet + string.punctuation +
                          string.whitespace)

    def set_binary_alphabet(self):
        self.set_alphabet('01')

    def set_hexdigits_alphabet(self):
        self.set_alphabet(string.hexdigits)

    def get_alphabet(self):
        return self.__alphabet

    def __len__(self):
        return len(self.__alphabet)

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

    def shift(self, letter, k):
        code = self.ord(letter)
        n = len(self.__alphabet)
        k = (k % n + n) % n
        return self.__alphabet[(code + k) % n]

    @takes(object, str)
    def anti_word(self, word):
        new_word = ''
        for c in word:
            if c not in self.__alphabet:
                raise ValueError("Word can contain only symbols from alphabet")
            new_word += self.__alphabet[-self.ord(c)]
        return new_word

    def __init__(self, alphabet=string.ascii_letters):
        self.__alphabet = None
        self.__consecutive = None
        self.set_alphabet(alphabet)

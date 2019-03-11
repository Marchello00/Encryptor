from takes import takes
import string

# it's without 'ёЁ'
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
        self.set_alphabet(string.ascii_letters + \
                          russian_alphabet + string.punctuation +
                          string.whitespace)

    def get_alphabet(self):
        return self.__alphabet

    def shift(self, letter, k):
        if self.__consecutive:
            code_now = ord(letter) - ord(self.__alphabet[0])
        else:
            code_now = self.__alphabet.find(letter)
        n = len(self.__alphabet)
        k = (k % n + n) % n
        return self.__alphabet[(code_now + k) % n]

    def __init__(self):
        self.__alphabet = 'a'
        self.__consecutive = True
        self.set_letters_alphabet()

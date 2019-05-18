from collections import Counter, defaultdict
import re
from math import sqrt


def freq(dct, summ=None):
    if not dct:
        return dct
    if not summ:
        summ = sum(dct.values())
    if not summ:
        raise ValueError("Number of elements must be positive integer")
    return {key: val / summ for key, val in dct.items()}


class Analyser:
    def count_letters(self):
        if not self.text:
            return None
        self.letters = freq(Counter(self.text), len(self.text))
        return self.letters

    def count_words(self, limit=None):
        if not limit:
            limit = len(self.text)
        ctr = Counter(re.findall(r'\w+', self.text.lower()))
        self.words = freq(dict(ctr.most_common(limit)))
        return self.words

    def count_n_grams(self, n_for_ngrams=None, with_punc=False):
        if not n_for_ngrams:
            n_for_ngrams = 2
        self.n_for_ngrams = n_for_ngrams
        text = self.text.lower()
        dct = defaultdict(list)
        if not with_punc:
            for word in re.findall(r'\w+', text):
                for i in range(0, len(word) - n_for_ngrams):
                    dct[word[i:i + n_for_ngrams]].append(
                        word[i + n_for_ngrams])
        else:
            for i in range(0, len(text) - n_for_ngrams):
                dct[text[i:i + n_for_ngrams]].append(text[i + n_for_ngrams])
        self.n_grams = {key: freq(Counter(val)) for key, val in dct.items()}
        return self.n_grams

    def count_avg(self):
        w = re.findall(r'\w+', self.text)
        part = max(min(1000, int(sqrt(len(w)))), 1)
        self.avg_letters, self.avg_words, self.avg_n_grams = 0, 0, 0
        for i in range(0, len(w), part):
            self.avg_words += get_words_analyse(self.text[i:i + part],
                                                self.words)
            self.avg_letters += get_letters_analyse(self.text[i:i + part],
                                                    self.letters)
            self.avg_n_grams += get_n_grams_analyse(self.text[i:i + part],
                                                    self.n_for_ngrams,
                                                    self.n_grams)
        self.avg_words /= len(w) / part
        self.avg_letters /= len(w) / part
        self.avg_n_grams /= len(w) / part
        if not self.avg_letters:
            self.avg_letters = 1
        if not self.avg_words:
            self.avg_words = 1
        if not self.avg_n_grams:
            self.avg_n_grams = 1

    def analyse(self, n_grams=None, dont_ignore_punc=False, top_n_words=None,
                count_avg=False):
        self.count_n_grams(n_grams, dont_ignore_punc)
        self.count_words(top_n_words)
        self.count_letters()
        if count_avg:
            self.count_avg()

    def get_analyse(self, text):
        return get_words_analyse(text, self.words) / self.avg_words + \
               get_letters_analyse(text, self.letters) / self.avg_letters + \
               get_n_grams_analyse(text, self.n_for_ngrams,
                                   self.n_grams) / self.avg_n_grams

    def __init__(self, text='', n_grams=None, dont_ignore_punc=False,
                 top_n_words=None, count_avg=False):
        self.text = text
        self.letters = dict()
        self.words = dict()
        self.n_for_ngrams = 0
        self.n_grams = dict()
        self.avg_words, self.avg_letters, self.avg_n_grams = 1, 1, 1
        self.analyse(n_grams, dont_ignore_punc, top_n_words, count_avg)

    def dump(self):
        return {key: self.__getattribute__(key) for key in self.__dict__}

    def load(self, model):
        for attr in self.__dict__:
            if attr not in model:
                raise ValueError('Model corrupted!')
            self.__setattr__(attr, model[attr])


def get_words_analyse(text, words_freq):
    summ = 0
    for word in re.findall(r'\w+', text.lower()):
        if word in words_freq:
            summ += words_freq[word]
    return summ


def get_letters_analyse(text, letters_freq):
    summ = 0
    for letter in list(text):
        if letter in letters_freq:
            summ += letters_freq[letter]
    return summ


def get_n_grams_analyse(text, n_for_ngrams, n_grams):
    summ = 0
    for i in range(0, len(text) - n_for_ngrams):
        if text[i:i + n_for_ngrams] in n_grams and \
                text[i + n_for_ngrams] in n_grams[text[i:i + n_for_ngrams]]:
            summ += n_grams[text[i:i + n_for_ngrams]][text[i + n_for_ngrams]]
    return summ

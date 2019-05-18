from collections import Counter, defaultdict
import re
from math import sqrt
import src.enums as enums


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

    def count_n_grams(self, n_for_ngrams=enums.N_FOR_NGRAMS_DEFAULT,
                      with_punc=enums.WITH_PUNC_DEFAULT):
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
        words = re.findall(r'\w+', self.text)
        if not words:
            return
        part = min(enums.MAX_LEN_OF_PARTS_TO_ANALYSE_IN_COUNT_AVG,
                   int(sqrt(len(words))))
        self.avg_letters, self.avg_words, self.avg_n_grams = 0, 0, 0
        step = part / enums.ANALYSE_FRAGMENTS_DENSITY
        for i in range(0, len(words), step):
            self.avg_words += get_words_analyse(self.text[i:i + part],
                                                self.words)
            self.avg_letters += get_letters_analyse(self.text[i:i + part],
                                                    self.letters)
            self.avg_n_grams += get_n_grams_analyse(self.text[i:i + part],
                                                    self.n_for_ngrams,
                                                    self.n_grams)
        self.avg_words /= len(words) / step
        self.avg_letters /= len(words) / step
        self.avg_n_grams /= len(words) / step
        if self.avg_letters == 0:
            self.avg_letters = 1
        if self.avg_words == 0:
            self.avg_words = 1
        if self.avg_n_grams == 0:
            self.avg_n_grams = 1

    def analyse(self, n_for_ngrams=enums.N_FOR_NGRAMS_DEFAULT,
                dont_ignore_punc=enums.WITH_PUNC_DEFAULT,
                top_n_words=enums.TOP_N_WORDS_DEFAULT,
                count_avg=enums.COUNT_AVG_DEFAULT):
        self.count_n_grams(n_for_ngrams, dont_ignore_punc)
        self.count_words(top_n_words)
        self.count_letters()
        if count_avg:
            self.count_avg()

    def get_analyse(self, text):
        return get_words_analyse(text, self.words) / self.avg_words + \
               get_letters_analyse(text, self.letters) / self.avg_letters + \
               get_n_grams_analyse(text, self.n_for_ngrams,
                                   self.n_grams) / self.avg_n_grams

    def __init__(self, text='', n_for_ngrams=enums.N_FOR_NGRAMS_DEFAULT,
                 dont_ignore_punc=enums.WITH_PUNC_DEFAULT,
                 top_n_words=enums.TOP_N_WORDS_DEFAULT,
                 count_avg=enums.COUNT_AVG_DEFAULT):
        self.text = text
        self.letters = dict()
        self.words = dict()
        self.n_for_ngrams = n_for_ngrams
        self.n_grams = dict()
        self.avg_words, self.avg_letters, self.avg_n_grams = 1, 1, 1
        self.analyse(n_for_ngrams, dont_ignore_punc, top_n_words, count_avg)

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

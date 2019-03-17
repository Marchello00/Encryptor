from collections import Counter, defaultdict
import re
from math import sqrt


def freq(dct, summ=None):
    if not summ:
        summ = sum(dct.values())
    if not summ:
        raise ValueError("Number of elements must be positive integer")
    return {key: val / summ for key, val in dct.items()}


class Analyser:
    def count_letters(self):
        if not self.text: return None
        self.letters = freq(Counter(self.text), len(self.text))
        return self.letters

    def count_words(self, limit=None):
        if not limit:
            limit = len(self.text)
        ctr = Counter(re.findall(r'\w+', self.text.lower()))
        self.words = freq(dict(ctr.most_common(limit)))
        return self.words

    def count_n_grams(self, n=None, with_punc=False):
        if not n:
            n = 2
        self.n = n
        text = self.text.lower()
        dct = defaultdict(list)
        if not with_punc:
            for word in re.findall(r'\w+', text):
                for i in range(0, len(word) - n):
                    dct[word[i:i + n]].append(word[i + n])
        else:
            for i in range(0, len(text) - n):
                dct[text[i:i + n]].append(text[i + n])
        self.n_grams = {key: Counter(val) for key, val in dct.items()}
        return self.n_grams

    def count_avg(self):
        w = re.findall(r'\w+', self.text)
        part = int(sqrt(len(w)))
        self.avg_letters, self.avg_words, self.avg_n_gramms = 0, 0, 0
        for i in range(len(w) - part):
            self.avg_words += get_words_analyse(self.text, self.words)
            self.avg_letters += get_letters_analyse(self.text, self.letters)
            self.avg_n_gramms += get_n_grams_analyse(self.text, self.n,
                                                     self.n_grams)
        self.avg_words /= len(w) - part
        self.avg_letters /= len(w) - part
        self.avg_n_gramms /= len(w) - part

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
               get_n_grams_analyse(text, self.n,
                                   self.n_grams) / self.avg_n_grams

    def __init__(self, text='', n_grams=None, dont_ignore_punc=False,
                 top_n_words=None, count_avg=False):
        self.text = text
        self.letters = dict()
        self.words = dict()
        self.n = 0
        self.n_grams = dict()
        self.analyse(n_grams, dont_ignore_punc, top_n_words, count_avg)
        self.avg_words, self.avg_letters, self.avg_n_grams = 1, 1, 1


def get_words_analyse(text, words_freq):
    summ = 0
    for word in re.findall(r'\w+', text.lower()):
        if word in words_freq:
            summ += words_freq[word]
    return summ


def get_letters_analyse(text, letters_freq):
    summ = 0
    for c in list(text):
        if c in letters_freq:
            summ += letters_freq[c]
    return summ


def get_n_grams_analyse(text, n, n_grams):
    summ = 0
    for i in range(0, len(text) - n):
        if text[i:i + n] in n_grams and \
                text[i + n] in n_grams[text[i:i + n]]:
            summ += n_grams[text[i:i + n]][text[i + n]]
    return summ

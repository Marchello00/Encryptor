from collections import Counter, defaultdict
import re


def freq(dct, summ=None):
    if not summ:
        summ = sum(dct.values())
    if not summ:
        raise ValueError("Number of elements must be positive integer")
    return {key: val / summ for key, val in dct.items()}


def count_letters(text):
    if not text: return None
    return freq(Counter(text), len(text))


def count_words(text, limit=None):
    if not limit:
        limit = len(text)
    ctr = Counter(re.findall(r'\w+', text.lower()))
    return freq(dict(ctr.most_common(limit)))


def count_n_grams(text, n=None, with_punc=False):
    if not n:
        n = 2
    text = text.lower()
    dct = defaultdict(list)
    if not with_punc:
        for word in re.findall(r'\w+', text):
            for i in range(0, len(word) - n):
                dct[word[i:i + n]].append(word[i + n])
    else:
        for i in range(0, len(text) - n):
            dct[text[i:i + n]].append(text[i + n])
    return {key: Counter(val) for key, val in dct.items()}


def analyse(text, n_grams=None, dont_ignore_punc=False, top_n_words=None):
    ng = count_n_grams(text, n_grams, dont_ignore_punc)
    w = count_words(text, top_n_words)
    lt = count_letters(text)
    return {'letters': lt, 'words': w, 'n':n_grams, 'n_grams': ng}


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

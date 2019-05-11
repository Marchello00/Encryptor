import pytest
import random

ENG_TEXT1 = 'encryptor/models/original/ShakespeareSonnets.txt'
ENG_TEXT2 = 'encryptor/models/original/TheLettersofJaneAusten.txt'
RUS_TEXT = 'encryptor/models/original/WarAndPeace.txt'


def get_random_text(file, seed, word_count):
    random.seed(seed)
    with open(file) as f:
        text = f.read().split()
    result = ''
    for i in range(word_count):
        result += random.choice(text) + ' '
    return result



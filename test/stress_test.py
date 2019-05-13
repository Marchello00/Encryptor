import pytest
import random
import src.caesar as caesar
from src.analyser import Analyser
import json

ENG_TEXT1 = 'models/original/ShakespeareSonnets.txt'
ENG_TEXT2 = 'models/original/TheLettersofJaneAusten.txt'
RUS_TEXT = 'models/original/WarAndPeace.txt'

ENG_MODEL1 = 'models/eng'
ENG_MODEL2 = 'models/eng2'
RUS_MODEL = 'models/rus'


def get_random_text(file, seed, word_count):
    random.seed(seed)
    with open(file) as f:
        text = f.read().split()
    result = ''
    for i in range(word_count):
        result += random.choice(text) + ' '
    return result


@pytest.mark.parametrize("text_path", (ENG_TEXT1, ENG_TEXT2, RUS_TEXT))
@pytest.mark.parametrize("word_count", (10, 100, 10000))
@pytest.mark.parametrize("key", (1, 5, 10, 14, 23))
def test_gen_encrypt(text_path, word_count, key):
    text = get_random_text(text_path, 0, word_count)
    caesar.encrypt(text, key)


@pytest.mark.parametrize("text_path", (ENG_TEXT1, ENG_TEXT2, RUS_TEXT))
@pytest.mark.parametrize("word_count", (10, 100, 10000))
@pytest.mark.parametrize("key", (1, 5, 10, 14, 23))
def test_gen_encrypt_decrypt(text_path, word_count, key):
    text = get_random_text(text_path, 0, word_count)
    enc = caesar.encrypt(text, key)
    assert caesar.decrypt(enc, key) == text


@pytest.mark.parametrize("text_path,model_path",
                         ((ENG_TEXT1, ENG_MODEL1),
                          (ENG_TEXT2, ENG_MODEL2),
                          (RUS_TEXT, RUS_MODEL)))
@pytest.mark.parametrize("word_count", (10, 100, 10000))
@pytest.mark.parametrize("key", (1, 5, 10, 14, 23))
def test_gen_encrypt_hack(text_path, model_path, word_count, key):
    text = get_random_text(ENG_TEXT1, 0, word_count)
    enc = caesar.encrypt(text, key)
    a = Analyser()
    with open(model_path) as m:
        a.load(json.load(m))
    assert caesar.hack(text=enc, trained=a) == text

import pytest
import src.vigenere as vigenere
from encryptor import get_alphabet
import json


def testdata(test_type=None):
    with open('tests/vigenere_data.json') as f:
        all_tests = json.load(f)
    result = []
    for key, value in all_tests.items():
        if test_type in value['type'] or test_type is None:
            for case in value['variants']:
                result.append(
                    (value['plain'],
                     case['key'],
                     case['encrypted'],
                     get_alphabet(value['alphabet']))
                )
    return result


@pytest.mark.parametrize("text,key,expected,alph", testdata())
def test_encrypt(text, key, expected, alph):
    assert vigenere.encrypt(text=text, key=key, alphabet=alph) == expected


@pytest.mark.parametrize("expected,key,encrypted,alph", testdata())
def test_decrypt(encrypted, key, expected, alph):
    assert vigenere.decrypt(text=encrypted, key=key, alphabet=alph) == expected

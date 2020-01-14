import pytest
import src.caesar as caesar
from src.analyser import Analyser
from encryptor import get_alphabet
import json


def testdata(test_type=None):
    with open('tests/caesar_data.json') as f:
        all_tests = json.load(f)
    result = []
    for key, value in all_tests.items():
        if test_type in value['type'] or test_type is None:
            for case in value['variants']:
                if test_type == 'hack':
                    result.append(
                        (value['plain'],
                         case['encrypted'],
                         value['model'],
                         get_alphabet(value['alphabet']))
                    )
                else:
                    result.append(
                        (value['plain'],
                         case['key'],
                         case['encrypted'],
                         get_alphabet(value['alphabet']))
                    )
    return result


@pytest.mark.parametrize("text,key,expected,alph", testdata())
def test_encrypt(text, key, expected, alph):
    assert caesar.encrypt(text=text, key=key, alphabet=alph) == expected


@pytest.mark.parametrize("expected,key,encrypted,alph", testdata())
def test_decrypt(encrypted, key, expected, alph):
    assert caesar.decrypt(text=encrypted, key=key, alphabet=alph) == expected


@pytest.mark.parametrize("expected,encrypted,model,alph",
                         testdata("hack"))
def test_hack(encrypted, expected, model, alph):
    analyse = Analyser()
    with open(model) as m:
        analyse.load(json.load(m))
    assert caesar.hack(text=encrypted, trained=analyse, alphabet=alph)

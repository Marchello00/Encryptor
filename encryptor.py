#!/usr/local/bin/python3

import sys
import argparse
import json
from contextlib import contextmanager
import src.alphabet as ab
import src.caesar as c
import src.vigenere as vg
import src.vernam as vn
import src.analyser as an


def encode_action(args):
    if args.cipher == 'caesar':
        try:
            args.key = int(args.key)
        except Exception:
            print('Key for caesar cipher must be integer value')
            return
    with smart_open(args.input_file, 'r') as input_file:
        text = input_file.read()
    if args.file_alphabet:
        with open(args.file_alphabet, 'r') as alphabet_file:
            alphabet = ab.Alphabet(alphabet_file.read())
    else:
        alphabet = get_alphabet(args.alphabet)
    if args.cipher == 'caesar':
        with smart_open(args.output_file, 'w') as output_file:
            output_file.write(c.encrypt(text, args.key, alphabet))
    if args.cipher == 'vigenere':
        with smart_open(args.output_file, 'w') as output_file:
            output_file.write(vg.encrypt(text, args.key, alphabet))
    if args.cipher == 'vernam':
        with smart_open(args.output_file, 'w') as output_file:
            output_file.write(vn.encrypt(text, args.key, alphabet))
            output_file.write('\n')


def decode_action(args):
    if args.cipher == 'caesar':
        try:
            args.key = int(args.key)
        except Exception:
            print('Key for caesar cipher must be integer value')
            return
    with smart_open(args.input_file, 'r') as input_file:
        text = input_file.read()
    if args.file_alphabet:
        with open(args.file_alphabet, 'r') as alphabet_file:
            alphabet = ab.Alphabet(alphabet_file.read())
    else:
        alphabet = get_alphabet(args.alphabet)
    if args.cipher == 'caesar':
        with smart_open(args.output_file, 'w') as output_file:
            output_file.write(c.decrypt(text, args.key, alphabet))
    if args.cipher == 'vigenere':
        with smart_open(args.output_file, 'w') as output_file:
            output_file.write(vg.decrypt(text, args.key, alphabet))
    if args.cipher == 'vernam':
        with smart_open(args.output_file, 'w') as output_file:
            output_file.write(vn.decrypt(text, args.key, alphabet))
            output_file.write('\n')


def train_action(args):
    with smart_open(args.text_file, 'r') as text_file:
        text = text_file.read()
    if not text:
        raise ValueError('Text must be non-empty')
    analyse = an.Analyser(
        text, args.ngrams, args.punc, args.top, args.count_avg
    )
    with smart_open(args.model_file, 'w') as model_file:
        json.dump(analyse.dump(), model_file)


def hack_action(args):
    with smart_open(args.input_file, 'r') as input_file:
        text = input_file.read()
    analyse = an.Analyser()
    with smart_open(args.model_file, 'r') as model_file:
        try:
            analyse.load(json.load(model_file))
        except Exception:
            raise ValueError('Model file is corrupted!')
    if args.file_alphabet:
        with open(args.file_alphabet, 'r') as alphabet_file:
            alphabet = ab.Alphabet(alphabet_file.read())
    else:
        alphabet = get_alphabet(args.alphabet)
    with smart_open(args.output_file, 'w') as output_file:
        output_file.write(c.hack(text, analyse, alphabet))


def parse_args():
    cyphers = ['caesar', 'vernam', 'vigenere']
    alphabets = ['eng', 'engpunc', 'engup', 'rus', 'bin', 'hex', 'all']

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='List of commands', dest='action')
    subparsers.required = True

    encode_parser = subparsers.add_parser('encode', help='Encode message')
    encode_parser.add_argument('--cipher', '-c', required=True,
                               choices=cyphers,
                               help='Encryption algorithm')
    encode_parser.add_argument('--key', '-k', required=True,
                               help='Key which will used for encoding message')
    encode_parser.add_argument('--input-file', '-i',
                               help='Message will be read from this file')
    encode_parser.add_argument('--output-file', '-o',
                               help='Encoded message '
                                    'will be written to this file')
    encode_alph = encode_parser.add_mutually_exclusive_group()
    encode_alph.add_argument('--alphabet', '-a', choices=alphabets,
                             default='eng',
                             help='Alphabet (builtin)'
                                  ' which will be used for encoding')
    encode_alph.add_argument('--file-alphabet', '-f',
                             help='Alphabet (yours)'
                                  ' which will be used for encoding'
                             )
    encode_parser.set_defaults(act=encode_action)

    decode_parser = subparsers.add_parser('decode', help='Decode message')
    decode_parser.add_argument('--cipher', '-c', required=True,
                               choices=cyphers,
                               help='Encryption algorithm')
    decode_parser.add_argument('--key', '-k', required=True,
                               help='Key what was used for encoding message')
    decode_parser.add_argument('--input-file', '-i',
                               help='Encoded message '
                                    'will be read from this file')
    decode_parser.add_argument('--output-file', '-o',
                               help='Decoded message '
                                    'will be written to this file')
    decode_alph = decode_parser.add_mutually_exclusive_group()
    decode_alph.add_argument('--alphabet', '-a', choices=alphabets,
                             default='eng',
                             help='Alphabet (builtin)'
                                  ' which will be used for decoding')
    decode_alph.add_argument('--file-alphabet', '-f',
                             help='Alphabet (your)'
                                  ' which will be used for decoding'
                             )
    decode_parser.set_defaults(act=decode_action)

    train_parser = subparsers.add_parser('train',
                                         help='Create train model '
                                              'on your text')
    train_parser.add_argument('--text-file', '-i',
                              help='Text for training')
    train_parser.add_argument('--model-file', '-m',
                              help='Trained model '
                                   'will be written to this file')
    train_parser.add_argument('--ngrams', '-n', type=int,
                              help='N for n-grams analyse')
    train_parser.add_argument('--punc', '-p', action='store_true',
                              help='If exist punctuation will be '
                                   'also analysed')
    train_parser.add_argument('--top', '-t', type=int,
                              help='How many most common words remember')
    train_parser.add_argument('--count-avg', '-c', action='store_true',
                              help='Count average statistics on your text'
                                   '(may work slower)')
    train_parser.set_defaults(act=train_action)

    hack_parser = subparsers.add_parser('hack', help='Try to hack message')
    hack_parser.add_argument('--input-file', '-i',
                             help='Encoded message '
                                  'will be read from this file')
    hack_parser.add_argument('--output-file', '-o',
                             help='Decoded message '
                                  'will be written to this file')
    hack_parser.add_argument('--model-file', '-m',
                             default='models/eng',
                             help='Trained model '
                                  'will be loaded from this file')
    hack_alph = hack_parser.add_mutually_exclusive_group()
    hack_alph.add_argument('--alphabet', '-a', choices=alphabets,
                           default='eng',
                           help='Alphabet (builtin)'
                                ' which will be used for decoding'
                           )
    hack_alph.add_argument('--file-alphabet', '-f',
                           help='Alphabet (your)'
                                ' which will be used for encoding'
                           )
    hack_parser.set_defaults(act=hack_action)
    return parser.parse_args()


@contextmanager
def smart_open(file, mode):
    opened = False
    write = mode in ['w', 'a', 'wb']
    try:
        if not file:
            if write:
                work_file = sys.stdout
            else:
                work_file = sys.stdin
        else:
            work_file = open(file, mode)
            opened = True
        yield work_file
    except Exception:
        raise
    finally:
        if opened:
            work_file.close()


def get_alphabet(choise):
    alph = ab.Alphabet()
    solver = {'eng': alph.set_letters_alphabet,
              'engpunc': alph.set_punctuation_alphabet,
              'engup': alph.set_big_letters_alphabet,
              'rus': alph.set_russian_alphabet,
              'bin': alph.set_binary_alphabet,
              'hex': alph.set_hexdigits_alphabet,
              'all': alph.set_all}
    solver[choise]()
    return alph


def main():
    args = parse_args()
    args.act(args)


if __name__ == '__main__':
    try:
        main()
    except Exception:
        print(sys.exc_info()[1])

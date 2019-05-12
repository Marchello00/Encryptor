#!/usr/local/bin/python3

import sys
import argparse
from contextlib import contextmanager
import encryptor.src.alphabet as ab
import encryptor.src.caesar as c
import encryptor.src.vigenere as vg
import encryptor.src.vernam as vn
import encryptor.src.analyser as an
import json


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
    encode_alph.add_argument('--file_alphabet', '-f',
                             help='Alphabet (yours)'
                                  ' which will be used for encoding'
                             )
    encode_parser.set_defaults(act='encode')

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
    decode_alph.add_argument('--file_alphabet', '-f',
                             help='Alphabet (your)'
                                  ' which will be used for decoding'
                             )
    decode_parser.set_defaults(act='decode')

    train_parser = subparsers.add_parser('train',
                                         help='Create train model '
                                              'on your text')
    train_parser.add_argument('--text_file', '-i',
                              help='Text for training')
    train_parser.add_argument('--model_file', '-m',
                              help='Trained model '
                                   'will be written to this file')
    train_parser.add_argument('--ngrams', '-n', type=int,
                              help='N for n-grams analyse')
    train_parser.add_argument('--punc', '-p', action='store_true',
                              help='If exist punctuation will be '
                                   'also analysed')
    train_parser.add_argument('--top', '-t', type=int,
                              help='How many most common words remember')
    train_parser.add_argument('--count_avg', '-c', action='store_true',
                              help='Count average statistics on your text'
                                   '(may work slower)')
    train_parser.set_defaults(act='train')

    hack_parser = subparsers.add_parser('hack', help='Try to hack message')
    hack_parser.add_argument('--input-file', '-i',
                             help='Encoded message '
                                  'will be read from this file')
    hack_parser.add_argument('--output-file', '-o',
                             help='Decoded message '
                                  'will be written to this file')
    hack_parser.add_argument('--model_file', '-m',
                             default='models/eng',
                             help='Trained model '
                                  'will be loaded from this file')
    hack_alph = hack_parser.add_mutually_exclusive_group()
    hack_alph.add_argument('--alphabet', '-a', choices=alphabets,
                           default='eng',
                           help='Alphabet (builtin)'
                                ' which will be used for decoding'
                           )
    hack_alph.add_argument('--file_alphabet', '-f',
                           help='Alphabet (your)'
                                ' which will be used for encoding'
                           )
    hack_parser.set_defaults(act='hack')
    return parser.parse_args()


@contextmanager
def smart_open(file, mode):
    opened = False
    write = mode in ['w', 'a', 'wb']
    try:
        if not file:
            if write:
                f = sys.stdout
            else:
                f = sys.stdin
        else:
            f = open(file, mode)
            opened = True
        yield f
    except Exception:
        raise
    finally:
        if opened:
            f.close()


def get_alphabet(choise):
    alph = ab.Alphabet()
    if choise == 'eng':
        alph.set_letters_alphabet()
    elif choise == 'engpunc':
        alph.set_punctuation_alphabet()
    elif choise == 'engup':
        alph.set_big_letters_alphabet()
    elif choise == 'rus':
        alph.set_russian_alphabet()
    elif choise == 'bin':
        alph.set_binary_alphabet()
    elif choise == 'hex':
        alph.set_hexdigits_alphabet()
    elif choise == 'all':
        alph.set_all()
    return alph


def main():
    args = parse_args()
    if args.act in ['encode', 'decode']:
        if args.cipher == 'caesar':
            try:
                args.key = int(args.key)
            except Exception:
                print('Key for caesar cipher must be integer value')
                return
        with smart_open(args.input_file, 'r') as i:
            text = i.read()
        if args.file_alphabet:
            with open(args.file_alphabet, 'r') as a:
                alphabet = ab.Alphabet(a.read())
        else:
            alphabet = get_alphabet(args.alphabet)
        if args.cipher == 'caesar':
            with smart_open(args.output_file, 'w') as o:
                if args.act == 'encode':
                    o.write(c.encrypt(text, args.key, alphabet))
                else:
                    o.write(c.decrypt(text, args.key, alphabet))
        if args.cipher == 'vigenere':
            with smart_open(args.output_file, 'w') as o:
                if args.act == 'encode':
                    o.write(vg.encrypt(text, args.key, alphabet))
                else:
                    o.write(vg.decrypt(text, args.key, alphabet))
        if args.cipher == 'vernam':
            with smart_open(args.output_file, 'w') as o:
                if args.act == 'encode':
                    o.write(vn.encrypt(text, args.key, alphabet))
                else:
                    o.write(vn.decrypt(text, args.key, alphabet))
                o.write('\n')
    elif args.act == 'train':
        with smart_open(args.text_file, 'r') as i:
            text = i.read()
        if not text:
            raise ValueError('Text must be non-empty')
        analyse = an.Analyser(
            text, args.ngrams, args.punc, args.top, args.count_avg
        )
        with smart_open(args.model_file, 'w') as o:
            json.dump(analyse.dump(), o)
    elif args.act == 'hack':
        with smart_open(args.input_file, 'r') as i:
            text = i.read()
        analyse = an.Analyser()
        with smart_open(args.model_file, 'r') as m:
            try:
                analyse.load(json.load(m))
            except Exception:
                raise ValueError('Model file is corrupted!')
        if args.file_alphabet:
            with open(args.file_alphabet, 'r') as a:
                alphabet = ab.Alphabet(a.read())
        else:
            alphabet = get_alphabet(args.alphabet)
        with smart_open(args.output_file, 'w') as o:
            o.write(c.hack(text, analyse, alphabet))


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print(sys.exc_info()[1])

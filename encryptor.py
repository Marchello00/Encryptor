#!/usr/local/bin/python3

import argparse


def parse_args():
    cyphers = ['caesar', 'vernam', 'vigenere']

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(help='List of commands')

    encode_parser = subparsers.add_parser('encode', help='Encode message')
    encode_parser.add_argument('--cipher', '-c', required=True,
                               choices=cyphers,
                               help='Encryption algorithm')
    encode_parser.add_argument('--key', '-k', required=True,
                               help='Key which will used for encoding message')
    encode_parser.add_argument('--input_file', '-i',
                               help='Message will be read from this file')
    encode_parser.add_argument('--output_file', '-o',
                               help='Encoded message '
                                    'will be written to this file')

    decode_parser = subparsers.add_parser('decode', help='Decode message')
    decode_parser.add_argument('--cipher', '-c', required=True,
                               choices=cyphers,
                               help='Encryption algorithm')
    decode_parser.add_argument('--key', '-k', required=True,
                               help='Key what was used for encoding message')
    decode_parser.add_argument('--input_file', '-i',
                               help='Encoded message '
                                    'will be read from this file')
    decode_parser.add_argument('--output_file', '-o',
                               help='Decoded message '
                                    'will be written to this file')

    train_parser = subparsers.add_parser('train',
                                         help='Create train model '
                                              'on your text')
    train_parser.add_argument('--text_file', '-t',
                              help='Text for training')
    train_parser.add_argument('--model-file', '-m',
                              help='Trained model '
                                   'will be written to this file')

    hack_parser = subparsers.add_parser('hack', help='Try to hack message')
    hack_parser.add_argument('--input_file', '-i',
                             help='Encoded message '
                                  'will be read from this file')
    hack_parser.add_argument('--output-file', '-o',
                             help='Decoded message '
                                  'will be written to this file')
    hack_parser.add_argument('--model-file', '-m',
                             help='Trained model '
                                  'will be loaded from this file')
    return parser.parse_args()


def main():
    args = parse_args()
    

if __name__ == '__main__':
    main()

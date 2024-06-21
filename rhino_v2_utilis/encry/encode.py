#!/bin/env python3

import argparse
from crypt import Encrypt, Decrypt, DecodeText

tk = "ENCRYPTED|"

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="encode/decode tools")
    parser.add_argument("-d", "--decode", nargs='?', default='encode',
                        help="decode the text", dest='code')
    parser.add_argument("-t", "--text", nargs="+",
                        help="the text to de/en code", type=str, dest='text')

    # pdb.set_trace()
    args = parser.parse_args()
    text = args.text[0]
    if args.code == 'encode':
        en_str = Encrypt(text)
        print(en_str)
        print(tk,en_str)
    else:
        try:
            if text.find(tk) >= 0:
                de_str = DecodeText(text)
            else:
                de_str = Decrypt(text)
            print(de_str)
        except:
            print("Bad args!")

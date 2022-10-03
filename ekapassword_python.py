'''EkaPassword in python

Tested on Python 3.10.7

https://vpnry.github.io/ekapassword
Ref: jsSHA-3.2.0/test/genHashRounds.py
'''

import math
import hashlib
import binascii


__version__ = 1

NN = "0123456789"
PP = "!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~"
SS = "abcdefghijklmnopqrstuvwxyz"
BB = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def hash_this(txt):
    s512 = hashlib.sha512()
    byte_txt = txt.encode(encoding='utf-8')
    s512.update(byte_txt)

    res = binascii.b2a_base64(s512.digest(), newline=False)

    return res.decode(encoding='utf-8')


def getch(pre_token, from_str):
    this_hash = hash_this(pre_token)
    haf = math.floor(len(this_hash) / 2)

    ccode = ord(this_hash[haf])
    n = ccode % len(from_str)

    return from_str[n]


def get4ch(pre_token):
    # hash + str => new hash
    # so 4 selected chars will be more random

    n = getch(f'{pre_token}{NN}', NN)
    s = getch(f'{pre_token}{SS}', SS)
    b = getch(f'{pre_token}{BB}', BB)
    p = getch(f'{pre_token}{PP}', PP)

    return f'{n}{s}{b}{p}'


def gen_password(resource, masterpwd, pwd_len):
    resource = str(resource).lower().strip()

    in_token = f'{pwd_len}{masterpwd}{resource}'
    this_hash = hash_this(in_token)

    add4chars = get4ch(in_token + this_hash)

    pwd_len = int(pwd_len)
    haf = math.floor(pwd_len / 2)

    # 4 chars in the original hash are replaced with add4chars
    # so the original hash is now hidden
    res = this_hash[0:haf] + add4chars + this_hash[haf + 4:]

    
    res = res[0:pwd_len]

    return res


if __name__ == '__main__':
    a = gen_password('user@gmail.com', 'testpassword1', 20)
    print(a)  # V13T1aYTQf9yA"r5vZTI

    b = gen_password('user@gmail.com', 'testpassword2', 20)
    print(b)  # zPrm9UdfSz0xE/Vi6x75

import string
from config import TOKEN_MIN_LEN


def calc_tokens(s):
    for char in string.punctuation:
        s = s.replace(char, ' ')

    s = s.replace('…', ' ')

    words = s.split()
    words.sort(key=len, reverse=True)
    return [x for x in words if len(x) >= TOKEN_MIN_LEN]


def omit_symbols(s):
    for char in string.punctuation:
        s = s.replace(char, ' ')

    s = s.replace('…', ' ')
    s = s.replace('//', '')
    s = s.replace(' ', '')
    return s

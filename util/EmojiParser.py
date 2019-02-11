import re

"""
Code pour parser les emoticons
[ref] https://stackoverflow.com/questions/40222971/python-find-equivalent-surrogate-pair-from-non-bmp-unicode-char
"""

_nonbmp = re.compile(r'[\U00010000-\U0010FFFF]')


def _surrogatepair(match):
    char = match.group()
    assert ord(char) > 0xffff
    encoded = char.encode('utf-16-le')
    return (
        chr(int.from_bytes(encoded[:2], 'little')) +
        chr(int.from_bytes(encoded[2:], 'little')))


def with_surrogates(text):
    return _nonbmp.sub(_surrogatepair, text)
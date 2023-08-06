import jellyfish
from sklearn.base import BaseEstimator

from ._prep import TextPrep


class PhoneticTextPrep(TextPrep, BaseEstimator):
    """
    The ProneticPrep object prepares strings by encoding them phonetically.

    Arguments:
        kind: type of encoding, either `"soundex"`, "`metaphone`" or `"nysiis"`

    Usage:

    ```python
    import spacy
    from tokenwiser.textprep import PhoneticTextPrep

    nlp = spacy.load("en_core_web_sm")
    example1 = PhoneticTextPrep(kind="soundex").transform(["dinosaurus book"])
    example2 = PhoneticTextPrep(kind="metaphone").transform(["dinosaurus book"])
    example3 = PhoneticTextPrep(kind="nysiis").transform(["dinosaurus book"])

    assert example1[0] == 'D526 B200'
    assert example2[0] == 'TNSRS BK'
    assert example3[0] == 'DANASAR BAC'
    ```
    """

    def __init__(self, kind="soundex"):
        methods = {
            "soundex": jellyfish.soundex,
            "metaphone": jellyfish.metaphone,
            "nysiis": jellyfish.nysiis,
        }
        self.kind = kind
        self.method = methods[kind]

    def encode_single(self, x):
        return " ".join([self.method(d) for d in x.split(" ")])

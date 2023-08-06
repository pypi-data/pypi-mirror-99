import pyphen
from sklearn.base import BaseEstimator

from ._prep import TextPrep


class HyphenTextPrep(TextPrep, BaseEstimator):
    """
    Hyphenate the text going in.

    Usage:

    ```python
    from tokenwiser.textprep import HyphenTextPrep

    multi = HyphenTextPrep().transform(["geology", "astrology"])
    assert multi == ['geo logy', 'as tro logy']
    ```
    """

    def __init__(self, lang="en_GB"):
        self.lang = lang
        self.dic = pyphen.Pyphen(lang=lang)

    def encode_single(self, x):
        return " ".join(self.dic.inserted(x).split("-", -1))

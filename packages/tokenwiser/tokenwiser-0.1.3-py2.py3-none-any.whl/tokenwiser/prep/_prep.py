from abc import ABC, abstractmethod


class Prep(ABC):
    def fit(self, X, y=None):
        return self

    def partial_fit(self, X):
        return self

    @abstractmethod
    def encode_single(self, x):
        pass

    def pipe(self, X):
        for x in X:
            yield self.encode_single(x)

    def transform(self, X, y=None):
        return [self.encode_single(x) for x in X]

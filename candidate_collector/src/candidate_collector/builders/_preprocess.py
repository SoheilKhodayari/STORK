import re
from abc import ABC, abstractmethod


class Preprocessor(ABC):
    @abstractmethod
    def process(self, value):
        return value


class EscapeREPreprocessor(Preprocessor):
    def process(self, value):
        return re.escape(value)


class ExpandSymbolsPreprocessor(Preprocessor):
    def __init__(self):
        self.expansion_rules = dict()

    def expand(self, symbol, value):
        self.expansion_rules[symbol] = value

    def process(self, value):
        expanded_value = value
        for symbol in self.expansion_rules.keys():
            expanded_value = expanded_value.replace(
                symbol, self.expansion_rules[symbol]
            )
        return expanded_value

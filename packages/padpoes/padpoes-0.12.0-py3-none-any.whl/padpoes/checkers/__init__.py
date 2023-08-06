"""Checkers list."""
from padpoes.checkers.empty import EmptyChecker
from padpoes.checkers.fuzzy import FuzzyChecker
from padpoes.checkers.glossary import GlossaryChecker
from padpoes.checkers.linelength import LineLengthChecker

checkers = [
    EmptyChecker(),
    FuzzyChecker(),
    GlossaryChecker(),
    LineLengthChecker(),
]

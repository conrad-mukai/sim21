"""
Simulation of a casino shoe. A shoe contains 2, 4, 6, or 8 decks of cards.
Reference:

    https://en.wikipedia.org/wiki/Shoe_(cards)
"""

# system imports
from enum import Enum
import random


class Suit(Enum):
    Diamond = 1
    Club = 2
    Heart = 3
    Spade = 4


class Rank(Enum):
    Ace = 1
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13


class Card(object):

    nvalues = len(Suit) * len(Rank)

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        if self.rank in (Rank.Jack, Rank.Queen, Rank.King):
            self.value = 10
        else:
            self.value = self.rank.value


class Deck:

    def __init__(self):
        self.cards = [Card(s, r) for s in Suit for r in Rank]


class Shoe:

    def __init__(self, ndecks):
        self.ncards = ndecks * Card.nvalues
        self.decks = ndecks * [Deck()]
        self.order = list(range(self.ncards))
        self.pointer = 0

    def shuffle(self):
        random.shuffle(self.order)
        self.pointer = 0

    def next(self):
        index = self.order[self.pointer]
        self.pointer += 1
        return self.decks[index // Card.nvalues].cards[index % Card.nvalues]

    def position(self):
        return self.pointer / self.ncards

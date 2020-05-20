"""
dealer playing strategies
"""

# package imports
from .base import PlayingStrategyBase


class Soft17(PlayingStrategyBase):

    def hit(self, player):
        score = player.score()
        if score == 17:
            return player.is_soft()
        else:
            return score < 17


class Stand17(PlayingStrategyBase):

    def hit(self, player):
        return player.score() < 17

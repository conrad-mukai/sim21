"""
Simple player playing strategy.
"""

# project imports
from .base import PlayingStrategyPlayerBase


class Simple(PlayingStrategyPlayerBase):

    def hit(self, player):
        return player.score() < 17

    def doubledown(self, player):
        return False

    def split(self, player):
        return False

    def surrender(self, player):
        return False

"""
Betting strategies
"""

# package imports
from .base import BettingStategyBase


class ConstantBettingStrategy(BettingStategyBase):

    def __init__(self):
        self.wager = self.get_minimum()

    def get_wager(self, player):
        if player.bankroll > self.wager:
            return self.wager
        else:
            return int(player.bankroll)

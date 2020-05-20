"""
Basic player strategy.
"""

# project imports
from .base import PlayingStrategyPlayerBase
from ..shoe import Rank


class Basic(PlayingStrategyPlayerBase):

    def doubledown(self, player):
        upcard = self.get_upcard()
        score = player.score()
        if player.is_soft():
            if upcard.rank is Rank.Ace or upcard.value > 6:
                return False
            if score >= 20:
                return False
            if score == 19:
                return upcard.value == 6
            if score == 18:
                return True
            if score == 17:
                return upcard.value >= 3
            if score >= 15 and score <= 16:
                return upcard.value >= 4
            if score >= 13 and score <= 14:
                return upcard.value >= 5
            else:
                return False
        else:
            if score > 11:
                return False
            if score == 11:
                return True
            if upcard.rank is Rank.Ace:
                return False
            if score == 10:
                return upcard.value <= 9
            if score == 9:
                return upcard.value >= 3 and upcard.value <= 6
            else:
                return False

    def split(self, player):
        card = player.hand[0]
        if card.rank is Rank.Ace:
            return True
        if card.value == 10:
            return False
        upcard = self.get_upcard()
        if card.value == 9:
            return upcard.rank is not Rank.Ace and upcard.value != 10 \
                   and upcard.value != 7
        if card.value == 8:
            return True
        if card.value == 7:
            return upcard.value <= 7 and upcard.rank is not Rank.Ace
        if card.value == 6:
            return upcard.value <= 6 and upcard.rank is not Rank.Ace
        if card.value == 5:
            return False
        if card.value == 4:
            return upcard.value in (5, 6)
        else:
            return upcard.value <= 7

    def surrender(self, player):
        if player.is_soft():
            return False
        upcard = self.get_upcard()
        score = player.score()
        if score == 17:
            return upcard.rank is Rank.Ace
        if score == 16:
            return upcard.rank is Rank.Ace or upcard.value in (9, 10)
        if score == 15:
            return upcard.rank is Rank.Ace or upcard.value == 10
        return False

    def hit(self, player):
        upcard = self.get_upcard()
        score = player.score()
        if player.is_soft():
            if score >= 19:
                return False
            if score == 18:
                return upcard.value >= 9 or upcard.rank is Rank.Ace
            else:
                return True
        else:
            if score >= 17:
                return False
            if score >= 13:
                return upcard.value >= 7 or upcard.rank is Rank.Ace
            if score == 12:
                if upcard.rank is Rank.Ace:
                    return True
                return upcard.value <= 3 or upcard.value >= 7
            else:
                return True

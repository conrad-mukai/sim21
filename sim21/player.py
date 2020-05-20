"""
Simulation of a player.
"""

# system imports
from enum import Enum

# project imports
from .shoe import Rank
from .stats import PlayerStats


class HandType(Enum):
    Soft = 0
    Hard = 1


class BasePlayer(object):

    def __init__(self):
        self.hand = []
        self.hand_divided = False

    def receive(self, card):
        self.hand.append(card)
        self.hand_divided = False

    def close_hand(self):
        del self.hand[:]
        self.hand_divided = False

    def blackjack(self):
        return len(self.hand) == 2 and self._score(HandType.Soft) == 21

    def busted(self):
        return self._score(HandType.Hard) > 21

    def is_soft(self):
        value, num_aces = self._divide_hand()
        if num_aces == 0:
            return False
        return value + 10 + num_aces <= 21

    def score(self):
        score = self._score(HandType.Soft)
        if score > 21:
            return self._score(HandType.Hard)
        else:
            return score

    def _score(self, hand_type):
        value, num_aces = self._divide_hand()
        if num_aces == 0:
            return value
        if hand_type is HandType.Soft:
            return value + 10 + num_aces
        else:
            return value + num_aces

    def _divide_hand(self):
        if not self.hand_divided:
            self.num_aces = 0
            self.value = 0
            for card in self.hand:
                if card.rank is Rank.Ace:
                    self.num_aces += 1
                else:
                    self.value += card.value
            self.hand_divided = True
        return self.value, self.num_aces


class Dealer(BasePlayer):

    # dealers hand
    up_card = 0
    hole_card = 1

    def __init__(self, playing_strategy):
        super().__init__()
        self.playing_strategy = playing_strategy

    def hit(self):
        return self.playing_strategy.hit(self)

    def get_upcard(self):
        return self.hand[Dealer.up_card]


class _SharedCount(object):

    def __init__(self, count):
        self.count = count

    def __eq__(self, other):
        return self.count == other

    def __gt__(self, other):
        return self.count > other

    def __ge__(self, other):
        return self.count >= other

    def __lt__(self, other):
        return self.count < other

    def __le__(self, other):
        return self.count <= other

    def __iadd__(self, other):
        self.count += other
        return self

    def __isub__(self, other):
        self.count -= other
        return self

    def __int__(self):
        return self.count


class PlayerType(Enum):
    Primary = 0
    Split = 1


class Player(BasePlayer):

    c_config = None

    def __init__(self, name, bankroll, betting_strategy, playing_strategy,
                 player_type=PlayerType.Primary, hand_count=None, stats=None):
        super().__init__()
        self.name = name
        self.wager = 0
        self.betting_strategy = betting_strategy
        self.playing_strategy = playing_strategy
        if stats is None:
            self.stats = PlayerStats(self.betting_strategy,
                                     self.playing_strategy,
                                     bankroll)
        else:
            self.stats = stats
        if type(bankroll) is int:
            self.bankroll = _SharedCount(bankroll)
        else:
            self.bankroll = bankroll
        self.player_type = player_type
        if hand_count is None:
            self.hand_count = _SharedCount(1)
        else:
            self.hand_count = hand_count
        self.split_game = False

    def blackjack(self):
        if super().blackjack() and not self.split_game:
            self.stats.blackjacks += 1
            return True
        else:
            return False

    def close_hand(self):
        super().close_hand()
        self.split_game = False
        self.hand_count.count = 1

    def is_bankrolled(self):
        return self.bankroll >= self.c_config.minimum

    def is_playing(self):
        return self.wager > 0

    def place_bet(self):
        self.wager = self.betting_strategy.get_wager(self)
        self.bankroll -= self.wager
        self.stats.games += 1

    def doubledown(self):
        if self.split_game and not self.c_config.DAS:
            return False
        if self.bankroll < self.wager:
            return False
        dd = self.playing_strategy.doubledown(self)
        if dd:
            self.bankroll -= self.wager
            self.wager <<= 1
            self.stats.doubles += 1
        return dd

    def split(self):
        if self.hand[0].value != self.hand[1].value:
            return False
        if self.hand_count == self.c_config.maxhands:
            return False
        if self.bankroll < self.wager:
            return False
        split = self.playing_strategy.split(self)
        if split:
            self.hand_count += 1
            self.stats.splits += 1
        return split

    def surrender(self):
        if self.split_game:
            return False
        surrender = self.playing_strategy.surrender(self)
        if surrender:
            self.wager >>= 1
            self.bankroll += self.wager
            self.stats.surrenders += 1
        return surrender

    def hit(self):
        if self.split_game and self.hand[0].rank is Rank.Ace:
            return False
        return self.playing_strategy.hit(self)

    def win(self, multiplier=None):
        if multiplier is None:
            winnings = self.wager
        else:
            winnings = multiplier * self.wager
        self.bankroll += winnings + self.wager
        self.wager = 0
        self.close_hand()
        self.stats.wins += 1
        return winnings

    def lose(self):
        wager = self.wager
        self.wager = 0
        self.close_hand()
        self.stats.loses += 1
        return wager

    def push(self):
        self.bankroll += self.wager
        self.wager = 0
        self.close_hand()
        self.stats.pushes += 1

    def remove(self):
        card = self.hand[-1]
        del self.hand[-1]
        self.hand_divided = False
        return card

    def clone(self, override=None):
        if override is None:
            cls = self.__class__
        else:
            cls = override
        clone = cls(self.name, self.bankroll, self.betting_strategy,
                    self.playing_strategy, player_type=PlayerType.Split,
                    hand_count=self.hand_count, stats=self.stats)
        clone.receive(self.remove())
        clone.wager = self.wager
        clone.bankroll -= clone.wager
        self.split_game = True
        clone.split_game = True
        return clone

"""
Recorder classes for debugging and testing.
"""

# system imports
import json

# project imports
from .player import Player, Dealer
from .shoe import Rank

# global variables
_simulations = []

# constants
RECORDER_PLAYERS_KEY = 'players'
RECORDER_DEALER_KEY = 'dealer'
RECORDER_PLAYER_WAGER_KEY = 'wager'
RECORDER_PLAYER_HAND_KEY = 'hand'
RECORDER_PLAYER_ACTION_KEY = 'action'
RECORDER_PLAYER_ACTION_TYPE_KEY = 'type'
RECORDER_PLAYER_ACTION_HIT = 'hit'
RECORDER_PLAYER_ACTION_STAND = 'stand'
RECORDER_PLAYER_ACTION_DOUBLE_DOWN = 'dd'
RECORDER_PLAYER_ACTION_SPLIT = 'split'
RECORDER_PLAYER_ACTION_SURRENDER = 'surr'
RECORDER_PLAYER_ACTION_DRAW_KEY = 'draw'
RECORDER_PLAYER_ACTION_SPLITS_KEY = 'splits'
RECORDER_PLAYER_ACTION_SPLIT_INDEX = 'index'
RECORDER_PLAYER_ACTION_SPLIT_PLAY = 'play'
RECORDER_PLAYER_RESULT_KEY = 'result'
RECORDER_PLAYER_BANKROLL_KEY = 'bankroll'
RECORDER_DEALER_HAND_KEY = 'hand'
RECORDER_DEALER_DRAW_KEY = 'draw'


def dump_simulations(rfile):
    with open(rfile, 'w') as f:
        json.dump(_simulations, f, indent=2)
    del _simulations[:]


def _bankroll(f):
    def _wrapper(self, *args):
        try:
            return f(self, *args)
        finally:
            self.record[RECORDER_PLAYER_BANKROLL_KEY] = int(self.bankroll)
    return _wrapper


class PlayerRecorder(Player):

    def place_bet(self):
        try:
            return super().place_bet()
        finally:
            if len(_simulations) == 0 \
               or self.name in _simulations[-1][RECORDER_PLAYERS_KEY]:
                _simulations.append({
                    RECORDER_PLAYERS_KEY: {},
                    RECORDER_DEALER_KEY: {
                        RECORDER_DEALER_HAND_KEY: [],
                        RECORDER_DEALER_DRAW_KEY: []
                    }
                })
            self.record = _simulations[-1][RECORDER_PLAYERS_KEY][self.name] \
                = {RECORDER_PLAYER_WAGER_KEY: self.wager,
                   RECORDER_PLAYER_HAND_KEY: [],
                   RECORDER_PLAYER_ACTION_KEY: {}}

    def receive(self, card):
        try:
            return super().receive(card)
        finally:
            if hasattr(self, 'record'):
                if len(self.record[RECORDER_PLAYER_HAND_KEY]) < 2:
                    self.record[RECORDER_PLAYER_HAND_KEY] \
                        .append(_convert_card(card))
                else:
                    self.record[RECORDER_PLAYER_ACTION_KEY] \
                               [RECORDER_PLAYER_ACTION_DRAW_KEY] \
                        .append(_convert_card(card))

    def hit(self):
        hit = super().hit()
        player_action = self.record[RECORDER_PLAYER_ACTION_KEY]
        if player_action.get(RECORDER_PLAYER_ACTION_TYPE_KEY) is None:
            if hit:
                player_action[RECORDER_PLAYER_ACTION_TYPE_KEY] \
                    = RECORDER_PLAYER_ACTION_HIT
                player_action[RECORDER_PLAYER_ACTION_DRAW_KEY] = []
            else:
                player_action[RECORDER_PLAYER_ACTION_TYPE_KEY] \
                    = RECORDER_PLAYER_ACTION_STAND
        return hit

    def doubledown(self):
        dd = super().doubledown()
        if dd:
            player_action = self.record[RECORDER_PLAYER_ACTION_KEY]
            player_action[RECORDER_PLAYER_ACTION_TYPE_KEY] \
                = RECORDER_PLAYER_ACTION_DOUBLE_DOWN
            player_action[RECORDER_PLAYER_ACTION_DRAW_KEY] = []
        return dd

    def split(self):
        split = super().split()
        if split:
            player_action = self.record[RECORDER_PLAYER_ACTION_KEY]
            player_action[RECORDER_PLAYER_ACTION_TYPE_KEY] \
                = RECORDER_PLAYER_ACTION_SPLIT
            player_action[RECORDER_PLAYER_ACTION_SPLITS_KEY] = [
                {
                    RECORDER_PLAYER_HAND_KEY: [],
                    RECORDER_PLAYER_ACTION_KEY: {}
                },
                {
                    RECORDER_PLAYER_HAND_KEY: [],
                    RECORDER_PLAYER_ACTION_KEY: {}
                }
            ]
        return split

    def surrender(self):
        surrender = super().surrender()
        if surrender:
            player_action = self.record[RECORDER_PLAYER_ACTION_KEY]
            player_action[RECORDER_PLAYER_ACTION_TYPE_KEY] \
                = RECORDER_PLAYER_ACTION_SURRENDER
        return surrender

    @_bankroll
    def win(self, *args):
        result = super().win(*args)
        self.record[RECORDER_PLAYER_RESULT_KEY] = result
        return result

    @_bankroll
    def lose(self):
        result = super().lose()
        self.record[RECORDER_PLAYER_RESULT_KEY] = -result
        return result

    @_bankroll
    def push(self):
        super().push()
        self.record[RECORDER_PLAYER_RESULT_KEY] = 0

    def clone(self):
        clone = super().clone(override=self.__class__)
        player_action = self.record[RECORDER_PLAYER_ACTION_KEY]
        self.record = player_action[RECORDER_PLAYER_ACTION_SPLITS_KEY][0]
        self.record[RECORDER_PLAYER_HAND_KEY].append(
            _convert_card(self.hand[0])
        )
        clone.record = player_action[RECORDER_PLAYER_ACTION_SPLITS_KEY][1]
        clone.record[RECORDER_PLAYER_HAND_KEY].extend(
            _convert_card(c) for c in clone.hand
        )
        return clone


class DealerRecorder(Dealer):

    def receive(self, card):
        try:
            return super().receive(card)
        finally:
            dealer_record = _simulations[-1][RECORDER_DEALER_KEY]
            if len(dealer_record[RECORDER_DEALER_HAND_KEY]) < 2:
                dealer_record[RECORDER_DEALER_HAND_KEY] \
                    .append(_convert_card(card))
            else:
                dealer_record[RECORDER_DEALER_DRAW_KEY] \
                    .append(_convert_card(card))


def _convert_card(card):
    if card.rank is Rank.Ace:
        return 'A'
    else:
        return card.value

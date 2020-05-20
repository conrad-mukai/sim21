"""
Manage all players in game. Players configured using JSON file.
"""

# system imports
from enum import Enum
import importlib

# project imports
from .config import PLAYER_NAME_KEY, PLAYER_STRATEGIES_KEY, \
    STRATEGY_BETTING_KEY, STRATEGY_PLAYING_KEY, STRATEGY_CLASS_KEY, \
    STRATEGY_ARGS_KEY, PLAYER_WAGERS_KEY
from .player import Player, PlayerType
from .recorder import PlayerRecorder

# constants
_PLAYER_WAGERS_DEFAULT = 100


class PlayerNode(object):

    def __init__(self, player):
        self.player = player
        self.next = None


class Players(object):

    def __init__(self, config, rfile):
        Player.c_config = config
        player_configs = config.player_configs()
        self.players = PlayerNode(self._create_player(player_configs[0],
                                                      config.minimum, rfile))
        node = self.players
        for player_config in player_configs[1:]:
            node.next = PlayerNode(self._create_player(player_config,
                                                       config.minimum, rfile))
            node = node.next

    def __iter__(self):
        self.ptr = self.players
        while self.ptr is not None:
            yield self.ptr.player
            self.ptr = self.ptr.next

    def _create_player(self, player_config, minimum, rfile):
        strategies = player_config[PLAYER_STRATEGIES_KEY]
        betting_strategy \
            = self._create_strategy_object(strategies[STRATEGY_BETTING_KEY])
        playing_strategy \
            = self._create_strategy_object(strategies[STRATEGY_PLAYING_KEY])
        bankroll = minimum * player_config.get(PLAYER_WAGERS_KEY,
                                               _PLAYER_WAGERS_DEFAULT)
        if rfile is None:
            return Player(player_config[PLAYER_NAME_KEY], bankroll,
                          betting_strategy, playing_strategy)
        else:
            return PlayerRecorder(player_config[PLAYER_NAME_KEY], bankroll,
                                  betting_strategy, playing_strategy)

    def _create_strategy_object(self, strategy_config):
        mname, cls = strategy_config[STRATEGY_CLASS_KEY].split(':')
        module = importlib.import_module(mname)
        return getattr(module, cls)(*strategy_config.get(STRATEGY_ARGS_KEY,
                                                         []))

    def split(self, card1, card2):
        curr = self.ptr
        player = curr.player
        clone = player.clone()
        player.receive(card1)
        clone.receive(card2)
        next = curr.next
        curr.next = PlayerNode(clone)
        curr.next.next = next

    def cleanup(self):
        prev = self.players
        curr = self.players.next
        while curr is not None:
            if curr.player.player_type is PlayerType.Split:
                prev.next = curr.next
            else:
                prev = curr
            curr = curr.next

"""
player statistics
"""

# system imports
import re
import collections
import json

# 3rd party imports
import tabulate

# project imports
from .cmdline import SFORMAT_RAW

# constants
_CLASS_REGEX = r"^<class '(.+)'>$"
_RAW_ITEMS = ('games', 'wins', 'loses', 'pushes', 'blackjacks', 'doubles',
              'splits', 'surrenders', 'outcome')
_NORM_ITEMS = ('games', 'hands', 'wins', 'loses', 'pushes', 'blackjacks',
               'doubles', 'splits', 'surrenders', 'outcome')
_HAND_NORM_PCT_ITEMS = ('wins', 'loses', 'pushes', 'doubles', 'splits')
_GAME_NORM_PCT_ITEMS = ('blackjacks', 'surrenders')


class _Stats(object):

    def __init__(self):
        self.games = 0
        self.wins = 0
        self.loses = 0
        self.pushes = 0
        self.blackjacks = 0
        self.doubles = 0
        self.splits = 0
        self.surrenders = 0


class PlayerStats(_Stats):

    def __init__(self, betting_strategy, playing_strategy, bankroll):
        super().__init__()
        self.id = (re.search(_CLASS_REGEX,
                            str(betting_strategy.__class__)).group(1),
                   re.search(_CLASS_REGEX,
                             str(playing_strategy.__class__)).group(1))
        if type(bankroll) is int:
            self.bankroll = bankroll


class _StrategyStats(_Stats):

    def __init__(self):
        super().__init__()
        self.outcome = 0

    def accumulate(self, player):
        player_stats = player.stats
        self.games += player_stats.games
        self.wins += player_stats.wins
        self.loses += player_stats.loses
        self.pushes += player_stats.pushes
        self.blackjacks += player_stats.blackjacks
        self.doubles += player_stats.doubles
        self.splits += player_stats.splits
        self.surrenders += player_stats.surrenders
        self.outcome += int(player.bankroll) - player_stats.bankroll


class SimStats(object):

    def __init__(self, sfile, sformat):
        self.stats = collections.defaultdict(_StrategyStats)
        self.sfile = sfile
        self.sformat = sformat

    def add_player(self, player):
        self.stats[player.stats.id].accumulate(player)

    def dump(self):
        if self.sfile is None:
            return
        with open(self.sfile, 'w') as f:
            json.dump(
                {
                    id[0] + ':' + id[1]: {
                        k: getattr(stats, k) for k in _RAW_ITEMS
                    }
                    for id, stats in self.stats.items()
                }, f
            )

    def display(self):
        header = ['Stat']
        if self.sformat == SFORMAT_RAW:
            table = [[r] for r in _RAW_ITEMS]
            nrows = len(_RAW_ITEMS)
            for id, stats in self.stats.items():
                header.append("%s\n%s" % (id[0], id[1]))
                for i in range(nrows):
                    table[i].append(getattr(stats, _RAW_ITEMS[i]))
        else:
            table = [[r] for r in _NORM_ITEMS]
            for id, stats in self.stats.items():
                header.append("%s\n%s" % (id[0], id[1]))
                games = stats.games
                splits = stats.splits
                hands = games + splits
                table[_NORM_ITEMS.index('games')].append(games)
                table[_NORM_ITEMS.index('hands')].append(hands)
                for item in _HAND_NORM_PCT_ITEMS:
                    table[_NORM_ITEMS.index(item)].append(
                        '%0.2f' % (100 * getattr(stats, item) / hands)
                    )
                for item in _GAME_NORM_PCT_ITEMS:
                    table[_NORM_ITEMS.index(item)].append(
                        '%0.2f' % (100 * getattr(stats, item) / games)
                    )
                table[_NORM_ITEMS.index('outcome')].append(
                    '%06.3f' % (stats.outcome / games)
                )
        print(tabulate.tabulate(table, headers=header))

"""
Simulation of a casino blackjack game. This game is based on the Wikipedia
article:
    https://en.wikipedia.org/wiki/Blackjack
"""

# system imports
import sys
import traceback

# 3rd party imports
from tqdm import tqdm

# project imports
from .cmdline import parse_cmdline
from .config import Config
from .game import Game
from .strategies import set_config, set_game, strategy_reset
from .stats import SimStats


def main(argv=sys.argv):
    try:
        args = parse_cmdline(argv)
        _sim(args)
    except Exception as e:
        traceback.print_exc()
        return 1
    return 0


def _sim(args):
    config = Config(args.cfile)
    set_config(config)
    stats = SimStats(args.sfile, args.sformat)
    try:
        for i in _progress(args.quiet, args.nsim):
            _play(_rfile(args.rfile, i), args.ngame, config, stats)
    finally:
        stats.dump()
        if not args.quiet:
            stats.display()


def _progress(quiet, nsim):
    if quiet:
        return range(nsim)
    else:
        return tqdm(range(nsim))


def _rfile(rfile, count):
    if rfile is None:
        return rfile
    return "%s-%d.json" % (rfile, count)


def _play(rfile, ngame, config, stats):
    game = Game(rfile, config)
    set_game(game)
    game.play(ngame)
    _stats(game, stats)
    strategy_reset()


def _stats(game, stats):
    for player in game.players:
        stats.add_player(player)

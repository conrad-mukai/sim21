"""
CLI for simulation
"""

# system imports
import argparse
import os

# exported constants
SFORMAT_RAW = 'raw'
SFORMAT_NORMAL = 'normal'

# constants
_NGAME_DEFAULT = 1000
_SFORMAT_DEFAULT = SFORMAT_NORMAL


def _positive_definite(string):
    n = int(string)
    if n < 1:
        raise argparse.ArgumentTypeError("value must be > 0")
    return n


def _file_exists(fpath):
    if not os.path.exists(fpath):
        raise argparse.ArgumentTypeError("'%s' does not exist" % fpath)
    return fpath


def parse_cmdline(argv):
    parser = argparse.ArgumentParser(description="Casino Blackjack Simulation")
    parser.add_argument('-q', '--quiet', action='store_true',
                        help="no output")
    parser.add_argument('-r', '--rfile', default=None,
                        help="basename of JSON files for simulation recording")
    parser.add_argument('-n', '--ngame', type=_positive_definite,
                        default=_NGAME_DEFAULT,
                        help="number of games per simulation (default %d)"
                             % _NGAME_DEFAULT)
    parser.add_argument('-s', '--sformat',
                        choices=(SFORMAT_RAW, SFORMAT_NORMAL),
                        default=_SFORMAT_DEFAULT,
                        help="stats format (default is %s)" % _SFORMAT_DEFAULT)
    parser.add_argument('nsim', type=_positive_definite,
                        help="number of simulations")
    parser.add_argument('cfile', type=_file_exists,
                        help="JSON file for simulation configuration")
    parser.add_argument('sfile', nargs='?', default=None,
                        help="JSON file for statistics output (default is "
                             "stdout)")
    return parser.parse_args(argv[1:])

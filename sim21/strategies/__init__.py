"""
Strategies package
"""

from .globals import set_config, set_game
from .base import BettingStategyBase, PlayingStrategyPlayerBase, strategy_reset
from .betting import ConstantBettingStrategy
from .dealer import Soft17, Stand17
from .simple import Simple
from .basic import Basic

"""
Strategies base classes
"""


class StrategyBase(object):
    c_config = None
    c_game = None


def strategy_reset():
    StrategyBase.c_game = None


class _StrategyDecorators(object):

    @staticmethod
    def config(f):
        def _wrapper(self, *args, **kwargs):
            if StrategyBase.c_config is None:
                from .globals import g_config
                StrategyBase.c_config = g_config
            return f(self, *args, **kwargs)
        return _wrapper

    @staticmethod
    def game(f):
        def _wrapper(self, *args, **kwargs):
            if StrategyBase.c_game is None:
                from .globals import g_game
                StrategyBase.c_game = g_game
            return f(self, *args, **kwargs)
        return _wrapper


class BettingStategyBase(StrategyBase):

    @_StrategyDecorators.config
    def get_minimum(self):
        return self.c_config.minimum

    def get_wager(self, player):
        raise NotImplementedError()


class PlayingStrategyBase(StrategyBase):

    @_StrategyDecorators.game
    def get_upcard(self):
        return self.c_game.dealer.get_upcard()

    def hit(self, player):
        raise NotImplementedError()


class PlayingStrategyPlayerBase(PlayingStrategyBase):

    def doubledown(self, player):
        raise NotImplementedError()

    def split(self, player):
        raise NotImplementedError()

    def surrender(self, player):
        raise NotImplementedError()

"""
Simulation configuration
"""

# system imports
import json

# 3rd party imports
import jsonschema

# exported constants
PLAYER_NAME_KEY = 'name'
PLAYER_STRATEGIES_KEY = 'strategies'
PLAYER_WAGERS_KEY = 'wagers'
STRATEGY_BETTING_KEY = 'betting'
STRATEGY_PLAYING_KEY = 'playing'
STRATEGY_CLASS_KEY = 'class'
STRATEGY_ARGS_KEY = 'args'
GAME_DEALER_H17 = 'H17'
GAME_DEALER_S17 = 'S17'
GAME_BLACKJACK_3_2 = '3:2'
GAME_BLACKJACK_6_5 = '6:5'
GAME_MAXHANDS_UNLIMITED = 0
GAME_SURRENDER_NONE = 'none'
GAME_SURRENDER_LATE = 'late'
GAME_SURRENDER_EARLY = 'early'

# constants
_PLAYERS_KEY = 'players'
_PLAYERS_MAX = 7
_GAME_KEY = 'game'
_GAME_DEALER_KEY = 'dealer'
_GAME_DEALER_DEFAULT = GAME_DEALER_H17
_GAME_SINGLE_DECK_KEY = 'single-deck'
_GAME_SINGLE_DECK_DEFAULT = False
_GAME_SHOE_KEY = 'shoe'
_GAME_SHOE_MIN = 2
_GAME_SHOE_MAX = 8
_GAME_SHOE_DEFAULT = 6
_GAME_BLACKJACK_KEY = 'blackjack'
_GAME_BLACKJACK_DEFAULT = GAME_BLACKJACK_3_2
_GAME_DAS_KEY = 'DAS'
_GAME_DAS_DEFAULT = True
_GAME_MAXHANDS_KEY = 'maxhands'
_GAME_MAXHANDS_DEFAULT = GAME_MAXHANDS_UNLIMITED
_GAME_SURRENDER_KEY = 'surrender'
_GAME_SURRENDER_DEFAULT = GAME_SURRENDER_LATE
_GAME_RESHUFFLE_KEY = 'reshuffle'
_GAME_RESHUFFLE_DEFAULT = 0.75


def _config_decorator(f):
    def _wrapper(self):
        attr = '_%s' % f.__name__
        val = getattr(self, attr, None)
        if val is None:
            val = f(self)
            setattr(self, attr, val)
        return val
    return _wrapper


class Config(object):

    _strategy_schema = {
        'type': 'object',
        'properties': {
            STRATEGY_CLASS_KEY: {
                'type': 'string',
                'pattern': '^[a-z][._0-9a-z]*:[A-Za-z][_0-9A-Za-z]*$'
            },
            STRATEGY_ARGS_KEY: {
                'type': 'array'
            }
        },
        'additionalProperties': False,
        'required': [STRATEGY_CLASS_KEY]
    }

    _schema = {
        'type': 'object',
        'properties': {
            _PLAYERS_KEY: {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        PLAYER_NAME_KEY: {
                            'type': 'string'
                        },
                        PLAYER_STRATEGIES_KEY: {
                            'type': 'object',
                            'properties': {
                                STRATEGY_BETTING_KEY: _strategy_schema,
                                STRATEGY_PLAYING_KEY: _strategy_schema
                            },
                            'additionalProperties': False,
                            'required': [STRATEGY_BETTING_KEY,
                                         STRATEGY_PLAYING_KEY]
                        },
                        PLAYER_WAGERS_KEY: {
                            'type': 'integer',
                            'minimum': 1
                        }
                    },
                    'additionalProperties': False,
                    'required': [PLAYER_NAME_KEY, PLAYER_STRATEGIES_KEY]
                },
                'minItems': 1,
                'maxItems': _PLAYERS_MAX
            },
            _GAME_KEY: {
                'type': 'object',
                'properties': {
                    _GAME_DEALER_KEY: {
                        'type': 'string',
                        'enum': [GAME_DEALER_H17, GAME_DEALER_S17]
                    },
                    _GAME_SINGLE_DECK_KEY: {
                        'type': 'boolean'
                    },
                    _GAME_SHOE_KEY: {
                        'type': 'integer',
                        'multipleOf': 2,
                        'minimum': _GAME_SHOE_MIN,
                        'maximum': _GAME_SHOE_MAX
                    },
                    _GAME_BLACKJACK_KEY: {
                        'type': 'string',
                        'enum': [GAME_BLACKJACK_3_2, GAME_BLACKJACK_6_5]
                    },
                    _GAME_DAS_KEY: {
                        'type': 'boolean'
                    },
                    _GAME_MAXHANDS_KEY: {
                        'type': 'integer',
                        'minimum': GAME_MAXHANDS_UNLIMITED
                    },
                    _GAME_SURRENDER_KEY: {
                        'type': 'string',
                        'enum': [GAME_SURRENDER_NONE, GAME_SURRENDER_LATE,
                                 GAME_SURRENDER_EARLY]
                    },
                    _GAME_RESHUFFLE_KEY: {
                        'type': 'number',
                        'minimum': 0.0,
                        'exclusiveMaximum': 1.0
                    }
                },
                'additionalProperties': False
            }
        },
        'additionalProperties': False,
        'required': [_PLAYERS_KEY]
    }

    def __init__(self, cfile):
        with open(cfile) as f:
            self.config = json.load(f)
        jsonschema.validate(self.config, self._schema)
        self._validate_player_names()

    def _validate_player_names(self):
        name_list = [o[PLAYER_NAME_KEY] for o in self.config[_PLAYERS_KEY]]
        if len(set(name_list)) != len(name_list):
            raise ValueError("duplicate player name")

    def player_configs(self):
        return self.config[_PLAYERS_KEY]

    @property
    @_config_decorator
    def dealer(self):
        return self._game_config(_GAME_DEALER_KEY, _GAME_DEALER_DEFAULT)

    @property
    @_config_decorator
    def single_deck(self):
        return self._game_config(_GAME_SINGLE_DECK_KEY,
                                 _GAME_SINGLE_DECK_DEFAULT)

    @property
    @_config_decorator
    def shoe(self):
        if self.single_deck:
            return 1
        else:
            return self._game_config(_GAME_SHOE_KEY, _GAME_SHOE_DEFAULT)

    @property
    @_config_decorator
    def blackjack(self):
        return self._game_config(_GAME_BLACKJACK_KEY, _GAME_BLACKJACK_DEFAULT)

    @property
    @_config_decorator
    def DAS(self):
        return self._game_config(_GAME_DAS_KEY, _GAME_DAS_DEFAULT)

    @property
    @_config_decorator
    def maxhands(self):
        return self._game_config(_GAME_MAXHANDS_KEY, _GAME_MAXHANDS_DEFAULT)

    @property
    @_config_decorator
    def surrender(self):
        return self._game_config(_GAME_SURRENDER_KEY, _GAME_SURRENDER_DEFAULT)

    @property
    @_config_decorator
    def reshuffle(self):
        return self._game_config(_GAME_RESHUFFLE_KEY, _GAME_RESHUFFLE_DEFAULT)

    @property
    @_config_decorator
    def minimum(self):
        _minimum = 5
        if self.blackjack == GAME_BLACKJACK_3_2 \
           or self.surrender != GAME_SURRENDER_NONE:
            _minimum *= 2
        return _minimum

    def _game_config(self, key, default):
        return self.config.get(_GAME_KEY, {}).get(key, default)

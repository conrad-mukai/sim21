"""
Sequence cards in shoe for testing.
"""

# system imports
import random

# project imports
from sim21.shoe import Card

# global variables
_sequences = None
_game = None

# constants
PLAYERS_KEY = 'players'
DEALER_KEY = 'dealer'


def sequencer(indices):
    if _sequences is None:
        raise RuntimeError("sequences not set")
    global _game
    from sim21.strategies.globals import g_game
    _game = g_game
    index = 0
    for sim in _sequences:
        for sequence in sim[PLAYERS_KEY]:
            _set_card(sequence[0], index, indices)
            index += 1
        _set_card(sim[DEALER_KEY][0], index, indices)
        index += 1
        for sequence in sim[PLAYERS_KEY]:
            _set_card(sequence[1], index, indices)
            index += 1
        _set_card(sim[DEALER_KEY][1], index, indices)
        index += 1
        for sequence in sim[PLAYERS_KEY]:
            for test_card in sequence[2:]:
                _set_card(test_card, index, indices)
                index += 1
        for test_card in sim[DEALER_KEY][2:]:
            _set_card(test_card, index, indices)
            index += 1
    n = len(indices)
    for i in range(index, n):
        j = random.randrange(i, n)
        _swap(i, j, indices)


def _set_card(test_card, index, indices):
    value = _get_value(test_card)
    i = _get_index(index, value, indices)
    _swap(index, i, indices)


def _get_value(test_card):
    if test_card == 'A':
        return 1
    else:
        return test_card


def _get_index(index, value, indices):
    delta = 0
    for i in indices[index:]:
        if _game.shoe.decks[i // Card.nvalues] \
                     .cards[i % Card.nvalues].value == value:
            return index + delta
        else:
            delta += 1
    raise RuntimeError("could not find card")


def _swap(i1, i2, indices):
    if i1 == i2:
        return
    indices[i1], indices[i2] = indices[i2], indices[i1]


def set_sequences(sequences):
    _validate_sequences(sequences)
    global _sequences
    _sequences = sequences


def _validate_sequences(sequences):
    if type(sequences) is not list:
        raise TypeError("invalid sequences type")
    for sim in sequences:
        _validate_sim(sim)


def _validate_sim(sim):
    if type(sim) is not dict:
        raise TypeError("invalid sim type")
    if set(sim.keys()) != set((PLAYERS_KEY, DEALER_KEY)):
        raise ValueError("invalid keys in sim")
    if any(type(v) is not list for v in sim.values()):
        raise TypeError("invalid value type in sim dict")
    if len(sim[PLAYERS_KEY]) == 0:
        raise ValueError("no player sequences")
    if any(type(s) is not list for s in sim[PLAYERS_KEY]):
        raise TypeError("invalid players sequence type")
    for sequence in sim[PLAYERS_KEY]:
        _validate_sequence(sequence)
    _validate_sequence(sim[DEALER_KEY])


def _validate_sequence(sequence):
    if len(sequence) < 2:
        raise ValueError("sequence has less than 2 cards")
    if any(type(c) is not int and c != 'A' for c in sequence):
        raise ValueError("sequence has invalid item: %s"
                         % ','.join(str(c) for c in sequence))
    if any(c < 2 or c > 10 for c in sequence if type(c) is int):
        raise ValueError("invalid card value in sequence: %s"
                         % ','.join(str(c) for c in sequence))

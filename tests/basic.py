"""
Test basic playing strategy.
    https://en.wikipedia.org/wiki/Blackjack#Basic_strategy
"""

# system imports
import random
import os

# test imports
from .base import TestBase, test_decorator
from .sequencer import PLAYERS_KEY, DEALER_KEY

# project imports
from sim21.recorder import RECORDER_DEALER_KEY, RECORDER_DEALER_HAND_KEY, \
    RECORDER_PLAYERS_KEY, RECORDER_PLAYER_HAND_KEY, \
    RECORDER_PLAYER_ACTION_KEY, RECORDER_PLAYER_ACTION_TYPE_KEY, \
    RECORDER_PLAYER_ACTION_DRAW_KEY, RECORDER_PLAYER_ACTION_HIT


class _BasicStrategyTestBase(TestBase):

    cards = (2, 3, 4, 5, 6, 7, 8, 9, 10, 'A')
    ncards = len(cards)
    player_name = 'test-player'

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.config = os.path.join(cls.config_dir, 'single_player.json')

    def tearDown(self):
        if os.path.exists(self.rfile):
            os.remove(self.rfile)

    @staticmethod
    def normalize_actions(actions):
        return {k: v for r,v in actions
                     for k in range(r[0], r[-1]+1)}

    def _test(self, card, player_hand, dealer_hand):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [player_hand],
                    DEALER_KEY: dealer_hand
                }
            ],
            self.config
        )
        self.assertEqual(card,
                         records[0][RECORDER_DEALER_KEY]
                                [RECORDER_DEALER_HAND_KEY][0])
        return records[0][RECORDER_PLAYERS_KEY][self.player_name]

    @classmethod
    def _make_dealer_hand(cls, card):
        if card == 'A':
            skip = 10
        elif card == 10:
            skip = 'A'
        else:
            skip = 0
        return [card, random.choice(list(c for c in cls.cards if c != skip))]


class BasicStrategyHardTests(_BasicStrategyTestBase):

    actions = {
        (18, 21): ('stand', 'stand', 'stand', 'stand', 'stand', 'stand',
                   'stand', 'stand', 'stand', 'stand'),
        (17,):    ('stand', 'stand', 'stand', 'stand', 'stand', 'stand',
                   'stand', 'stand', 'stand', 'surr'),
        (16,):    ('stand', 'stand', 'stand', 'stand', 'stand', 'hit',
                   'hit',   'surr',  'surr',  'surr'),
        (15, ):   ('stand', 'stand', 'stand', 'stand', 'stand', 'hit',
                   'hit',   'hit',   'surr',  'surr'),
        (13, 14): ('stand', 'stand', 'stand', 'stand', 'stand', 'hit',
                   'hit',   'hit',   'hit',   'hit'),
        (12,):    ('hit',   'hit',   'stand', 'stand', 'stand', 'hit',
                   'hit',   'hit',   'hit',   'hit'),
        (11,):    ('dd',    'dd',    'dd',    'dd',    'dd',    'dd',
                   'dd',    'dd',    'dd',    'dd'),
        (10,):    ('dd',    'dd',    'dd',    'dd',    'dd',    'dd',
                   'dd',    'dd',    'hit',   'hit'),
        (9,):     ('hit',   'dd',    'dd',    'dd',    'dd',    'hit',
                   'hit',   'hit',   'hit',   'hit'),
        (5, 8):   ('hit',   'hit',   'hit',   'hit',   'hit',   'hit',
                   'hit',   'hit',   'hit',   'hit')
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._actions = cls.normalize_actions(cls.actions.items())

    def test_2card(self):
        for total, results in self._actions.items():
            if total == 21:
                continue
            for i in range(self.ncards):
                with self.subTest(id=total, upcard=self.cards[i]):
                    player_hand = self._make_player_hand(total)
                    dealer_hand = self._make_dealer_hand(self.cards[i])
                    self._test_2card(total, self.cards[i], results[i],
                                     player_hand, dealer_hand)

    @test_decorator
    def _test_2card(self, total, card, action, player_hand, dealer_hand):
        player_record = self._test(card, player_hand, dealer_hand)
        self.assertEqual(total, sum(player_record[RECORDER_PLAYER_HAND_KEY]))
        self.assertEqual(action,
                         player_record[RECORDER_PLAYER_ACTION_KEY]
                                      [RECORDER_PLAYER_ACTION_TYPE_KEY])

    def test_21(self):
        for card in self.cards:
            with self.subTest(id=21, upcard=card):
                dealer_hand = self._make_dealer_hand(card)
                player_hand = self._make_21_hand(dealer_hand[0])
                self._test_21(21, card, player_hand, dealer_hand)

    @test_decorator
    def _test_21(self, total, card, player_hand, dealer_hand):
        player_record = self._test(card, player_hand, dealer_hand)
        self.assertEqual(total,
                         sum(player_record[RECORDER_PLAYER_HAND_KEY]
                             +player_record[RECORDER_PLAYER_ACTION_KEY]
                                           [RECORDER_PLAYER_ACTION_DRAW_KEY]))
        self.assertEqual(RECORDER_PLAYER_ACTION_HIT,
                         player_record[RECORDER_PLAYER_ACTION_KEY]
                                      [RECORDER_PLAYER_ACTION_TYPE_KEY])

    @staticmethod
    def _make_player_hand(total):
        hand = []
        if total == 20:
            return [10, 10]
        else:
            if total % 2 == 0:
                skip = total // 2
            else:
                skip = 0
        maxval = min(10, total-2)
        v1 = random.choice(list(v for v in range(total-maxval, maxval+1)
                                if v != skip))
        hand.append(v1)
        hand.append(total-v1)
        return hand

    @classmethod
    def _make_21_hand(cls, upcard):
        i = cls.cards.index(upcard)
        totals = []
        for total, results in cls._actions.items():
            if results[i] == 'hit':
                totals.append(total)
        hand = cls._make_player_hand(random.choice(totals))
        score = sum(hand)
        card = 21 - score
        if card <= 10:  # just need 1 more card
            hand.append(card)
        else:   # need 2 more cards
            for total, results in cls._actions.items():
                if results[i] == 'dd':
                    totals.append(total)
            min_card = max(card - 10, 2)
            card = random.choice([s for s in (t-score for t in totals)
                                  if s>=min_card and s<11])
            hand.append(card)
            hand.append(21-card-score)
        return hand


class BasicStrategySoftTests(_BasicStrategyTestBase):

    actions = {
        (9,):   ('stand', 'stand', 'stand', 'stand', 'stand', 'stand', 'stand',
                 'stand', 'stand', 'stand'),
        (8,):   ('stand', 'stand', 'stand', 'stand', 'dd',    'stand', 'stand',
                 'stand', 'stand', 'stand'),
        (7,):   ('dd',    'dd',    'dd',    'dd',    'dd',    'stand', 'stand',
                 'hit',   'hit',   'hit'),
        (6,):   ('hit',   'dd',    'dd',    'dd',    'dd',    'hit',   'hit',
                 'hit',   'hit',   'hit'),
        (4, 5): ('hit',   'hit',   'dd',    'dd',    'dd',    'hit',   'hit',
                 'hit',   'hit',   'hit'),
        (2, 3): ('hit',   'hit',   'hit',   'dd',    'dd',    'hit',   'hit',
                 'hit',   'hit',   'hit')
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._actions = cls.normalize_actions(cls.actions.items())

    def test_soft(self):
        for player_card, results in self._actions.items():
            for i in range(self.ncards):
                with self.subTest(player_card=player_card,
                                  upcard=self.cards[i]):
                    player_hand = self._make_player_hand(player_card)
                    dealer_hand = self._make_dealer_hand(self.cards[i])
                    self._test_soft(player_card, self.cards[i], results[i],
                                    player_hand, dealer_hand)

    @test_decorator
    def _test_soft(self, player_card, upcard, action, player_hand,
                   dealer_hand):
        player_record = self._test(upcard, player_hand, dealer_hand)
        self.assertEqual(player_card,
                         player_record[RECORDER_PLAYER_HAND_KEY][1])
        self.assertEqual(action,
                         player_record[RECORDER_PLAYER_ACTION_KEY]
                                      [RECORDER_PLAYER_ACTION_TYPE_KEY])

    @staticmethod
    def _make_player_hand(card):
        return ['A', card]


class BasicStrategyPairTests(_BasicStrategyTestBase):

    actions = {
        'A':    ('split', 'split', 'split', 'split', 'split', 'split', 'split',
                 'split', 'split', 'split'),
        (10,):  ('stand', 'stand', 'stand', 'stand', 'stand', 'stand', 'stand',
                 'stand', 'stand', 'stand'),
        (9,):   ('split', 'split', 'split', 'split', 'split', 'stand', 'split',
                 'split', 'stand', 'stand'),
        (8,):   ('split', 'split', 'split', 'split', 'split', 'split', 'split',
                 'split', 'split', 'surr'),
        (7,):   ('split', 'split', 'split', 'split', 'split', 'split', 'hit',
                 'hit',   'hit',   'hit'),
        (6,):   ('split', 'split', 'split', 'split', 'split', 'hit',   'hit',
                 'hit',   'hit',   'hit'),
        (5,):   ('dd',    'dd',    'dd',    'dd',    'dd',    'dd',    'dd',
                 'dd',    'hit',   'hit'),
        (4,):   ('hit',   'hit',   'hit',   'split', 'split', 'hit',   'hit',
                 'hit',   'hit',   'hit'),
        (2, 3): ('split', 'split', 'split', 'split', 'split', 'split', 'hit',
                 'hit',   'hit',   'hit')
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._actions = {}
        cls._actions['A'] = cls.actions['A']
        cls._actions.update(cls.normalize_actions(
            (k,v) for k,v in cls.actions.items() if k is tuple
        ))

    def test_split(self):
        for player_card, results in self._actions.items():
            for i in range(self.ncards):
                with self.subTest(player_card=player_card,
                                  upcard=self.cards[i]):
                    player_hand = self._make_player_hand(player_card)
                    dealer_hand = self._make_dealer_hand(self.cards[i])
                    self._test_split(player_card, self.cards[i], results[i],
                                     player_hand, dealer_hand)

    @test_decorator
    def _test_split(self, player_card, upcard, action, player_hand,
                    dealer_hand):
        player_record = self._test(upcard, player_hand, dealer_hand)
        self.assertListEqual([player_card, player_card],
                             player_record[RECORDER_PLAYER_HAND_KEY])
        self.assertEqual(action,
                         player_record[RECORDER_PLAYER_ACTION_KEY]
                                      [RECORDER_PLAYER_ACTION_TYPE_KEY])

    @staticmethod
    def _make_player_hand(card):
        return [card, card]

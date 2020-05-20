"""
tests for double down scenarios
"""

# system imports
import os

# project imports
from sim21.recorder import RECORDER_PLAYERS_KEY, RECORDER_PLAYER_ACTION_KEY, \
    RECORDER_PLAYER_ACTION_TYPE_KEY, RECORDER_PLAYER_RESULT_KEY, \
    RECORDER_PLAYER_ACTION_SPLITS_KEY

# test imports
from .base import TestBase, test_decorator
from .sequencer import PLAYERS_KEY, DEALER_KEY


class DoubleDownTests(TestBase):

    player_name = 'test-player'

    @test_decorator
    def test_win(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        [6, 5, 10]
                    ],
                    DEALER_KEY: [10, 7]
                }
            ],
            os.path.join(self.config_dir, 'single_player.json')
        )
        player_record = records[0][RECORDER_PLAYERS_KEY][self.player_name]
        self.assertEqual('dd',
                         player_record[RECORDER_PLAYER_ACTION_KEY]
                                      [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(20, player_record[RECORDER_PLAYER_RESULT_KEY])

    @test_decorator
    def test_lose(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        [6, 5, 6]
                    ],
                    DEALER_KEY: [10, 8]
                }
            ],
            os.path.join(self.config_dir, 'single_player.json')
        )
        player_record = records[0][RECORDER_PLAYERS_KEY][self.player_name]
        self.assertEqual('dd',
                         player_record[RECORDER_PLAYER_ACTION_KEY]
                                      [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(-20, player_record[RECORDER_PLAYER_RESULT_KEY])

    @test_decorator
    def test_das(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        ['A', 'A', 8, 10, 9]
                    ],
                    DEALER_KEY: [6, 8, 3]
                }
            ],
            os.path.join(self.config_dir, 'das.json')
        )
        player_action = records[0][RECORDER_PLAYERS_KEY][self.player_name] \
                               [RECORDER_PLAYER_ACTION_KEY]
        self.assertEqual('split',
                         player_action[RECORDER_PLAYER_ACTION_TYPE_KEY])
        splits = player_action[RECORDER_PLAYER_ACTION_SPLITS_KEY]
        hand_1 = splits[0]
        self.assertEqual('dd',
                         hand_1[RECORDER_PLAYER_ACTION_KEY]
                               [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(20, hand_1[RECORDER_PLAYER_RESULT_KEY])
        hand_2 = splits[1]
        self.assertEqual('stand',
                         hand_2[RECORDER_PLAYER_ACTION_KEY]
                               [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(10, hand_2[RECORDER_PLAYER_RESULT_KEY])

    @test_decorator
    def test_no_das(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        ['A', 'A', 8, 10]
                    ],
                    DEALER_KEY: [6, 8, 5]
                }
            ],
            os.path.join(self.config_dir, 'no_das.json')
        )
        player_action = records[0][RECORDER_PLAYERS_KEY][self.player_name] \
            [RECORDER_PLAYER_ACTION_KEY]
        self.assertEqual('split',
                         player_action[RECORDER_PLAYER_ACTION_TYPE_KEY])
        splits = player_action[RECORDER_PLAYER_ACTION_SPLITS_KEY]
        hand_1 = splits[0]
        self.assertEqual('stand',
                         hand_1[RECORDER_PLAYER_ACTION_KEY]
                         [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(0, hand_1[RECORDER_PLAYER_RESULT_KEY])
        hand_2 = splits[1]
        self.assertEqual('stand',
                         hand_2[RECORDER_PLAYER_ACTION_KEY]
                         [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(10, hand_2[RECORDER_PLAYER_RESULT_KEY])

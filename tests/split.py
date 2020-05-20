"""
tests for split scenarios
"""

# system imports
import os

# project imports
from sim21.recorder import RECORDER_PLAYERS_KEY, RECORDER_PLAYER_ACTION_KEY, \
    RECORDER_PLAYER_ACTION_TYPE_KEY, RECORDER_PLAYER_ACTION_SPLITS_KEY, \
    RECORDER_PLAYER_RESULT_KEY, RECORDER_PLAYER_BANKROLL_KEY

# test imports
from .base import TestBase, test_decorator
from .sequencer import PLAYERS_KEY, DEALER_KEY

class SplitTests(TestBase):

    player_name = 'test-player'

    @test_decorator
    def test_split_unlimited(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        ['A', 'A', 'A', 'A', 'A', 10, 10, 10, 10, 10]
                    ],
                    DEALER_KEY: [6, 7, 7]
                }
            ],
            os.path.join(self.config_dir, 'split_unlimited.json')
        )
        action_record = records[0][RECORDER_PLAYERS_KEY][self.player_name] \
                                  [RECORDER_PLAYER_ACTION_KEY]
        self.assertEqual('split',
                         action_record[RECORDER_PLAYER_ACTION_TYPE_KEY])
        splits = action_record[RECORDER_PLAYER_ACTION_SPLITS_KEY]
        action_record_1 = splits[0][RECORDER_PLAYER_ACTION_KEY]
        action_record_2 = splits[1][RECORDER_PLAYER_ACTION_KEY]
        self.assertEqual('split',
                         action_record_1[RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual('split',
                         action_record_2[RECORDER_PLAYER_ACTION_TYPE_KEY])
        splits_1 = action_record_1[RECORDER_PLAYER_ACTION_SPLITS_KEY]
        action_record_1_1 = splits_1[0][RECORDER_PLAYER_ACTION_KEY]
        player_record_1_2 = splits_1[1]
        self.assertEqual('split',
                         action_record_1_1[RECORDER_PLAYER_ACTION_TYPE_KEY])
        splits_1_1 = action_record_1_1[RECORDER_PLAYER_ACTION_SPLITS_KEY]
        player_record_1_1_1 = splits_1_1[0]
        player_record_1_1_2 = splits_1_1[1]
        self.assertEqual('stand',
                         player_record_1_1_1[RECORDER_PLAYER_ACTION_KEY]
                         [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(10, player_record_1_1_1[RECORDER_PLAYER_RESULT_KEY])
        self.assertEqual(970,
                         player_record_1_1_1[RECORDER_PLAYER_BANKROLL_KEY])
        self.assertEqual('stand',
                         player_record_1_1_2[RECORDER_PLAYER_ACTION_KEY]
                                            [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(10, player_record_1_1_2[RECORDER_PLAYER_RESULT_KEY])
        self.assertEqual(990,
                         player_record_1_1_2[RECORDER_PLAYER_BANKROLL_KEY])
        self.assertEqual('stand',
                         player_record_1_2[RECORDER_PLAYER_ACTION_KEY]
                                          [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(10, player_record_1_2[RECORDER_PLAYER_RESULT_KEY])
        self.assertEqual(1010, player_record_1_2[RECORDER_PLAYER_BANKROLL_KEY])
        splits_2 = action_record_2[RECORDER_PLAYER_ACTION_SPLITS_KEY]
        player_record_2_1 = splits_2[0]
        player_record_2_2 = splits_2[1]
        self.assertEqual('stand',
                         player_record_2_1[RECORDER_PLAYER_ACTION_KEY]
                                          [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(10, player_record_2_1[RECORDER_PLAYER_RESULT_KEY])
        self.assertEqual(1030, player_record_2_1[RECORDER_PLAYER_BANKROLL_KEY])
        self.assertEqual('stand',
                         player_record_2_2[RECORDER_PLAYER_ACTION_KEY]
                                          [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(10, player_record_2_2[RECORDER_PLAYER_RESULT_KEY])
        self.assertEqual(1050, player_record_2_2[RECORDER_PLAYER_BANKROLL_KEY])


    @test_decorator
    def test_split_maxhand_4(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        ['A', 'A', 'A', 'A', 'A', 10, 10, 10]
                    ],
                    DEALER_KEY: [6, 7, 7]
                }
            ],
            os.path.join(self.config_dir, 'split_maxhand_4.json')
        )
        action_record = records[0][RECORDER_PLAYERS_KEY][self.player_name] \
                                  [RECORDER_PLAYER_ACTION_KEY]
        self.assertEqual('split',
                         action_record[RECORDER_PLAYER_ACTION_TYPE_KEY])
        splits = action_record[RECORDER_PLAYER_ACTION_SPLITS_KEY]
        action_record_1 = splits[0][RECORDER_PLAYER_ACTION_KEY]
        player_record_2 = splits[1]
        self.assertEqual('split',
                         action_record_1[RECORDER_PLAYER_ACTION_TYPE_KEY])
        splits_1 = action_record_1[RECORDER_PLAYER_ACTION_SPLITS_KEY]
        action_record_1_1 = splits_1[0][RECORDER_PLAYER_ACTION_KEY]
        player_record_1_2 = splits_1[1]
        self.assertEqual('split',
                         action_record_1_1[RECORDER_PLAYER_ACTION_TYPE_KEY])
        splits_1_1 = action_record_1_1[RECORDER_PLAYER_ACTION_SPLITS_KEY]
        player_record_1_1_1 = splits_1_1[0]
        player_record_1_1_2 = splits_1_1[1]
        self.assertEqual('stand',
                         player_record_1_1_1[RECORDER_PLAYER_ACTION_KEY]
                                            [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(10, player_record_1_1_1[RECORDER_PLAYER_RESULT_KEY])
        self.assertEqual(980,
                         player_record_1_1_1[RECORDER_PLAYER_BANKROLL_KEY])
        self.assertEqual('stand',
                         player_record_1_1_2[RECORDER_PLAYER_ACTION_KEY]
                                            [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(10, player_record_1_1_2[RECORDER_PLAYER_RESULT_KEY])
        self.assertEqual(1000,
                         player_record_1_1_2[RECORDER_PLAYER_BANKROLL_KEY])
        self.assertEqual('stand',
                         player_record_1_2[RECORDER_PLAYER_ACTION_KEY]
                                          [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(10, player_record_1_2[RECORDER_PLAYER_RESULT_KEY])
        self.assertEqual(1020, player_record_1_2[RECORDER_PLAYER_BANKROLL_KEY])
        self.assertEqual('stand',
                         player_record_2[RECORDER_PLAYER_ACTION_KEY]
                                        [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(-10, player_record_2[RECORDER_PLAYER_RESULT_KEY])
        self.assertEqual(1020, player_record_2[RECORDER_PLAYER_BANKROLL_KEY])

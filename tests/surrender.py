"""
test for surrender scenarios
"""

# system imports
import os

# project imports
from sim21.recorder import RECORDER_PLAYERS_KEY, RECORDER_PLAYER_ACTION_KEY, \
    RECORDER_PLAYER_ACTION_TYPE_KEY, RECORDER_PLAYER_RESULT_KEY

# test imports
from .base import TestBase, test_decorator
from .sequencer import PLAYERS_KEY, DEALER_KEY


class SurrenderTests(TestBase):

    player_name = 'test-player'

    @test_decorator
    def test_early(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        [6, 10]
                    ],
                    DEALER_KEY: [10, 'A']
                }
            ],
            os.path.join(self.config_dir, 'surrender_early.json')
        )
        player_record = records[0][RECORDER_PLAYERS_KEY][self.player_name]
        self.assertEqual("surr",
                         player_record[RECORDER_PLAYER_ACTION_KEY]
                                      [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(-5, player_record[RECORDER_PLAYER_RESULT_KEY])

    @test_decorator
    def test_late_blackjack(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        [6, 10]
                    ],
                    DEALER_KEY: [10, 'A']
                }
            ],
            os.path.join(self.config_dir, 'surrender_late.json')
        )
        player_record = records[0][RECORDER_PLAYERS_KEY][self.player_name]
        self.assertEqual(0, len(player_record[RECORDER_PLAYER_ACTION_KEY]))
        self.assertEqual(-10, player_record[RECORDER_PLAYER_RESULT_KEY])

    @test_decorator
    def test_late_no_blackjack(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        [6, 10]
                    ],
                    DEALER_KEY: [10, 7]
                }
            ],
            os.path.join(self.config_dir, 'surrender_late.json')
        )
        player_record = records[0][RECORDER_PLAYERS_KEY][self.player_name]
        self.assertEqual("surr",
                         player_record[RECORDER_PLAYER_ACTION_KEY]
                                      [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(-5, player_record[RECORDER_PLAYER_RESULT_KEY])

    @test_decorator
    def test_none(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        [6, 10, 5]
                    ],
                    DEALER_KEY: [10, 'A']
                }
            ],
            os.path.join(self.config_dir, 'surrender_none.json')
        )
        player_record = records[0][RECORDER_PLAYERS_KEY][self.player_name]
        self.assertEqual('hit',
                         player_record[RECORDER_PLAYER_ACTION_KEY]
                                      [RECORDER_PLAYER_ACTION_TYPE_KEY])
        self.assertEqual(-10, player_record[RECORDER_PLAYER_RESULT_KEY])

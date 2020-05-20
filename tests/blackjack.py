"""
Test blackjack scenarios.
"""

# system imports
import os

# project import
from sim21.recorder import RECORDER_PLAYERS_KEY, RECORDER_PLAYER_RESULT_KEY

# test imports
from .base import TestBase, test_decorator
from .sequencer import PLAYERS_KEY, DEALER_KEY


class BlackjackTests(TestBase):

    player_name = 'test-player'

    @test_decorator
    def test_32(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        [10, 'A']
                    ],
                    DEALER_KEY: [10, 7]
                }
            ],
            os.path.join(self.config_dir, 'blackjack_32.json')
        )
        self.assertEqual(15,
                         records[0][RECORDER_PLAYERS_KEY]
                                [self.player_name][RECORDER_PLAYER_RESULT_KEY])

    @test_decorator
    def test_65(self):
        records = self.run_sim21(
            [
                {
                    PLAYERS_KEY: [
                        [10, 'A']
                    ],
                    DEALER_KEY: [10, 7]
                }
            ],
            os.path.join(self.config_dir, 'blackjack_65.json')
        )
        self.assertEqual(12,
                         records[0][RECORDER_PLAYERS_KEY][self.player_name]
                                   [RECORDER_PLAYER_RESULT_KEY])

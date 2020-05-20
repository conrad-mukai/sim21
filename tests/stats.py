"""
stats test
"""

# system imports
import unittest
import os
import json

# project imports
from sim21 import main


class StatsTests(unittest.TestCase):

    config_dir = os.path.join(os.path.dirname(__file__), 'configs')
    stats_file = 'stats.json'

    def test_stats(self):
        try:
            result = main(['sim21', '-q', '1',
                           os.path.join(self.config_dir, 'single_player.json'),
                           self.stats_file])
            self.assertEqual(0, result)
            with open(self.stats_file) as f:
                stats = list(json.load(f).values())[0]
            self.assertEqual(stats['games'] + stats['splits'],
                             stats['wins'] + stats['loses'] + stats['pushes'])
        finally:
            if os.path.exists(self.stats_file):
                os.remove(self.stats_file)

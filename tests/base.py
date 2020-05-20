"""
Unit test base class.
"""

# system imports
import random
import unittest
import os
import json
import re

# test imports
from .sequencer import sequencer, set_sequences

# project imports
from sim21 import main


class TestBase(unittest.TestCase):

    rfile_base = 'records'
    rfile = 'records-0.json'

    @classmethod
    def setUpClass(cls):
        cls._shuffle = random.shuffle
        random.shuffle = sequencer
        cls.config_dir = os.path.join(os.path.dirname(__file__), 'configs')

    @classmethod
    def tearDownClass(cls):
        random.shuffle = cls._shuffle

    def run_sim21(self, sequences, config):
        set_sequences(sequences)
        result = main(['sim21', '-q', '-r', self.rfile_base, '-n',
                       str(len(sequences)), '1', config])
        self.assertEqual(0, result)
        with open(self.rfile) as f:
            return json.load(f)


def test_decorator(f):
    def _wrapper(self, *args):
        try:
            f(self, *args)
        except:
            if os.path.exists(self.rfile):
                test_case = self
                while test_case._subtest is not None:
                    test_case = test_case._subtest
                test_label = re.sub(r'=', '_',
                                    re.sub(r'[(,]', '.',
                                           re.sub(r'[\s)\']', '',
                                                  test_case.id())))
                os.rename(self.rfile, "%s.json" % test_label)
            raise
        else:
            os.remove(self.rfile)
    return _wrapper

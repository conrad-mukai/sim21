"""
Simulation of a blackjack game.
"""

# project imports
from .config import GAME_DEALER_H17, GAME_BLACKJACK_3_2, \
    GAME_SURRENDER_EARLY, GAME_SURRENDER_LATE
from .shoe import Shoe
from .player import Dealer
from .players import Players
from .recorder import DealerRecorder, dump_simulations
from .strategies import Soft17, Stand17


class _Multiplier(object):

    def __init__(self, num, den):
        self.num = num
        self.den = den

    def __mul__(self, other):
        return (self.num * other) // self.den


class Game(object):

    def __init__(self, rfile, config):
        self.config = config
        self.shoe = Shoe(self.config.shoe)
        if self.config.dealer == GAME_DEALER_H17:
            dealer_strategy = Stand17()
        else:
            dealer_strategy = Soft17()
        self.rfile = rfile
        if self.rfile is None:
            self.dealer = Dealer(dealer_strategy)
        else:
            self.dealer = DealerRecorder(dealer_strategy)
        if self.config.blackjack == GAME_BLACKJACK_3_2:
            self.blackjack_multiplier = _Multiplier(3, 2)
        else:
            self.blackjack_multiplier = _Multiplier(6, 5)
        self.players = Players(self.config, self.rfile)
        self.house = 0

    def play(self, ngame):
        self.shoe.shuffle()
        count = 0
        while count < ngame:
            try:
                self._shuffle()
                self._place_bets()
                self._deal()
                if self._surrender():
                    continue
                if self._player_hands():
                    continue
                if self._dealer_hand():
                    continue
                self._show_hands()
            finally:
                self.players.cleanup()
                self.dealer.close_hand()
                count += 1
                if self._all_done():
                    break
        if self.rfile is not None:
            dump_simulations(self.rfile)

    def _shuffle(self):
        if self.shoe.position() > self.config.reshuffle:
            self.shoe.shuffle()

    def _place_bets(self):
        for player in self._bet_iter():
            player.place_bet()

    def _deal(self):
        self._deal_round()
        self._deal_round()

    def _deal_round(self):
        for player in self._play_iter():
            player.receive(self.shoe.next())
        self.dealer.receive(self.shoe.next())

    def _surrender(self):
        surrender_policy = self.config.surrender
        if surrender_policy == GAME_SURRENDER_EARLY:
            self._player_surrender()
        elif surrender_policy == GAME_SURRENDER_LATE:
            if self.dealer.blackjack():
                self._dealer_blackjack()
            else:
                self._player_surrender()
        else:
            return False
        return len(list(self._play_iter())) == 0

    def _player_surrender(self):
        for player in self._play_iter():
            if player.surrender():
                self.house += player.lose()

    def _player_hands(self):
        for player in self._play_iter():
            first_call = True
            while first_call:
                if player.doubledown():
                    player.receive(self.shoe.next())
                    self._busted(player)
                    break
                if player.split():
                    self.players.split(self.shoe.next(), self.shoe.next())
                    continue
                first_call = False
                while player.hit():
                    player.receive(self.shoe.next())
                    if self._busted(player):
                        break
        return len(list(self._play_iter())) == 0

    def _busted(self, player):
        if player.busted():
            self.house += player.lose()
            return True
        return False

    def _dealer_hand(self):
        while self.dealer.hit():
            self.dealer.receive(self.shoe.next())
            if self.dealer.busted():
                for player in self._play_iter():
                    self.house -= player.win()
                return True
        return False

    def _show_hands(self):
        if self.dealer.blackjack():
            self._dealer_blackjack()
        else:
            dealer_score = self.dealer.score()
            for player in self._play_iter():
                if player.blackjack():
                    self.house -= player.win(self.blackjack_multiplier)
                    continue
                player_score = player.score()
                if player_score < dealer_score:
                    self.house += player.lose()
                elif player_score > dealer_score:
                    self.house -= player.win()
                else:
                    player.push()

    def _dealer_blackjack(self):
        for player in self._play_iter():
            if player.blackjack():
                player.push()
            else:
                self.house += player.lose()

    def _all_done(self):
        return len(list(self._bet_iter())) == 0

    def _bet_iter(self):
        return (p for p in self.players if p.is_bankrolled())

    def _play_iter(self):
        return (p for p in self.players if p.is_playing())

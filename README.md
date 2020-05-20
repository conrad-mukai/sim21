# sim21

Simulation to evaluate blackjack playing strategies.

## Introduction

This script allows the user to test betting and playing strategies for an
American casino version of blackjack. The rules of play are described in the
following Wikipedia article:

    https://en.wikipedia.org/wiki/Blackjack

The simulation sets up a table with between 1 and 7 players. Each player is
configured with a betting strategy and a playing strategy. At the beginning of
a game all players receive an amount of money called the bankroll. The
simulation then runs a specfied number of games. Each player participates in
all games unless their bankroll falls below the minimum required to play.

After a game all bankrolls are reset and the process is repeated for another
simulation. This is repeated many times to get a statistically meaningful
result. During execution a progress bar is displayed, and at the end a table
of results is output. After installing you can run an example as follows:

    % cd examples
    % sim21 100 config.json
    100%|███████████████████████████████████████████████████████████████████████████████████████| 100/100 [00:17<00:00,  5.71it/s]
    Stat          sim21.strategies.betting.ConstantBettingStrategy    sim21.strategies.betting.ConstantBettingStrategy
                                    sim21.strategies.simple.Simple                        sim21.strategies.basic.Basic
    ----------  --------------------------------------------------  --------------------------------------------------
    games                                               291334                                              299712
    hands                                               291334                                              307592
    wins                                                    41.07                                               42.28
    loses                                                   49.24                                               49.51
    pushes                                                   9.69                                                8.2
    blackjacks                                               3.34                                                3.43
    doubles                                                  0                                                  10.63
    splits                                                   0                                                   2.56
    surrenders                                               0                                                   5.43
    outcome                                                 -0.661                                              -0.126

Most terms in the results are explained in the Wikipedia article, but a few are
specific to this program. Games refers to how many initial games were played
for the particular combination of betting and playing strategy. Hands are the
number of games plus the number of splits. The wins, loses, and pushes are the
percentage of each result for all hands. Blackjacks, doubles, splits, and
surrenders are the percentage occurence of each event during the course of
play. Finally, outcome is the average change in a players bankroll per game.

## Requirements

This script uses Python 3. Package dependencies are defined in `setup.py` in
the root.

## Installation

To install just use the `setup.py` in the root:

    python setup.py (install|develop)

If you want to just run the code the use the `install` sub-command. If you want
to modify the code then use the `develop` sub-command.

## Command Line

The program usage is:

    usage: sim21 [-h] [-q] [-r RFILE] [-n NGAME] [-s {raw,normal}]
                 nsim cfile [sfile]
    
    Casino Blackjack Simulation
    
    positional arguments:
      nsim                  number of simulations
      cfile                 JSON file for simulation configuration
      sfile                 JSON file for statistics output (default is stdout)
    
    optional arguments:
      -h, --help            show this help message and exit
      -q, --quiet           no output
      -r RFILE, --rfile RFILE
                            basename of JSON files for simulation recording
      -n NGAME, --ngame NGAME
                            number of games per simulation (default 1000)
      -s {raw,normal}, --sformat {raw,normal}
                            stats format (default is normal)

The 2 required arguments are `nsim`, the number of simulations and `cfile`, the
configuration file. The optional `quiet` and `rfile` arguments are generally
useful for testing. The `ngame` option specifies the number of games played
before the simulation is reset. The total number of games played is
`nsim * ngame`. Finally `sformat` how the resulting statistics are displayed.
The `normal` setting displays results normalized by number of games or number
of hands. The `raw` settings displays raw counts.

## Configuration

The configuration file is in JSON format. It has the following syntax:

    {
      "players": [
        {
          "name": string,
          "strategies": {
            "betting": {
              "class": string,
              "args": [ // optional
                string | int | bool | ...,
                ...
              ]
            },
            "playing": {
              // same as betting
            }
          },
          "wagers": int // optional, default 100
        },
        ...
      ],
      "game": { // optional
        "dealer": "H17" | "S17",                // default H17
        "single-deck": bool,                    // default false
        "shoe": int,                            // [2..8], default 6
        "blackjack": "3:2" | "6:5",             // default 3:2
        "DAS": bool,                            // default true
        "maxhands": int,                        // [0..), default 0 (unlimited)
        "surrender": "none" | "early" | "late", // default late
        "reshuffle": float                      // [0.0 .. 1.0), default 0.75
      }
    }

### players section

* **name** Unique name.
* **strategies** Classes specifying betting and playing behavior. The
`class` parameter specifies a Python module and class and the optional `args`
parameter specifies arguments to pass to the class constructor. The two
strategies defined are for placing bets and for playing hands.
* **wagers** An optional parameter specifying the number of minimum wagers in
players initial bankroll. Default is 100.

### game section

This entire section is optional.

* **dealer** The two values are `H17` which indicates hit on soft 17, and `S17`
which indicates stand on all 17s.
* **single-deck** Boolean indicating a single deck. If this is `true` the
`shoe` parameter is ignored.
* **shoe** Number of decks in the shoe. Possible values are 2, 4, 6, or 8. The
default is 6.
* **blackjack** Payout on player blackjack. Possible values are `3:2` and `6:5`
which indicate the ratio of return on original bet. Default is `3:2`. The `6:5`
payout is generally tied to `single-deck` games.
* **DAS** Double on split. A boolean indicates if double down after splits is
allowed.
* **maxhands** Maximum number of hands a player is allowed due to splits. A
value of 0 indicates unlimited number of splits. 0 is the default.
* **surrender** Type of surrender. Possible values are `none`, `early`, or
`late`. `none` means surrender is not allowed, `early` indicates surrender
before dealer checks for blackjack, and `late` indicates surrender after
dealer checks for blackjack. Default is `late`.
* **reshuffle** Fraction into the shoe before a reshuffle occurs. Default is
0.75.

## Strategies

Strategies are defined by implementing classes derived from
`sim21.strategies.BettingStategyBase` and
`sim21.strategies.PlayingStrategyPlayerBase`. The base classes have access
to both configuration and game settings. There are several functions which must
be implemented to define a strategy. These functions are passed a player object
which gives the function access to player attributes like their bankroll
balance or their hand.

Examples of strategies 

### Betting Strategy

The betting strategy class must define the following:

* `get_wager(self, player)` Returns the wager to place.

### Playing Strategy

The playing strategy class must define the following:

* `hit(self, player)` Returns boolean indicating whether to hit or stand.
* `doubledown(self, player)` Returns boolean indicating whether to double down
or not.
* `split(self, player)` Returns boolean indicating whether to split a hand or
not.
* `surrender(self, player)` Returns boolean indicating whether to surrender a
hand or not.

## Testing

Unit tests are run as follows:

    python -m unittest tests

The `tests` directory contains the test definitions. Most of the tests are
derived from the `tests.base.TestBase` class. This class does the following:

* Provide access to the configuration object for the simulation.
* Replaces the `random.shuffle` function with a `sequencer` method. This method
allows the test case to specify what cards will be dealt for the test. The
sequences are specified by the `set_sequences` method.
* A method called `run_sim21`. This method calls `set_sequences` to setup a
scenario and then calls the `sim21` entrypoint with the quiet and recorder
options enabled.

In addition the `tests.base` module contains a function decorator called
`test_decorator`. This decorator is for methods in a test case. If a test fails
or errors the decorator will save the recording made by `run_sim21` into a file
with the name of the test; otherwise it removes the recording.

"""The vocabulary of games: who moves, what they can do and who won.

The names follow the standard notation of the literature (Russell & Norvig): a
game has an ``initial`` state, ``to_move``, ``actions``, a transition model
``result``, a terminal test ``is_terminal`` and ``utility``, the final score of a
terminal state for one player.

The games in this package report every call to ``result`` (event ``"result"``)
and to ``utility`` (event ``"utility"``) to an active recording, so tests and
experiments can see how many positions a search looked at.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from collections.abc import Hashable, Sequence

State = Hashable
Action = Hashable
Player = str


class Game(ABC):
    """A two-player, turn-taking game with perfect information."""

    initial: State
    players: tuple[Player, Player]

    @abstractmethod
    def to_move(self, state: State) -> Player:
        """The player whose turn it is in ``state``."""

    @abstractmethod
    def actions(self, state: State) -> Sequence[Action]:
        """The moves available in ``state``, in a fixed order."""

    @abstractmethod
    def result(self, state: State, action: Action) -> State:
        """The state reached by playing ``action`` in ``state``."""

    @abstractmethod
    def is_terminal(self, state: State) -> bool:
        """Whether the game is over in ``state``."""

    @abstractmethod
    def utility(self, state: State, player: Player) -> float:
        """The final score of the terminal ``state`` for ``player``."""

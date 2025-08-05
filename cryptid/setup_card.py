from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated, Final

from cryptid.clue import Clue
from cryptid.hex import FixedLength, Hex
from cryptid.tile import Structure


@dataclass
class SetupCard:
    board_sections: Annotated[list[int], FixedLength(6)]
    board_sections_inverted: Annotated[list[bool], FixedLength(6)]
    structures: list[tuple[Hex, Structure]]
    clues_3_player: tuple[Clue, Clue, Clue]
    clues_4_player: tuple[Clue, Clue, Clue, Clue]
    clues_5_player: tuple[Clue, Clue, Clue, Clue, Clue]
    hints_tuple: tuple[int, int, int]

    def __post_init__(self) -> None:
        self.clues: dict[int, tuple[Clue, ...]] = {
            3: self.clues_3_player,
            4: self.clues_4_player,
            5: self.clues_5_player,
        }

        # TODO: HINTS
        self.hints: dict[int, int] = {
            3: self.hints_tuple[0],
            4: self.hints_tuple[1],
            5: self.hints_tuple[2],
        }


SETUP_CARDS: Final[list[SetupCard]] = []

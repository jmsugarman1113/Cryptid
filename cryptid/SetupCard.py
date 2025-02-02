from __future__ import annotations

from dataclasses import dataclass
from typing import Annotated

from cryptid.Clue import Clue
from cryptid.Hex import FixedLength, Hex
from cryptid.Tile import Structure


@dataclass
class SetupCard:
    board_sections: Annotated[list[int], FixedLength(6)]
    structures: list[tuple[Hex, Structure]]
    clues_3_player: tuple[Clue, Clue, Clue]
    clues_4_player: tuple[Clue, Clue, Clue, Clue]
    clues_5_player: tuple[Clue, Clue, Clue, Clue, Clue]

    def __post_init__(self) -> None:
        self.clues: dict[int, tuple[Clue, ...]] = {
            3: self.clues_3_player,
            4: self.clues_4_player,
            5: self.clues_5_player,
        }

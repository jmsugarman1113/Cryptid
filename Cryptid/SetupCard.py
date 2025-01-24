from __future__ import annotations
from dataclasses import dataclass
from Cryptid.Hex import FixedLength, Hex
from typing import Annotated
from Cryptid.Clue import Clue
from Tile import Structure


@dataclass
class SetupCard:
    board_sections: Annotated[list[int], FixedLength(6)]
    structures: list[tuple[Hex, Structure]]
    clues: Annotated[dict[int, list[Clue]], FixedLength(3)]  # keys are guaranteed to be 3, 4, 5 for num players

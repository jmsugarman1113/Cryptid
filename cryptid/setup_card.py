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


SETUP_CARDS: Final[Annotated[list[SetupCard], 54]] = [
    # SetupCard(
    #     board_sections=[1, 6, 2, 5, 3, 4],
    #     board_sections_inverted=[True, True, False, False, True, False],
    #     structures=[
    #         (DoubledHeightCoordinateHex(1, 1), Structure(Shape.STANDING_STONE, Color.BLUE)),
    #         (DoubledHeightCoordinateHex(3, 5), Structure(Shape.ABANDONED_SHACK, Color.WHITE)),
    #         (DoubledHeightCoordinateHex(5, 5), Structure(Shape.STANDING_STONE, Color.WHITE)),
    #         (DoubledHeightCoordinateHex(4, 16), Structure(Shape.ABANDONED_SHACK, Color.BLUE)),
    #         (DoubledHeightCoordinateHex(11, 1), Structure(Shape.STANDING_STONE, Color.GREEN)),
    #         (DoubledHeightCoordinateHex(9, 13), Structure(Shape.ABANDONED_SHACK, Color.GREEN)),
    #     ],
    #     clues_3_player=(ALPHA_CLUES[28], DELTA_CLUES[85], EPSILON_CLUES[8]),
    #     clues_4_player=(ALPHA_CLUES[2], BETA_CLUES[43], DELTA_CLUES[52], EPSILON_CLUES[42]),
    #     clues_5_player=(ALPHA_CLUES[17], BETA_CLUES[19], GAMMA_CLUES[73], DELTA_CLUES[50], EPSILON_CLUES[11]),
    #     hints_tuple=(25, 74, 15),
    # ),
]

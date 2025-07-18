# mypy: ignore-errors

from cryptid.board_sections import BOARD_SECTIONS
from cryptid.clue import GREEN_CLUES
from cryptid.hex import AxialCoordinateHex, DoubledHeightCoordinateHex
from cryptid.tile import Terrain

if __name__ == "__main__":
    h = DoubledHeightCoordinateHex(0, 2)
    h = DoubledHeightCoordinateHex(3, 3)
    print(h.to_axial_coordinate_hex())
    print(h.reflect_over_hex())

    # A = AxialCoordinateHex(0, 0)
    #
    # print(A.neighbors)
    #
    # print(-1*A.neighbors[0])
    #
    # print(-A.neighbors[1])
    #
    # print(A.hexes_within_range(0))
    # print(A.hexes_within_range(1))
    # print((l := A.hexes_within_range(3)), f'\n{len(l)}')
    #
    # B = A.to_cube_coordinate_hex()
    # print(B.neighbors)

    C = AxialCoordinateHex(-2, -1).to_cube_coordinate_hex()
    D = AxialCoordinateHex(-4, 4).to_cube_coordinate_hex()
    E = C.reflect_over_hex(D)
    # print(E)

    print(C.reflect_over_hex())
    print(C.reflect_over_Q_axis())
    print(C.reflect_over_R_axis())
    print(C.reflect_over_S_axis())

    print(C.reflect_over_Q(q=0))
    print(C.reflect_over_Q(q=-1))
    print(C.reflect_over_Q(q=-2))
    # print(C.reflect_over_R(r=0))
    # print(C.reflect_over_S(s=0))

    print()
    print()
    clue = GREEN_CLUES[1]
    print(clue)
    print(repr(clue))

    h, tile = next(iter(BOARD_SECTIONS[0].tiles.items()))
    print(tile)
    print(str(tile))

    print(Terrain.WATER.value)

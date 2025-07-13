import random

from cryptid.hex import AxialCoordinateHex, CubeCoordinateHex, DoubledHeightCoordinateHex, DoubledWidthCoordinateHex


def get_random_AxialCooredinateHex(
    radius: int,
    random_seed: int,
    row_offset: int = 0,
    column_offset: int = 0,
) -> AxialCoordinateHex:
    random.seed(random_seed)
    q = random.randint(-radius, radius) + row_offset
    r = random.randint(-radius, radius) + column_offset
    return AxialCoordinateHex(q, r)


def get_random_CubeCooredinateHex(
    radius: int,
    random_seed: int,
    row_offset: int = 0,
    column_offset: int = 0,
) -> CubeCoordinateHex:
    random.seed(random_seed)
    q = random.randint(-radius, radius) + row_offset
    r = random.randint(-radius, radius) + column_offset
    return CubeCoordinateHex(q, r, -q - r)


def get_random_DoubleHeightCoordinateHex(
    radius: int,
    random_seed: int,
    row_offset: int = 0,
    column_offset: int = 0,
) -> DoubledHeightCoordinateHex:
    random.seed(random_seed)
    row = random.randint(-radius, radius) + row_offset
    col = random.randint(-radius, radius) // 2 + column_offset
    if (row + col) % 2 != 0:
        row += 1
    return DoubledHeightCoordinateHex.from_row_col(row, col)


def get_random_DoubleWidthCoordinateHex(
    radius: int,
    random_seed: int,
    row_offset: int = 0,
    column_offset: int = 0,
) -> DoubledWidthCoordinateHex:
    random.seed(random_seed)
    col = random.randint(-radius, radius) + row_offset
    row = random.randint(-radius, radius) // 2 + column_offset
    if (row + col) % 2 != 0:
        row += 1
    return DoubledWidthCoordinateHex.from_row_col(row, col)

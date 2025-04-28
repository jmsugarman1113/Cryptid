import copy
import random

import pytest

from cryptid.hex import AxialCoordinateHex, CubeCoordinateHex, DoubledHeightCoordinateHex


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


class TestDoubledHeightCoordinateHex:
    origin: DoubledHeightCoordinateHex = DoubledHeightCoordinateHex.origin()

    def test_double_width_condition(self):
        h1 = DoubledHeightCoordinateHex(3, 5)
        h2 = DoubledHeightCoordinateHex(6, 6)
        h3 = DoubledHeightCoordinateHex(-20, -14)
        h4 = DoubledHeightCoordinateHex(5, -1)

        with pytest.raises(AssertionError):
            h5 = DoubledHeightCoordinateHex(0, 1)

        with pytest.raises(AssertionError):
            h6 = DoubledHeightCoordinateHex(-1, -2)

    def test_equality(self):
        assert DoubledHeightCoordinateHex(0, 0) == DoubledHeightCoordinateHex.origin()
        assert DoubledHeightCoordinateHex(3, -1) == DoubledHeightCoordinateHex(3, -1)

        for value in [0, -1.5, False, "test"]:
            with pytest.raises(AssertionError):
                assert DoubledHeightCoordinateHex(1, 1) == value
            with pytest.raises(AssertionError):
                assert value == DoubledHeightCoordinateHex(1, 1)

    def test_not_equal(self):
        assert DoubledHeightCoordinateHex(3, 1) != DoubledHeightCoordinateHex(3, 3)
        assert DoubledHeightCoordinateHex(3, 1) != DoubledHeightCoordinateHex(1, 3)
        assert DoubledHeightCoordinateHex(3, 1) != DoubledHeightCoordinateHex(1, 1)

    def test_hash(self):
        assert hash(DoubledHeightCoordinateHex(0, 0)) == hash(DoubledHeightCoordinateHex.origin())
        assert hash(get_random_DoubleHeightCoordinateHex(10, 42)) != hash(get_random_DoubleHeightCoordinateHex(10, 43))

        my_dict = dict()
        my_dict[DoubledHeightCoordinateHex(0, 0)] = "origin"
        my_dict[DoubledHeightCoordinateHex(-1, 1)] = "test_1"
        my_dict[get_random_DoubleHeightCoordinateHex(20, 20)] = "test_2"

        assert my_dict[DoubledHeightCoordinateHex.origin()] == "origin"
        assert my_dict[DoubledHeightCoordinateHex(-1, 1)] == "test_1"
        assert my_dict[get_random_DoubleHeightCoordinateHex(20, 20)] == "test_2"

    def test_to_2d_coordinates(self):
        assert DoubledHeightCoordinateHex.origin().to_2d_coordinates() == (0, 0)
        assert DoubledHeightCoordinateHex(3, 5).to_2d_coordinates() == (3, 5)

        random_hex = get_random_DoubleHeightCoordinateHex(radius=20, random_seed=1)
        assert random_hex.to_2d_coordinates() == (random_hex.q, random_hex.r)

    def test_from_2d_coordinates(self):
        assert DoubledHeightCoordinateHex.from_2d_coordinates(0, 0) == DoubledHeightCoordinateHex.origin()
        assert DoubledHeightCoordinateHex.from_2d_coordinates(-12, 8) == DoubledHeightCoordinateHex(-12, 8)

        q = random.randint(-20, 21)
        r = q + 2 * random.randint(-10, 11)
        assert DoubledHeightCoordinateHex.from_2d_coordinates(q, r) == DoubledHeightCoordinateHex(q, r)

    def test_axial_conversion(self):
        assert DoubledHeightCoordinateHex.origin().to_axial_coordinate_hex() == AxialCoordinateHex.origin()
        assert (
            DoubledHeightCoordinateHex.from_axial_coordinate_hex(AxialCoordinateHex.origin())
            == DoubledHeightCoordinateHex.origin()
        )

        assert DoubledHeightCoordinateHex(3, 1).to_axial_coordinate_hex() == AxialCoordinateHex(3, -1)
        assert DoubledHeightCoordinateHex.from_axial_coordinate_hex(
            AxialCoordinateHex(3, -1)
        ) == DoubledHeightCoordinateHex(3, 1)

        assert DoubledHeightCoordinateHex(0, 4).to_axial_coordinate_hex() == AxialCoordinateHex(0, 2)
        assert DoubledHeightCoordinateHex.from_axial_coordinate_hex(
            AxialCoordinateHex(0, 2)
        ) == DoubledHeightCoordinateHex(0, 4)

    def test_cube_conversion(self):
        assert DoubledHeightCoordinateHex.origin().to_cube_coordinate_hex() == CubeCoordinateHex.origin()
        assert (
            DoubledHeightCoordinateHex.from_cube_coordinate_hex(CubeCoordinateHex.origin())
            == DoubledHeightCoordinateHex.origin()
        )

        assert DoubledHeightCoordinateHex(3, 1).to_cube_coordinate_hex() == CubeCoordinateHex(3, -1, -2)
        assert DoubledHeightCoordinateHex.from_cube_coordinate_hex(
            CubeCoordinateHex(3, -1, -2)
        ) == DoubledHeightCoordinateHex(3, 1)

        assert DoubledHeightCoordinateHex(0, 4).to_cube_coordinate_hex() == CubeCoordinateHex(0, 2, -2)
        assert DoubledHeightCoordinateHex.from_cube_coordinate_hex(
            CubeCoordinateHex(0, 2, -2)
        ) == DoubledHeightCoordinateHex(0, 4)

    def test_addition(self):
        assert DoubledHeightCoordinateHex(3, 5) + DoubledHeightCoordinateHex(3, 5) == DoubledHeightCoordinateHex(6, 10)
        assert DoubledHeightCoordinateHex(3, 5) + DoubledHeightCoordinateHex(0, 0) == DoubledHeightCoordinateHex(3, 5)
        assert DoubledHeightCoordinateHex(0, 0) + DoubledHeightCoordinateHex(3, 5) == DoubledHeightCoordinateHex(3, 5)
        assert DoubledHeightCoordinateHex(-4, -6) + DoubledHeightCoordinateHex(6, 6) == DoubledHeightCoordinateHex(2, 0)

        with pytest.raises(TypeError):
            test = 5 + DoubledHeightCoordinateHex(0, 0)

        with pytest.raises(TypeError):
            test = DoubledHeightCoordinateHex(0, 0) + 5

        # TODO: add other types of hexes

    def test_subtraction(self):
        assert DoubledHeightCoordinateHex(3, 5) - DoubledHeightCoordinateHex(3, 5) == DoubledHeightCoordinateHex(0, 0)
        assert DoubledHeightCoordinateHex(3, 5) - DoubledHeightCoordinateHex(0, 0) == DoubledHeightCoordinateHex(3, 5)
        assert DoubledHeightCoordinateHex(0, 0) - DoubledHeightCoordinateHex(3, 5) == DoubledHeightCoordinateHex(-3, -5)
        assert DoubledHeightCoordinateHex(-4, -6) - DoubledHeightCoordinateHex(6, 6) == DoubledHeightCoordinateHex(
            -10, -12
        )

        with pytest.raises(TypeError):
            test = 5 - DoubledHeightCoordinateHex(0, 0)

        with pytest.raises(TypeError):
            test = DoubledHeightCoordinateHex(0, 0) - 5

        # TODO: add other types of hexes

    def test_multiply(self):
        assert DoubledHeightCoordinateHex(1, 3) * 5 == DoubledHeightCoordinateHex(5, 15)
        assert 5 * DoubledHeightCoordinateHex(1, 3) == DoubledHeightCoordinateHex(5, 15)
        assert DoubledHeightCoordinateHex(1, 3) * 0 == DoubledHeightCoordinateHex(0, 0)
        assert 0 * DoubledHeightCoordinateHex(1, 3) == DoubledHeightCoordinateHex(0, 0)
        assert DoubledHeightCoordinateHex(1, 3) * -2 == DoubledHeightCoordinateHex(-2, -6)
        assert -2 * DoubledHeightCoordinateHex(1, 3) == DoubledHeightCoordinateHex(-2, -6)
        assert 3 * DoubledHeightCoordinateHex.origin() == DoubledHeightCoordinateHex.origin()
        assert DoubledHeightCoordinateHex.origin() * 3 == DoubledHeightCoordinateHex.origin()

        with pytest.raises(TypeError):
            assert -1.5 * DoubledHeightCoordinateHex(2, 4) == DoubledHeightCoordinateHex(-3, -6)
        with pytest.raises(TypeError):
            assert DoubledHeightCoordinateHex(2, 4) * 1.5 == DoubledHeightCoordinateHex(3, 6)

    def test_neg(self):
        assert -DoubledHeightCoordinateHex(-1, 3) == DoubledHeightCoordinateHex(1, -3)
        assert -DoubledHeightCoordinateHex.origin() == DoubledHeightCoordinateHex.origin()
        h = DoubledHeightCoordinateHex(2, -2)
        assert -(-h) == h

    def test_copy(self):
        o = DoubledHeightCoordinateHex.origin()
        o2 = copy.copy(o)
        assert o == o2
        assert id(o) != id(o2)
        assert o2.q == 0 and o2.r == 0

        h = get_random_DoubleHeightCoordinateHex(20, 17)
        h2 = copy.copy(h)
        assert h == h2
        assert id(h) != id(h2)

    def test_deepcopy(self):
        o = DoubledHeightCoordinateHex.origin()
        o2 = copy.deepcopy(o)
        assert o == o2
        assert id(o) != id(o2)
        assert o2.q == 0 and o2.r == 0

        h = get_random_DoubleHeightCoordinateHex(20, 17)
        h2 = copy.deepcopy(h)
        assert h == h2
        assert id(h) != id(h2)

    def test_neighbors(self):
        origin_neighbors = self.origin.neighbors
        assert len(origin_neighbors) == 6
        assert set(origin_neighbors) == set(self.origin.neighbor_directions)

        center = DoubledHeightCoordinateHex(-2, -4)
        assert center.neighbors == [
            DoubledHeightCoordinateHex(-1, -3),
            DoubledHeightCoordinateHex(-1, -5),
            DoubledHeightCoordinateHex(-2, -6),
            DoubledHeightCoordinateHex(-3, -5),
            DoubledHeightCoordinateHex(-3, -3),
            DoubledHeightCoordinateHex(-2, -2),
        ]

    def test_reflection(self):
        assert DoubledHeightCoordinateHex(4, 8).reflect_over_hex(
            DoubledHeightCoordinateHex(3, 5)
        ) == DoubledHeightCoordinateHex(2, 2)
        assert DoubledHeightCoordinateHex(3, 3).reflect_over_hex() == DoubledHeightCoordinateHex(-3, -3)
        h = DoubledHeightCoordinateHex(1, 3)
        assert h.reflect_over_hex() == -h

    def test_distance(self):
        h = get_random_DoubleHeightCoordinateHex(radius=20, random_seed=13)
        assert all(h.distance(other) == 1 for other in h.neighbors)
        assert h.distance(h) == 0
        assert DoubledHeightCoordinateHex(2, 0).distance(DoubledHeightCoordinateHex(3, 5)) == 3

    def test_range(self):
        center = get_random_DoubleHeightCoordinateHex(radius=20, random_seed=11)
        for radius in range(1, 5):
            hexes_in_ranges = center.hexes_within_range(radius)
            assert all(0 <= center.distance(other) <= radius for other in hexes_in_ranges)
            centered_hex_number = 3 * radius * (radius + 1) + 1
            assert len(set(hexes_in_ranges)) == centered_hex_number

import copy
import random

import pytest

from cryptid.hex import AxialCoordinateHex, CubeCoordinateHex, DoubledWidthCoordinateHex


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


class TestDoubledWidthCoordinateHex:
    origin: DoubledWidthCoordinateHex = DoubledWidthCoordinateHex.origin()

    def test_double_width_condition(self):
        h1 = DoubledWidthCoordinateHex(3, 5)
        h2 = DoubledWidthCoordinateHex(6, 6)
        h3 = DoubledWidthCoordinateHex(-20, -14)
        h4 = DoubledWidthCoordinateHex(5, -1)

        with pytest.raises(AssertionError):
            h5 = DoubledWidthCoordinateHex(0, 1)

        with pytest.raises(AssertionError):
            h6 = DoubledWidthCoordinateHex(-1, -2)

    def test_equality(self):
        assert DoubledWidthCoordinateHex(0, 0) == DoubledWidthCoordinateHex.origin()
        assert DoubledWidthCoordinateHex(3, -1) == DoubledWidthCoordinateHex(3, -1)

        for value in [0, -1.5, False, "test"]:
            with pytest.raises(AssertionError):
                assert DoubledWidthCoordinateHex(1, 1) == value
            with pytest.raises(AssertionError):
                assert value == DoubledWidthCoordinateHex(1, 1)

    def test_not_equal(self):
        assert DoubledWidthCoordinateHex(3, 1) != DoubledWidthCoordinateHex(3, 3)
        assert DoubledWidthCoordinateHex(3, 1) != DoubledWidthCoordinateHex(1, 3)
        assert DoubledWidthCoordinateHex(3, 1) != DoubledWidthCoordinateHex(1, 1)

    def test_hash(self):
        assert hash(DoubledWidthCoordinateHex(0, 0)) == hash(DoubledWidthCoordinateHex.origin())
        assert hash(get_random_DoubleWidthCoordinateHex(10, 42)) != hash(get_random_DoubleWidthCoordinateHex(10, 43))

        my_dict = dict()
        my_dict[DoubledWidthCoordinateHex(0, 0)] = "origin"
        my_dict[DoubledWidthCoordinateHex(-1, 1)] = "test_1"
        my_dict[get_random_DoubleWidthCoordinateHex(20, 20)] = "test_2"

        assert my_dict[DoubledWidthCoordinateHex.origin()] == "origin"
        assert my_dict[DoubledWidthCoordinateHex(-1, 1)] == "test_1"
        assert my_dict[get_random_DoubleWidthCoordinateHex(20, 20)] == "test_2"

    def test_to_2d_coordinates(self):
        assert DoubledWidthCoordinateHex.origin().to_2d_coordinates() == (0, 0)
        assert DoubledWidthCoordinateHex(3, 5).to_2d_coordinates() == (3, 5)

        random_hex = get_random_DoubleWidthCoordinateHex(radius=20, random_seed=1)
        assert random_hex.to_2d_coordinates() == (random_hex.q, random_hex.r)

    def test_from_2d_coordinates(self):
        assert DoubledWidthCoordinateHex.from_2d_coordinates(0, 0) == DoubledWidthCoordinateHex.origin()
        assert DoubledWidthCoordinateHex.from_2d_coordinates(-12, 8) == DoubledWidthCoordinateHex(-12, 8)

        q = random.randint(-20, 21)
        r = q + 2 * random.randint(-10, 11)
        assert DoubledWidthCoordinateHex.from_2d_coordinates(q, r) == DoubledWidthCoordinateHex(q, r)

    def test_axial_conversion(self):
        assert DoubledWidthCoordinateHex.origin().to_axial_coordinate_hex() == AxialCoordinateHex.origin()
        assert (
            DoubledWidthCoordinateHex.from_axial_coordinate_hex(AxialCoordinateHex.origin())
            == DoubledWidthCoordinateHex.origin()
        )

        assert DoubledWidthCoordinateHex(3, 1).to_axial_coordinate_hex() == AxialCoordinateHex(1, 1)
        assert DoubledWidthCoordinateHex.from_axial_coordinate_hex(
            AxialCoordinateHex(1, 1)
        ) == DoubledWidthCoordinateHex(3, 1)

        assert DoubledWidthCoordinateHex(0, 4).to_axial_coordinate_hex() == AxialCoordinateHex(-2, 4)
        assert DoubledWidthCoordinateHex.from_axial_coordinate_hex(
            AxialCoordinateHex(-2, 4)
        ) == DoubledWidthCoordinateHex(0, 4)

    def test_cube_conversion(self):
        assert DoubledWidthCoordinateHex.origin().to_cube_coordinate_hex() == CubeCoordinateHex.origin()
        assert (
            DoubledWidthCoordinateHex.from_cube_coordinate_hex(CubeCoordinateHex.origin())
            == DoubledWidthCoordinateHex.origin()
        )

        assert DoubledWidthCoordinateHex(3, 1).to_cube_coordinate_hex() == CubeCoordinateHex(1, 1, -2)
        assert DoubledWidthCoordinateHex.from_cube_coordinate_hex(
            CubeCoordinateHex(1, 1, -2)
        ) == DoubledWidthCoordinateHex(3, 1)

        assert DoubledWidthCoordinateHex(0, 4).to_cube_coordinate_hex() == CubeCoordinateHex(-2, 4, -2)
        assert DoubledWidthCoordinateHex.from_cube_coordinate_hex(
            CubeCoordinateHex(-2, 4, -2)
        ) == DoubledWidthCoordinateHex(0, 4)

    def test_addition(self):
        assert DoubledWidthCoordinateHex(3, 5) + DoubledWidthCoordinateHex(3, 5) == DoubledWidthCoordinateHex(6, 10)
        assert DoubledWidthCoordinateHex(3, 5) + DoubledWidthCoordinateHex(0, 0) == DoubledWidthCoordinateHex(3, 5)
        assert DoubledWidthCoordinateHex(0, 0) + DoubledWidthCoordinateHex(3, 5) == DoubledWidthCoordinateHex(3, 5)
        assert DoubledWidthCoordinateHex(-4, -6) + DoubledWidthCoordinateHex(6, 6) == DoubledWidthCoordinateHex(2, 0)

        with pytest.raises(TypeError):
            test = 5 + DoubledWidthCoordinateHex(0, 0)

        with pytest.raises(TypeError):
            test = DoubledWidthCoordinateHex(0, 0) + 5

        # TODO: add other types of hexes

    def test_subtraction(self):
        assert DoubledWidthCoordinateHex(3, 5) - DoubledWidthCoordinateHex(3, 5) == DoubledWidthCoordinateHex(0, 0)
        assert DoubledWidthCoordinateHex(3, 5) - DoubledWidthCoordinateHex(0, 0) == DoubledWidthCoordinateHex(3, 5)
        assert DoubledWidthCoordinateHex(0, 0) - DoubledWidthCoordinateHex(3, 5) == DoubledWidthCoordinateHex(-3, -5)
        assert DoubledWidthCoordinateHex(-4, -6) - DoubledWidthCoordinateHex(6, 6) == DoubledWidthCoordinateHex(
            -10, -12
        )

        with pytest.raises(TypeError):
            test = 5 - DoubledWidthCoordinateHex(0, 0)

        with pytest.raises(TypeError):
            test = DoubledWidthCoordinateHex(0, 0) - 5

        # TODO: add other types of hexes

    def test_multiply(self):
        assert DoubledWidthCoordinateHex(1, 3) * 5 == DoubledWidthCoordinateHex(5, 15)
        assert 5 * DoubledWidthCoordinateHex(1, 3) == DoubledWidthCoordinateHex(5, 15)
        assert DoubledWidthCoordinateHex(1, 3) * 0 == DoubledWidthCoordinateHex(0, 0)
        assert 0 * DoubledWidthCoordinateHex(1, 3) == DoubledWidthCoordinateHex(0, 0)
        assert DoubledWidthCoordinateHex(1, 3) * -2 == DoubledWidthCoordinateHex(-2, -6)
        assert -2 * DoubledWidthCoordinateHex(1, 3) == DoubledWidthCoordinateHex(-2, -6)
        assert 3 * DoubledWidthCoordinateHex.origin() == DoubledWidthCoordinateHex.origin()
        assert DoubledWidthCoordinateHex.origin() * 3 == DoubledWidthCoordinateHex.origin()

        with pytest.raises(TypeError):
            assert -1.5 * DoubledWidthCoordinateHex(2, 4) == DoubledWidthCoordinateHex(-3, -6)
        with pytest.raises(TypeError):
            assert DoubledWidthCoordinateHex(2, 4) * 1.5 == DoubledWidthCoordinateHex(3, 6)

    def test_neg(self):
        assert -DoubledWidthCoordinateHex(-1, 3) == DoubledWidthCoordinateHex(1, -3)
        assert -DoubledWidthCoordinateHex.origin() == DoubledWidthCoordinateHex.origin()
        h = DoubledWidthCoordinateHex(2, -2)
        assert -(-h) == h

    def test_copy(self):
        o = DoubledWidthCoordinateHex.origin()
        o2 = copy.copy(o)
        assert o == o2
        assert id(o) != id(o2)
        assert o2.q == 0 and o2.r == 0

        h = get_random_DoubleWidthCoordinateHex(20, 17)
        h2 = copy.copy(h)
        assert h == h2
        assert id(h) != id(h2)

    def test_deepcopy(self):
        o = DoubledWidthCoordinateHex.origin()
        o2 = copy.deepcopy(o)
        assert o == o2
        assert id(o) != id(o2)
        assert o2.q == 0 and o2.r == 0

        h = get_random_DoubleWidthCoordinateHex(20, 17)
        h2 = copy.deepcopy(h)
        assert h == h2
        assert id(h) != id(h2)

    def test_neighbors(self):
        origin_neighbors = self.origin.neighbors
        assert len(origin_neighbors) == 6
        assert set(origin_neighbors) == set(self.origin.neighbor_directions)

        center = DoubledWidthCoordinateHex(-2, -4)
        assert center.neighbors == [
            DoubledWidthCoordinateHex(0, -4),
            DoubledWidthCoordinateHex(-1, -5),
            DoubledWidthCoordinateHex(-3, -5),
            DoubledWidthCoordinateHex(-4, -4),
            DoubledWidthCoordinateHex(-3, -3),
            DoubledWidthCoordinateHex(-1, -3),
        ]

    def test_reflection(self):
        assert DoubledWidthCoordinateHex(4, 8).reflect_over_hex(
            DoubledWidthCoordinateHex(3, 5)
        ) == DoubledWidthCoordinateHex(2, 2)
        assert DoubledWidthCoordinateHex(3, 3).reflect_over_hex() == DoubledWidthCoordinateHex(-3, -3)
        h = DoubledWidthCoordinateHex(1, 3)
        assert h.reflect_over_hex() == -h

    def test_distance(self):
        h = get_random_DoubleWidthCoordinateHex(radius=20, random_seed=13)
        assert all(h.distance(other) == 1 for other in h.neighbors)
        assert h.distance(h) == 0
        assert DoubledWidthCoordinateHex(2, 0).distance(DoubledWidthCoordinateHex(3, 5)) == 5

    def test_range(self):
        center = get_random_DoubleWidthCoordinateHex(radius=20, random_seed=11)
        for radius in range(1, 5):
            hexes_in_ranges = center.hexes_within_range(radius)
            assert all(0 <= center.distance(other) <= radius for other in hexes_in_ranges)
            centered_hex_number = 3 * radius * (radius + 1) + 1
            assert len(set(hexes_in_ranges)) == centered_hex_number

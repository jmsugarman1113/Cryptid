import copy
import random

import pytest

from cryptid.hex import AxialCoordinateHex, CubeCoordinateHex, EvenRowOffsetCoordinateHex


def get_random_EvenRowOffsetCoordinateHex(
    radius: int,
    random_seed: int,
    row_offset: int = 0,
    column_offset: int = 0,
) -> EvenRowOffsetCoordinateHex:
    random.seed(random_seed)
    row = random.randint(-radius, radius) + row_offset
    col = random.randint(-radius, radius) + column_offset
    return EvenRowOffsetCoordinateHex.from_row_col(row, col)


class TestEvenRowOffsetCoordinateHex:
    origin: EvenRowOffsetCoordinateHex = EvenRowOffsetCoordinateHex.origin()

    def test_equality(self):
        assert EvenRowOffsetCoordinateHex(0, 0) == EvenRowOffsetCoordinateHex.origin()
        assert EvenRowOffsetCoordinateHex(3, -1) == EvenRowOffsetCoordinateHex(3, -1)

        for value in [0, -1.5, False, "test"]:
            with pytest.raises(AssertionError):
                assert EvenRowOffsetCoordinateHex(1, 1) == value
            with pytest.raises(AssertionError):
                assert value == EvenRowOffsetCoordinateHex(1, 1)

    def test_not_equal(self):
        assert EvenRowOffsetCoordinateHex(3, 1) != EvenRowOffsetCoordinateHex(3, 3)
        assert EvenRowOffsetCoordinateHex(3, 1) != EvenRowOffsetCoordinateHex(1, 3)
        assert EvenRowOffsetCoordinateHex(3, 1) != EvenRowOffsetCoordinateHex(1, 1)

    def test_hash(self):
        assert hash(EvenRowOffsetCoordinateHex(0, 0)) == hash(EvenRowOffsetCoordinateHex.origin())
        assert hash(get_random_EvenRowOffsetCoordinateHex(10, 42)) != hash(
            get_random_EvenRowOffsetCoordinateHex(10, 43)
        )

        my_dict = dict()
        my_dict[EvenRowOffsetCoordinateHex(0, 0)] = "origin"
        my_dict[EvenRowOffsetCoordinateHex(-1, 1)] = "test_1"
        my_dict[get_random_EvenRowOffsetCoordinateHex(20, 20)] = "test_2"

        assert my_dict[EvenRowOffsetCoordinateHex.origin()] == "origin"
        assert my_dict[EvenRowOffsetCoordinateHex(-1, 1)] == "test_1"
        assert my_dict[get_random_EvenRowOffsetCoordinateHex(20, 20)] == "test_2"

    def test_to_2d_coordinates(self):
        assert EvenRowOffsetCoordinateHex.origin().to_2d_coordinates() == (0, 0)
        assert EvenRowOffsetCoordinateHex(3, 5).to_2d_coordinates() == (3, 5)

        random_hex = get_random_EvenRowOffsetCoordinateHex(radius=20, random_seed=1)
        assert random_hex.to_2d_coordinates() == (random_hex.q, random_hex.r)

    def test_from_2d_coordinates(self):
        assert EvenRowOffsetCoordinateHex.from_2d_coordinates(0, 0) == EvenRowOffsetCoordinateHex.origin()
        assert EvenRowOffsetCoordinateHex.from_2d_coordinates(-12, 8) == EvenRowOffsetCoordinateHex(-12, 8)

        q = random.randint(-20, 21)
        r = q + 2 * random.randint(-10, 11)
        assert EvenRowOffsetCoordinateHex.from_2d_coordinates(q, r) == EvenRowOffsetCoordinateHex(q, r)

    def test_axial_conversion(self):
        assert EvenRowOffsetCoordinateHex.origin().to_axial_coordinate_hex() == AxialCoordinateHex.origin()
        assert (
            EvenRowOffsetCoordinateHex.from_axial_coordinate_hex(AxialCoordinateHex.origin())
            == EvenRowOffsetCoordinateHex.origin()
        )

        assert EvenRowOffsetCoordinateHex(3, 1).to_axial_coordinate_hex() == AxialCoordinateHex(2, 1)
        assert EvenRowOffsetCoordinateHex.from_axial_coordinate_hex(
            AxialCoordinateHex(2, 1)
        ) == EvenRowOffsetCoordinateHex(3, 1)

        assert EvenRowOffsetCoordinateHex(0, 4).to_axial_coordinate_hex() == AxialCoordinateHex(-2, 4)
        assert EvenRowOffsetCoordinateHex.from_axial_coordinate_hex(
            AxialCoordinateHex(-2, 4)
        ) == EvenRowOffsetCoordinateHex(0, 4)

        # assert [neighbor.to_axial_coordinate_hex() for neighbor in EvenRowOffsetCoordinateHex(0, 0).neighbors] == [
        #     AxialCoordinateHex(1, 0),
        #     AxialCoordinateHex(1, -1),
        #     AxialCoordinateHex(0, -1),
        #     AxialCoordinateHex(-1, 0),
        #     AxialCoordinateHex(-1, 1),
        #     AxialCoordinateHex(0, 1),
        # ]

        # assert [neighbor.to_axial_coordinate_hex() for neighbor in EvenRowOffsetCoordinateHex(0, 0).neighbors] == [
        #     AxialCoordinateHex(1, 0),
        #     AxialCoordinateHex(1, -1),
        #     AxialCoordinateHex(0, -1),
        #     AxialCoordinateHex(-1, 0),
        #     AxialCoordinateHex(-1, 1),
        #     AxialCoordinateHex(0, 1),
        # ]

    def test_cube_conversion(self):
        assert EvenRowOffsetCoordinateHex.origin().to_cube_coordinate_hex() == CubeCoordinateHex.origin()
        assert (
            EvenRowOffsetCoordinateHex.from_cube_coordinate_hex(CubeCoordinateHex.origin())
            == EvenRowOffsetCoordinateHex.origin()
        )

        assert EvenRowOffsetCoordinateHex(3, 1).to_cube_coordinate_hex() == CubeCoordinateHex(2, 1, -3)
        assert EvenRowOffsetCoordinateHex.from_cube_coordinate_hex(
            CubeCoordinateHex(2, 1, -3)
        ) == EvenRowOffsetCoordinateHex(3, 1)

        assert EvenRowOffsetCoordinateHex(0, 4).to_cube_coordinate_hex() == CubeCoordinateHex(-2, 4, -2)
        assert EvenRowOffsetCoordinateHex.from_cube_coordinate_hex(
            CubeCoordinateHex(-2, 4, -2)
        ) == EvenRowOffsetCoordinateHex(0, 4)

    # def test_addition(self):
    #     assert EvenRowOffsetCoordinateHex(3, 5) + EvenRowOffsetCoordinateHex(3, 5) == EvenRowOffsetCoordinateHex(6, 10)
    #     assert EvenRowOffsetCoordinateHex(3, 5) + EvenRowOffsetCoordinateHex(0, 0) == EvenRowOffsetCoordinateHex(3, 5)
    #     assert EvenRowOffsetCoordinateHex(0, 0) + EvenRowOffsetCoordinateHex(3, 5) == EvenRowOffsetCoordinateHex(3, 5)
    #     assert EvenRowOffsetCoordinateHex(-4, -6) + EvenRowOffsetCoordinateHex(6, 6) == EvenRowOffsetCoordinateHex(2, 0)
    #
    #     with pytest.raises(TypeError):
    #         test = 5 + EvenRowOffsetCoordinateHex(0, 0)
    #
    #     with pytest.raises(TypeError):
    #         test = EvenRowOffsetCoordinateHex(0, 0) + 5
    #
    #     # TODO: add other types of hexes
    #
    # def test_subtraction(self):
    #     assert EvenRowOffsetCoordinateHex(3, 5) - EvenRowOffsetCoordinateHex(3, 5) == EvenRowOffsetCoordinateHex(0, 0)
    #     assert EvenRowOffsetCoordinateHex(3, 5) - EvenRowOffsetCoordinateHex(0, 0) == EvenRowOffsetCoordinateHex(3, 5)
    #     assert EvenRowOffsetCoordinateHex(0, 0) - EvenRowOffsetCoordinateHex(3, 5) == EvenRowOffsetCoordinateHex(-3, -5)
    #     assert EvenRowOffsetCoordinateHex(-4, -6) - EvenRowOffsetCoordinateHex(6, 6) == EvenRowOffsetCoordinateHex(
    #         -10, -12
    #     )
    #
    #     with pytest.raises(TypeError):
    #         test = 5 - EvenRowOffsetCoordinateHex(0, 0)
    #
    #     with pytest.raises(TypeError):
    #         test = EvenRowOffsetCoordinateHex(0, 0) - 5
    #
    #     # TODO: add other types of hexes
    #
    # def test_multiply(self):
    #     assert EvenRowOffsetCoordinateHex(1, 3) * 5 == EvenRowOffsetCoordinateHex(5, 15)
    #     assert 5 * EvenRowOffsetCoordinateHex(1, 3) == EvenRowOffsetCoordinateHex(5, 15)
    #     assert EvenRowOffsetCoordinateHex(1, 3) * 0 == EvenRowOffsetCoordinateHex(0, 0)
    #     assert 0 * EvenRowOffsetCoordinateHex(1, 3) == EvenRowOffsetCoordinateHex(0, 0)
    #     assert EvenRowOffsetCoordinateHex(1, 3) * -2 == EvenRowOffsetCoordinateHex(-2, -6)
    #     assert -2 * EvenRowOffsetCoordinateHex(1, 3) == EvenRowOffsetCoordinateHex(-2, -6)
    #     assert 3 * EvenRowOffsetCoordinateHex.origin() == EvenRowOffsetCoordinateHex.origin()
    #     assert EvenRowOffsetCoordinateHex.origin() * 3 == EvenRowOffsetCoordinateHex.origin()
    #
    #     with pytest.raises(TypeError):
    #         assert -1.5 * EvenRowOffsetCoordinateHex(2, 4) == EvenRowOffsetCoordinateHex(-3, -6)
    #     with pytest.raises(TypeError):
    #         assert EvenRowOffsetCoordinateHex(2, 4) * 1.5 == EvenRowOffsetCoordinateHex(3, 6)
    #
    # def test_neg(self):
    #     assert -EvenRowOffsetCoordinateHex(-1, 3) == EvenRowOffsetCoordinateHex(1, -3)
    #     assert -EvenRowOffsetCoordinateHex.origin() == EvenRowOffsetCoordinateHex.origin()
    #     h = EvenRowOffsetCoordinateHex(2, -2)
    #     assert -(-h) == h

    def test_copy(self):
        o = EvenRowOffsetCoordinateHex.origin()
        o2 = copy.copy(o)
        assert o == o2
        assert id(o) != id(o2)
        assert o2.q == 0 and o2.r == 0

        h = get_random_EvenRowOffsetCoordinateHex(20, 17)
        h2 = copy.copy(h)
        assert h == h2
        assert id(h) != id(h2)

    def test_deepcopy(self):
        o = EvenRowOffsetCoordinateHex.origin()
        o2 = copy.deepcopy(o)
        assert o == o2
        assert id(o) != id(o2)
        assert o2.q == 0 and o2.r == 0

        h = get_random_EvenRowOffsetCoordinateHex(20, 17)
        h2 = copy.deepcopy(h)
        assert h == h2
        assert id(h) != id(h2)

    # def test_neighbors(self):
    #     origin_neighbors = self.origin.neighbors
    #     assert len(origin_neighbors) == 6
    #     assert set(origin_neighbors) == set(self.origin.neighbor_directions)
    #
    #     center = EvenRowOffsetCoordinateHex(3, 0)
    #     assert center.neighbors == [
    #         EvenRowOffsetCoordinateHex(4, 0),
    #         EvenRowOffsetCoordinateHex(4, -1),
    #         EvenRowOffsetCoordinateHex(3, -1),
    #         EvenRowOffsetCoordinateHex(2, 0),
    #         EvenRowOffsetCoordinateHex(3, 1),
    #         EvenRowOffsetCoordinateHex(4, 1),
    #     ]
    #
    #     center = EvenRowOffsetCoordinateHex(2, 3)
    #     print(center.neighbors)
    #     assert center.neighbors == [
    #         EvenRowOffsetCoordinateHex(3, 3),
    #         EvenRowOffsetCoordinateHex(2, 2),
    #         EvenRowOffsetCoordinateHex(1, 2),
    #         EvenRowOffsetCoordinateHex(1, 3),
    #         EvenRowOffsetCoordinateHex(1, 4),
    #         EvenRowOffsetCoordinateHex(2, 4),
    #     ]
    #
    # def test_reflection(self):
    #     assert EvenRowOffsetCoordinateHex(4, 8).reflect_over_hex(
    #         EvenRowOffsetCoordinateHex(3, 5)
    #     ) == EvenRowOffsetCoordinateHex(2, 2)
    #     assert EvenRowOffsetCoordinateHex(3, 3).reflect_over_hex() == EvenRowOffsetCoordinateHex(-3, -3)
    #     h = EvenRowOffsetCoordinateHex(1, 3)
    #     assert h.reflect_over_hex() == -h
    #
    # def test_distance(self):
    #     h = get_random_EvenRowOffsetCoordinateHex(radius=20, random_seed=13)
    #     assert all(h.distance(other) == 1 for other in h.neighbors)
    #     assert h.distance(h) == 0
    #     assert EvenRowOffsetCoordinateHex(2, 0).distance(EvenRowOffsetCoordinateHex(3, 5)) == 5

    def test_range(self):
        center = get_random_EvenRowOffsetCoordinateHex(radius=20, random_seed=11)
        for radius in range(5):
            hexes_in_ranges = center.hexes_within_range(radius)
            assert all(0 <= center.distance(other) <= radius for other in hexes_in_ranges)
            centered_hex_number = 3 * radius * (radius + 1) + 1
            assert len(set(hexes_in_ranges)) == centered_hex_number

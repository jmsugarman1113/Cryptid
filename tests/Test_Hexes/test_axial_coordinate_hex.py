import copy
import random

import pytest

from cryptid.hex import AxialCoordinateHex, CubeCoordinateHex


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


class TestAxialCoordinateHex:
    origin: AxialCoordinateHex = AxialCoordinateHex.origin()

    def test_equality(self):
        assert AxialCoordinateHex(0, 0) == AxialCoordinateHex.origin()
        assert AxialCoordinateHex(3, -1) == AxialCoordinateHex(3, -1)

        for value in [0, -1.5, False, "test"]:
            with pytest.raises(AssertionError):
                assert AxialCoordinateHex(1, 1) == value
            with pytest.raises(AssertionError):
                assert value == AxialCoordinateHex(1, 1)

    def test_not_equal(self):
        assert AxialCoordinateHex(3, 1) != AxialCoordinateHex(3, 3)
        assert AxialCoordinateHex(3, 1) != AxialCoordinateHex(1, 3)
        assert AxialCoordinateHex(3, 1) != AxialCoordinateHex(1, 1)

    def test_hash(self):
        assert hash(AxialCoordinateHex(0, 0)) == hash(AxialCoordinateHex.origin())
        assert hash(get_random_AxialCooredinateHex(10, 42)) != hash(get_random_AxialCooredinateHex(10, 43))

        my_dict = dict()
        my_dict[AxialCoordinateHex(0, 0)] = "origin"
        my_dict[AxialCoordinateHex(-1, 1)] = "test_1"
        my_dict[get_random_AxialCooredinateHex(20, 20)] = "test_2"

        assert my_dict[AxialCoordinateHex.origin()] == "origin"
        assert my_dict[AxialCoordinateHex(-1, 1)] == "test_1"
        assert my_dict[get_random_AxialCooredinateHex(20, 20)] == "test_2"

    def test_to_2d_coordinates(self):
        assert AxialCoordinateHex.origin().to_2d_coordinates() == (0, 0)
        assert AxialCoordinateHex(3, 5).to_2d_coordinates() == (3, 5)

        random_hex = get_random_AxialCooredinateHex(radius=20, random_seed=1)
        assert random_hex.to_2d_coordinates() == (random_hex.q, random_hex.r)

    def test_from_2d_coordinates(self):
        assert AxialCoordinateHex.from_2d_coordinates(0, 0) == AxialCoordinateHex.origin()
        assert AxialCoordinateHex.from_2d_coordinates(-12, 8) == AxialCoordinateHex(-12, 8)

        q = random.randint(-20, 21)
        r = random.randint(-20, 21)
        assert AxialCoordinateHex.from_2d_coordinates(q, r) == AxialCoordinateHex(q, r)

    def test_axial_conversion(self):
        assert AxialCoordinateHex.origin().to_axial_coordinate_hex() == AxialCoordinateHex.origin()
        assert AxialCoordinateHex.from_axial_coordinate_hex(AxialCoordinateHex.origin()) == AxialCoordinateHex.origin()

        assert AxialCoordinateHex(3, 1).to_axial_coordinate_hex() == AxialCoordinateHex(3, 1)
        assert AxialCoordinateHex.from_axial_coordinate_hex(AxialCoordinateHex(3, 1)) == AxialCoordinateHex(3, 1)

        assert AxialCoordinateHex(0, 4).to_axial_coordinate_hex() == AxialCoordinateHex(0, 4)
        assert AxialCoordinateHex.from_axial_coordinate_hex(AxialCoordinateHex(0, 4)) == AxialCoordinateHex(0, 4)

        hex_a = AxialCoordinateHex(4, 2)
        hex_b = hex_a.to_axial_coordinate_hex()
        hex_c = AxialCoordinateHex.from_axial_coordinate_hex(hex_a)
        assert hex_a == hex_b and id(hex_a) != id(hex_b)
        assert hex_a == hex_c and id(hex_a) != id(hex_c)
        assert hex_c == hex_b and id(hex_c) != id(hex_b)

    def test_cube_conversion(self):
        assert AxialCoordinateHex.origin().to_cube_coordinate_hex() == CubeCoordinateHex.origin()
        assert AxialCoordinateHex.from_cube_coordinate_hex(CubeCoordinateHex.origin()) == AxialCoordinateHex.origin()

        assert AxialCoordinateHex(3, 1).to_cube_coordinate_hex() == CubeCoordinateHex(3, 1, -4)
        assert AxialCoordinateHex.from_cube_coordinate_hex(CubeCoordinateHex(3, 1, -4)) == AxialCoordinateHex(3, 1)

        assert AxialCoordinateHex(0, 2).to_cube_coordinate_hex() == CubeCoordinateHex(0, 2, -2)
        assert AxialCoordinateHex.from_cube_coordinate_hex(CubeCoordinateHex(0, 2, -2)) == AxialCoordinateHex(0, 2)

    def test_addition(self):
        assert AxialCoordinateHex(3, 5) + AxialCoordinateHex(3, 5) == AxialCoordinateHex(6, 10)
        assert AxialCoordinateHex(3, 5) + AxialCoordinateHex(0, 0) == AxialCoordinateHex(3, 5)
        assert AxialCoordinateHex(0, 0) + AxialCoordinateHex(3, 5) == AxialCoordinateHex(3, 5)
        assert AxialCoordinateHex(-4, -6) + AxialCoordinateHex(6, 6) == AxialCoordinateHex(2, 0)

        with pytest.raises(TypeError):
            test = 5 + AxialCoordinateHex(0, 0)

        with pytest.raises(TypeError):
            test = AxialCoordinateHex(0, 0) + 5

        # TODO: add other types of hexes

    def test_subtraction(self):
        assert AxialCoordinateHex(3, 5) - AxialCoordinateHex(3, 5) == AxialCoordinateHex(0, 0)
        assert AxialCoordinateHex(3, 5) - AxialCoordinateHex(0, 0) == AxialCoordinateHex(3, 5)
        assert AxialCoordinateHex(0, 0) - AxialCoordinateHex(3, 5) == AxialCoordinateHex(-3, -5)
        assert AxialCoordinateHex(-4, -6) - AxialCoordinateHex(6, 6) == AxialCoordinateHex(-10, -12)

        with pytest.raises(TypeError):
            test = 5 - AxialCoordinateHex(0, 0)

        with pytest.raises(TypeError):
            test = AxialCoordinateHex(0, 0) - 5

        # TODO: add other types of hexes

    def test_multiply(self):
        assert AxialCoordinateHex(1, 3) * 5 == AxialCoordinateHex(5, 15)
        assert 5 * AxialCoordinateHex(1, 3) == AxialCoordinateHex(5, 15)
        assert AxialCoordinateHex(1, 3) * 0 == AxialCoordinateHex(0, 0)
        assert 0 * AxialCoordinateHex(1, 3) == AxialCoordinateHex(0, 0)
        assert AxialCoordinateHex(1, 3) * -2 == AxialCoordinateHex(-2, -6)
        assert -2 * AxialCoordinateHex(1, 3) == AxialCoordinateHex(-2, -6)
        assert 3 * AxialCoordinateHex.origin() == AxialCoordinateHex.origin()
        assert AxialCoordinateHex.origin() * 3 == AxialCoordinateHex.origin()

        with pytest.raises(TypeError):
            assert -1.5 * AxialCoordinateHex(2, 4) == AxialCoordinateHex(-3, -6)
        with pytest.raises(TypeError):
            assert AxialCoordinateHex(2, 4) * 1.5 == AxialCoordinateHex(3, 6)

    def test_neg(self):
        assert -AxialCoordinateHex(-1, 3) == AxialCoordinateHex(1, -3)
        assert -AxialCoordinateHex.origin() == AxialCoordinateHex.origin()
        h = AxialCoordinateHex(2, -2)
        assert -(-h) == h

    def test_copy(self):
        o = AxialCoordinateHex.origin()
        o2 = copy.copy(o)
        assert o == o2
        assert id(o) != id(o2)
        assert o2.q == 0 and o2.r == 0

        h = get_random_AxialCooredinateHex(20, 17)
        h2 = copy.copy(h)
        assert h == h2
        assert id(h) != id(h2)

    def test_deepcopy(self):
        o = AxialCoordinateHex.origin()
        o2 = copy.deepcopy(o)
        assert o == o2
        assert id(o) != id(o2)
        assert o2.q == 0 and o2.r == 0

        h = get_random_AxialCooredinateHex(20, 17)
        h2 = copy.deepcopy(h)
        assert h == h2
        assert id(h) != id(h2)

    def test_neighbors(self):
        origin_neighbors = self.origin.neighbors
        assert len(origin_neighbors) == 6
        assert set(origin_neighbors) == set(self.origin.neighbor_directions)

        center = AxialCoordinateHex(-2, -4)
        assert center.neighbors == [
            AxialCoordinateHex(-1, -4),
            AxialCoordinateHex(-1, -5),
            AxialCoordinateHex(-2, -5),
            AxialCoordinateHex(-3, -4),
            AxialCoordinateHex(-3, -3),
            AxialCoordinateHex(-2, -3),
        ]

    def test_reflection(self):
        assert AxialCoordinateHex(4, 8).reflect_over_hex(AxialCoordinateHex(3, 5)) == AxialCoordinateHex(2, 2)
        assert AxialCoordinateHex(3, 3).reflect_over_hex() == AxialCoordinateHex(-3, -3)
        h = AxialCoordinateHex(1, 3)
        assert h.reflect_over_hex() == -h

    def test_reflect_over_q_axis(self):
        assert AxialCoordinateHex.origin().reflect_over_q_axis() == AxialCoordinateHex.origin()
        assert AxialCoordinateHex(3, -5).reflect_over_q_axis() == AxialCoordinateHex(3, 2)
        original = get_random_AxialCooredinateHex(20, 1234)
        reflected = original.reflect_over_q_axis()
        assert original.q == reflected.q
        assert original.r == reflected._s
        assert original._s == reflected.r

    def test_reflect_over_r_axis(self):
        assert AxialCoordinateHex.origin().reflect_over_r_axis() == AxialCoordinateHex.origin()
        assert AxialCoordinateHex(3, -5).reflect_over_r_axis() == AxialCoordinateHex(2, -5)
        original = get_random_AxialCooredinateHex(20, 2345)
        reflected = original.reflect_over_r_axis()
        assert original.q == reflected._s
        assert original.r == reflected.r
        assert original._s == reflected.q

    def test_reflect_over_s_axis(self):
        assert AxialCoordinateHex.origin().reflect_over_s_axis() == AxialCoordinateHex.origin()
        assert AxialCoordinateHex(3, -5).reflect_over_s_axis() == AxialCoordinateHex(-5, 3)
        original = get_random_AxialCooredinateHex(20, 3456)
        reflected = original.reflect_over_s_axis()
        assert original.q == reflected.r
        assert original.r == reflected.q
        assert original._s == reflected._s

    def test_reflect_over_q_value(self):
        h1 = get_random_AxialCooredinateHex(20, 4567)
        assert h1.reflect_over_q_value(0) == AxialCoordinateHex(-h1.q, -h1._s)
        assert h1.reflect_over_q_value(0) == -h1.reflect_over_q_axis()

        for n in range(-5, 5):
            assert h1.reflect_over_q_value(h1.q + n) == AxialCoordinateHex(h1.q + 2 * n, h1.r - n)

        assert AxialCoordinateHex(4, -5).reflect_over_q_value(-1) == AxialCoordinateHex(-6, 0)

        assert AxialCoordinateHex(2, 2).reflect_over_q_value(3) == AxialCoordinateHex(4, 1)

    def test_reflect_over_r_value(self):
        h1 = get_random_AxialCooredinateHex(20, 5678)
        assert h1.reflect_over_r_value(0) == AxialCoordinateHex(-h1._s, -h1.r)
        assert h1.reflect_over_r_value(0) == -h1.reflect_over_r_axis()

        for n in range(-5, 5):
            assert h1.reflect_over_r_value(h1.r + n) == AxialCoordinateHex(h1.q - n, h1.r + 2 * n)

        assert AxialCoordinateHex(-1, -2).reflect_over_r_value(-1) == AxialCoordinateHex(-2, 0)

        assert AxialCoordinateHex(-2, 4).reflect_over_r_value(1) == AxialCoordinateHex(1, -2)

    def test_reflect_over_s_value(self):
        h1 = get_random_AxialCooredinateHex(20, 6789)
        print(h1)
        assert h1.reflect_over_s_value(0) == AxialCoordinateHex(-h1.r, -h1.q)
        assert h1.reflect_over_s_value(0) == -h1.reflect_over_s_axis()

        for n in range(-5, 5):
            assert h1.reflect_over_s_value(h1._s + n) == AxialCoordinateHex(h1.q - n, h1.r - n)

        assert AxialCoordinateHex(-2, -3).reflect_over_s_value(1) == AxialCoordinateHex(2, 1)

        assert AxialCoordinateHex(-2, 4).reflect_over_s_value(-1) == AxialCoordinateHex(-3, 3)

    def test_distance(self):
        h = get_random_AxialCooredinateHex(radius=20, random_seed=13)
        assert all(h.distance(other) == 1 for other in h.neighbors)
        assert h.distance(h) == 0
        assert AxialCoordinateHex(2, 0).distance(AxialCoordinateHex(-1, 2)) == 3

    def test_range(self):
        center = get_random_AxialCooredinateHex(radius=20, random_seed=11)
        for radius in range(1, 5):
            hexes_in_ranges = center.hexes_within_range(radius)
            assert all(0 <= center.distance(other) <= radius for other in hexes_in_ranges)
            centered_hex_number = 3 * radius * (radius + 1) + 1
            assert len(set(hexes_in_ranges)) == centered_hex_number

import copy
import random

import pytest

from cryptid.hex import AxialCoordinateHex, CubeCoordinateHex
from tests.test_utils import get_random_CubeCooredinateHex


class TestCubeCoordinateHex:
    origin: CubeCoordinateHex = CubeCoordinateHex.origin()

    def test_planar_condition(self):
        h1 = CubeCoordinateHex(0, 0, 0)
        h2 = CubeCoordinateHex(1, 2, -3)
        h3 = CubeCoordinateHex(3, -1, -2)
        h4 = CubeCoordinateHex(-5, 0, 5)

        with pytest.raises(AssertionError):
            h5 = CubeCoordinateHex(1, 0, 0)

        with pytest.raises(AssertionError):
            h6 = CubeCoordinateHex(-5, -5, -5)

    def test_equality(self):
        assert CubeCoordinateHex(0, 0, 0) == CubeCoordinateHex.origin()
        assert CubeCoordinateHex(3, -1, -2) == CubeCoordinateHex(3, -1, -2)

        for value in [0, -1.5, False, "test"]:
            with pytest.raises(AssertionError):
                assert CubeCoordinateHex(1, 1, -2) == value
            with pytest.raises(AssertionError):
                assert value == CubeCoordinateHex(1, 1, -2)

    def test_not_equal(self):
        assert CubeCoordinateHex(3, 1, -4) != CubeCoordinateHex(3, 3, -6)
        assert CubeCoordinateHex(3, 1, -4) != CubeCoordinateHex(1, 3, -4)
        assert CubeCoordinateHex(3, 1, -4) != CubeCoordinateHex(1, 1, -2)

    def test_hash(self):
        assert hash(CubeCoordinateHex(0, 0, 0)) == hash(CubeCoordinateHex.origin())
        assert hash(get_random_CubeCooredinateHex(10, 42)) != hash(get_random_CubeCooredinateHex(10, 43))

        my_dict = dict()
        my_dict[CubeCoordinateHex(0, 0, 0)] = "origin"
        my_dict[CubeCoordinateHex(-1, 1, 0)] = "test_1"
        my_dict[get_random_CubeCooredinateHex(20, 20)] = "test_2"

        assert my_dict[CubeCoordinateHex.origin()] == "origin"
        assert my_dict[CubeCoordinateHex(-1, 1, 0)] == "test_1"
        assert my_dict[get_random_CubeCooredinateHex(20, 20)] == "test_2"

    def test_to_2d_coordinates(self):
        assert CubeCoordinateHex.origin().to_2d_coordinates() == (0, 0)
        assert CubeCoordinateHex(3, 5, -8).to_2d_coordinates() == (3, 5)

        random_hex = get_random_CubeCooredinateHex(radius=20, random_seed=1)
        assert random_hex.to_2d_coordinates() == (random_hex.q, random_hex.r)

    def test_from_2d_coordinates(self):
        assert CubeCoordinateHex.from_2d_coordinates(0, 0) == CubeCoordinateHex.origin()
        assert CubeCoordinateHex.from_2d_coordinates(-12, 8) == CubeCoordinateHex(-12, 8, 4)

        q = random.randint(-20, 21)
        r = random.randint(-20, 21)
        assert CubeCoordinateHex.from_2d_coordinates(q, r) == CubeCoordinateHex(q, r, -q - r)

    def test_axial_conversion(self):
        assert CubeCoordinateHex.origin().to_axial_coordinate_hex() == AxialCoordinateHex.origin()
        assert CubeCoordinateHex.from_axial_coordinate_hex(AxialCoordinateHex.origin()) == CubeCoordinateHex.origin()

        assert CubeCoordinateHex(3, 1, -4).to_axial_coordinate_hex() == AxialCoordinateHex(3, 1)
        assert CubeCoordinateHex.from_axial_coordinate_hex(AxialCoordinateHex(3, 1)) == CubeCoordinateHex(3, 1, -4)

        assert CubeCoordinateHex(0, 4, -4).to_axial_coordinate_hex() == AxialCoordinateHex(0, 4)
        assert CubeCoordinateHex.from_axial_coordinate_hex(AxialCoordinateHex(0, 4)) == CubeCoordinateHex(0, 4, -4)

    def test_cube_conversion(self):
        assert CubeCoordinateHex.origin().to_cube_coordinate_hex() == CubeCoordinateHex.origin()
        assert CubeCoordinateHex.from_cube_coordinate_hex(CubeCoordinateHex.origin()) == CubeCoordinateHex.origin()

        assert CubeCoordinateHex(3, 1, -4).to_cube_coordinate_hex() == CubeCoordinateHex(3, 1, -4)
        assert CubeCoordinateHex.from_cube_coordinate_hex(CubeCoordinateHex(3, 1, -4)) == CubeCoordinateHex(3, 1, -4)

        assert CubeCoordinateHex(0, 2, -2).to_cube_coordinate_hex() == CubeCoordinateHex(0, 2, -2)
        assert CubeCoordinateHex.from_cube_coordinate_hex(CubeCoordinateHex(0, 2, -2)) == CubeCoordinateHex(0, 2, -2)

        hex_a = CubeCoordinateHex(4, 2, -6)
        hex_b = hex_a.to_cube_coordinate_hex()
        hex_c = CubeCoordinateHex.from_cube_coordinate_hex(hex_a)
        assert hex_a == hex_b and id(hex_a) != id(hex_b)
        assert hex_a == hex_c and id(hex_a) != id(hex_c)
        assert hex_c == hex_b and id(hex_c) != id(hex_b)

    def test_addition(self):
        assert CubeCoordinateHex(3, 5, -8) + CubeCoordinateHex(3, 5, -8) == CubeCoordinateHex(6, 10, -16)
        assert CubeCoordinateHex(3, 5, -8) + CubeCoordinateHex(0, 0, 0) == CubeCoordinateHex(3, 5, -8)
        assert CubeCoordinateHex(0, 0, 0) + CubeCoordinateHex(3, 5, -8) == CubeCoordinateHex(3, 5, -8)
        assert CubeCoordinateHex(-4, -6, 10) + CubeCoordinateHex(6, 6, -12) == CubeCoordinateHex(2, 0, -2)

        with pytest.raises(TypeError):
            test = 5 + CubeCoordinateHex(0, 0, 0)

        with pytest.raises(TypeError):
            test = CubeCoordinateHex(0, 0, 0) + 5

        # TODO: add other types of hexes

    def test_subtraction(self):
        assert CubeCoordinateHex(3, 5, -8) - CubeCoordinateHex(3, 5, -8) == CubeCoordinateHex(0, 0, 0)
        assert CubeCoordinateHex(3, 5, -8) - CubeCoordinateHex(0, 0, 0) == CubeCoordinateHex(3, 5, -8)
        assert CubeCoordinateHex(0, 0, 0) - CubeCoordinateHex(3, 5, -8) == CubeCoordinateHex(-3, -5, 8)
        assert CubeCoordinateHex(-4, -6, 10) - CubeCoordinateHex(6, 6, -12) == CubeCoordinateHex(-10, -12, 22)

        with pytest.raises(TypeError):
            test = 5 - CubeCoordinateHex(0, 0, 0)

        with pytest.raises(TypeError):
            test = CubeCoordinateHex(0, 0, 0) - 5

        # TODO: add other types of hexes

    def test_multiply(self):
        assert CubeCoordinateHex(1, 3, -4) * 5 == CubeCoordinateHex(5, 15, -20)
        assert 5 * CubeCoordinateHex(1, 3, -4) == CubeCoordinateHex(5, 15, -20)
        assert CubeCoordinateHex(1, 3, -4) * 0 == CubeCoordinateHex(0, 0, 0)
        assert 0 * CubeCoordinateHex(1, 3, -4) == CubeCoordinateHex(0, 0, 0)
        assert CubeCoordinateHex(1, 3, -4) * -2 == CubeCoordinateHex(-2, -6, 8)
        assert -2 * CubeCoordinateHex(1, 3, -4) == CubeCoordinateHex(-2, -6, 8)
        assert 3 * CubeCoordinateHex.origin() == CubeCoordinateHex.origin()
        assert CubeCoordinateHex.origin() * 3 == CubeCoordinateHex.origin()

        with pytest.raises(TypeError):
            assert -1.5 * CubeCoordinateHex(2, 4, -6) == CubeCoordinateHex(-3, -6, 9)
        with pytest.raises(TypeError):
            assert CubeCoordinateHex(2, 4, -6) * 1.5 == CubeCoordinateHex(3, 6, 9)

    def test_neg(self):
        assert -CubeCoordinateHex(-1, 3, -2) == CubeCoordinateHex(1, -3, 2)
        assert -CubeCoordinateHex.origin() == CubeCoordinateHex.origin()
        h = CubeCoordinateHex(2, -2, 0)
        assert -(-h) == h

    def test_copy(self):
        o = CubeCoordinateHex.origin()
        o2 = copy.copy(o)
        assert o == o2
        assert id(o) != id(o2)
        assert o2.q == 0 and o2.r == 0 and o2.s == 0

        h = get_random_CubeCooredinateHex(20, 17)
        h2 = copy.copy(h)
        assert h == h2
        assert id(h) != id(h2)

    def test_deepcopy(self):
        o = CubeCoordinateHex.origin()
        o2 = copy.deepcopy(o)
        assert o == o2
        assert id(o) != id(o2)
        assert o2.q == 0 and o2.r == 0 and o2.s == 0

        h = get_random_CubeCooredinateHex(20, 17)
        h2 = copy.deepcopy(h)
        assert h == h2
        assert id(h) != id(h2)

    def test_neighbors(self):
        origin_neighbors = self.origin.neighbors
        assert len(origin_neighbors) == 6
        assert set(origin_neighbors) == set(self.origin.neighbor_directions)

        center = CubeCoordinateHex(-2, -4, 6)
        assert center.neighbors == [
            CubeCoordinateHex(-1, -4, 5),
            CubeCoordinateHex(-1, -5, 6),
            CubeCoordinateHex(-2, -5, 7),
            CubeCoordinateHex(-3, -4, 7),
            CubeCoordinateHex(-3, -3, 6),
            CubeCoordinateHex(-2, -3, 5),
        ]

    def test_reflection(self):
        assert CubeCoordinateHex(4, 8, -12).reflect_over_hex(CubeCoordinateHex(3, 5, -8)) == CubeCoordinateHex(2, 2, -4)
        assert CubeCoordinateHex(3, 3, -6).reflect_over_hex() == CubeCoordinateHex(-3, -3, 6)
        h = CubeCoordinateHex(1, 3, -4)
        assert h.reflect_over_hex() == -h

    def test_reflect_over_q_axis(self):
        assert CubeCoordinateHex.origin().reflect_over_q_axis() == CubeCoordinateHex.origin()
        assert CubeCoordinateHex(3, -5, 2).reflect_over_q_axis() == CubeCoordinateHex(3, 2, -5)
        original = get_random_CubeCooredinateHex(20, 1234)
        reflected = original.reflect_over_q_axis()
        assert original.q == reflected.q
        assert original.r == reflected.s
        assert original.s == reflected.r

    def test_reflect_over_r_axis(self):
        assert CubeCoordinateHex.origin().reflect_over_r_axis() == CubeCoordinateHex.origin()
        assert CubeCoordinateHex(3, -5, 2).reflect_over_r_axis() == CubeCoordinateHex(2, -5, 3)
        original = get_random_CubeCooredinateHex(20, 2345)
        reflected = original.reflect_over_r_axis()
        assert original.q == reflected.s
        assert original.r == reflected.r
        assert original.s == reflected.q

    def test_reflect_over_s_axis(self):
        assert CubeCoordinateHex.origin().reflect_over_s_axis() == CubeCoordinateHex.origin()
        assert CubeCoordinateHex(3, -5, 2).reflect_over_s_axis() == CubeCoordinateHex(-5, 3, 2)
        original = get_random_CubeCooredinateHex(20, 3456)
        reflected = original.reflect_over_s_axis()
        assert original.q == reflected.r
        assert original.r == reflected.q
        assert original.s == reflected.s

    def test_reflect_over_q_value(self):
        h1 = get_random_CubeCooredinateHex(20, 4567)
        assert h1.reflect_over_q_value(0) == CubeCoordinateHex(-h1.q, -h1.s, -h1.r)
        assert h1.reflect_over_q_value(0) == -h1.reflect_over_q_axis()

        for n in range(-5, 5):
            assert h1.reflect_over_q_value(h1.q + n) == CubeCoordinateHex(h1.q + 2 * n, h1.r - n, h1.s - n)

        assert CubeCoordinateHex(4, -5, 1).reflect_over_q_value(-1) == CubeCoordinateHex(-6, 0, 6)

        assert CubeCoordinateHex(2, 2, -4).reflect_over_q_value(3) == CubeCoordinateHex(4, 1, -5)

    def test_reflect_over_r_value(self):
        h1 = get_random_CubeCooredinateHex(20, 5678)
        assert h1.reflect_over_r_value(0) == CubeCoordinateHex(-h1.s, -h1.r, -h1.q)
        assert h1.reflect_over_r_value(0) == -h1.reflect_over_r_axis()

        for n in range(-5, 5):
            assert h1.reflect_over_r_value(h1.r + n) == CubeCoordinateHex(h1.q - n, h1.r + 2 * n, h1.s - n)

        assert CubeCoordinateHex(-1, -2, 3).reflect_over_r_value(-1) == CubeCoordinateHex(-2, 0, 2)

        assert CubeCoordinateHex(-2, 4, -2).reflect_over_r_value(1) == CubeCoordinateHex(1, -2, 1)

    def test_reflect_over_s_value(self):
        h1 = get_random_CubeCooredinateHex(20, 6789)
        print(h1)
        assert h1.reflect_over_s_value(0) == CubeCoordinateHex(-h1.r, -h1.q, -h1.s)
        assert h1.reflect_over_s_value(0) == -h1.reflect_over_s_axis()

        for n in range(-5, 5):
            assert h1.reflect_over_s_value(h1._s + n) == CubeCoordinateHex(h1.q - n, h1.r - n, h1.s + 2 * n)

        assert CubeCoordinateHex(-2, -3, 5).reflect_over_s_value(1) == CubeCoordinateHex(2, 1, -3)
        assert CubeCoordinateHex(-2, 4, -2).reflect_over_s_value(-1) == CubeCoordinateHex(-3, 3, 0)

    def test_distance(self):
        h = get_random_CubeCooredinateHex(radius=20, random_seed=13)
        assert all(h.distance(other) == 1 for other in h.neighbors)
        assert h.distance(h) == 0
        assert CubeCoordinateHex(2, 0, -2).distance(CubeCoordinateHex(-1, 2, -1)) == 3
        assert CubeCoordinateHex(2, 0, -2).distance(AxialCoordinateHex(-1, 2)) == 3
        assert AxialCoordinateHex(2, 0).distance(CubeCoordinateHex(-1, 2, -1)) == 3

    def test_range(self):
        center = get_random_CubeCooredinateHex(radius=20, random_seed=11)
        for radius in range(1, 5):
            hexes_in_ranges = center.hexes_within_range(radius)
            assert all(0 <= center.distance(other) <= radius for other in hexes_in_ranges)
            centered_hex_number = 3 * radius * (radius + 1) + 1
            assert len(set(hexes_in_ranges)) == centered_hex_number

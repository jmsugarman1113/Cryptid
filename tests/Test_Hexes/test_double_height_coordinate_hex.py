import pytest

from cryptid.Hex import AxialCoordinateHex, CubeCoordinateHex, DoubledHeightCoordinateHex


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

    def test_hash(self):
        assert hash(DoubledHeightCoordinateHex(0, 0)) == hash(DoubledHeightCoordinateHex.origin())

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

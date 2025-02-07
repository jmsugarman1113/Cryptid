import pytest

from cryptid.Hex import DoubledHeightCoordinateHex


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

    def test_neighbors(self):
        origin_neighbors = self.origin.neighbors
        assert len(origin_neighbors) == 6
        assert set(origin_neighbors) == set(self.origin.neighbor_directions)

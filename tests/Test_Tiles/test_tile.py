from cryptid.hex import DoubledHeightCoordinateHex
from cryptid.tile import AnimalTerritory, Color, Shape, Structure, Terrain, Tile


class TestTile:
    def test_tile_addition(self):
        tileA = Tile(
            hex=DoubledHeightCoordinateHex(1, 5),
            terrain=Terrain.MOUNTAIN,
            animal_territory=AnimalTerritory.BEAR,
        )
        tileB = Tile(
            hex=DoubledHeightCoordinateHex(2, -4),
            terrain=Terrain.FOREST,
            structure=Structure(shape=Shape.STANDING_STONE, color=Color.BLUE),
        )

        hex_offset = DoubledHeightCoordinateHex(-1, 1)

        tile_AB = tileA + tileB
        assert isinstance(tile_AB, Tile)
        assert tile_AB is not tileA and tile_AB is not tileB
        assert tile_AB.hex == DoubledHeightCoordinateHex(3, 1)
        assert tile_AB.terrain == tileA.terrain
        assert tile_AB.terrain == Terrain.MOUNTAIN
        assert tile_AB.animal_territory == tileA.animal_territory
        assert tile_AB.animal_territory == AnimalTerritory.BEAR
        assert tile_AB.structure == tileA.structure
        assert tile_AB.structure is None

        tile_BA = tileB + tileA
        assert isinstance(tile_BA, Tile)
        assert tile_BA is not tileA and tile_AB is not tileB
        assert tile_BA.hex == DoubledHeightCoordinateHex(3, 1)
        assert tile_BA.terrain == tileB.terrain
        assert tile_BA.terrain == Terrain.FOREST
        assert tile_BA.animal_territory == tileB.animal_territory
        assert tile_BA.animal_territory is None
        assert tile_BA.structure == tileB.structure
        assert tile_BA.structure == Structure(Shape.STANDING_STONE, Color.BLUE)

        tileA_offset = tileA + hex_offset
        assert isinstance(tileA_offset, Tile)
        assert tileA_offset is not tileA
        assert tileA_offset.hex == DoubledHeightCoordinateHex(0, 6)
        assert tileA_offset.terrain == tileA.terrain
        assert tileA_offset.terrain == Terrain.MOUNTAIN
        assert tileA_offset.animal_territory == tileA.animal_territory
        assert tileA_offset.animal_territory == AnimalTerritory.BEAR
        assert tileA_offset.structure == tileA.structure
        assert tileA_offset.structure is None

        tileB_offset = tileB + hex_offset
        assert isinstance(tileB_offset, Tile)
        assert tileB_offset is not tileB
        assert tileB_offset.hex == DoubledHeightCoordinateHex(1, -3)
        assert tileB_offset.terrain == tileB.terrain
        assert tileB_offset.terrain == Terrain.FOREST
        assert tileB_offset.animal_territory == tileB.animal_territory
        assert tileB_offset.animal_territory is None
        assert tileB_offset.structure == tileB.structure
        assert tileB_offset.structure == Structure(Shape.STANDING_STONE, Color.BLUE)

        tileA_offset2 = tileA + DoubledHeightCoordinateHex.origin()
        assert isinstance(tileA_offset, Tile)
        assert tileA_offset2 == tileA
        assert tileA_offset2 is not tileA
        assert tileA_offset2.hex == DoubledHeightCoordinateHex(1, 5)
        assert tileA_offset2.terrain == tileA.terrain
        assert tileA_offset2.terrain == Terrain.MOUNTAIN
        assert tileA_offset2.animal_territory == tileA.animal_territory
        assert tileA_offset2.animal_territory == AnimalTerritory.BEAR
        assert tileA_offset2.structure == tileA.structure
        assert tileA_offset2.structure is None

        tileB_offset2 = tileB + DoubledHeightCoordinateHex.origin()
        assert isinstance(tileB_offset, Tile)
        assert tileB_offset2 == tileB
        assert tileB_offset2 is not tileB
        assert tileB_offset2.hex == DoubledHeightCoordinateHex(2, -4)
        assert tileB_offset2.terrain == tileB.terrain
        assert tileB_offset2.terrain == Terrain.FOREST
        assert tileB_offset2.animal_territory == tileB.animal_territory
        assert tileB_offset2.animal_territory is None
        assert tileB_offset2.structure == tileB.structure
        assert tileB_offset2.structure == Structure(Shape.STANDING_STONE, Color.BLUE)

    def test_tile_subtraction(self):
        tileA = Tile(
            hex=DoubledHeightCoordinateHex(1, 5),
            terrain=Terrain.MOUNTAIN,
            animal_territory=AnimalTerritory.BEAR,
        )
        tileB = Tile(
            hex=DoubledHeightCoordinateHex(2, -4),
            terrain=Terrain.FOREST,
            structure=Structure(shape=Shape.STANDING_STONE, color=Color.BLUE),
        )

        hex_offset = DoubledHeightCoordinateHex(-1, 1)

        tile_AB = tileA - tileB
        assert isinstance(tile_AB, Tile)
        assert tile_AB is not tileA and tile_AB is not tileB
        assert tile_AB.hex == DoubledHeightCoordinateHex(-1, 9)
        assert tile_AB.terrain == tileA.terrain
        assert tile_AB.terrain == Terrain.MOUNTAIN
        assert tile_AB.animal_territory == tileA.animal_territory
        assert tile_AB.animal_territory == AnimalTerritory.BEAR
        assert tile_AB.structure == tileA.structure
        assert tile_AB.structure is None

        tile_BA = tileB - tileA
        assert isinstance(tile_BA, Tile)
        assert tile_BA is not tileA and tile_AB is not tileB
        assert tile_BA.hex == DoubledHeightCoordinateHex(1, -9)
        assert tile_BA.terrain == tileB.terrain
        assert tile_BA.terrain == Terrain.FOREST
        assert tile_BA.animal_territory == tileB.animal_territory
        assert tile_BA.animal_territory is None
        assert tile_BA.structure == tileB.structure
        assert tile_BA.structure == Structure(Shape.STANDING_STONE, Color.BLUE)

        tileA_offset = tileA - hex_offset
        assert isinstance(tileA_offset, Tile)
        assert tileA_offset is not tileA
        assert tileA_offset.hex == DoubledHeightCoordinateHex(2, 4)
        assert tileA_offset.terrain == tileA.terrain
        assert tileA_offset.terrain == Terrain.MOUNTAIN
        assert tileA_offset.animal_territory == tileA.animal_territory
        assert tileA_offset.animal_territory == AnimalTerritory.BEAR
        assert tileA_offset.structure == tileA.structure
        assert tileA_offset.structure is None

        tileB_offset = tileB - hex_offset
        assert isinstance(tileB_offset, Tile)
        assert tileB_offset is not tileB
        assert tileB_offset.hex == DoubledHeightCoordinateHex(3, -5)
        assert tileB_offset.terrain == tileB.terrain
        assert tileB_offset.terrain == Terrain.FOREST
        assert tileB_offset.animal_territory == tileB.animal_territory
        assert tileB_offset.animal_territory is None
        assert tileB_offset.structure == tileB.structure
        assert tileB_offset.structure == Structure(Shape.STANDING_STONE, Color.BLUE)

        tileA_offset2 = tileA - DoubledHeightCoordinateHex.origin()
        assert isinstance(tileA_offset, Tile)
        assert tileA_offset2 == tileA
        assert tileA_offset2 is not tileA
        assert tileA_offset2.hex == DoubledHeightCoordinateHex(1, 5)
        assert tileA_offset2.terrain == tileA.terrain
        assert tileA_offset2.terrain == Terrain.MOUNTAIN
        assert tileA_offset2.animal_territory == tileA.animal_territory
        assert tileA_offset2.animal_territory == AnimalTerritory.BEAR
        assert tileA_offset2.structure == tileA.structure
        assert tileA_offset2.structure is None

        tileB_offset2 = tileB - DoubledHeightCoordinateHex.origin()
        assert isinstance(tileB_offset, Tile)
        assert tileB_offset2 == tileB
        assert tileB_offset2 is not tileB
        assert tileB_offset2.hex == DoubledHeightCoordinateHex(2, -4)
        assert tileB_offset2.terrain == tileB.terrain
        assert tileB_offset2.terrain == Terrain.FOREST
        assert tileB_offset2.animal_territory == tileB.animal_territory
        assert tileB_offset2.animal_territory is None
        assert tileB_offset2.structure == tileB.structure
        assert tileB_offset2.structure == Structure(Shape.STANDING_STONE, Color.BLUE)

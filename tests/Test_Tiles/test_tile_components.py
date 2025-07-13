from cryptid.tile import AnimalTerritory, Color, Shape, Structure, Terrain


class TestAnimalTerritory:
    def test_num_values(self):
        assert len(AnimalTerritory) == 2

    def test_string_representations(self):
        assert AnimalTerritory.BEAR.value == "BEAR"
        assert AnimalTerritory.COUGAR.value == "COUGAR"


class TestTerrain:
    def test_num_values(self):
        assert len(Terrain) == 5

    def test_string_representations(self):
        assert Terrain.DESERT.value == "DESERT"
        assert Terrain.WATER.value == "WATER"
        assert Terrain.SWAMP.value == "SWAMP"
        assert Terrain.FOREST.value == "FOREST"
        assert Terrain.MOUNTAIN.value == "MOUNTAIN"


class TestColor:
    def test_num_values(self):
        assert len(Color) == 4

    def test_string_representations(self):
        assert Color.WHITE.value == "WHITE"
        assert Color.BLACK.value == "BLACK"
        assert Color.BLUE.value == "BLUE"
        assert Color.GREEN.value == "GREEN"


class TestShape:
    def test_num_values(self):
        assert len(Shape) == 2

    def test_string_representations(self):
        assert Shape.ABANDONED_SHACK.value == "ABANDONED_SHACK"
        assert Shape.STANDING_STONE.value == "STANDING_STONE"


class TestStructure:
    def test_string_representation(self):
        struct = Structure(
            shape=Shape.STANDING_STONE,
            color=Color.BLUE,
        )
        assert str(struct) == "Structure(shape=STANDING_STONE, color=BLUE)"

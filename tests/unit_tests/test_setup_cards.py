from cryptid.setup_card import SetupCard, SETUP_CARDS
from cryptid.board import Board
from cryptid.tile import Tile, Terrain, AnimalTerritory, Structure, Shape, Color
from cryptid.hex import DoubledHeightCoordinateHex


class TestSetUpCards:
    @staticmethod
    def default_board_from_card_test(board: Board) -> bool:
        assert len(board.tiles) == 108  # size of board

        # static animal territory sizes
        assert len([tile for tile in board.tiles.values() if tile.animal_territory == AnimalTerritory.BEAR]) == 8
        assert len([tile for tile in board.tiles.values() if tile.animal_territory == AnimalTerritory.COUGAR]) == 8

        # static terrain counts
        for terrain, count in zip(
            [Terrain.FOREST, Terrain.WATER, Terrain.DESERT, Terrain.MOUNTAIN, Terrain.SWAMP],
            [22, 22, 21, 22, 21],
        ):
            assert len([tile for tile in board.tiles.values() if tile.terrain == terrain]) == count

        # bounds on static hex locations
        for tile in board.tiles.values():
            axial_hex = tile.hex.to_axial_coordinate_hex()
            assert 0 <= axial_hex.q <= 11
            assert -5 <= axial_hex.r <= 8
        return True

    def test_SETUPCARDS(self):
        # assert len(SETUP_CARDS) == 54  # TODO: uncomment once all cards created
        assert all(isinstance(card, SetupCard) for card in SETUP_CARDS)
        assert all([self.default_board_from_card_test(Board.from_setup_card(card)) for card in SETUP_CARDS])

    def test_to_board(self):
        card = SETUP_CARDS[0]
        board = Board.from_setup_card(card)
        assert self.default_board_from_card_test(board)
        assert len([tile for tile in board.tiles.values() if tile.structure is not None]) == len(card.structures) == 6

        location = DoubledHeightCoordinateHex(1, 1)
        assert board.tiles[location] == Tile(
            hex=location,
            terrain=Terrain.DESERT,
            animal_territory=AnimalTerritory.BEAR,
            structure=Structure(Shape.STANDING_STONE, Color.BLUE),
        )

        location = DoubledHeightCoordinateHex(9, 13)
        assert board.tiles[location] == Tile(
            hex=location, terrain=Terrain.MOUNTAIN, structure=Structure(Shape.ABANDONED_SHACK, Color.GREEN)
        )

        location = DoubledHeightCoordinateHex(7, 7)
        assert board.tiles[location] == Tile(
            hex=location,
            terrain=Terrain.WATER,
        )

    # TODO: test clues
    # TODO: test clues

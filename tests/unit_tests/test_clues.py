from cryptid.clue import Clue, NullClue, ALPHA_CLUES, BETA_CLUES, GAMMA_CLUES, DELTA_CLUES


class TestClues:
    def test_clue_books(self):
        for clue_book in [
            ALPHA_CLUES,
            BETA_CLUES,
            GAMMA_CLUES,
            DELTA_CLUES,
            # EPSILON_CLUES,
        ]:
            assert len(clue_book) == 97
            assert isinstance(clue_book[0], NullClue)
            assert all(isinstance(clue, Clue) and not isinstance(clue, NullClue) for clue in clue_book[1:])

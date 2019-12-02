import unittest

from solutions.day02.solution import ship_computer
from tests.helpers import Puzzle


class DayTwoTests(unittest.TestCase):
    """Tests for my solutions to Day 1 of the Advent of Code 2019."""

    def test_ship_computer_with_example_data(self):
        """Test the ship computer used for day 2 using the example data provided in the puzzle."""
        test_cases = (
            Puzzle(data=[1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], answer=3500),
        )

        for puzzle in test_cases:
            with self.subTest(data=puzzle.data, answer=puzzle.answer):
                # We don't have a noun or verb, so fake it by supplying the values already in place
                noun = puzzle.data[1]
                verb = puzzle.data[2]

                self.assertEqual(ship_computer(puzzle.data, noun=noun, verb=verb), puzzle.answer)

import unittest

from solutions.day01 import part_one, part_two
from tests.helpers import Puzzle


class DayOneTests(unittest.TestCase):
    """Tests for my solutions to Day 1 of the Advent of Code 2019."""

    def test_part_one_examples(self):
        """Test part one of day 1 using the example data provided in the puzzle."""
        test_cases = (
            Puzzle(data=[12], answer=2),
            Puzzle(data=[14], answer=2),
            Puzzle(data=[1969], answer=654),
            Puzzle(data=[100756], answer=33583),
        )

        for puzzle in test_cases:
            with self.subTest(data=puzzle.data, answer=puzzle.answer):
                self.assertEqual(part_one(puzzle.data), puzzle.answer)

    def test_part_two_examples(self):
        """Test part two of day 1 using the example data provided in the puzzle."""
        test_cases = (
            Puzzle(data=[14], answer=2),
            Puzzle(data=[1969], answer=966),
            Puzzle(data=[100756], answer=50346),
        )

        for puzzle in test_cases:
            with self.subTest(data=puzzle.data, answer=puzzle.answer):
                self.assertEqual(part_two(puzzle.data), puzzle.answer)

from typing import List, Tuple


def part_one(data: List[int]) -> int:
    """Part one of today's Advent of Code puzzle."""


def part_two(data: List[int]) -> int:
    """Part two of today's Advent of Code puzzle."""


def main(data: List[str]) -> Tuple[int]:
    """The main function taking care of parsing the input data and running the solutions."""
    data = [int(number) for number in data]
    answer_one = part_one(data)
    answer_two = part_two(data)
    return answer_one, answer_two

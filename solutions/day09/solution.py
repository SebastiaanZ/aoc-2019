from typing import List, Tuple

from solutions.helpers import IntCodeApplication


def part_one(data: List[int]) -> int:
    """Part one of today's Advent of Code puzzle."""
    app = IntCodeApplication(data, name="BOOST Part I", flexible_memory=True)
    app.stdin.put(1)
    app.run()
    return app.stdout.get()


def part_two(data: List[int]) -> int:
    """Part two of today's Advent of Code puzzle."""
    app = IntCodeApplication(data, name="BOOST Part II", flexible_memory=True)
    app.stdin.put(2)
    app.run()
    return app.stdout.get()


def main(data: List[str]) -> Tuple[int, int]:
    """The main function taking care of parsing the input data and running the solutions."""
    data = [int(number) for number in data[0].split(",")]

    answer_one = part_one(data)
    answer_two = part_two(data)
    return answer_one, answer_two

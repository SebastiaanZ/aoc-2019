from typing import List, Tuple

from solutions.day05.helpers import System, terminal


def part_one(data: List[int]) -> int:
    """Run the diagnostics on the Thermal Environment Supervision Terminal."""
    system = System(application=list(data), stdin=iter([1]))
    system = terminal(system)
    return system.stdout.pop()


def part_two(data: List[int]) -> int:
    """Run diagnostics on System ID 5 of the Thermal Environment Supervision Terminal."""
    system = System(application=list(data), stdin=iter([5]))
    system = terminal(system)
    return system.stdout.pop()


def main(data: List[str]) -> Tuple[int]:
    """The main function taking care of parsing the input data and running the solutions."""
    data = [int(number) for number in data[0].split(",")]

    answer_one = part_one(data)
    answer_two = part_two(data)
    return answer_one, answer_two

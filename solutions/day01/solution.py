import itertools
from typing import List


def _fuel_requirement(mass: int) -> int:
    """Calculates the fuel requirement for a given mass."""
    return mass // 3 - 2


def _module_fuel(mass):
    """Yields the `n+1` fuel requirements, starting with the `n+1` of `mass`."""
    while True:
        mass = _fuel_requirement(mass)
        yield mass


def part_one(data: List[int]) -> int:
    """Calculates the fuel requirements of my spacecraft."""
    return sum(_fuel_requirement(number) for number in data)


def part_two(data: List[int]) -> int:
    """Calculates the fuel requirements including the fuel mass itself."""
    return sum(sum(itertools.takewhile(lambda fuel: fuel > 0, _module_fuel(mass))) for mass in data)


def main(data: List[str]) -> None:
    data = [int(number) for number in data]
    answer_one = part_one(data)
    answer_two = part_two(data)
    return answer_one, answer_two

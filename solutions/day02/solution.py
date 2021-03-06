import functools
import itertools
import operator
from typing import Callable, List, Tuple


def cpu_operation(a: int, b: int, destination: int, data: List[int], operation: Callable) -> None:
    """Uses operation on numbers `a` and `b` and stores the result at `destination` in `data`."""
    data[destination] = operation(a, b)


COMPUTER_OPERATIONS = {
    1: functools.partial(cpu_operation, operation=operator.add),
    2: functools.partial(cpu_operation, operation=operator.mul),
}


def ship_computer(data: List[int], noun: int, verb: int) -> int:
    """The computer of my space ship, processing the intcodes in `data`."""
    data = list(data)

    data[1] = noun
    data[2] = verb

    operation_code = iter(data)

    while (operation := next(operation_code)) != 99:
        a = data[next(operation_code)]
        b = data[next(operation_code)]
        destination = next(operation_code)
        COMPUTER_OPERATIONS[operation](a, b, destination, data=data)
    return data[0]


def part_one(data: List[int]) -> int:
    """Calculate the result value of the intcode application with noun=12, verb=2."""
    return ship_computer(data, noun=12, verb=2)


def part_two(data: List[int]) -> int:
    """Determine the noun and verb needed to get `19690720` out of the ship's computer."""
    for noun, verb in itertools.product(range(100), repeat=2):
        result = ship_computer(data, noun=noun, verb=verb)
        if result == 19690720:
            return 100 * noun + verb


def main(data: List[str]) -> Tuple[int]:
    """The main function taking care of parsing the input data and running the solutions."""
    op_codes = data[0].split(",")
    data = [int(number) for number in op_codes]
    answer_one = part_one(data)
    answer_two = part_two(data)
    return answer_one, answer_two

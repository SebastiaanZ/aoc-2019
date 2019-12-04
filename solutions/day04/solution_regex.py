import re
from typing import List, Tuple


def part_one(start: int, stop: int) -> int:
    """Part one of today's Advent of Code puzzle."""
    pattern = re.compile(r"(?:(?=.*(\d)\1{1,}.*))^1*2*3*4*5*6*7*8*9*$")
    return sum(pattern.fullmatch(str(password)) is not None for password in range(start, stop))


def part_two(start: int, stop: int) -> int:
    """Part two of today's Advent of Code puzzle."""
    pattern = re.compile(
        r"(?:"
        r"(?=.*(?<!1)(?:1){2}(?!1).*)|"
        r"(?=.*(?<!2)(?:2){2}(?!2).*)|"
        r"(?=.*(?<!3)(?:3){2}(?!3).*)|"
        r"(?=.*(?<!4)(?:4){2}(?!4).*)|"
        r"(?=.*(?<!5)(?:5){2}(?!5).*)|"
        r"(?=.*(?<!6)(?:6){2}(?!6).*)|"
        r"(?=.*(?<!7)(?:7){2}(?!7).*)|"
        r"(?=.*(?<!8)(?:8){2}(?!8).*)|"
        r"(?=.*(?<!9)(?:9){2}(?!9)).*)"
        r"^1*2*3*4*5*6*7*8*9*$"
    )
    return sum(pattern.fullmatch(str(password)) is not None for password in range(start, stop))


def main(data: List[str]) -> Tuple[int]:
    """The main function taking care of parsing the input data and running the solutions."""
    start, stop = [int(n) for n in data[0].split("-")]
    answer_one = part_one(start, stop+1)
    answer_two = part_two(start, stop+1)
    return answer_one, answer_two

from collections import Counter
from typing import List, Tuple


def ascending_values(start: str, stop: str) -> str:
    """Yield striclty ascending numbers between `start` and `stop`, boundaries includes."""
    stop = int(stop)
    number = start
    while int(number) <= stop:
        for i, (a, b) in enumerate(zip(number, number[1:]), start=1):
            if a > b:
                number = number[:i] + a * (6 - i)
                break
        else:
            yield number
            number = str(int(number)+1)


def main(data: List[str]) -> Tuple[int]:
    """The main function taking care of parsing the input data and running the solutions."""
    start, stop = data[0].split("-")
    answer_one = 0
    answer_two = 0

    for number in ascending_values(start, stop):
        c = Counter(number)
        answer_one += max(c.values()) >= 2
        answer_two += 2 in c.values()

    return answer_one, answer_two

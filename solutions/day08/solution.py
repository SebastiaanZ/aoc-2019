from collections import Counter
from operator import itemgetter
from typing import List, Tuple

import numpy as np


def part_one(data: str) -> int:
    """Find the layer with the least amount of `0`s and return number of `1`s *  number of `2`s."""
    min_layer = min((Counter(layer) for layer in zip(*[iter(data)]*150)), key=itemgetter("0"))
    return min_layer["1"] * min_layer["2"]


def part_two_numpy(data: List[int]) -> str:
    """Reconstruct the image of the password by stacking partially transparent layers."""
    image = np.full(150, 2, dtype=np.uint8)
    for layer in zip(*[iter(data)]*150):
        mask = image == 2
        image[mask] = np.array(layer)[mask]
    image = image.reshape((6, 25)).tolist()
    return "\n".join("".join("\u2588" if pixel == 1 else " " for pixel in row) for row in image)


def part_two(data: str) -> str:
    """Reconstruct the image of the password by stacking partially transparent layers."""
    pixels = [[] for _ in range(6)]
    for i in range(150):
        for pixel in data[i::150]:
            if pixel != "2":
                row = i // 25
                pixels[row].append(pixel)
                break
    return "\n".join("".join("\u2588" if pixel == "1" else " " for pixel in row) for row in pixels)


def main(data: List[str]) -> Tuple[int, str]:
    """The main function taking care of parsing the input data and running the solutions."""
    data = data[0]
    answer_one = part_one(data)
    answer_two = part_two(data)
    return answer_one, "\n" + answer_two

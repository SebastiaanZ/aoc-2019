import threading
from typing import List, Tuple

from solutions.helpers import IntCodeApplication


def part_one(data: List[int]) -> int:
    """Test the Emergency Hull Painting Robot by running its application."""
    canvas = {}
    application = IntCodeApplication(
        application=data,
        name="Painting App",
        flexible_memory=True,
    )
    pipe_in = application.stdin
    pipe_out = application.stdout

    robot = threading.Thread(target=application.run)
    robot.start()

    location = complex(0, 0)
    direction = complex(0, 1)

    while robot.is_alive():
        pipe_in.put(canvas.get(location, 0))
        canvas[location] = pipe_out.get()
        direction *= complex(0, 1 - 2*pipe_out.get())
        location += direction

    return len(canvas)


def part_two(data: List[int]) -> int:
    """Paint a Registration Identifier on my Spaceship to please the Space police."""
    canvas = {complex(0, 0): 1}
    application = IntCodeApplication(
        application=data,
        name="Painting App",
        flexible_memory=True,
    )
    pipe_in = application.stdin
    pipe_out = application.stdout

    robot = threading.Thread(target=application.run)
    robot.start()

    location = complex(0, 0)
    direction = complex(0, 1)

    while robot.is_alive():
        pipe_in.put(canvas.get(location, 0))
        canvas[location] = pipe_out.get()
        direction *= complex(0, 1 - 2*pipe_out.get())
        location += direction

    x_min, x_max = min(c.real for c in canvas), max(c.real for c in canvas)
    y_min, y_max = min(c.imag for c in canvas), max(c.imag for c in canvas)

    panels = [[' ']*int(x_max-x_min+1) for _ in range(int(y_min), int(y_max)+1)]

    for coordinate, color in canvas.items():
        x, y = int(coordinate.real)-int(x_min), int(coordinate.imag) - int(y_min)
        panels[y][x] = ' ' if color == 0 else "\u25AF"

    return "\n".join("".join(row) for row in reversed(panels))


def main(data: List[str]) -> Tuple[int]:
    """The main function taking care of parsing the input data and running the solutions."""
    data = [int(number) for number in data[0].split(",")]

    answer_one = part_one(data)
    answer_two = part_two(data)
    return answer_one, "\n" + answer_two

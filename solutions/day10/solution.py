import functools
import itertools
import operator
from typing import Dict, Generator, List, Tuple

from solutions.day10 import helpers


def line_of_sight(
    lines_of_sight: List[List[complex]], max_edge_distance: int
) -> Generator[complex, None, None]:
    """Yield coprime coordinates that fall within the grid from the perspective of the astroid."""
    for row in lines_of_sight:
        for point in row:
            if not point.imag < max_edge_distance:
                return
            if not point.real < max_edge_distance:
                break
            yield point


def point_in_range(point: complex, grid_size: int) -> bool:
    """Check if a coordinate is still in range of the grid."""
    return 0 <= point.real < grid_size and 0 <= point.imag < grid_size


def distance_to_edge(coordinate, grid_size):
    """Calculate the maximum distance to the edge for this coordinate."""
    half_point = (grid_size + 1) / 2
    return int(round(abs(coordinate - half_point + 1) + half_point, 0))


def part_one(
    data: List[int], asteroids: Dict[complex, int], lines_of_sight: List[List[complex]]
) -> int:
    """
    Calculate the number of astroids each astroid can see.

    In each line of sight, the first possible integer, integer coordinate is a coprime. That's why I
    iterate over each coprime coordinate in range relative to each asteroid and extend that line of
    sight until I go out of bounds or find an astroid.
    """
    grid_size = len(data)

    # Since the grid size is constant, create partial functions to lessen the visual noise later
    to_edge = functools.partial(distance_to_edge, grid_size=grid_size)
    in_range = functools.partial(point_in_range, grid_size=grid_size)

    # Instantiate `i`, the square root of -1
    im = complex(0, 1)

    # Iterate over all astroids
    for asteroid in asteroids:
        # Calculate the maximum distance to one of the edges, we can use this later to minimize the
        # number of steps we take while checking each line of sight.
        edge = max(to_edge(asteroid.real), to_edge(asteroid.imag))
        visible_astroids = 0

        # Since the lines of sight have rotational symmetry, I've only calculated the coprimes in a
        # single quadrant (x ∊ {0, 1, ..., len(grid)}, y ∊ {0, 1, ..., len(grid)}). Since I use
        # complex numbers to represent the coordinates (x = real part, y = imaginary part), we can
        # then simply rotate this quadrant by multiplying it by powers of `i` (sqrt(-1)).
        for coprime, rotation in itertools.product(line_of_sight(lines_of_sight, edge), range(4)):
            # `a` represents the number of coprime steps taken
            a = 1

            # Check each rational coordiante in this line of sight until we hit an astroid or go out
            # of bounds.
            while in_range(c := asteroid + a * im**rotation * coprime):  # noqa: E203, E231
                if c in asteroids:
                    visible_astroids += 1
                    break
                # If we haven't found an astroid, take another step along the line and try again.
                a += 1
        asteroids[asteroid] = visible_astroids
        visible_astroids = 0

    return max(asteroids.items(), key=operator.itemgetter(1))


def part_two(
    data: List[int],
    asteroids: Dict[complex, int],
    lines_of_sight: List[List[complex]],
    coordinate: complex,
) -> int:
    """
    Calculate the 200th asteroid we'll vaporize using our laser.

    The method I'm using is by rotating around the asteroid exactly once, looking for asteroids in
    each line of sight we encounter. If we find a second astroid in a line of sight, we know that it
    will only be distroyed during the next rotation. Since `lines_of_sight` only contains lines for
    one quadrant, we know that we can destroy at most 4*len(lines) in one rotation. We can use that
    fact to assign guaranteed increasing scores that indicate the order in which astroids will be
    vaporized.
    """
    grid_size = len(data)
    in_range = functools.partial(point_in_range, grid_size=grid_size)

    # Define `i`
    im = complex(0, 1)

    # Sort all lines of sight by their angle (using their gradient factor)
    lines = sorted(itertools.chain.from_iterable(lines_of_sight), key=lambda c: c.imag / c.real)

    # Keep track of destroyed stars with their rank order score
    destroyed = {}
    # We start at rotation 3, since our laser points upwards at the start
    for i, rotation in enumerate((3, 0, 1, 2)):
        for j, line in enumerate(lines):
            # Again, keep track of the number of coprime steps in each line of sight.
            a = 1

            # Keep track of how many astroids we encounter in this line of sight
            n = 0
            while in_range(c := coordinate + a * im**rotation * line):  # noqa: E203, E231
                if c in asteroids:
                    # If we find an asteroid in this line of sight, give it a score to indicate the
                    # order in which it will be destroyed in the laser operation based on the line
                    # of sight it's in and how many other asteroids we've already seen in this line
                    # of sight.
                    destroyed[c] = i * len(lines) + j + n * 4 * len(lines)
                    n += 1
                # Increase the coprime step in this line of sight.
                a += 1

    asteroid = sorted(destroyed.items(), key=operator.itemgetter(1))[199][0]
    return int(asteroid.real * 100 + asteroid.imag)


def main(data: List[str]) -> Tuple[int]:
    """The main function taking care of parsing the input data and running the solutions."""
    data = [line.strip() for line in data]

    lines_of_sight = helpers.lines_of_sight(len(data[0]), len(data))

    asteroids = {}
    for y, row in enumerate(data):
        for x, cell in enumerate(row):
            if cell == "#":
                asteroids[complex(x, y)] = 0

    coordinate, answer_one = part_one(data, asteroids, lines_of_sight)
    answer_two = part_two(asteroids, asteroids, lines_of_sight, coordinate)
    return answer_one, answer_two

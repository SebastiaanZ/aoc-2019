import collections
import operator
from typing import List, Tuple


def branch_off(seed: complex) -> Tuple[complex, complex, complex]:
    """Create branches for each coprime node in the tree."""
    branch_one = complex(2 * seed.real - seed.imag, seed.real)
    branch_two = complex(2 * seed.real + seed.imag, seed.real)
    branch_three = complex(seed.real + 2 * seed.imag, seed.imag)
    return branch_one, branch_two, branch_three


def reflect(coordinate: complex) -> complex:
    """Reflect the coordinate on the `y=x` diagonal."""
    return complex(coordinate.imag, coordinate.real)


def lines_of_sight(width, height) -> List[List[complex]]:
    """
    Generate the first visible lattice point in each line of sight that falls within the grid.

    The coordinates are represented by a complex number, with the imaginary axis conceptualized as
    the vertical axis.
    """
    visible_lattice_points = [[] for _ in range(height)]

    seeds = collections.deque((complex(2, 1), complex(3, 1)))

    while seeds:
        for branch in branch_off(seeds.popleft()):
            if branch.real < width and branch.imag < height:
                # Add branch to the lattice of visible points
                visible_lattice_points[int(branch.imag)].append(branch)

                # Add its reflection along x=y line as well
                reflection = reflect(branch)
                visible_lattice_points[int(reflection.imag)].append(reflection)

                # Add the current branch as seed for the next iteration of branching
                seeds.append(branch)

    # Add (1, 1) and the seeds/their reflections. Very manual, but it works.
    visible_lattice_points[0].append(complex(1, 0))
    visible_lattice_points[1].append(complex(1, 1))
    visible_lattice_points[1].append(complex(2, 1))
    visible_lattice_points[2].append(complex(1, 2))
    visible_lattice_points[1].append(complex(3, 1))
    visible_lattice_points[3].append(complex(1, 3))

    return [sorted(row, key=operator.attrgetter('real')) for row in visible_lattice_points]


if __name__ == "__main__":
    for i, row in enumerate(lines_of_sight(10, 10)):
        print(f"{i:0>2}", row)

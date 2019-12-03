from __future__ import annotations

import collections
import enum
from typing import List, NamedTuple, Optional, Tuple


class Orientation(enum.IntEnum):
    VERTICAL = 0
    HORIZONTAL = 1


Move = collections.namedtuple("Move", ("direction", "distance"))
Intersection = collections.namedtuple("Intersection", "location steps")

MOVEMENT = {
    "U": lambda start, dist: Point(start.x, start.y + dist),
    "R": lambda start, dist: Point(start.x + dist, start.y),
    "D": lambda start, dist: Point(start.x, start.y - dist),
    "L": lambda start, dist: Point(start.x - dist, start.y),
}


class Point(NamedTuple):
    x: int
    y: int

    def __sub__(self, other: Point) -> Point:
        """Subtract `other` from `self`."""
        return Point(self.x - other.x, self.y - other.y)

    def __matmul__(self, other: Point) -> int:
        """Calculate the cityblock distance between `self` and `other`."""
        return abs(self.x - other.x) + abs(self.y - other.y)

    def __eq__(self, other: Point) -> bool:
        """Compare if `self` is equal to `other` by comparing coordinates."""
        return self.x == other.x and self.y == other.y


class Line:
    def __init__(self, start: Point, end: Point, steps: int):
        self.start = start
        self.end = end
        self.orientation = Orientation.HORIZONTAL if start.y == end.y else Orientation.VERTICAL
        self.steps = steps

    def intersection(self, other: Line) -> Optional[Intersection]:
        """Return the intersection with `other` if it exists; otherwiser return `None`."""
        if self.orientation == other.orientation:
            return

        start_diff = self.start - other.start
        end_diff = self.end - other.end

        if start_diff.x * end_diff.x <= 0 and start_diff.y * end_diff.y <= 0:
            if self.orientation == Orientation.VERTICAL:
                location = Point(self.start.x, other.start.y)
            else:
                location = Point(other.start.x, self.start.y)

            return Intersection(
                location,
                self.steps + (self.start @ location) + other.steps + (other.start @ location),
            )

    def __repr__(self) -> str:
        """Create internal representation of the object."""
        return f"Line(start={self.start}, end={self.end}, start_steps={self.start_steps}"


def draw_lines(wire: List[str]) -> List[Line]:
    """Create the line segments that make up a wire."""
    moves = [Move(direction, int(''.join(distance))) for direction, *distance in wire.split(',')]

    location = Point(0, 0)
    steps = 0
    lines = []
    for move in moves:
        new_location = MOVEMENT[move.direction](location, move.distance)
        lines.append(Line(location, new_location, steps))
        steps += move.distance
        location = new_location

    return lines


def find_intersections(data: List[List[Line]]) -> List[Intersection]:
    """Find the intersections between line segments in both lists."""
    wire_one, wire_two = data
    origin = Point(0, 0)
    intersections = [
        intersection for a in wire_one for b in wire_two
        if (intersection := a.intersection(b)) and intersection.location != origin  # noqa
    ]
    return intersections


def part_one(intersections: List[Intersection]) -> int:
    """Find the intersection closest the origin in terms of the Manhattan distance."""
    origin = Point(0, 0)
    return min(i.location @ origin for i in intersections)


def part_two(intersections: List[Intersection]) -> int:
    """Find the intersection closest to the origin in terms of the number of steps taken."""
    return min(i.steps for i in intersections)


def main(data: List[str]) -> Tuple[int]:
    """The main function taking care of parsing the input data and running the solutions."""
    data = [draw_lines(wire) for wire in data]
    intersections = find_intersections(data)

    answer_one = part_one(intersections)
    answer_two = part_two(intersections)

    return answer_one, answer_two

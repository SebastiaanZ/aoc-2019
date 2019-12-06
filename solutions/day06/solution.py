from __future__ import annotations

from operator import attrgetter
from typing import Iterator, List, Tuple


class Node:
    """An orbital node used the OrbitalMap."""

    __slots__ = ["name", "parent", "_depth", "_ancestors"]

    def __init__(self, name: str):
        self.name = name
        self.parent = None
        self._depth = None
        self._ancestors = None

    def __repr__(self) -> str:
        """Return a developer-friendly representation of the node."""
        cls = self.__class__
        return f"{cls.name}(name={self.name!r})"

    def __hash__(self) -> int:
        """Hash the node using its name."""
        return hash(self.name)

    @property
    def depth(self) -> int:
        """Calculate the distance from this node to the Central Orbital Mass."""
        if self._depth is None:
            if self.parent:
                self._depth = self.parent.depth + 1
            else:
                self._depth = 0

        return self._depth

    @property
    def ancestors(self) -> List[Node]:
        """List all the ancestors of the node."""
        if self._ancestors is None:
            self._ancestors = []
            node = self
            while (node := node.parent):  # noqa: E203, E231
                self._ancestors.append(node)
        return self._ancestors


class OrbitalMap:
    """A map of all known orbits, including my orbit and Santa's orbit."""

    def __init__(self):
        self.nodes = {}

    def __iter__(self) -> Iterator[Node]:
        """Return an iterator over all orbital nodes in the map."""
        return iter(self.nodes.values())

    def __getitem__(self, key: str) -> Node:
        """Get a specific node from the orbital map using its name."""
        return self.nodes[key]

    def add_orbit(self, parent, child):
        """Register an orbit of `child` around `parent`, creating the nodes if they are new."""
        parent = self.nodes.setdefault(parent, Node(name=parent))
        child = self.nodes.setdefault(child, Node(name=parent))
        child.parent = parent


def part_one(orbital_map) -> int:
    """Compute the total number of direct and indirect orbits in the orbital map."""
    return sum(node.depth for node in orbital_map)


def part_two(orbital_map) -> int:
    """Compute the number of orbital transfers needed to get to Santa."""
    me = orbital_map["YOU"]
    santa = orbital_map["SAN"]
    common_ancestor = max(
        set(me.ancestors).intersection(santa.ancestors),
        key=attrgetter("depth")
    )
    return (me.depth - common_ancestor.depth) + (santa.depth - common_ancestor.depth) - 2


def main(data: List[str]) -> Tuple[int]:
    """Run my solution to day 6 of the Advent of Code."""
    orbital_map = OrbitalMap()
    for orbit in data:
        orbital_map.add_orbit(*orbit.split(")"))

    answer_one = part_one(orbital_map)
    answer_two = part_two(orbital_map)
    return answer_one, answer_two

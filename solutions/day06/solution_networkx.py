from typing import List, Tuple

import networkx as nx


def part_one(orbits: nx.Graph) -> int:
    """Compute the total number of direct and indirect orbits in the orbital map."""
    return sum(nx.shortest_path_length(orbits, source="COM").values())


def part_two(orbits: nx.Graph) -> int:
    """Compute the number of orbital transfers needed to get to Santa."""
    return nx.shortest_path_length(orbits, source="YOU", target="SAN") - 2


def main(data: List[str]) -> Tuple[int, int]:
    """Run my solution to day 6 of the Advent of Code."""
    orbits = nx.Graph()
    orbits.add_edges_from([number.split(")") for number in data])
    answer_one = part_one(orbits)
    answer_two = part_two(orbits)
    return answer_one, answer_two

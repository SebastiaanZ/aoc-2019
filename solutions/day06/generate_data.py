import collections
import itertools
import random
from string import ascii_letters, digits


Node = collections.namedtuple("Node", ["name", "child_count"])


def random_node(max_children):
    """Generate nodes with a random name and a random number of children."""
    characters = list(ascii_letters + digits)
    random.shuffle(characters)
    names = itertools.product(characters, repeat=3)

    for name in names:
        name = "".join(name)
        if name in ("COM", "YOU", "SAN"):
            continue
        yield Node(name=name, child_count=random.randint(1, max_children))


def random_tree(max_edges=40, max_children=4):
    """Creates a tree graph with a maximum number of edges in total and children per node."""
    tree = collections.deque()
    tree.append(Node("COM", 1))

    edges = []

    node_generator = random_node(max_children=max_children)

    while True:
        parent = tree.popleft()
        for _ in range(parent.child_count):
            child = next(node_generator)
            edges.append(f"{parent.name}){child.name}")
            tree.append(child)

            if len(edges) >= max_edges - 2:
                _, parent_you = random.choice(edges).split(")")
                _, parent_san = random.choice(edges).split(")")
                edges.append(f"{parent_you})YOU")
                edges.append(f"{parent_san})SAN")
                random.shuffle(edges)
                return edges

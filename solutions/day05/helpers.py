import dataclasses
import functools
import operator
from typing import Callable, Iterator, List


@dataclasses.dataclass
class System:
    """A class for represeting my ship's internal terminal system."""

    application: List[int]
    stdin: Iterator
    stdout: List[int] = dataclasses.field(default_factory=list)
    _pointer: int = 0

    def __next__(self):
        """Get the next operation code and increment the application pointer."""
        operation = self.application[self.pointer]
        if str(operation) == "99":
            raise StopIteration

        self.pointer += 1
        return operation

    def __iter__(self):
        """Return `self` as System implements the iterator protocol."""
        return self

    def __getitem__(self, mode):
        """Get the application code based on the mode of the get operation."""
        if mode == "0":
            return self.application[next(self)]

        return next(self)

    @property
    def pointer(self):
        """Public interface for accessing the application pointer."""
        return self._pointer

    @pointer.setter
    def pointer(self, new_pointer):
        """Public interface for setting the application pointer that validates the value."""
        if new_pointer < 0 or new_pointer >= len(self.application):
            raise IndexError(f"Pointer {new_pointer} not in range of application.")
        self._pointer = new_pointer


def math_operation(system: System, modes: str, operation: Callable) -> None:
    """Perform a mathematical operation that mutates the `system`'s application state."""
    a = system[modes[-1]]
    b = system[modes[-2]]
    system.application[next(system)] = operation(a, b)


def jump_operation(system: System, modes: str, operation: Callable) -> None:
    """Jump to another point in the `system`'s application if a certain condition holds."""
    if operation(system[modes[-1]], 0):
        system.pointer = system[modes[-2]]
    else:
        next(system)


def logic_operation(system: System, modes: str, operation: Callable) -> None:
    """Store the result of a logical comparison at a certain location in the application."""
    if operation(system[modes[-1]], system[modes[-2]]):
        system.application[next(system)] = 1
    else:
        system.application[next(system)] = 0


def read_input(system: System, modes: str) -> None:
    """Read an input value from `System.stdin`."""
    system.application[next(system)] = next(system.stdin)


def put_output(system: System, modes: str) -> None:
    """Append output to `System.stdout`."""
    system.stdout.append(system.application[next(system)])


OPERATIONS = {
    "01": functools.partial(math_operation, operation=operator.add),
    "02": functools.partial(math_operation, operation=operator.mul),
    "03": read_input,
    "04": put_output,
    "05": functools.partial(jump_operation, operation=operator.ne),
    "06": functools.partial(jump_operation, operation=operator.eq),
    "07": functools.partial(logic_operation, operation=operator.lt),
    "08": functools.partial(logic_operation, operation=operator.eq),
}


def terminal(system: System) -> System:
    """The Thermal Environment Supervision Terminal of my space ship."""

    for opcode in system:  # noqa: E203, E231
        opcode = str(opcode)
        operation = f"{opcode[-2:]:0>2}"
        modes = f"{opcode[:-2]:0>3}"
        OPERATIONS[operation](
            modes=modes,
            system=system
        )

    return system

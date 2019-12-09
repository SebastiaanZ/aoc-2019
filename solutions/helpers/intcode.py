from __future__ import annotations

import collections
import functools
import logging
import operator
import queue
from typing import Callable, List, Optional

log = logging.getLogger(__name__)


class IntCodeApplication:
    """A class for representing my ship's internal terminal system."""

    def __init__(
        self,
        application: List[int],
        stdin: Optional[queue.SimpleQueue[int]] = None,
        stdout: Optional[queue.SimpleQueue[int]] = None,
        name: str = "",
        flexible_memory: bool = False,
    ) -> None:
        if flexible_memory:
            # Use a defaultdict if we need an extendable application memory
            self.application = collections.defaultdict(int, enumerate(application))
        else:
            # Otherwise, use a simple list
            self.application = list(application)

        self.stdin = stdin if stdin is not None else queue.SimpleQueue()
        self.stdout = stdout if stdout is not None else queue.SimpleQueue()
        self.name = name

        self._pointer: int = 0
        self.relative_base = 0

        self.operations = {
            "01": self.addition,
            "02": self.multiplication,
            "03": self.get_input,
            "04": self.put_output,
            "05": self.jump_true,
            "06": self.jump_false,
            "07": self.logical_lt,
            "08": self.logical_eq,
            "09": self.change_relative_base,
        }

    def __next__(self) -> int:
        """Get the next operation code and increment the application pointer."""
        operation = self.application[self.pointer]
        if operation == 99:
            raise StopIteration

        self.pointer += 1
        return operation

    def __iter__(self) -> IntCodeApplication:
        """Return `self` as System implements the iterator protocol."""
        return self

    def __hash__(self) -> int:
        """Create a hash of the entire state of the application."""
        return hash(tuple(self.application))

    def process_opcode(self, opcode: int) -> Tuple[str, str]:
        """Process the opcode by padding it with zeros and returning the modes and instruction."""
        opcode = f"{opcode:0>5}"
        return opcode[-2:], opcode[:-2]

    def run(self) -> None:
        """Run the IntCodeApplication until it halts."""
        for opcode in self:
            operation, modes = self.process_opcode(opcode)
            self.operations[operation](modes=modes)

    def read(self, mode: str) -> int:
        """Get the application code based on the mode of the get operation."""
        if mode == "0":
            return self.application[next(self)]

        if mode == "2":
            return self.application[self.relative_base + next(self)]

        return next(self)

    def write(self, mode: str, value: int) -> None:
        """Write `value` to the application's memory, taking relative pointers into account."""
        pointer = next(self)
        if mode == "2":
            pointer += self.relative_base
        self.application[pointer] = value

    @property
    def pointer(self) -> int:
        """Public interface for accessing the application pointer."""
        return self._pointer

    @pointer.setter
    def pointer(self, new_pointer: int) -> None:
        """Public interface for setting the application pointer that validates the value."""
        if new_pointer < 0:
            raise IndexError(f"The application pointer {new_pointer} cannot be negative.")
        self._pointer = new_pointer

    def math_operation(self, modes: str, operation: Callable) -> None:
        """Perform a mathematical operation that mutates the `self`'s application state."""
        a = self.read(modes[-1])
        b = self.read(modes[-2])
        self.write(modes[-3], operation(a, b))

    def jump_operation(self, modes: str, operation: Callable) -> None:
        """Jump to another point in the `self`'s application if a certain condition holds."""
        if operation(self.read(modes[-1]), 0):
            self.pointer = self.read(modes[-2])
        else:
            next(self)

    def logic_operation(self, modes: str, operation: Callable) -> None:
        """Store the result of a logical comparison at a certain location in the application."""
        if operation(self.read(modes[-1]), self.read(modes[-2])):
            self.write(modes[-3], 1)
        else:
            self.write(modes[-3], 0)

    def get_input(self, modes: str) -> None:
        """Read a value from `self.stdin`."""
        self.write(modes[-1], self.stdin.get())

    def put_output(self, modes: str) -> None:
        """Write a value to `self.stdout`."""
        self.stdout.put(self.read(modes[-1]))

    def change_relative_base(self, modes: str) -> None:
        """Change the base of the relative pointers."""
        self.relative_base += self.read(modes[-1])

    addition = functools.partialmethod(math_operation, operation=operator.add)
    multiplication = functools.partialmethod(math_operation, operation=operator.mul)
    jump_true = functools.partialmethod(jump_operation, operation=operator.ne)
    jump_false = functools.partialmethod(jump_operation, operation=operator.eq)
    logical_lt = functools.partialmethod(logic_operation, operation=operator.lt)
    logical_eq = functools.partialmethod(logic_operation, operation=operator.eq)

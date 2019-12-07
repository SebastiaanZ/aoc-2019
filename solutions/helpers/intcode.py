from __future__ import annotations


import functools
import logging
import operator
import queue
from typing import Callable, List, Optional

log = logging.getLogger(__name__)


class IntCodeApplication:
    """A class for represeting my ship's internal terminal system."""

    def __init__(
        self,
        application: List[int],
        stdin: Optional[queue.SimpleQueue[int]] = None,
        stdout: Optional[queue.SimpleQueue[int]] = None,
        name: str = "",
    ) -> None:
        self.application = list(application)
        self.stdin = stdin if stdin is not None else queue.SimpleQueue()
        self.stdout = stdout if stdout is not None else queue.SimpleQueue()
        self.name = name
        self._pointer: int = 0

        log.debug(f"{self.name} stdin: {id(self.stdin)} stdout: {id(self.stdout)}")

        self.operations = {
            "01": self.addition,
            "02": self.multiplication,
            "03": self.get_input,
            "04": self.put_output,
            "05": self.jump_true,
            "06": self.jump_false,
            "07": self.logical_lt,
            "08": self.logical_eq,
        }

    def __next__(self) -> int:
        """Get the next operation code and increment the application pointer."""
        operation = self.application[self.pointer]
        if str(operation) == "99":
            raise StopIteration

        self.pointer += 1
        return operation

    def __iter__(self) -> IntCodeApplication:
        """Return `self` as System implements the iterator protocol."""
        return self

    def __hash__(self) -> int:
        return hash(tuple(self.application))

    def run(self) -> None:
        for opcode in self:
            opcode = str(opcode)
            operation = f"{opcode[-2:]:0>2}"
            modes = f"{opcode[:-2]:0>3}"
            self.operations[operation](
                modes=modes,
            )

    def read(self, mode: str) -> int:
        """Get the application code based on the mode of the get operation."""
        if mode == "0":
            return self.application[next(self)]

        return next(self)

    @property
    def pointer(self) -> int:
        """Public interface for accessing the application pointer."""
        return self._pointer

    @pointer.setter
    def pointer(self, new_pointer: int) -> None:
        """Public interface for setting the application pointer that validates the value."""
        if new_pointer < 0 or new_pointer >= len(self.application):
            raise IndexError(f"Pointer {new_pointer} not in range of the application.")
        self._pointer = new_pointer

    def math_operation(self, modes: str, operation: Callable) -> None:
        """Perform a mathematical operation that mutates the `self`'s application state."""
        a = self.read(modes[-1])
        b = self.read(modes[-2])
        self.application[next(self)] = operation(a, b)

    def jump_operation(self, modes: str, operation: Callable) -> None:
        """Jump to another point in the `self`'s application if a certain condition holds."""
        if operation(self.read(modes[-1]), 0):
            self.pointer = self.read(modes[-2])
        else:
            next(self)

    def logic_operation(self, modes: str, operation: Callable) -> None:
        """Store the result of a logical comparison at a certain location in the application."""
        if operation(self.read(modes[-1]), self.read(modes[-2])):
            self.application[next(self)] = 1
        else:
            self.application[next(self)] = 0

    def get_input(self, modes: str) -> None:
        """Read a value from `self.stdin`."""
        log.debug(f"[{self.name}] Reading input")
        self.application[next(self)] = self.stdin.get()
        log.debug(f"[{self.name}] Got input!")

    def put_output(self, modes: str) -> None:
        """Write a value to `self.stdout`."""
        log.debug(f"[{self.name}] Writing output")
        self.stdout.put(self.application[next(self)])
        log.debug(f"[{self.name}] Wrote output!")

    addition = functools.partialmethod(math_operation, operation=operator.add)
    multiplication = functools.partialmethod(math_operation, operation=operator.mul)
    jump_true = functools.partialmethod(jump_operation, operation=operator.ne)
    jump_false = functools.partialmethod(jump_operation, operation=operator.eq)
    logical_lt = functools.partialmethod(logic_operation, operation=operator.lt)
    logical_eq = functools.partialmethod(logic_operation, operation=operator.eq)

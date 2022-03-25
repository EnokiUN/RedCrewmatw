from __future__ import annotations
from typing import Callable, Optional, Awaitable

class CommandNotFound(Exception):
    """
    An exception that is raised when a command is not found.

    Attributes
    ----------
    command: :class:`str`
        The name of the command that was not found.
    """
    def __init__(self, command: str):
        self.command = command

    def __str__(self):
        return f"Command {self.command} not found"

class NotEnoughArgs(Exception):
    """
    An exception that is raised when not enough args are supplied.

    Attributes
    ----------
    command: :class:`Command`
        The command that was being called.
    expected: :class:`int`
        The number of args that were expected.
    actual: :class:`int`
        The number of args that were actually supplied.
    """
    def __init__(self, command: Command, expected: int, actual: int):
        self.command = command
        self.expected = expected
        self.actual = actual

    def __str__(self):
        return f"{self.command.name} expected {self.expected} args, got {self.actual}"

class CommandContext:
    pass

class Command:
    pass

class Cog:
    pass

class CommandsCLient:
    pass

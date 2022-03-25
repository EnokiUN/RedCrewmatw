from __future__ import annotations
from typing import Callable, Optional, Awaitable, Any

import voltage

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
    """
    A context for a command.

    Attributes
    ----------
    message: :class:`voltage.Message`
        The message that invoked the command.
    content: :class:`str`
        The content of the message that invoked the command.
    author: Union[:class:`voltage.User`, :class:`voltage.Member`]
        The author of the message that invoked the command.
    channel: :class:`voltage.Channel`
        The channel that the command was invoked in.
    server: :class:`voltage.Server`
        The server that the command was invoked in.
    command: :class:`Command`
        The command that was invoked.
    """
    __slots__ = ('message', 'content', 'author', 'channel', 'server', 'send', 'reply', 'delete', 'command')

    def __init__(self, message: voltage.Message, command: Command):
        self.message = message
        self.content = message.content
        self.author = message.author
        self.channel = message.channel
        self.server = message.server
        self.send = message.channel.send
        self.reply = message.reply
        self.delete = message.delete
        self.command = command

class Command:
    """
    A class representing a command.

    Attributes
    ----------
    name: :class:`str`
        The name of the command.
    description: Optional[:class:`str`]
        The description of the command.
    aliases: Optional[List[:class:`str`]]
        The aliases of the command.
    """
    def __init__(self, func: Callable[..., Awaitable[Any]], name: Optional[str] = None, description: Optional[str] = None, aliases: Optional[list[str]] = None):
        self.func = func
        self.name = name or func.__name__
        self.description = description or func.__doc__
        self.aliases = aliases or [self.name]
        self.error_handler = None

    def error(self, func: Callable[[Exception, CommandContext], Awaitable[Any]]):
        """
        Sets the error handler for this command.

        Parameters
        ----------
        func: :class:`Callable[[Exception, CommandContext], Awaitable[Any]]`
            The function to call when an error occurs.
        """
        self.error_handler = func
        return self

    def invoke(self, context: CommandContext, prefix: str):
        pass

class Cog:
    def __init__(self, name: str, description: Optional[str] = None):
        self.name = name
        self.description = description
        self.commands: list[Command] = [] 

    def add_command(self, command: Command):
        """
        Adds a command to the cog.
        
        idk why you're doing thit but consider using the decorator for this /shrug.

        Parameters
        ----------
        command: :class:`Command`
            The command to add.
        """
        self.commands.append(command)

    def command(self, name: Optional[str], description: Optional[str] = None, aliases: Optional[list[str]] = None):
        """
        A decorator for adding commands to the cog.

        Parameters
        ----------
        name: Optional[:class:`str`]
            The name of the command.
        description: Optional[:class:`str`]
            The description of the command.
        aliases: Optional[List[:class:`str`]]
            The aliases of the command.
        """
        def decorator(func: Callable[..., Awaitable[Any]]):
            command = Command(func, name, description, aliases)
            self.add_command(command)
            return command
        return decorator

class CommandsCLient:
    pass

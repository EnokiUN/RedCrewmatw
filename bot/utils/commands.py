from __future__ import annotations
from typing import Callable, Optional, Awaitable, Any, Union
from types import ModuleType
from inspect import signature, Parameter, _empty
from shlex import split
from itertools import zip_longest
from importlib import import_module, reload

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
    __slots__ = ('message', 'content', 'author', 'channel', 'server', 'send', 'reply', 'delete', 'command', 'me')

    def __init__(self, message: voltage.Message, command: Command, client: voltage.Client):
        self.message = message
        self.content = message.content
        self.author = message.author
        self.channel = message.channel
        self.server = message.server
        self.send = message.channel.send # type: ignore
        self.reply = message.reply
        self.delete = message.delete
        self.command = command
        self.me = client

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
    __slots__ = ('func', 'name', 'description', 'aliases', 'error_handler', 'signature', 'cog')

    def __init__(self, func: Callable[..., Awaitable[Any]], name: Optional[str] = None, description: Optional[str] = None, aliases: Optional[list[str]] = None, cog: Optional[Cog] = None):
        self.func = func
        self.name = name or func.__name__
        self.description = description or func.__doc__
        self.aliases = aliases or [self.name]
        self.error_handler = None
        self.signature = signature(func)
        self.cog = cog

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

    async def convert_arg(self, arg: Parameter, given: str, context: CommandContext) -> Any:
        if arg.annotation is _empty or arg.annotation is Any or issubclass(arg.annotation, str):
            return given
        elif issubclass(arg.annotation, int):
            return int(given)
        elif issubclass(arg.annotation, float):
            return float(given)
        elif issubclass(arg.annotation, voltage.User):
            return context.me.get_user(given)
        elif issubclass(arg.annotation, voltage.Member):
            return context.server.get_member(given) # type: ignore

    async def invoke(self, context: CommandContext, prefix: str):
        if len(( params := self.signature.parameters )) > 1:
            given = split(context.content[len(prefix+self.name):])
            args = []
            kwargs = {}

            for i, (param, arg) in enumerate(zip_longest(list(params.items())[1:], given)):
                if param is None:
                    break
                name, data = param

                if data.kind == data.VAR_POSITIONAL or data.kind == data.POSITIONAL_OR_KEYWORD:
                    if arg is None:
                        if data.default is _empty:
                            raise NotEnoughArgs(self, len(params)-1, len(args))
                        arg = data.default
                    args.append(await self.convert_arg(data, arg, context))

                elif data.kind == data.KEYWORD_ONLY:
                    if i == len(params) - 2:
                        if arg is None:
                            if data.default is _empty:
                                raise NotEnoughArgs(self, len(params)-1, len(given))
                            kwargs[name] = await self.convert_arg(data, data.default, context)
                            break
                        kwargs[name] = await self.convert_arg(data, " ".join(given[i:]), context)
                    else:
                        if arg is None:
                            if data.default is _empty:
                                raise NotEnoughArgs(self, len(params)-1, len(given))
                            arg = data.default
                        kwargs[name] = await self.convert_arg(data, arg, context)

            if self.error_handler:
                try:
                    return await self.func(context, *args, **kwargs)
                except Exception as e:
                    return await self.error_handler(e, context)
            return await self.func(context, *args, **kwargs)
        if self.error_handler:
            try:
                return await self.func(context)
            except Exception as e:
                return await self.error_handler(e, context)
        return await self.func(context)
        

class Cog:
    """
    A class representing a cog.

    Attributes
    ----------
    name: :class:`str`
        The name of the cog.
    description: Optional[:class:`str`]
        The description of the cog.
    commands: List[:class:`Command`]
        The commands in the cog.
    """
    __slots__ = ('name', 'description', 'commands')

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

    def command(self, name: Optional[str] = None, description: Optional[str] = None, aliases: Optional[list[str]] = None):
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
            command = Command(func, name, description, aliases, self)
            self.add_command(command)
            return command
        return decorator

class CommandsClient(voltage.Client):
    """
    A class representing a client that uses commands.

    Attributes
    ----------
    cogs: List[:class:`Cog`]
        The cogs that are loaded.
    """
    def __init__(self, prefix: Union[str, list[str], Callable[[voltage.Message], Awaitable[Any]]]):
        super().__init__()
        self.listeners = {"message": self.handle_commands}
        self.prefix = prefix
        self.cogs: dict[str, Cog] = {}
        self.extensions: dict[str, ModuleType] = {}
        self.commands: dict[str, Command] = {}

    async def get_prefix(self, message: voltage.Message, prefix: Union[str, list[str], Callable[[voltage.Message], Awaitable[Any]]]) -> str:
        if isinstance(prefix, str):
            return prefix
        elif isinstance(prefix, list):
            for p in prefix:
                if message.content.startswith(p):
                    return p
        elif isinstance(prefix, Callable):
            return await self.get_prefix(message, await prefix(message))
        return str(prefix)

    def add_command(self, command: Command):
        """
        Adds a command to the client.

        Parameters
        ----------
        command: :class:`Command`
            The command to add.
        """
        for alias in command.aliases:
            self.commands[alias] = command

    def add_cog(self, cog: Cog):
        """
        Adds a cog to the client.

        Parameters
        ----------
        cog: :class:`Cog`
            The cog to add.
        """
        self.cogs[cog.name] = cog
        for command in cog.commands:
            self.add_command(command)

    def add_extension(self, path: str, *args, **kwargs):
        """
        Adds an extension to the client.

        Parameters
        ----------
        path: :class:`str`
            The path to the extension as a python dotpath.
        """
        module = import_module(path)
        self.extensions[path] = module
        if not hasattr(module, "setup"):
            raise AttributeError("Extension {} does not have a setup function.".format(path))
        self.add_cog(module.setup(self, *args, **kwargs))

    def reload_extension(self, path: str):
        """
        Reloads an extension.

        Parameters
        ----------
        path: :class:`str`
            The path to the extension as a python dotpath.
        """
        module = self.extensions.get(path)
        if module is None:
            raise KeyError("Extension {} does not exist.".format(path))
        reload(module)
        for i in self.commands:
            print(self.commands)
            if self.commands[i].cog == module:
                del self.commands[i]
            print(self.commands)
        if not hasattr(module, "setup"):
            raise AttributeError("Extension {} does not have a setup function.".format(path))
        self.add_cog(module.setup(self))

    def remove_extension(self, path: str):
        """
        removes an extension.

        Parameters
        ----------
        path: :class:`str`
            The path to the extension as a python dotpath.
        """
        module = self.extensions.get(path)
        if module is None:
            raise KeyError("Extension {} does not exist.".format(path))
        for i in self.commands:
            if self.commands[i].cog == module:
                del self.commands[i]
        del self.cogs[path]
        del self.extensions[path]

    def command(self, name: Optional[str] = None, description: Optional[str] = None, aliases: Optional[list[str]] = None):
        """
        A decorator for adding commands to the client.

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

    async def handle_commands(self, message: voltage.Message):
        prefix = await self.get_prefix(message, self.prefix)
        if message.content.startswith(prefix):
            content = message.content[len(prefix):]
            command = content.split(" ")[0]
            if command in self.commands:
                if "command" in self.error_handlers:
                    try:
                        return await self.commands[command].invoke(CommandContext(message, self.commands[command], self), prefix)
                    except Exception as e:
                        return await self.error_handlers["command"](e, CommandContext(message, self.commands[command], self))
                return await self.commands[command].invoke(CommandContext(message, self.commands[command], self), prefix)
            raise CommandNotFound(command)

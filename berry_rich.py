from rich.console import Console, ConsoleOptions, RenderResult
from .berry import Berry


def __rich__(self) -> str:
    return f"[bold cyan]{self}"


def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
    yield f"[bold red]{self}"


def install():
    Berry.__rich__ = __rich__
    Berry.__rich_console__ = __rich_console__

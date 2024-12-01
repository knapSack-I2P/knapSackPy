from rich import print
from rich.console import Console


def _initialize():
    global _rich_console
    _rich_console = Console()


try:
    console = _rich_console
    print = print
except NameError:
    _initialize()
    console = _rich_console
    print = print

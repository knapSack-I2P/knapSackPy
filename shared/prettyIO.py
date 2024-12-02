import rich
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.text import Text


class IO:
    def __init__(self):
        self.console = Console()
        self.live = Live()

    def print(self, *args, **kwargs):
        ...

    def update(self):
        ...


def _initialize():
    global io
    io = IO()


try:
    io
except NameError:
    _initialize()
finally:
    console = io.console
    print = io.print
    update = io.update

server_tag = '[bold frame]kSk_SERVER[/bold frame] '


def server_print(*args, **kwargs):
    console.print(server_tag, *[str(arg).replace('\n', '\n' + server_tag) for arg in args])


client_tag = '[bold frame]kSk_CLIENT[/bold frame] '


def client_print(*args, **kwargs):
    console.print(client_tag, *[str(arg).replace('\n', '\n' + client_tag) for arg in args])

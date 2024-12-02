
server_tag = '[bold frame]kSk_SERVER[/bold frame] '


def server_print(*args, **kwargs):
    print(server_tag, *[str(arg).replace('\n', '\n' + server_tag) for arg in args])


client_tag = '[bold frame]kSk_CLIENT[/bold frame] '


def client_print(*args, **kwargs):
    print(client_tag, *[str(arg).replace('\n', '\n' + client_tag) for arg in args])

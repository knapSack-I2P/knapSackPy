def server_print(*args, **kwargs):
    print('[kSk_SERVER]', end=' ')
    for arg in args:
        print(str(arg).replace('\n', '\nS --- '), **kwargs)

def client_print(*args, **kwargs):
    print('[kSk_CLIENT]', end=' ')
    for arg in args:
        print(str(arg).replace('\n', '\nC --- '), **kwargs)
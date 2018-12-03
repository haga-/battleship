import socket
import sys

from player import Player


class ClientGame:
    def __init__(self):
        self.player = Player()

    def get_player(self):
        return self.player


def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8888
    client = ClientGame()

    try:
        soc.connect((host, port))
    except:
        print('Connection error')
        sys.exit()

    print("Enter 'quit' to exit")
    message = input(' -> ')

    while message != 'give_up;;':
        soc.sendall(message.encode('utf8'))
        code, position, data = soc.recv(5120).decode('utf8').split(';')
        if code == 'begin':
            print(data)
            message = ''
            pass
        elif code == 'your_turn':
            if data == 'can_shoot':
                print('Can Shoot')
                message = input(' -> ')
        message = input(' -> ')

    soc.send(b'--quit--;;')


if __name__ == '__main__':
    main()
    # client = ClientGame()
    # client.get_player().print_boards()

import socket
import sys

from player import Player


class ClientGame:
    def __init__(self, socket):
        self.player = Player()
        self.socket = socket

    def get_player(self):
        return self.player

    def send_message(self, message):
        self.socket.sendall(message)

    def recv_message(self, bytes=4096):
        return self.socket.recv(bytes).decode('utf8')


def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = '127.0.0.1'
    port = 8888

    try:
        soc.connect((host, port))
    except:
        print('Connection error')
        sys.exit()

    client = ClientGame(soc)

    board = client.get_player().send_my_board()
    client.send_message(('begin;;' + board).encode('utf8'))

    code, position, data = client.recv_message().split(';')
    while code not in ['lost', 'won']:
        if code == 'begin':
            print(data)
            code, position, data = client.recv_message().split(';')
        elif code == 'your_turn':
            if data == 'can_shoot':
                print('Can Shoot')
                message = input(' -> ')
                client.send_message(message.encode('utf8'))
        else:
            code, position, data = client.recv_message().split(';')

    client.send_message(b'--quit--;;')


if __name__ == '__main__':
    main()

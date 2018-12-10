import pdb
import socket
import sys

from player import Player

WIN_MSGS = {
    'opp_gup': 'Você ganhou a partida! Seu oponente desistiu.',
    'sunk_all': 'Parabéns, você afundou todos os navios do adversário'
}


class ClientGame:
    def __init__(self, socket):
        self.player = Player()
        self.socket = socket

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

    board = client.player.send_my_board()
    client.send_message(('begin;;' + board).encode('utf8'))

    code, position, data = client.recv_message().split(';')
    while code not in ['lost', 'won']:
        print(code, position, data)
        if code == 'begin':
            print(data)
            code, position, data = client.recv_message().split(';')
        elif code == 'your_turn':
            print('Your turn')
            if data == 'can_shoot':
                print('Can Shoot')
            elif data == 'hit_opp':
                print('Hit opponent')
                client.player.update_opponent_board(position, 'hit')
            elif data == 'opp_missed':
                print('Opponent missed')
                client.player.update_my_board(position, 'miss')
            message = input(' -> ')
            client.send_message(message.encode('utf8'))
            code = ''
        elif code == 'opp_turn':
            print('Opponent turn')
            if data == 'missed_opp':
                print('Missed opponent')
                client.player.update_opponent_board(position, 'miss')
            elif data == 'opp_hit':
                print('Opponent hit')
                client.player.update_my_board(position, 'hit')
            code = ''
        else:
            code, position, data = client.recv_message().split(';')

    if code == 'won':
        print(WIN_MSGS[data])
    elif code == 'lost':
        print('Você perdeu :/')

    client.player.print_boards()

    client.send_message(b'--quit--;;')


if __name__ == '__main__':
    main()

import pdb
import socket
import string
import sys

from player import Player

BEGIN_MSGS = {
    'wait_for_opp': 'Conectado, espere por outro jogador',
    'opp_found': 'Conectado, espere pela sua vez'
}

WIN_MSGS = {
    'opp_gup': 'Você ganhou a partida! Seu oponente desistiu.',
    'sunk_all': 'Parabéns, você afundou todos os navios do adversário'
}


def get_row():
    print('Escolha uma letra entre A e J')
    x = input(' -> ')
    while not x.upper() in string.ascii_uppercase[:10]:
        print('Linha inválida')
        x = input(' -> ')
    return x.upper()


def get_col():
    print('Escolha um número entre 1 e 10')
    y = int(input(' -> '))
    while not y in range(1, 11):
        print('Coluna inválida')
        y = int(input(' -> '))
    return y


def get_input():
    print('Informe a linha se quiser colocar o navio na horizontal, e coluna, se quiser colocar na vertical')
    print('1) Coluna')
    print('2) Linha')
    option = int(input(' -> '))
    while not option in range(1, 3):
        print('Número inválido')
        option = int(input(' -> '))
    if option == 2:
        x = get_row()
        print('Informe a coluna')
        y = get_col()
    elif option == 1:
        x = get_col()
        print('Informe a linha')
        y = get_row()
    return x, y


def get_shot_position():
    print('Deseja desistir? (s/n)')
    give_up = input(' -> ')
    if give_up == 'n':
        print('Informe a linha e a coluna em que deseja atirar.')
        x = get_row()
        y = get_col()
        return 'shoot;{},{};'.format(x, y)
    else:
        return 'give_up;;'


class ClientGame:
    def __init__(self, socket):
        self.player = Player()
        self.socket = socket

    def send_message(self, message):
        self.socket.sendall(message)

    def recv_message(self, bytes=4096):
        return self.socket.recv(bytes).decode('utf8')

    def set_board(self):
        for i in range(5, 0, -1):
            print('Informe a posição inicial do navio de tamanho {}'.format(i))
            self.player.print_board('mine')
            x, y = get_input()
            set_board_again = self.player.set_board(x, y, i)
            while not set_board_again:
                print('Posição inválida!')
                x, y = get_input()
                set_board_again = self.player.set_board(x, y, i)
            self.player.print_board('mine')


def main():
    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = input(' -> Informe o IP do servidor: ')
    port = 8888

    try:
        soc.connect((host, port))
    except:
        print('Connection error')
        sys.exit()

    client = ClientGame(soc)
    client.set_board()

    board = client.player.send_my_board()
    client.send_message(('begin;;' + board).encode('utf8'))

    code, position, data = client.recv_message().split(';')
    while code not in ['lost', 'won']:
        if code == 'begin':
            print(BEGIN_MSGS[data])
            code, position, data = client.recv_message().split(';')
        elif code == 'your_turn':
            print('Sua vez')
            if data == 'can_shoot':
                print('Pode atirar')
            elif data == 'hit_opp':
                client.player.update_opponent_board(position, 'hit')
            elif data == 'opp_missed':
                client.player.update_my_board(position, 'miss')
            message = get_shot_position()
            client.send_message(message.encode('utf8'))
            code = ''
        elif code == 'opp_turn':
            print('Vez do adversário')
            if data == 'missed_opp':
                client.player.update_opponent_board(position, 'miss')
            elif data == 'opp_hit':
                client.player.update_my_board(position, 'hit')
            code = ''
        else:
            code, position, data = client.recv_message().split(';')

    if code == 'won':
        print(WIN_MSGS[data])
    elif code == 'lost':
        print('Você perdeu :/')

    client.player.print_boards()

    client.socket.close()


if __name__ == '__main__':
    main()

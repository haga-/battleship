import pdb
import socket
import sys
import traceback

from board import Board
from threading import Thread


class ServerGame:
    def __init__(self):
        self.boards = {}
        self.player1 = None
        self.player2 = None

    def add_client(self, client, board):
        self.boards[client.getpeername()] = Board(board)
        if len(self.boards) == 1:
            self.player1 = client
            self.player1.send('begin;;wait_for_opp'.encode('utf8'))
        elif len(self.boards) == 2:
            self.player1.send('your_turn;;can_shoot'.encode('utf8'))
            self.player2 = client
            self.player2.send('begin;;opp_found'.encode('utf8'))

    def handle_give_up(self, client):
        # player1 is giving up
        if self.player1 == client:
            self.player1.send('lost;;'.encode('utf8'))
            self.player2.send('won;;opp_gup'.encode('utf8'))
        # player2 is giving up
        else:
            self.player2.send('lost;;'.encode('utf8'))
            self.player1.send('won;;opp_gup'.encode('utf8'))

    def handle_shot(self, client, pos):
        # player1 is shooting
        if self.player1 == client:
            if self.boards[self.player2.getpeername()].hit_ship(pos):
                print('P1: acertou')
                self.boards[self.player2.getpeername()].update_board(pos, 'hit')
                if self.boards[self.player2.getpeername()].no_more_ships():
                    self.player1.send('won;;sunk_all'.encode('utf8'))
                    self.player2.send('lost;;'.encode('utf8'))
                else:
                    self.player1.send('your_turn;{};hit_opp'.format(pos).encode('utf8'))
                    self.player2.send('opp_turn;{};opp_hit'.format(pos).encode('utf8'))
            else:
                print('P1: errou')
                self.boards[self.player2.getpeername()].update_board(pos, 'miss')
                self.player1.send('opp_turn;{};missed_opp'.format(pos).encode('utf8'))
                self.player2.send('your_turn;{};opp_missed'.format(pos).encode('utf8'))
        # player2 is shooting
        else:
            if self.boards[self.player1.getpeername()].hit_ship(pos):
                print('P2: acertou')
                self.boards[self.player1.getpeername()].update_board(pos, 'hit')
                if self.boards[self.player1.getpeername()].no_more_ships():
                    self.player2.send('won;;sunk_all'.encode('utf8'))
                    self.player1.send('lost;;'.encode('utf8'))
                else:
                    self.player2.send('your_turn;{};hit_opp'.format(pos).encode('utf8'))
                    self.player1.send('opp_turn;{};opp_hit'.format(pos).encode('utf8'))
            else:
                print('P2: errou')
                self.boards[self.player1.getpeername()].update_board(pos, 'miss')
                self.player2.send('opp_turn;{};missed_opp'.format(pos).encode('utf8'))
                self.player1.send('your_turn;{};opp_missed'.format(pos).encode('utf8'))


server_game = ServerGame()


def start_server():
    port = 8888         # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
    # without waiting for its natural timeout to expire
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    clients = 0

    try:
        soc.bind(('', port))
    except:
        print('Erro: ' + str(sys.exc_info()))
        sys.exit()

    print('Servidor aguardando jogadores')

    soc.listen(2)       # queue up to 2 requests

    while clients < 2:
        clients = clients + 1
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print('Jogador {} conectado. IP: {}, porta: {}'.format(clients, ip, port))

        try:
            Thread(target=client_thread, args=(connection, clients)).start()
        except:
            print('Thread não iniciou.')
            traceback.print_exc()

    soc.close()


def client_thread(connection, client):
    is_active = True

    while is_active:
        client_input = receive_input(connection)
        if client_input == '':
            is_active = False
        else:
            code, position, data = client_input.split(';')

            if code == 'begin':
                server_game.add_client(connection, data)
            elif code == 'shoot':
                print('shoot')
                server_game.handle_shot(connection, position)
            elif code == 'give_up':
                print('Jogador {}, desistiu'.format(client))
                server_game.handle_give_up(connection)
                is_active = False


def receive_input(connection):
    client_input = connection.recv(2**12)
    # return decoded input
    return client_input.decode('utf8')


if __name__ == '__main__':
    start_server()

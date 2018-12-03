# https://kuntalchandra.wordpress.com/2017/08/23/python-socket-programming-server-client-application-using-threads/
import pdb
import socket
import sys
import traceback
from threading import Thread


class ServerGame:
    def __init__(self):
        self.boards = []
        self.player1 = None
        self.player2 = None

    def add_client(self, client, board):
        print(board)
        self.boards.append({client.getpeername()[1]: board})
        if len(self.boards) == 1:
            self.player1 = client
            self.player1.send('begin;;wait_for_opp'.encode('utf8'))
        elif len(self.boards) == 2:
            self.player1.send('your_turn;;can_shoot'.encode('utf8'))
            self.player2 = client
            self.player2.send('begin;;opp_found'.encode('utf8'))

    def get_boards(self):
        return self.boards


server_game = ServerGame()

def start_server():
    host = '127.0.0.1'
    port = 8888         # arbitrary non-privileged port

    soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # SO_REUSEADDR flag tells the kernel to reuse a local socket in TIME_WAIT state,
    # without waiting for its natural timeout to expire
    soc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    print('Socket created')
    clients = 0

    try:
        soc.bind((host, port))
    except:
        print('Bind failed. Error : ' + str(sys.exc_info()))
        sys.exit()

    soc.listen(5)       # queue up to 5 requests
    print('Socket now listening')

    while clients < 2:
        connection, address = soc.accept()
        ip, port = str(address[0]), str(address[1])
        print('Connected with {}: {}'.format(ip, port))
        clients = clients + 1

        try:
            Thread(target=client_thread, args=(connection, ip, port)).start()
        except:
            print('Thread did not start.')
            traceback.print_exc()

    soc.close()


def client_thread(connection, ip, port, max_buffer_size=5120):
    is_active = True

    while is_active:
        client_input = receive_input(connection, max_buffer_size)
        code, position, data = client_input.split(';')

        if '--quit--' in client_input:
            print('Client is requesting to quit')
            connection.close()
            print('Connection {}:{} closed'.format(ip, port))
            is_active = False
            print(server_game.get_boards())
        elif code == 'begin':
            server_game.add_client(connection, data)
        elif code == 'shoot':
            print('shoot')
            pdb.set_trace()
        else:
            print('Processed result: {}'.format(client_input))
            connection.sendall('-'.encode('utf8'))


def receive_input(connection, max_buffer_size):
    client_input = connection.recv(max_buffer_size)
    client_input_size = sys.getsizeof(client_input)

    if client_input_size > max_buffer_size:
        print('The input size is greater than expected {}'.format(client_input_size))

    decoded_input = client_input.decode('utf8').rstrip()  # decode and strip end of line
    result = process_input(decoded_input, connection.getpeername())

    return result


def process_input(input_str, socket_name):
    print('Processing the input received from {}'.format(socket_name))

    return str(input_str)


if __name__ == '__main__':
    start_server()

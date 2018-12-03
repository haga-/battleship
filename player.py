from sys import stdout

PRINT = {
    'hit': '| ❌ ',
    'miss': '| ― ',
    'blank': '|   ',
    'ship': '| ◇ ',
    'trace': '+---'
}


class Player:
    # constructor
    def __init__(self):
        self.my_board = [['blank' for x in range(10)] for y in range(10)]
        self.opponent_board = [['blank' for x in range(10)] for y in range(10)]

    #
    def send_my_board(self):
        board = ''
        for x in range(10):
            for y in range(10):
                board += self.my_board[x][y] + ','
        return board

    # shoot players opponent board at position(x,y)
    def shoot(self, x, y, socket):
        if type(x) is str:
            x = ord(x.upper()) - 65
            y = y - 1
        elif type(y) is str:
            tmp = x
            x = ord(y.upper()) - 65
            y = tmp - 1
        socket.send('shoot;{},{};'.format(x, y))

    # set a ship on players own board
    def set_board(self, start_1, start_2, n):
        # vertical
        if type(start_1) is int:
            start_2 = ord(start_2) - 65
            ship_to_be = []
            for i in range(start_2, n + start_2):
                ship_to_be.append(self.my_board[i][start_1 - 1])
            if ship_to_be == ['blank'] * n:
                for i in range(start_2, n + start_2):
                    self.my_board[i][start_1 - 1] = 'ship'
            else:
                return False
        # horizontal
        elif type(start_1) is str:
            start_1 = ord(start_1) - 65
            start = start_2 - 1
            finish = n + start_2 - 1
            if self.my_board[start_1][start:finish] == ['blank'] * n:
                for i in range(start, finish):
                    self.my_board[start_1][i] = 'ship'
            else:
                return False
        return True

    # updates own board after opponents play, and prints boards
    def update_my_board(self, x, y, message):
        if message == 'hit':
            print('Seu navio foi atingido!')
            self.my_board[x][y] == message
        else:
            print('Seu oponente errou, ufa!')
            self.my_board[x][y] == 'miss'
        self.print_boards()

    # updates opponent board after shooting, and prints boards
    def update_opponent_board(self, x, y, message):
        if message == 'hit':
            print('Você acertou um navio oponente, uhuul!')
            self.opponent_board[x][y] = message
        else:
            print('Você acertou água :(')
            self.opponent_board[x][y] = 'miss'
        self.print_boards()

    def print_traces(self):
        for x in range(10):
            if x == 0:
                stdout.write('  ')
            stdout.write(PRINT['trace'])
        print('+')

    def print_board(self, which_board):
        board, header = [], ''
        if which_board == 'mine':
            board = self.my_board
            header = 'My board'
        elif which_board == 'opponent':
            board = self.opponent_board
            header = '\nOpponent board'
        print(header)
        row = 'A'
        print('\n    1   2   3   4   5   6   7   8   9   10')
        for x in range(10):
            self.print_traces()
            for y in range(10):
                if y == 0:
                    stdout.write('%c ' % row)
                stdout.write(PRINT[board[x][y]])
            print('|')
            row = chr(ord(row) + 1)
        self.print_traces()

    def print_boards(self):
        self.print_board('mine')
        self.print_board('opponent')

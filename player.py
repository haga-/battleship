from sys import stdout

from board import Board

class Player:
    # constructor
    def __init__(self):
        self.my_board = Board()
        self.opponent_board = Board()

    # sends board as string
    def send_my_board(self):
        return self.my_board.send_board()

    # set a ship on players own board
    def set_board(self, start_1, start_2, n):
        # vertical
        if type(start_1) is int:
            start_2 = ord(start_2) - 65
            ship_to_be = []
            for i in range(start_2, n + start_2):
                ship_to_be.append(self.my_board.board[i][start_1 - 1])
            if ship_to_be == ['blank'] * n:
                for i in range(start_2, n + start_2):
                    self.my_board.board[i][start_1 - 1] = 'ship'
            else:
                return False
        # horizontal
        elif type(start_1) is str:
            start_1 = ord(start_1) - 65
            start = start_2 - 1
            finish = n + start_2 - 1
            if self.my_board.board[start_1][start:finish] == ['blank'] * n:
                for i in range(start, finish):
                    self.my_board.board[start_1][i] = 'ship'
            else:
                return False
        return True

    # updates own board after opponents play, and prints boards
    def update_my_board(self, position, message):
        if message == 'hit':
            print('Seu navio foi atingido!')
        elif message == 'miss':
            print('Seu oponente errou, ufa!')
        self.my_board.update_board(position, message)
        self.print_boards()

    # updates opponent board after shooting, and prints boards
    def update_opponent_board(self, position, message):
        if message == 'hit':
            print('Você acertou um navio oponente, uhuul!')
        elif message == 'miss':
            print('Você acertou água :(')
        self.opponent_board.update_board(position, message)
        self.print_boards()

    def print_board(self, which_board):
        if which_board == 'mine':
            board = self.my_board
            header = 'My board'
        elif which_board == 'opponent':
            board = self.opponent_board
            header = '\nOpponent board'
        print(header)
        board.print_board()


    def print_boards(self):
        self.print_board('mine')
        self.print_board('opponent')

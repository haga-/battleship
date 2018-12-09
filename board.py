from sys import stdout

PRINT = {
    'hit': '| ❌ ',
    'miss': '| ― ',
    'blank': '|   ',
    'ship': '| ◇ ',
    'trace': '+---'
}


def get_row_and_col_from_pos(pos):
    row, col = pos.split(',')
    row = ord(row.upper()) - 65
    col = int(col) - 1
    return (row, col)


class Board:
    # constructor
    def __init__(self, board=None):
        self.my_board = [['blank' for x in range(10)] for y in range(10)]
        if board != None:
            board = board.split(',')
            for x in range(10):
                for y in range(10):
                    self.my_board[x][y] = board[(x * 10) + y]

    def hit_ship(self, pos):
        row, col = get_row_and_col_from_pos(pos)
        return self.my_board[row][col] == 'ship'

    def print_board(self):
        row = 'A'
        print('\n    1   2   3   4   5   6   7   8   9   10')
        for x in range(10):
            self.print_traces()
            for y in range(10):
                if y == 0:
                    stdout.write('%c ' % row)
                stdout.write(PRINT[self.my_board[x][y]])
            print('|')
            row = chr(ord(row) + 1)
        self.print_traces()

    def print_traces(self):
        for x in range(10):
            if x == 0:
                stdout.write('  ')
            stdout.write(PRINT['trace'])
        print('+')

    def send_board(self):
        board = ''
        for x in range(10):
            for y in range(10):
                board += self.my_board[x][y] + ','
        # To remove last comma
        return board[:len(board) - 1]

    def update_board(self, pos, message):
        row, col = get_row_and_col_from_pos(pos)
        self.my_board[row][col] = message
        # self.print_board()

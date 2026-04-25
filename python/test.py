
###Visual Studio Codeでオセロゲームを作成するためのコード例です。###
import numpy as np
class Othello:
    def __init__(self):
        self.board = np.zeros((8, 8), dtype=int)  # 0: empty, 1: black, -1: white
        self.board[3][3] = self.board[4][4] = -1  # White pieces
        self.board[3][4] = self.board[4][3] = 1   # Black pieces
        self.current_player = 1  # Black starts

    def is_valid_move(self, x, y):
        if self.board[x][y] != 0:
            return False
        opponent = -self.current_player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            found_opponent = False
            while 0 <= nx < 8 and 0 <= ny < 8:
                if self.board[nx][ny] == opponent:
                    found_opponent = True
                elif self.board[nx][ny] == self.current_player and found_opponent:
                    return True
                else:
                    break
                nx += dx
                ny += dy
        return False

    def make_move(self, x, y):
        if not self.is_valid_move(x, y):
            return False
        self.board[x][y] = self.current_player
        opponent = -self.current_player
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            pieces_to_flip = []
            while 0 <= nx < 8 and 0 <= ny < 8:
                if self.board[nx][ny] == opponent:
                    pieces_to_flip.append((nx, ny))
                elif self.board[nx][ny] == self.current_player and pieces_to_flip:
                    for px, py in pieces_to_flip:
                        self.board[px][py] = self.current_player
                    break
                else:
                    break
                nx += dx
                ny += dy
        self.current_player *= -1  # Switch player
        return True
    def has_valid_moves(self):
        for x in range(8):
            for y in range(8):
                if self.is_valid_move(x, y):
                    return True
        return False
    def get_winner(self):
        black_count = np.sum(self.board == 1)
        white_count = np.sum(self.board == -1)
        if black_count > white_count:
            return "Black wins!"
        elif white_count > black_count:
            return "White wins!"
        else:
            return "It's a tie!"
# Example usage
game = Othello()
while game.has_valid_moves():
    print(game.board)
    x, y = map(int, input("Enter your move (x y): ").split())
    if not game.make_move(x, y):
        print("Invalid move. Try again.")
print(game.get_winner())

    
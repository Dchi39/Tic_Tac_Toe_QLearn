# --- Tic Tac Toe Environment ---
class TicTacToeEnv:
    def __init__(self):
        self.reset()

    def reset(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        return self.get_state()

    def get_state(self):
        return ''.join(self.board)

    def available_actions(self):
        return [i for i, spot in enumerate(self.board) if spot == ' ']

    def make_move(self, action):
        if self.board[action] != ' ':
            return self.get_state(), -10, True  # Invalid move
        self.board[action] = self.current_player
        done, winner = self.check_winner()
        reward = 0
        if done:
            if winner == 'X':
                reward = 1
            elif winner == 'O':
                reward = -1
            else:
                reward = 0.5  # Draw
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return self.get_state(), reward, done

    def check_winner(self):
        b = self.board
        lines = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for line in lines:
            if b[line[0]] == b[line[1]] == b[line[2]] != ' ':
                return True, b[line[0]]
        if ' ' not in b:
            return True, 'draw'
        return False, None
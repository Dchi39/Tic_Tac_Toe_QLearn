import tkinter as tk
from tkinter import messagebox
import pickle
from collections import defaultdict
from QLearningAgent import QLearningAgent, default_q_values
from tictactoe_env import TicTacToeEnv  



# --- Load the trained Q-table ---
def load_agent():
    agent = QLearningAgent()
    with open("q_table.pkl", "rb") as f:
        raw_q_table = pickle.load(f)
    agent.q_table = defaultdict(default_q_values, raw_q_table)  # Re-wrap as defaultdict
    return agent

# --- GUI Section ---
class TicTacToeGUI:
    def __init__(self, root, agent):
        self.agent = agent
        self.env = TicTacToeEnv()
        self.root = root
        self.buttons = []
        self.draw_board()

    def draw_board(self):
        for i in range(9):
            btn = tk.Button(self.root, text=' ', font='Helvetica 24', width=4, height=2,
                            command=lambda i=i: self.player_move(i))
            btn.grid(row=i//3, column=i%3)
            self.buttons.append(btn)


    def player_move(self, index):
        state, reward, done = self.env.make_move(index)
        if reward == -10:
            messagebox.showwarning("Invalid Move", "That spot is already taken!")
            return
        self.update_ui()
        done, winner = self.env.check_winner()
        if done:
            self.end_game(winner)
        else:
            self.agent_move()


    def agent_move(self):
        state = self.env.get_state()
        available = self.env.available_actions()
        action = self.agent.choose_action(state, available)
        self.env.make_move(action)
        self.update_ui()
        done, winner = self.env.check_winner()
        if done:
            self.end_game(winner)

    def update_ui(self):
        for i in range(9):
            self.buttons[i]['text'] = self.env.board[i]

    def end_game(self, winner):
        msg = "Draw!" if winner == 'draw' else f"{winner} wins!"
        messagebox.showinfo("Game Over", msg)
        self.env.reset()
        self.update_ui()

# --- Run GUI ---
if __name__ == "__main__":
    agent = load_agent()
    root = tk.Tk()
    root.title("Tic Tac Toe - Q Learning")
    app = TicTacToeGUI(root, agent)
    root.mainloop()

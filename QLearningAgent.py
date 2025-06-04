import random
from collections import defaultdict

# Define default Q-values for unseen states
def default_q_values():
    return [0] * 9

class QLearningAgent:
    def __init__(self, alpha=0.1, gamma=0.9, epsilon=0.1):
        self.q_table = defaultdict(default_q_values)
        self.alpha = alpha
        self.gamma = gamma
        self.epsilon = epsilon

    def choose_action(self, state, available_actions):
        if random.random() < self.epsilon:
            return random.choice(available_actions)
        q_values = self.q_table[state]
        max_q = max([q_values[a] for a in available_actions])
        best_actions = [a for a in available_actions if q_values[a] == max_q]
        return random.choice(best_actions)

    def update(self, state, action, reward, next_state, done, next_available):
        max_future_q = 0 if done else max([self.q_table[next_state][a] for a in next_available])
        current_q = self.q_table[state][action]
        new_q = current_q + self.alpha * (reward + self.gamma * max_future_q - current_q)
        self.q_table[state][action] = new_q

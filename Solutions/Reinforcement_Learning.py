# Reinforcement Learning
import numpy as np
import random

class MissionariesCannibalsEnv:
    def __init__(self):
        self.state = (3, 3, 1)  # Initial state (M_left, C_left, B_side) with boat on the right
        self.goal_state = (0, 0, 0)  # Goal state with all on the right bank and boat on the left

    def reset(self):
        self.state = (3, 3, 1)  # Reset to initial state
        return self.state

    def is_valid_state(self, m_left, c_left):
        # Check if the state is valid (missionaries not outnumbered by cannibals)
        return (m_left == 0 or m_left >= c_left) and (3 - m_left == 0 or 3 - m_left >= 3 - c_left)

    def step(self, action):
        m_left, c_left, b_side = self.state
        if b_side == 1:  # Boat on the right bank
            new_state = (m_left - action[0], c_left - action[1], 0)  # Move from right to left
        else:  # Boat on the left bank
            new_state = (m_left + action[0], c_left + action[1], 1)  # Move from left to right

        # Validate new state
        if self.is_valid_state(*new_state[:2]) and all(0 <= x <= 3 for x in new_state):
            reward = 1 if new_state == self.goal_state else -1  # Goal reward
            self.state = new_state
        else:
            reward = -10  # Invalid move
            new_state = self.state  # Stay in the same state

        return new_state, reward, new_state == self.goal_state

def train_q_learning(episodes, alpha, gamma, epsilon):
    env = MissionariesCannibalsEnv()
    q_table = np.zeros((4, 4, 2, 5))  # State space (M_left, C_left, B_side) x Action space

    for episode in range(episodes):
        state = env.reset()
        done = False

        while not done:
            m_left, c_left, b_side = state
            
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, 4)  # Explore
            else:
                action = np.argmax(q_table[m_left, c_left, b_side])  # Exploit
            
            action_values = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
            
            if action < len(action_values):  # Ensure action is within valid range
                next_state, reward, done = env.step(action_values[action])
                next_m_left, next_c_left, next_b_side = next_state

                # Check that next state indices are valid before accessing q_table
                if 0 <= next_m_left < 4 and 0 <= next_c_left < 4 and 0 <= next_b_side < 2:
                    # Update Q-value
                    q_table[m_left, c_left, b_side, action] += alpha * (
                        reward + gamma * np.max(q_table[next_m_left, next_c_left, next_b_side]) - q_table[m_left, c_left, b_side, action]
                    )
                    state = next_state  # Update current state
                else:
                    print("Invalid next state:", next_state)  # Optional: Debugging info

    return q_table

# Parameters
episodes = 10000
alpha = 0.1
gamma = 0.9
epsilon = 0.1

q_table = train_q_learning(episodes, alpha, gamma, epsilon)

# Test the trained Q-table
def test_q_learning(q_table):
    env = MissionariesCannibalsEnv()
    state = env.reset()
    done = False
    path = []

    while not done:
        m_left, c_left, b_side = state
        action = np.argmax(q_table[m_left, c_left, b_side])
        action_values = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]
        
        if action < len(action_values):  # Ensure action is valid
            path.append(action_values[action])
            state, _, done = env.step(action_values[action])

    return path

solution_path = test_q_learning(q_table)
print("Solution Path:", solution_path)

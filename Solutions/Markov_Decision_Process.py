# Markov Decision Process
import numpy as np

# Define the MDP environment for Missionaries and Cannibals
class MissionariesCannibalsMDP:
    def __init__(self):
        self.states = [(m, c, b) for m in range(4) for c in range(4) for b in range(2)]
        self.goal_state = (0, 0, 0)  # Goal: All people on the right, boat on the left side
        self.actions = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]  # Possible moves

    def is_valid(self, state):
        m, c, _ = state
        m_right = 3 - m
        c_right = 3 - c
        # Check validity of state: no missionaries outnumbered by cannibals
        return (0 <= m <= 3 and 0 <= c <= 3 and
                (m == 0 or m >= c) and
                (m_right == 0 or m_right >= c_right))

    def next_state(self, state, action):
        m, c, b = state
        m_move, c_move = action

        if b == 1:  # Boat is on the right
            new_state = (m - m_move, c - c_move, 0)  # Move to the left bank
        else:  # Boat is on the left
            new_state = (m + m_move, c + c_move, 1)  # Move to the right bank

        if self.is_valid(new_state):
            return new_state
        else:
            return None  # Invalid state

    def reward(self, state):
        return 1 if state == self.goal_state else -1

    def value_iteration(self, gamma=0.9, theta=1e-4):
        # Initialize value table with zeros
        V = {state: 0 for state in self.states}
        
        while True:
            delta = 0
            for state in self.states:
                if state == self.goal_state:
                    continue  # Skip the goal state

                best_action_value = float('-inf')
                for action in self.actions:
                    next_state = self.next_state(state, action)
                    if next_state is not None:
                        action_value = self.reward(next_state) + gamma * V[next_state]
                        best_action_value = max(best_action_value, action_value)

                delta = max(delta, abs(V[state] - best_action_value))
                V[state] = best_action_value

            if delta < theta:
                break

        # Extract policy from the value function
        policy = {}
        for state in self.states:
            if state == self.goal_state:
                continue

            best_action = None
            best_action_value = float('-inf')
            for action in self.actions:
                next_state = self.next_state(state, action)
                if next_state is not None:
                    action_value = self.reward(next_state) + gamma * V[next_state]
                    if action_value > best_action_value:
                        best_action_value = action_value
                        best_action = action

            policy[state] = best_action

        return policy

    def get_solution_path(self, policy):
        # Follow the policy to extract the path from start to goal state
        state = (3, 3, 1)  # Initial state
        path = []

        while state != self.goal_state:
            action = policy.get(state)
            if action is None:
                break  # No policy for this state

            path.append(action)
            state = self.next_state(state, action)

        return path

# Initialize the MDP and solve it with Value Iteration
mdp = MissionariesCannibalsMDP()
policy = mdp.value_iteration()
solution_path = mdp.get_solution_path(policy)
print("Optimal Solution Path with MDP:", solution_path)

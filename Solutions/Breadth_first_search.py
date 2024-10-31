# Breadth First Search
from collections import deque

def is_valid_state(m, c, b):
    """ Check if the current state is valid. """
    return (m >= 0 and c >= 0 and
            (m == 0 or m >= c) and  # Left bank
            (M - m == 0 or M - m >= C - c))  # Right bank

def bfs_solution():
    """ Solve the problem using BFS and return moves. """
    initial_state = (3, 3, 1)  # (missionaries_left, cannibals_left, boat_position)
    goal_state = (0, 0, 0)      # All on the right bank
    queue = deque([(initial_state, [], [])])  # (current_state, path, moves)
    visited = set()
    
    while queue:
        current_state, path, moves = queue.popleft()
        m_left, c_left, boat_position = current_state
        
        if current_state in visited:
            continue
        
        visited.add(current_state)
        path.append(current_state)

        # Check if we've reached the goal state
        if current_state == goal_state:
            return path, moves
        
        # Possible moves: (missionaries, cannibals)
        for m_move in range(0, 3):
            for c_move in range(0, 3):
                if (m_move + c_move >= 1 and m_move + c_move <= 2):  # At least one and at most two can cross
                    # Determine new state after the move
                    if boat_position == 1:  # Boat is on the left
                        new_m_left = m_left - m_move
                        new_c_left = c_left - c_move
                        new_boat_position = 0
                        # Record the move as (left_to_right, right_to_left)
                        move = (m_move, c_move)
                    else:  # Boat is on the right
                        new_m_left = m_left + m_move
                        new_c_left = c_left + c_move
                        new_boat_position = 1
                        move = (0, m_move + c_move)  # Return move

                    new_state = (new_m_left, new_c_left, new_boat_position)

                    # Check if the new state is valid
                    if is_valid_state(new_m_left, new_c_left, new_boat_position):
                        queue.append((new_state, path.copy(), moves + [move]))  # Add the new state and move

    return [], []  # Return empty if no solution found

# Global variables
M, C = 3, 3  # Number of missionaries and cannibals

solution_path, solution_moves = bfs_solution()
for state in solution_path:
    print(state)

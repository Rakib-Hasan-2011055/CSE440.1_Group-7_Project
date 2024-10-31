# A* search
import heapq

class MissionariesCannibalsEnv:
    def __init__(self):
        self.goal_state = (0, 0, 0)  # Goal: All on the right bank, boat on the left side

    def valid_state(self, state):
        m_left, c_left, _ = state
        m_right = 3 - m_left
        c_right = 3 - c_left

        # Valid if no missionaries are outnumbered on either side
        return (0 <= m_left <= 3 and 0 <= c_left <= 3 and
                (m_left == 0 or m_left >= c_left) and
                (m_right == 0 or m_right >= c_right))

    def get_successors(self, state):
        m_left, c_left, b_side = state
        successors = []
        possible_actions = [(1, 0), (2, 0), (0, 1), (0, 2), (1, 1)]

        for m_move, c_move in possible_actions:
            if b_side == 1:  # Boat on the right
                new_state = (m_left - m_move, c_left - c_move, 0)  # Move to the left bank
            else:  # Boat on the left
                new_state = (m_left + m_move, c_left + c_move, 1)  # Move to the right bank

            if self.valid_state(new_state):
                successors.append((new_state, (m_move, c_move)))
                
        return successors

    def heuristic(self, state):
        """ Heuristic function to estimate remaining steps to goal. """
        m_left, c_left, b_side = state
        return (m_left + c_left + 1) // 2  # Estimate crossings needed

    def a_star_search(self):
        initial_state = (3, 3, 1)  # Boat starts on the right
        # Priority queue for A* with (estimated total cost, cost so far, state, path)
        frontier = [(self.heuristic(initial_state), 0, initial_state, [])]
        visited = set()

        while frontier:
            est_total_cost, cost_so_far, state, path = heapq.heappop(frontier)

            if state == self.goal_state:
                return path  # Return the path to reach the goal

            if state in visited:
                continue

            visited.add(state)

            for successor, action in self.get_successors(state):
                if successor not in visited:
                    new_cost = cost_so_far + 1
                    est_cost = new_cost + self.heuristic(successor)
                    heapq.heappush(frontier, (est_cost, new_cost, successor, path + [action]))

        return None  # No solution found

# Initialize environment and find solution using A*
env = MissionariesCannibalsEnv()
solution_path = env.a_star_search()
print("Shortest Solution Path with A*:", solution_path)

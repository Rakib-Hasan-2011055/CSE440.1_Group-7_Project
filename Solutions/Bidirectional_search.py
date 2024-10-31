# Bi-Directional Search
from collections import deque 

class State:
    def __init__(self, missionaries_left, cannibals_left, boat_position):
        self.missionaries_left = missionaries_left
        self.cannibals_left = cannibals_left
        self.boat_position = boat_position  # 0 for left, 1 for right

    def is_goal(self):
        return self.missionaries_left == 0 and self.cannibals_left == 0 and self.boat_position == 0

    def is_valid(self):
        if self.missionaries_left < 0 or self.cannibals_left < 0:
            return False
        if self.missionaries_left > 3 or self.cannibals_left > 3:
            return False
        # Check the other side of the river
        missionaries_right = 3 - self.missionaries_left
        cannibals_right = 3 - self.cannibals_left
        if (self.missionaries_left > 0 and self.missionaries_left < self.cannibals_left) or \
           (missionaries_right > 0 and missionaries_right < cannibals_right):
            return False
        return True

    def get_successors(self):
        successors = []
        if self.boat_position == 1:  # Boat on the right side
            for m in range(3):
                for c in range(3):
                    if 1 <= m + c <= 2:  # At least one and at most two can cross
                        new_state = State(self.missionaries_left - m, self.cannibals_left - c, 0)
                        if new_state.is_valid():
                            successors.append(new_state)
        else:  # Boat on the left side
            for m in range(3):
                for c in range(3):
                    if 1 <= m + c <= 2:  # At least one and at most two can cross
                        new_state = State(self.missionaries_left + m, self.cannibals_left + c, 1)
                        if new_state.is_valid():
                            successors.append(new_state)
        return successors

    def __hash__(self):
        return hash((self.missionaries_left, self.cannibals_left, self.boat_position))

    def __eq__(self, other):
        return (self.missionaries_left, self.cannibals_left, self.boat_position) == (other.missionaries_left, other.cannibals_left, other.boat_position)

def bidirectional_search():
    initial_state = State(3, 3, 1)  # Start with boat on the right side
    goal_state = State(0, 0, 0)     # Goal: All on the right side, boat on the left

    front_queue = deque([initial_state])
    back_queue = deque([goal_state])

    visited_front = {initial_state: None}
    visited_back = {goal_state: None}

    while front_queue and back_queue:
        # Forward Search
        current = front_queue.popleft()
        for succ in current.get_successors():
            if succ not in visited_front:
                visited_front[succ] = current
                front_queue.append(succ)
                if succ in visited_back:
                    return reconstruct_path(visited_front, visited_back, succ)

        # Backward Search
        current = back_queue.popleft()
        for succ in current.get_successors():
            if succ not in visited_back:
                visited_back[succ] = current
                back_queue.append(succ)
                if succ in visited_front:
                    return reconstruct_path(visited_front, visited_back, succ)

    return None

def reconstruct_path(visited_front, visited_back, meeting_point):
    path = []
    # Reconstruct path from the start to the meeting point
    current = meeting_point
    while current is not None:
        path.append(current)
        current = visited_front[current]
    path.reverse()

    # Reconstruct path from the goal to the meeting point
    current = visited_back[meeting_point]
    while current is not None:
        path.append(current)
        current = visited_back[current]

    return path

# Test the bidirectional search
solution_path = bidirectional_search()
if solution_path:
    for state in solution_path:
        print(f"({state.missionaries_left}, {state.cannibals_left}, {state.boat_position})")
else:
    print("No solution found.")

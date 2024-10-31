# Depth First Search
class State:
    def __init__(self, missionaries, cannibals, boat):
        self.missionaries = missionaries
        self.cannibals = cannibals
        self.boat = boat  # 0 for left side, 1 for right side

    def is_valid(self):
        # Ensure no side has more cannibals than missionaries
        if self.missionaries < 0 or self.cannibals < 0 or self.missionaries > 3 or self.cannibals > 3:
            return False
        if (self.missionaries > 0 and self.missionaries < self.cannibals) or \
           (self.missionaries < 3 and self.cannibals < self.missionaries):
            return False
        return True

    def is_goal(self):
        return self.missionaries == 0 and self.cannibals == 0 and self.boat == 0

    def __hash__(self):
        return hash((self.missionaries, self.cannibals, self.boat))

    def __eq__(self, other):
        return (self.missionaries, self.cannibals, self.boat) == (other.missionaries, other.cannibals, other.boat)

    def __str__(self):
        return f"({self.missionaries}, {self.cannibals}, {self.boat})"


def dfs(state, path, visited):
    if state.is_goal():
        return path

    visited.add(state)

    # Possible moves: (M, C)
    possible_moves = [
        (1, 0), (0, 1), (2, 0), (0, 2), (1, 1)
    ]

    for m, c in possible_moves:
        if state.boat == 1:  # If the boat is on the right side
            new_state = State(state.missionaries - m, state.cannibals - c, 0)
        else:  # If the boat is on the left side
            new_state = State(state.missionaries + m, state.cannibals + c, 1)

        if new_state.is_valid() and new_state not in visited:
            result = dfs(new_state, path + [new_state], visited)
            if result:
                return result

    return None  # No solution found


def solve_missionaries_and_cannibals():
    initial_state = State(3, 3, 1)  # 3 missionaries, 3 cannibals, boat on right
    visited = set()
    path = [initial_state]

    result = dfs(initial_state, path, visited)

    if result:
        for state in result:
            print(state)
    else:
        print("No solution found.")


# Run the solution
solve_missionaries_and_cannibals()

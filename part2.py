# storing states as ((a, b), (c,d), e)
from copy import deepcopy
from enum import Enum
from typing import List, Tuple


class State:
    def __init__(self, a_x, a_y, t_x, t_y, call):
        self.a_x: int = a_x
        self.a_y: int = a_y
        self.t_x: int = t_x
        self.t_y: int = t_y
        self.call: int = call

    def get_id(self):
        idx = 2 * (self.a_x * 16 + self.a_y * 8 + self.t_x * 2 + self.t_y) + self.call
        return idx

    def get_a_pos(self):
        return (self.a_x, self.a_y)

    def set_a_pos(self, x):
        self.a_x = x[0]
        self.a_y = x[1]

    def increase_x(self):
        self.a_x = min(self.a_x + 1, 3)

    def decrease_x(self):
        self.a_x = max(self.a_x - 1, 0)

    def increase_y(self):
        self.a_y = min(self.a_y + 1, 1)

    def decrease_y(self):
        self.a_y = max(self.a_y - 1, 0)

    def t_increase_x(self):
        self.t_x = min(self.t_x + 1, 3)

    def t_decrease_x(self):
        self.t_x = max(self.t_x - 1, 0)

    def t_increase_y(self):
        self.t_y = min(self.t_y + 1, 1)

    def t_decrease_y(self):
        self.t_y = max(self.t_y - 1, 0)


class Actions(Enum):
    STAY, UP, DOWN, LEFT, RIGHT = range(5)


class POMDP:
    def __init__(self, states):
        self.states = states

    def apply_transition(self, state: State, action):
        results = []
        # Agent Movements
        if action == Actions.RIGHT:
            new_state = deepcopy(state)
            new_state.increase_x()
            results.append((x, new_state))
            new_state = deepcopy(state)
            new_state.decrease_x()
            results.append((1 - x, new_state))
        elif action == Actions.LEFT:
            new_state = deepcopy(state)
            new_state.increase_x()
            results.append((1 - x, new_state))
            new_state = deepcopy(state)
            new_state.decrease_x()
            results.append((x, new_state))
        elif action == Actions.DOWN:
            new_state = deepcopy(state)
            new_state.increase_y()
            results.append((x, new_state))
            new_state = deepcopy(state)
            new_state.decrease_y()
            results.append((1 - x, new_state))
        elif action == Actions.UP:
            new_state = deepcopy(state)
            new_state.increase_y()
            results.append((1 - x, new_state))
            new_state = deepcopy(state)
            new_state.decrease_y()
            results.append((x, new_state))
        elif action == Actions.STAY:
            results.append((1, state))

        movements_results = []
        # APPLY TARGET MOVEMENT
        for pr, state in results:
            next_state: State = deepcopy(state)
            # STAY
            movements_results.append((0.6 * pr, next_state))
            # RIGHT
            next_state = deepcopy(state)
            next_state.t_increase_x()
            movements_results.append((0.1 * pr, next_state))
            # LEFT
            next_state = deepcopy(state)
            next_state.t_decrease_x()
            movements_results.append((0.1 * pr, next_state))
            # DOWN
            next_state = deepcopy(state)
            next_state.t_increase_y()
            movements_results.append((0.1 * pr, next_state))
            # UP
            next_state = deepcopy(state)
            next_state.t_decrease_y()
            movements_results.append((0.1 * pr, next_state))

        final_results: List[Tuple[float, State]] = []
        if state.call == 0:
            for pr, state in final_results:
                # CALL IS ON
                next_state = deepcopy(state)
                final_results.append((pr * 0.5, next_state))
                # CALL IS OFF
                next_state = deepcopy(state)
                next_state.call = 1
                final_results.append((pr * 0.5, next_state))
        elif state.call == 1:
            for pr, state in final_results:
                # CALL IS ON
                next_state = deepcopy(state)
                final_results.append((pr * 0.9, next_state))
                # CALL IS OFF
                next_state = deepcopy(state)
                next_state.call = 0
                final_results.append((pr * 0.1, next_state))


if __name__ == "__main__":
    discount = 1
    states = []
    roll_no = 2019101050
    x = 1 - ((roll_no % 10000) % 30 + 1) / 100
    count = 0
    for a_x in range(4):
        for a_y in range(2):
            for t_x in range(4):
                for t_y in range(2):
                    for call in range(2):
                        states.append(State(a_x, a_y, t_x, t_y, call))
                        assert count == states[-1].get_id()
                        count += 1

    num_states = len(states)
    num_actions = len(Actions)
    pass

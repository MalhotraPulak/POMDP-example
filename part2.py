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

    def __str__(self):
        return f"S{self.a_y}{self.a_x}{self.t_y}{self.t_x}{self.call}"

    def get_a_pos(self):
        return self.a_x, self.a_y

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


class Observations(Enum):
    o1, o2, o3, o4, o5, o6 = range(6)


class POMDP:
    def __init__(self, states):
        self.states = states

    def apply_transition(self, state: State, action):
        results = []
        # Agent Movements
        # print(action)
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

        # FILTER MOVEMENT RESULTS
        filter_movements = []
        unique_states = set([st.get_id() for pr, st in movements_results])
        for st in unique_states:
            prt = 0.0
            for pr, st2 in movements_results:
                if st2.get_id() == st:
                    prt += pr
            filter_movements.append((prt, self.states[st]))

        final_results: List[Tuple[float, State]] = []
        if state.call == 0:
            for pr, state in filter_movements:
                # CALL IS ON
                next_state = deepcopy(state)
                final_results.append((pr * 0.5, next_state))
                # CALL IS OFF
                next_state = deepcopy(state)
                next_state.call = 1
                final_results.append((pr * 0.5, next_state))
        elif state.call == 1:
            for pr, state in filter_movements:
                # CALL IS ON
                next_state = deepcopy(state)
                final_results.append((pr * 0.9, next_state))
                # CALL IS OFF
                next_state = deepcopy(state)
                next_state.call = 0
                final_results.append((pr * 0.1, next_state))

        # for idx, (_, st) in enumerate(final_results):
        #     for idx2, (_, st2) in enumerate(final_results):
        #         if idx != idx2:
        #             assert st.get_id() != st2.get_id()
        total = 0.0
        for (pr, _) in final_results:
            total += pr
        assert 0.99 < total < 1.01
        return final_results

    def transition_table(self):
        for state in self.states:
            for action in Actions:
                rez = self.apply_transition(state, action)
                for pr, res in rez:
                    print(f"T: {action.name} : {str(state)} : {str(res)} {pr}", file=f)

    def observation_table(self):
        results = []
        for end_state in self.states:
            pos_diff = (end_state.a_x - end_state.t_x, end_state.a_y - end_state.t_y)
            if pos_diff == (0, 0):
                results.append((Observations.o1, end_state))
            elif pos_diff == (-1, 0):
                # target is to right
                results.append((Observations.o2, end_state))
            elif pos_diff == (1, 0):
                # target it to left
                results.append((Observations.o4, end_state))
            elif pos_diff == (0, -1):
                # target is to down
                results.append((Observations.o3, end_state))
            elif pos_diff == (0, 1):
                # target is up
                results.append((Observations.o5, end_state))
            else:
                results.append((Observations.o6, end_state))
        for obs, state in results:
            print(f"O : * : {str(state)} : {obs.name} {1.0}", file=f)

    def reward_table(self):
        results = []
        for obs in range(len(Observations)):
            for state in self.states:
                curr_obs = Observations(obs)
                if curr_obs == Observations.o1 and state.call == 1:
                    results.append((curr_obs, reeward, state))
                else:
                    results.append((curr_obs, -1, state))
        for obs, reward, state in results:
            print(f"R: * : * : {str(state)}: {obs.name} {reward}", file=f)


if __name__ == "__main__":
    discount = 1
    states = []
    roll_no = 2019101009
    x = 1 - ((roll_no % 10000) % 30 + 1) / 100
    count = 0
    reeward = (roll_no % 90 + 10)
    f = open("res.pomdp", "w")
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
    num_observation = len(Observations)
    print("discount: 0.5", file=f)
    print("values: reward", file=f)
    print("states:", end=" ", file=f)
    for state in states:
        print(state, end=" ", file=f)
    print(file=f)
    print("actions:", end=" ", file=f)
    for action in Actions:
        print(action.name, end=" ", file=f)
    print(file=f)
    print("observations:", end=" ", file=f)
    for obs in Observations:
        print(obs.name, end=" ", file=f)
    print(file=f)
    print("start: ", end=" ", file=f)
    count = 0
    for state in states:
        pos = (state.t_x, state.t_y)
        a_pos = (state.a_x, state.a_y)
        if a_pos == (1, 0) and not (pos == (0, 0) or pos == (1, 1) or pos == (1, 0)):
            count += 1
        else:
            pass
    for state in states:
        pos = (state.t_x, state.t_y)
        a_pos = (state.a_x, state.a_y)
        if a_pos == (1, 0) and not (pos == (0, 0) or pos == (1, 1) or pos == (1, 0)):
            print(1 / count, end=" ", file=f)
        else:
            print(0, end=" ", file=f)
    print(file=f)
    p = POMDP(states)
    p.transition_table()
    p.observation_table()
    p.reward_table()
    pass

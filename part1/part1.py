from typing import List
from copy import deepcopy


def t(old_state, a, curr_state):
    if a == RIGHT:
        if curr_state == min(num_states - 1, old_state + 1):
            return x
        elif curr_state == max(old_state - 1, 0):
            return 1 - x
        else:
            return 0
    elif a == LEFT:
        if curr_state == min(num_states - 1, old_state + 1):
            return 1 - x
        elif curr_state == max(old_state - 1, 0):
            return x
        else:
            return 0
    assert False


def color(s):
    if s in [0, 2, 5]:
        return RED
    elif s in [1, 3, 4]:
        return GREEN


def O(new_state, a, o):
    if color(new_state) == GREEN:
        if o == GREEN:
            return pgg
        elif o == RED:
            return 1 - pgg
        assert False
    if color(new_state) == RED:
        if o == RED:
            return prr
        elif o == GREEN:
            return 1 - prr
        assert False


def printer(b):
    for i in range(num_states):
        print("{:03f}".format(b[i]), end=" ", file=f)
    print(file=f)


class Belief:
    def __init__(self):
        debug = False
        b = [1 / 3, 0, 1 / 3, 0, 0, 1 / 3]
        b_prime: List[float] = [0.0 for _ in range(num_states)]
        for a, o in [(RIGHT, GREEN), (LEFT, RED), (LEFT, GREEN)]:
            for new_state in range(num_states):
                if debug:
                    print(f"Calculating b_prime[{new_state}]")
                    print(f"Move is {a}")
                # prob_states = [t(old_state, a, new_state) * b[old_state] for old_state in range(num_states)]
                transitions = [0 for _ in range(num_states)]
                for old_state in range(num_states):
                    transitions[old_state] = t(old_state, a, new_state)
                    if debug:
                        print(
                            f"T({old_state}->{new_state},{a}) = {round(transitions[old_state], 3)}")
                    if transitions[old_state] == 0:
                        continue
                    transitions[old_state] *= b[old_state]
                    if debug:
                        print(
                            f"On multiplying by b[{old_state}]={round(b[old_state], 3)} gives {round(transitions[old_state], 3)}")

                sum_transition = sum(transitions)
                observation_prob = O(new_state, a, o)
                b_prime[new_state] = sum_transition * observation_prob
                if debug:
                    print("sum of transitions", sum_transition)
                    print(f"P(o={o}|a={a},s'={new_state}) = {observation_prob}")
                    print(f"b_prime[{new_state}]={b_prime[new_state]}")
                    print()
            numerator = deepcopy(b_prime)
            denominator = sum(numerator)
            for idx in range(num_states):
                b_prime[idx] = numerator[idx] / denominator
            if debug:
                print()
                print("Not normalized numerator", numerator)
                print("Denominator", denominator)
                print(b_prime)
                print("-----------------------------------------")
            b = deepcopy(b_prime)
            printer(b)


if __name__ == "__main__":
    RIGHT = "R"
    LEFT = "L"
    GREEN = "G"
    RED = "R"
    num_states = 6
    roll_no = 2019101050
    x = 1 - ((roll_no % 10000) % 30 + 1) / 100
    y = (roll_no % 100) % 4 + 1
    pgg = 0.90
    prr = 0.85
    f = open("2019101050_2019101049.txt", "w+")
    print("2019101050 2019101049", file=f)
    print(x, y, file=f)
    Belief()

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


import math


def truncate(number, decimals=0):
    """
    Returns a value truncated to a specific number of decimal places.
    """
    if not isinstance(decimals, int):
        raise TypeError("decimal places must be an integer.")
    elif decimals < 0:
        raise ValueError("decimal places has to be 0 or more.")
    elif decimals == 0:
        return math.trunc(number)

    factor = 10.0 ** decimals
    return math.trunc(number * factor) / factor


def printer(b):
    for i in range(num_states):
        print("{:.04f}".format(truncate(number=b[i], decimals=4)), end=" ", file=f)
    print(file=f)


def printerr(b):
    for i in range(num_states):
        print("{:.04f}".format(b[i]), end=" ")
    print()


class Belief:
    def __init__(self):
        b = [1 / 3, 0, 1 / 3, 0, 0, 1 / 3]
        b_prime: List[float] = [0.0 for _ in range(num_states)]
        for a, o in [(RIGHT, GREEN), (LEFT, RED), (LEFT, GREEN)]:
            print(f"### Move is {a}, Observation is {o}")
            print()
            for new_state in range(num_states):
                if debug:
                    print(f"Calculating b_prime[{new_state}]")

                # prob_states = [t(old_state, a, new_state) * b[old_state] for old_state in range(num_states)]
                transitions = [0 for _ in range(num_states)]
                for old_state in range(num_states):
                    transitions[old_state] = t(old_state, a, new_state)
                    if debug:
                        print(
                            f"- T({old_state}->{new_state},{a}) = {round(transitions[old_state], 7)}")
                    if transitions[old_state] == 0:
                        continue
                    transitions[old_state] *= b[old_state]
                    if debug:
                        print(
                            f"\t- On multiplying by b[{old_state}]={round(b[old_state], 7)} gives {round(transitions[old_state], 7)}")

                sum_transition = sum(transitions)
                observation_prob = O(new_state, a, o)
                b_prime[new_state] = sum_transition * observation_prob
                if debug:
                    print("  ")
                    print("sum of transitions=", round(sum_transition, 7), " ")
                    print(f"P(o={o}|a={a},s'={new_state}) = {round(observation_prob, 7)}  ")
                    print(
                        f"b_prime[{new_state}]= {round(sum_transition, 7)} * {round(observation_prob, 7)} = {round(b_prime[new_state], 7)}  ")
                    print()
            numerator = deepcopy(b_prime)
            denominator = sum(numerator)
            for idx in range(num_states):
                b_prime[idx] = numerator[idx] / denominator
            if debug:
                print()
                print("Not normalized numerator  ")
                printerr(numerator)
                print("  ")
                print("Denominator", round(denominator, 7), " ")
                print("Updated Beliefs  ")
                printerr(b_prime)
                print("  ")
            b = deepcopy(b_prime)
            printer(b)


if __name__ == "__main__":
    RIGHT = "Right"
    LEFT = "Left"
    GREEN = "Green"
    RED = "Right"
    num_states = 6
    roll_no = 2019101050
    x = 1 - ((roll_no % 10000) % 30 + 1) / 100
    y = (roll_no % 100) % 4 + 1
    pgg = 0.9
    prr = 0.85
    debug = True
    f = open("2019101050_2019101049.txt", "w+")
    print("2019101050 2019101049", file=f)
    print(x, y, file=f)
    Belief()

from typing import List

RIGHT = "r"
LEFT = "l"
GREEN = "g"
RED = "r"
num_states = 6
roll_no = 2019101050
x = 1 - ((roll_no % 10000) % 30 + 1) / 100
y = (roll_no % 100) % 4


def t(old_state, a, curr_state):
    if a == RIGHT:
        if curr_state == max(num_states - 1, old_state + 1):
            return x
        elif curr_state == min(old_state - 1, 0):
            return 1 - x
        else:
            return 0
    elif a == LEFT:
        if curr_state == max(num_states - 1, old_state + 1):
            return 1 - x
        elif curr_state == min(old_state - 1, 0):
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
    if o == GREEN:
        if color(new_state) == GREEN:
            return 0.85
        elif color(new_state) == RED:
            return 0.15
        assert False
    if o == RED:
        if color(new_state) == RED:
            return 0.9
        elif color(new_state) == GREEN:
            return 0.1
        assert False


def printer(b):
    for i in range(num_states):
        print("{:03f}".format(b[i]), end=" ")
    print()


class Belief:
    def __init__(self):
        print("2019101050 2019101049")
        print(x, y)
        b = [1 / 3, 0, 1 / 3, 0, 0, 1 / 3]
        b_prime: List[float] = [0.0 for _ in range(num_states)]
        for a, o in [(RIGHT, GREEN), (LEFT, RED), (LEFT, GREEN)]:
            printer(b)
            for new_state in range(num_states):
                b_prime[new_state] = sum(
                    [t(old_state, a, new_state) * b[old_state] for old_state in range(num_states)])
                b_prime[new_state] *= O(new_state, a, o)
                denominator = sum(b_prime)
                for idx in range(num_states):
                    b_prime[idx] = b_prime[idx] / denominator
            b = b_prime
        printer(b)


Belief()

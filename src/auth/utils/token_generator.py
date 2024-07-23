import random


def generate_int_token(length: int = 4):
    if length < 1:
        length = 1
    return random.randint(10 * (length-1), (10 * length) - 1)

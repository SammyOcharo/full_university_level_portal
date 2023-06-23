
import random


def create_security_id(first_name):
    number = random.randint(111, 999)
    first_name = first_name[:3]

    security_id = f'{first_name}-{number}'

    return security_id
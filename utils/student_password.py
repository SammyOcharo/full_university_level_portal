import random

def get_student_password(full_name):
    random_number = random.randint(1111, 9999)

    name = full_name[:4]
    password = f'{name}{random_number}'

    return password

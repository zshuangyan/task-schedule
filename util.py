import random
import string


def generate_name():
    return "".join(random.choice(string.digits + string.ascii_letters) for i in range(8))

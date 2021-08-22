import random
import string


# Returns secret value
def get_secret_value(name):
    f = None
    try:
        f = open("/run/secrets/" + name, "r")
        return f.read()
    finally:
        f.close()


# Returns random string
def generate_random_string(prefix):
    return prefix + ''.join(
        random.choice(string.ascii_lowercase) for i in range(20)
    )

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


# Raises an exception if value is not a one word
def validate_is_one_word(value):
    if len(value.split()) > 1:
        raise Exception("Invalid value: " + value)

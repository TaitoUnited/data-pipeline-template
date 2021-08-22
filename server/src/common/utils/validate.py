# Raises an exception if value is not a one word
def validate_is_one_word(value):
    if len(value.split()) > 1:
        raise Exception("Invalid value: " + value)

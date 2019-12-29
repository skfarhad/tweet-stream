
def is_empty_str(v):
    return v is str and len(v) == 0


def is_empty_set(v):
    return v is set and len(v) == 0


def is_null(v):
    return v is None


def is_zero(v):
    return v is int and v == 0

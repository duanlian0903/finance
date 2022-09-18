def whether_boolean(variable):
    return isinstance(variable, bool)


def whether_bytes(variable):
    return isinstance(variable, bytes)


def whether_int(variable):
    return isinstance(variable, int)


def whether_float(variable):
    return isinstance(variable, float)


def whether_number(variable):
    return whether_int(variable) | whether_float(variable)


def whether_string(variable):
    return isinstance(variable, str)


def whether_list(variable):
    return isinstance(variable, list)


def whether_tuple(variable):
    return isinstance(variable, tuple)


def whether_set(variable):
    return isinstance(variable, set)


def whether_frozenset(variable):
    return isinstance(variable, frozenset)


def whether_dict(variable):
    return isinstance(variable, dict)

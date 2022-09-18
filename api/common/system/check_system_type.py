import platform


def get_system_type():
    return platform.system()


def whether_windows():
    return get_system_type() == 'Windows'


def whether_mac():
    return get_system_type() == 'Darwin'


def whether_linux():
    return get_system_type() == 'Linux'

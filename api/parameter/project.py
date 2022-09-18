import math
import multiprocessing


def whether_debug():
    return False


def whether_show_fundamental_operation_exception_message():
    return True


def whether_show_normal_operation_exception_message():
    return True


def whether_save_csv_for_dataframe():
    return True


def get_number_of_thread_for_calculating():
    return math.floor(0.8*multiprocessing.cpu_count())

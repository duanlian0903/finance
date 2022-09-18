import math
import api.common.system.message as acsm


def get_math_nan_value():  # tested
    return math.nan


def check_whether_nan_value(number):  # tested
    try:
        return math.isnan(number)
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error[' + str(number) + '], and the data type is not number.')
        return False


def get_log_value(number, base_number=math.e):  # tested
    log_value = get_math_nan_value()
    try:
        log_value = math.log(number, base_number)
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error for log calculation [' + str(number) + ', ' + str(base_number) + '], and return nan value.')
    return log_value


def get_exponential_value(number, base_number=math.e):  # tested
    exponential_value = get_math_nan_value()
    try:
        exponential_value = math.pow(base_number, number)
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error for power calculation [' + str(number) + ', ' + str(base_number) + '], and return nan value.')
    return exponential_value


def get_original_percent_change_number(current_positive_number, base_positive_number):  # tested
    percent_change = get_math_nan_value()
    try:
        if (current_positive_number > 0) & (base_positive_number > 0):
            percent_change = (current_positive_number - base_positive_number)/base_positive_number
        else:
            acsm.show_fundamental_operation_exception_message('Having non-positive numbers [' + str(current_positive_number) + ', ' + str(base_positive_number) + '], and return nan value.')
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error [' + str(current_positive_number) + ', ' + str(base_positive_number) + '], and return nan value.')
    return percent_change


def get_transformed_percent_change_number(current_positive_number, base_positive_number):  # tested
    percent_change = get_math_nan_value()
    try:
        if (current_positive_number > 0) & (base_positive_number > 0):
            if current_positive_number > base_positive_number:
                percent_change = (current_positive_number - base_positive_number) / base_positive_number
            else:
                percent_change = -(base_positive_number - current_positive_number) / current_positive_number
        else:
            acsm.show_fundamental_operation_exception_message('Having non-positive numbers [' + str(current_positive_number) + ', ' + str(base_positive_number) + '], and return nan value.')
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error [' + str(current_positive_number) + ', ' + str(base_positive_number) + '], and return nan value.')
    return percent_change


def get_percent_position(current_number, highest_number, lowest_number):  # tested
    percent_position = get_math_nan_value()
    try:
        if (highest_number > lowest_number) & (highest_number >= current_number) & (current_number >= lowest_number):
            percent_position = 100*(current_number-lowest_number)/(highest_number-lowest_number)
        else:
            acsm.show_fundamental_operation_exception_message('Having unexpected number [' + str(current_number) + ', ' + str(highest_number) + ', ' + str(lowest_number) + '], and return nan value.')
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error [' + str(current_number) + ', ' + str(highest_number) + ', ' + str(lowest_number) + '], and return nan value.')
    return percent_position


def get_relative_percent_portion(portion1_number, portion2_number):  # tested
    portion = get_math_nan_value()
    try:
        if (portion1_number >= 0) & (portion2_number >= 0) & (portion1_number+portion2_number > 0):
            portion = 100*portion1_number/(portion1_number+portion2_number)
        else:
            acsm.show_fundamental_operation_exception_message('Having unexpected number [' + str(portion1_number) + ', ' + str(portion2_number) + '], and return nan value.')
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error [' + str(portion1_number) + ', ' + str(portion2_number) + '], and return nan value.')
    return portion


def get_updated_max(current_max, new_value):  # tested
    try:
        if current_max > new_value:
            return current_max
        else:
            return new_value
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error to get max[' + str(current_max) + ', ' + str(new_value) + '], and return None value.')
        return get_math_nan_value()


def get_updated_min(current_min, new_value):  # tested
    try:
        if current_min < new_value:
            return current_min
        else:
            return new_value
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error to get min[' + str(current_min) + ', ' + str(new_value) + '], and return None value.')
        return get_math_nan_value()


def get_decimal_value_position(number_value):
    position = 0
    try:
        while abs(number_value) < 1:
            position = position + 1
            number_value = number_value * 10
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error[' + str(number_value) + '], and the data type is not number.')
    return position


def get_power_value_position(number_value):
    position = 0
    try:
        while abs(number_value) > 1:
            position = position + 1
            number_value = number_value / 10
    except:
        acsm.show_fundamental_operation_exception_message('Having unexpected error[' + str(number_value) + '], and the data type is not number.')
    return position


def convert_comma_string_into_number(comma_string):  # tested
    try:
        result = float(comma_string.replace(',', ''))
    except:
        acsm.show_fundamental_operation_exception_message('Having error converting string [' + str(comma_string) + '] to number, and return nan value.')
        result = get_math_nan_value()
    return result


def convert_special_letter_ending_string_into_number(special_letter_ending_string):  # tested
    try:
        if special_letter_ending_string.endswith('%'):
            result = float(special_letter_ending_string[:-1]) / 100
        elif special_letter_ending_string.endswith('K') | special_letter_ending_string.endswith('k'):
            result = float(special_letter_ending_string[:-1]) * 1000
        elif special_letter_ending_string.endswith('M') | special_letter_ending_string.endswith('m'):
            result = float(special_letter_ending_string[:-1]) * 1000000
        elif special_letter_ending_string.endswith('B') | special_letter_ending_string.endswith('b'):
            result = float(special_letter_ending_string[:-1]) * 1000000000
        elif special_letter_ending_string.endswith('T') | special_letter_ending_string.endswith('t'):
            result = float(special_letter_ending_string[:-1]) * 1000000000000
        else:
            acsm.show_fundamental_operation_exception_message('Having unexpected ending [' + str(special_letter_ending_string) + '], and return nan value.')
            result = get_math_nan_value()
    except:
        acsm.show_fundamental_operation_exception_message('Having error converting string [' + str(special_letter_ending_string) + '] to number, and return nan value.')
        result = get_math_nan_value()
    return result

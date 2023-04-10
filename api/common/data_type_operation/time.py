import datetime as dt


def day_datetime_formatstring():
    return '%Y-%m-%d'


def convert_string_to_datetime(given_string, given_formatstring):
    return dt.datetime.strptime(given_string, given_formatstring)


def convert_datetime_to_string(given_datetime, given_formatstring):
    return dt.datetime.strftime(given_datetime, given_formatstring)


def get_current_time():
    return dt.datetime.now()


def get_timestamp_from_datetime(given_datetime):
    return given_datetime.timestamp()


def get_datetime_from_timestamp(given_timestamp):
    return dt.datetime.fromtimestamp(given_timestamp)


def get_year_stamp_from_datetime(given_datetime):
    return get_timestamp_from_datetime(given_datetime)/31536000


def get_datetime_from_year_stamp(given_year_stamp):
    return get_datetime_from_timestamp(round(given_year_stamp * 31536000))


def get_removed_timezone_datetime(given_datetime):
    return given_datetime.replace(tzinfo=None)


def get_yardstick_datetime():
    return convert_string_to_datetime('1990-01-01', day_datetime_formatstring())


def get_week_index(given_datetime):
    timedelta = given_datetime - get_yardstick_datetime()
    return int((timedelta.total_seconds())/604800)


def get_month_index(given_datetime):
    return (given_datetime.year-get_yardstick_datetime().year)*12 + given_datetime.month


def get_needed_datetime_with_day_interval(start_datetime, day_interval):
    return start_datetime + dt.timedelta(days=day_interval)


def get_needed_datetime_with_year_interval(start_datetime, year_interval):
    if (start_datetime.month == 2) & (start_datetime.day == 29):
        return dt.datetime(year=start_datetime.year + year_interval, month=start_datetime.month, day=start_datetime.day - 1)
    else:
        return dt.datetime(year=start_datetime.year + year_interval, month=start_datetime.month, day=start_datetime.day)


def get_datetime_by_removing_hour_and_minute(given_datetime):
    return get_needed_datetime_with_year_interval(given_datetime, 0)

import api.common.data_type_operation.time as acdtot
import api.finance.name.attribute.fundamental_analysis as afnafa


def __convert_date_string_into_datetime(date_string):
    year_str = date_string[:4]
    month_str = date_string[4:6]
    if int(month_str) <= 3:
        return acdtot.convert_string_to_datetime(year_str+'-03-31', acdtot.day_datetime_formatstring())
    elif int(month_str) <= 6:
        return acdtot.convert_string_to_datetime(year_str+'-06-30', acdtot.day_datetime_formatstring())
    elif int(month_str) <= 9:
        return acdtot.convert_string_to_datetime(year_str+'-09-30', acdtot.day_datetime_formatstring())
    else:
        return acdtot.convert_string_to_datetime(year_str+'-12-31', acdtot.day_datetime_formatstring())


def __get_non_time_interval_attribute_list():
    return []


def __get_time_interval_attribute_list():
    return []

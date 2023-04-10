import pandas as pd
import api.common.system.message as acsm


def get_empty_data_frame():  # tested
    return pd.DataFrame([])


def get_df_from_series(series_data):
    return pd.DataFrame(series_data)


def generate_one_row_dataframe_from_dictionary(index, dict_data):  # tested
    result = get_empty_data_frame()
    try:
        if len(dict_data) != 0:
            result = pd.DataFrame([dict_data], index=[index])
    except:
        acsm.show_fundamental_operation_exception_message('We generate an empty data frame because of unexpected errors.')
    return result


def generate_multi_row_dataframe_from_list_of_dictionary(list_of_dictionary_data):  # tested
    result = get_empty_data_frame()
    try:
        if len(list_of_dictionary_data) != 0:
            result = pd.DataFrame(list_of_dictionary_data)
    except:
        acsm.show_fundamental_operation_exception_message('We generate an empty data frame because of unexpected errors with dictionary list: ' + str(list_of_dictionary_data))
    return result


def generate_multi_row_dataframe_from_matrix(matrix, column_name_list):
    result = get_empty_data_frame()
    try:
        if len(matrix) != 0:
            result = pd.DataFrame(matrix, columns=column_name_list)
    except:
        acsm.show_fundamental_operation_exception_message('We generate an empty data frame because of unexpected errors with matrix: ' + str(matrix))
    return result


def combine_dataframe(dataframe_list, axis=0):  # tested
    result = get_empty_data_frame()
    try:
        result = pd.concat(dataframe_list, axis=axis)
    except:
        acsm.show_fundamental_operation_exception_message('We generate an empty data frame because of unexpected errors with combine df list: ' + str(dataframe_list))
    return result


def join_auxiliary_df(primary_df, secondary_df):
    result = primary_df
    try:
        result = primary_df.join(secondary_df)
    except:
        acsm.show_fundamental_operation_exception_message('We return the original target data frame because of unexpected left join errors.')
    return result


def add_matching_column_value_df(target_df, reference_df, column_name, none_value):  # tested
    try:
        result_df = target_df.copy()
        result_df[column_name] = none_value
        for index_value in result_df.index:
            if index_value in reference_df.index:
                result_df.loc[index_value, column_name] = reference_df.loc[index_value, column_name]
            else:
                print('Cannot find the matching index ' + str(index_value) + ', so the value ' + str(none_value) + ' is assigned.')
        return result_df
    except:
        acsm.show_fundamental_operation_exception_message('We return the original target data frame because of unexpected errors.')
        return target_df


def add_matching_column_value_and_delete_unmatched_row_df(target_df, reference_df, column_name):  # tested
    return select_sub_df_without_none_value(add_matching_column_value_df(target_df, reference_df, column_name, None), column_name)


def select_sub_df_without_none_value(original_df, column_name):  # tested
    try:
        result_df = original_df.copy()
        index_list = []
        for index_value in result_df.index:
            if result_df.loc[index_value, column_name] is not None:
                index_list.append(index_value)
            else:
                print(str(index_value) + ' is not selected for the None value.')
        return result_df.loc[index_list, ]
    except:
        acsm.show_fundamental_operation_exception_message('We return the original data frame because of unexpected errors.')
        return original_df


def change_dataframe_column_name(df, column_name_dict):  # tested
    result = df
    try:
        result = df.rename(columns=column_name_dict)
    except:
        acsm.show_fundamental_operation_exception_message('We return the original dataframe because of unexpected change column name errors.')
    return result


def change_dataframe_column_name_with_column_name_list(df, column_name_list):
    result = df
    try:
        result.columns = column_name_list
    except:
        acsm.show_fundamental_operation_exception_message('We return the original dataframe because of unexpected change column name errors.')
    return result


def change_dataframe_column_name_and_select_only_existing_and_related_columns(df, column_name_dict):  # tested
    result = df
    try:
        new_df = change_dataframe_column_name(df, column_name_dict)
        result = new_df[list(set(column_name_dict.values()).intersection(set(new_df.columns)))]
    except:
        acsm.show_fundamental_operation_exception_message('We return the original dataframe because of unexpected errors.')
    return result


def get_duplicated_index_removed_with_the_first_df(original_df):
    return original_df[~original_df.index.duplicated(keep='first')]


def set_wide_print_setting():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', 15)


def get_df_with_given_index_list(df, given_list):
    selected_list = []
    for item in given_list:
        if item in df.index:
            selected_list.append(item)
    return df.loc[selected_list, ]


def get_df_from_csv_file(file_name, sep=','):
    try:
        return pd.read_csv(file_name, sep=sep)
    except:
        acsm.show_fundamental_operation_exception_message('We return the null dataframe because of unexpected errors.')
        return get_empty_data_frame()


def get_related_past_df(past_df, new_raw_df):
    index_list = []
    for index in past_df.index:
        if index in new_raw_df.index:
            index_list.append(index)
    return past_df.loc[index_list, ]


def get_appended_column_name_df(original_df, append_text):
    new_column_name_list = []
    for column_name in original_df.columns:
        new_column_name_list.append(append_text + ' ' + column_name)
    original_df.columns = new_column_name_list
    return original_df

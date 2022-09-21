import json
import pandas as pd
import pickle
import os
import shutil
import api.common.system.message as acsm
import api.common.data_type_operation.check_data_type as acdtocdt


def check_file_existence(file_path):  # tested
    if acdtocdt.whether_string(file_path):
        return os.path.isfile(file_path)
    else:
        return False


def check_folder_existence(folder_path):  # tested
    if acdtocdt.whether_string(folder_path):
        return os.path.isdir(folder_path)
    else:
        return False


def copy_file(source_file_path, destine_file_path):  # tested
    try:
        shutil.copy2(source_file_path, destine_file_path)
    except:
        acsm.show_fundamental_operation_exception_message('Fail to copy due to unexpected errors[' + str(source_file_path) + ', ' + str(destine_file_path) + '].')


def delete_file(file_path):  # tested
    if check_file_existence(file_path):
        os.remove(file_path)


def get_folder_path(file_path):
    try:
        letter_index1 = file_path.rfind('/')
        letter_index2 = file_path.rfind('\\')
        if (letter_index1 == -1) & (letter_index2 == -1):
            return ''
        else:
            return file_path[:max(letter_index1, letter_index2)]
    except:
        acsm.show_fundamental_operation_exception_message('Fail to get path information due to unexpected errors.')
        return ''


def make_all_related_folders(folder_path):
    try:
        if folder_path != '':
            os.makedirs(folder_path)
    except:
        acsm.show_fundamental_operation_exception_message('Fail to generate all the related folders due to unexpected errors.')


def make_all_related_folders_for_a_given_file_path(file_path):
    make_all_related_folders(get_folder_path(file_path))


def delete_file_in_the_current_folder(folder_path):  # tested
    try:
        make_all_related_folders_for_a_given_file_path(folder_path + '/test.txt')
        file_folder_list = os.listdir(folder_path)
        for file_folder in file_folder_list:
            file_name = folder_path + '/' + file_folder
            delete_file(file_name)
    except:
        acsm.show_fundamental_operation_exception_message('Fail to delete files in the given folder level due to unexpected errors.')


def delete_file_inside_folder(folder_path):  # tested
    try:
        delete_file_in_the_current_folder(folder_path)
        file_folder_list = os.listdir(folder_path)
        for file_folder in file_folder_list:
            path = folder_path + '/' + file_folder
            if check_folder_existence(path):
                delete_file_inside_folder(path)
    except:
        acsm.show_fundamental_operation_exception_message('Fail to delete files insider all the sub-folders due to unexpected errors.')


def read_file_into_list(file_path):
    try:
        if acdtocdt.whether_string(file_path):
            file = open(file_path)
            lines = file.readlines()
            result = []
            for line in lines:
                result.append(line[:-1])
            return result
        else:
            acsm.show_fundamental_operation_exception_message('The file path passed is not a string ' + str(file_path))
            return []
    except:
        acsm.show_fundamental_operation_exception_message('Fail to read file due to unexpected errors.')
        return []


def read_file_into_set(file_path):  # tested
    return set(read_file_into_list(file_path))


def load_json_file_as_dict(file_path):  # tested
    try:
        if check_file_existence(file_path):
            result = json.load(open(file_path))
        else:
            acsm.show_fundamental_operation_exception_message('We will return an empty dictionary due to non-existing file:' + str(file_path))
            result = {}
    except:
        acsm.show_fundamental_operation_exception_message('We will return an empty dictionary due to unexpected errors.')
        result = {}
    return result


def save_dict_as_json_file(dict_data, file_path):  # tested
    try:
        make_all_related_folders_for_a_given_file_path(file_path)
        json.dump(dict_data, open(file_path, 'w'))
        content = open(file_path, 'r').read().replace(',', ',\n')
        open(file_path, 'w').write(content)
    except:
        acsm.show_fundamental_operation_exception_message('We have unexpected errors to save json file: ' + str(file_path))


def update_json_file(file_path, updating_dict_data):  # tested
    json_dict = load_json_file_as_dict(file_path)
    try:
        for key in updating_dict_data:
            json_dict[key] = updating_dict_data[key]
    except:
        acsm.show_fundamental_operation_exception_message('We have unexpected errors to update json file with dict ' + str(updating_dict_data))
    save_dict_as_json_file(json_dict, file_path)


'''


def save_pickle_data(data, file_name, whether_save_csv=False):  # tested
    try:
        if isinstance(file_name, str):
            generate_folder_for_file(file_name)
            pickle_file = open(file_name, 'wb')
            pickle.dump(data, pickle_file)
            pickle_file.close()
            if whether_save_csv:
                if isinstance(data, pd.DataFrame):
                    data.to_csv(file_name+'.csv')
                else:
                    asm.show_exception_message('We have trouble saving ' + str(file_name) + '.csv because the variable is not a dataframe.')
        else:
            asm.show_exception_message('We have trouble saving ' + str(file_name) + '.csv because the file name is not a string.')
    except:
        asm.show_exception_message('We have trouble saving ' + str(file_name) + '.csv due to unexpected errors.')


def load_pickle_data(file_name):  # tested
    pickle_data = pd.DataFrame([])
    try:
        if isinstance(file_name, str):
            if check_file_existence(file_name):
                pickle_file = open(file_name, 'rb')
                pickle_data = pickle.load(pickle_file)
                pickle_file.close()
            else:
                asm.show_exception_message('We will return a null dataframe due to non-existing file:' + str(file_name))
        else:
            asm.show_exception_message('We will return a null dataframe because the file name is not a string.')
    except:
        asm.show_exception_message('We will return a null dataframe due to unexpected errors.')
    return pickle_data


def load_pickle_data_dict(file_name):  # tested
    data = pd.DataFrame([])
    whether_has_file = False
    try:
        if isinstance(file_name, str):
            if check_file_existence(file_name):
                data = load_pickle_data(file_name)
                whether_has_file = True
            else:
                asm.show_exception_message('We will return False value due to non-existing file: '+str(file_name))
        else:
            asm.show_exception_message('We will return False value because the file name is not a string.')
    except:
        asm.show_exception_message('We will return False value due to unexpected errors.')
    return {'whether_has_file': whether_has_file, 'data': data}


def save_excel_file(df, file_name):  # tested
    try:
        if isinstance(file_name, str):
            if isinstance(df, pd.DataFrame):
                generate_folder_for_file(file_name)
                writer = pd.ExcelWriter(file_name+'.xlsx', engine='xlsxwriter')
                df.to_excel(writer, sheet_name='sheet1')
                workbook = writer.book
                worksheet = writer.sheets['sheet1']
                worksheet.freeze_panes(1, 1)
                worksheet.autofilter(0, 0, len(df), len(df.columns))
                header_format = workbook.add_format({'bold': True, 'text_wrap': True, 'align': 'center', 'valign': 'vcenter', 'shrink': True, 'fg_color': '#7ccbfc', 'border': 1})
                for col_num, value in enumerate(df.columns.values):
                    worksheet.write(0, col_num+1, value, header_format)
                writer.save()
            else:
                asm.show_exception_message('We have trouble saving excel file because the variable is not a dataframe.')
        else:
            asm.show_exception_message('We have trouble saving excel file because the file name is not a string.')
    except:
        asm.show_exception_message('We have trouble saving excel file due to unexpected errors.')




def generate_summary_df_in_the_folder(folder_name):  # tested
    try:
        file_folder_list = os.listdir(folder_name)
        df_list = []
        for file_folder in file_folder_list:
            file_name = folder_name+'/'+file_folder
            if os.path.isfile(file_name):
                df_list.append(load_pickle_data(file_name))
        result = pd.DataFrame([])
        if len(df_list) > 0:
            result = pd.concat(df_list)
        return result
    except:
        asm.show_exception_message('We will return a null dataframe due to unexpected errors to generate summary df from the folder ' + str(folder_name))
        return pd.DataFrame([])


def get_index_list(df_file_name):  # tested
    try:
        return sorted(list(set(load_pickle_data(df_file_name).index)))
    except:
        asm.show_exception_message('We will return an empty list due to unexpected errors for the df file ' + str(df_file_name))
        return []


def save_given_source_information_df_with_overwrite(ticker, filename_function, retrieve_df_function, whether_save_csv=False):  # tested
    try:
        given_source_information_df = retrieve_df_function(ticker)
        if len(given_source_information_df) != 0:
            save_pickle_data(given_source_information_df, filename_function(ticker), whether_save_csv)
        else:
            print('Information for ' + str(ticker) + ' is not saved for the empty dataframe retrieved with ' + str(retrieve_df_function))
    except:
        asm.show_exception_message('Information for ' + str(ticker) + ' is not updated due to unexpected errors.')


def save_given_source_information_df_without_overwrite(ticker, filename_function, retrieve_df_function, whether_save_csv=False):  # tested
    try:
        if not load_pickle_data_dict(filename_function(ticker))['whether_has_file']:
            save_given_source_information_df_with_overwrite(ticker, filename_function, retrieve_df_function, whether_save_csv)
    except:
        asm.show_exception_message('Information for ' + str(ticker) + ' is not updated due to unexpected errors.')


def update_ticker_list_df_based_on_generated_file(filename_function_for_each_ticker, filename_function_for_ticker_list, currency):  # tested
    try:
        previous_ticker_df = load_pickle_data(filename_function_for_ticker_list())
        current_ticker_list = []
        for ticker in previous_ticker_df.index:
            if check_file_existence(filename_function_for_each_ticker(ticker, currency)):
                current_ticker_list.append(ticker)
        current_ticker_df = previous_ticker_df.loc[current_ticker_list, ]
        save_pickle_data(current_ticker_df, filename_function_for_ticker_list(), True)
    except:
        asm.show_exception_message('The ticker list df is not updated due to unexpected errors.')
'''

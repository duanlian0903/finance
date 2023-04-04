import json
import os
import pandas as pd
import pickle
import shutil
import api.common.system.message as acsm
import api.common.data_type_operation.check_data_type as acdtocdt
import zipfile


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


def get_file_folder_list(folder_path):
    try:
        return os.listdir(folder_path)
    except:
        acsm.show_fundamental_operation_exception_message('Fail to get file and folder list in the given folder due to unexpected errors.')
        return []


def get_file_list(folder_path):
    file_folder_list = get_file_folder_list(folder_path)
    file_list = []
    for file_folder in file_folder_list:
        if check_file_existence(folder_path + '/' + file_folder):
            file_list.append(file_folder)
    return file_list


def get_folder_list(folder_path):
    file_folder_list = get_file_folder_list(folder_path)
    folder_list = []
    for file_folder in file_folder_list:
        if check_folder_existence(folder_path + '/' + file_folder):
            folder_list.append(file_folder)
    return folder_list


def delete_file_in_the_current_folder(folder_path):  # tested
    try:
        make_all_related_folders_for_a_given_file_path(folder_path + '/test.txt')
        file_list = get_file_list(folder_path)
        for file in file_list:
            file_name = folder_path + '/' + file
            delete_file(file_name)
    except:
        acsm.show_fundamental_operation_exception_message('Fail to delete files in the given folder level due to unexpected errors.')


def delete_file_inside_folder(folder_path):  # tested
    try:
        delete_file_in_the_current_folder(folder_path)
        folder_list = get_folder_list(folder_path)
        for folder in folder_list:
            path = folder_path + '/' + folder
            delete_file_inside_folder(path)
    except:
        acsm.show_fundamental_operation_exception_message('Fail to delete files insider all the sub-folders due to unexpected errors.')


def load_txt_file_as_list(file_path):
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


def load_txt_file_as_set(file_path):  # tested
    return set(load_txt_file_as_list(file_path))


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


def load_csv_file_as_pandas_dataframe(file_path, sep=','):
    try:
        return pd.read_csv(file_path, sep=sep)
    except:
        acsm.show_fundamental_operation_exception_message('We have unexpected errors to load pandas dataframe from csv file ' + str(file_path))
        return pd.DataFrame([])


def save_pickle_data(data, file_path, whether_save_csv=False):  # tested
    try:
        if acdtocdt.whether_string(file_path):
            make_all_related_folders_for_a_given_file_path(file_path)
            pickle_file = open(file_path, 'wb')
            pickle.dump(data, pickle_file)
            pickle_file.close()
            if whether_save_csv:
                if acdtocdt.whether_pandas_dataframe(data):
                    data.to_csv(file_path + '.csv')
                else:
                    acsm.show_fundamental_operation_exception_message('We have trouble saving ' + str(file_path) + '.csv because the variable is not a dataframe.')
        else:
            acsm.show_fundamental_operation_exception_message('We have trouble saving ' + str(file_path) + '.csv because the file name is not a string.')
    except:
        acsm.show_fundamental_operation_exception_message('We have trouble saving ' + str(file_path) + '.csv due to unexpected errors.')


def load_pickle_data_as_dict(file_path):  # tested
    data = pd.DataFrame([])
    whether_has_file = False
    try:
        if acdtocdt.whether_string(file_path):
            if check_file_existence(file_path):
                whether_has_file = True
                pickle_file = open(file_path, 'rb')
                data = pickle.load(pickle_file)
                pickle_file.close()
            else:
                acsm.show_fundamental_operation_exception_message('We will return False value due to non-existing file: ' + str(file_path))
        else:
            acsm.show_fundamental_operation_exception_message('We will return False value because the file name is not a string.')
    except:
        acsm.show_fundamental_operation_exception_message('We will return empty dataframe due to unexpected errors.')
    return {'whether_has_file': whether_has_file, 'data': data}


def load_pickle_data(file_path):  # tested
    return load_pickle_data_as_dict(file_path)['data']


def save_excel_file(df, file_path):  # tested
    try:
        if acdtocdt.whether_string(file_path):
            if acdtocdt.whether_pandas_dataframe(df):
                make_all_related_folders_for_a_given_file_path(file_path)
                writer = pd.ExcelWriter(file_path + '.xlsx', engine='xlsxwriter')
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
                acsm.show_fundamental_operation_exception_message('We have trouble saving excel file because the variable is not a dataframe.')
        else:
            acsm.show_fundamental_operation_exception_message('We have trouble saving excel file because the file name is not a string.')
    except:
        acsm.show_fundamental_operation_exception_message('We have trouble saving excel file due to unexpected errors.')


def save_file(content, file_path, whether_binary=True):
    try:
        if acdtocdt.whether_string(file_path):
            make_all_related_folders_for_a_given_file_path(file_path)
            if whether_binary:
                file = open(file_path, 'wb')
            else:
                file = open(file_path, 'wt')
            file.write(content)
            file.close()
        else:
            acsm.show_fundamental_operation_exception_message('We have trouble saving binary content because the file name is not a string.')
    except:
        acsm.show_fundamental_operation_exception_message('We have trouble saving binary content due to unexpected errors.')


def unzip_zip_file(file_path, folder_path):
    try:
        if acdtocdt.whether_string(file_path) & acdtocdt.whether_string(folder_path):
            z_object = zipfile.ZipFile(file_path, 'r')
            z_object.extractall(folder_path)
        else:
            acsm.show_fundamental_operation_exception_message('We have trouble unzipping files because the file or folder name is not a string.')
    except:
        acsm.show_fundamental_operation_exception_message('We have trouble unzipping files due to unexpected errors.')


'''
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

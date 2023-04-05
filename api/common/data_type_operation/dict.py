import api.common.data_type_operation.check_data_type as acdtocdt


def merge_dict(dict_original, dict_update):
    for key, value in dict_update.items():
        if acdtocdt.whether_dict(value):
            dict_original[key] = merge_dict(dict_original.get(key, {}), value)
        else:
            dict_original[key] = dict_update[key]
    return dict_original

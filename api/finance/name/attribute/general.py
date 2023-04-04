import api.common.data_type_operation.check_data_type as acdtocdt


def append_prefix(attribute_name, prefix):
    return str(prefix) + ' ' + str(attribute_name)


def append_prefix_list(attribute_name, prefix_list):
    final_attribute_name = attribute_name
    if acdtocdt.whether_list(prefix_list):
        for prefix in prefix_list:
            final_attribute_name = append_prefix(final_attribute_name, prefix)
    return final_attribute_name

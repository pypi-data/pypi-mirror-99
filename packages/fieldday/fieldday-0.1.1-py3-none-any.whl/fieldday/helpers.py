def rename_keys(field_dict: dict, key_replacement_map: dict):
    """ Replaces keys in a dictionary according to a key replacement map """
    for key in list(field_dict.keys()):
        if key in key_replacement_map:
            field_dict[key_replacement_map[key]] = field_dict.pop(key)


def encode_field(field):
    """ for JSON.dumps """
    return field.encode()


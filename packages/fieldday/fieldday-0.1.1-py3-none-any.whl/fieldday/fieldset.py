import json
import fieldday.helpers as helpers


class FieldSet(dict):
    """
    A set (dict) of fields.  If field_types is provided, this class will store the set as
    a dict of field types.
    The built-in methods can provide the user with two versions of the field values:
        1. Encoded: This is the encoded JSON version of the field set, for transmission. Accessed with encode().
        2. Decoded: This is the human-readable version.  Accessed with the str() or print() methods.
    Examples:

    """

    def __init__(self, input_field_set, rename_dict=None, field_types=None):
        """
        Instantiate a FieldSet from an encoded list.
        Nominally, decode from a JSON string, but also can work from a `dict`.
        Args:
            input_field_set (str, dict): set of input fields
            rename_dict (dict): dict of field names to rename (key is original field name)
            field_types (dict): set of tuples (field types, kwargs) (key is renamed field name)
        """
        if isinstance(input_field_set, str):
            # assume it's a JSON object (an unordered collection of name–value pairs)
            field_dict = json.loads(input_field_set)
        else:
            if isinstance(input_field_set, dict):
                field_dict = input_field_set.copy()
            else:
                raise ValueError('input is not a JSON object or dict')
        if rename_dict is not None:
            helpers.rename_keys(field_dict, rename_dict)
        if field_types is not None:
            field_dict = self.load_encoded_dict(field_dict, field_types)
        super().__init__(field_dict)

    def encode(self):
        """
        Returns: self as a json string of encoded values - can then json.load() into a dict (key is field name)
        """
        return json.dumps(self, default=lambda f: f.encode())

    @staticmethod
    def load_encoded_dict(raw_dict, fieldtypes):
        """ load an encoded dictionary and return a dictionary of Fields """
        newdict = {}
        for key, val in raw_dict.items():
            if key in fieldtypes:
                fielddef = fieldtypes[key]
                newdict[key] = fielddef[0](val, **fielddef[1])
            else:
                newdict[key] = val
        return newdict

    def modify_fields(self, field_modifier_dict):
        """ modify specific fields in this set in place with modifier functions
        Args:
            field_modifier_dict (dict): a dict of modifier functions (key is field names to modify)
        """
        for key, modifier in field_modifier_dict.items():
            if key in self:
                field_modifier_dict[key](self[key])

    def modify_types(self, types_modifier_list):
        """ modify specific field types in this set in place with modifier functions if a criteria is met
        Args:
            types_modifier_list (list): a list of lists or tuples (field_type, modifier, criteria_checker)
                field_type: the type of field to modify
                modifier: a reference to the method that will perform the modification
                criteria_checker: a reference to the method that must return True for the modification to happen
        """
        for item in types_modifier_list:
            for key, val in self.items():
                if isinstance(val, item[0]):
                    if len(item) > 2:
                        meetscriteria = item[2](self[key])
                    else:
                        meetscriteria = True
                    if meetscriteria:
                        item[1](self[key])

    def cast_fields(self, new_field_types):
        """ modify specific fields in this set in place with modifier functions
        Args:
            new_field_types (dict): a dict of new field types (key is field names to modify)
        """
        for key, modifier in new_field_types.items():
            if key in self:
                self[key] = new_field_types[key](self[key])

    def __str__(self):
        # use .join() to avoid a newline at the end of the list
        slist = []
        for key in self:
            slist.append(key + ': ' + str(self[key]))
        return '\n'.join(slist)

    # def replace_fields(self, field_convert_dict):
    #     """ Converty """
    #     pass
    #
    # def replace_types(self, field_types_dict):
    #     """ Modify a field set using a list of types """
    #     pass

    """dot.notation access to dictionary attributes"""
    __getattr__ = dict.get
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__

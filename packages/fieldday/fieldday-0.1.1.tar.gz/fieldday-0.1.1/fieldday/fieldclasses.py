from fieldday import QTY_CAPABLE
if QTY_CAPABLE:
    from fieldday import ureg, Q_  # from pint via __init__.py


class Field:
    def __init__(self, value, desc='', units='', fmt='', **otherkwargs: object):
        """ Base class for a data item.
        This class and its subclasses are meant for maniupulating fields passed around an IoT system, e.g. MQTT as
        JSON payloads.  They provide the means for:
        - decoding from numeric or string values via their constructor,
        - encoding to numeric or string values via an encode() method, and
        - formatting output in various ways
        This class and its subclasses should always be able to construct (decode) from a string representation.
        In cases where the field's magnitude can be represented as a more compact numeric value, the encoder
        should generate a numeric value and construct (decode) from a numeric value as well as a string.
        This class is meant to be subclassed.  For example, you can add a convert() method to convert
        a class to different units ot to a different type of field class.
        Besides `value`, `desc`, and `units`, other attributes can be user-defined with `otherkwargs`.
        Args:
            value (obj): stored data value (can be any object)
            desc (str): a short description of the field
            units (str): measurement units (if any)
            fmt (str): format string for output of __str__ magnitude component only
            otherkwargs (dict): dynamically user-defined application-specific attributes
        """
        self.value = value
        self.desc = desc
        self.units = units
        self.fmt = fmt
        self.__dict__.update(otherkwargs) # anything else

    def encode(self):
        """
        Returns: The encoded field as a JSON-encodable object and the most compact object that that can be decoded
        by the constructor
        """
        return self.value

    def __str__(self):
        """
        Returns: the encoded value as a string with a specific format if provided
        """
        s = ''
        if self.desc:
            s = s + self.desc + ': '
        s = s + str(self.str_value())
        if self.units:
            s = s + ' ' + self.units
        return s

    def str_value(self):
        s = '{0'
        if self.fmt:
            s = s + ':' + self.fmt
        s = s + '}'
        return s.format(self.value)

    def __repr__(self):
        return f"{self.__class__.__name__}({self.encode()!r}, {self.desc!r}, {self.units!r}, {self.fmt!r})"


class FieldFloat(Field):
    """ Basic numeric (`float`) field """
    def __init__(self, encoded_value, **kwargs):
        super().__init__(float(encoded_value), **kwargs)


class FieldInt(Field):
    """ Basic `int` field
    optional keyword arguments:
        base (int): if encoded_value is a string, this can represent the base as second parameter of int()
    """
    def __init__(self, encoded_value, **kwargs):
        if isinstance(encoded_value, str):
            base = kwargs.pop('base', 0)
            value = int(encoded_value, base)
        else:
            value = int(encoded_value)
        super().__init__(value, **kwargs)


class FieldStr(Field):
    """ Basic numeric (`float`) field """
    def __init__(self, encoded_value, **kwargs):
        super().__init__(str(encoded_value), **kwargs)



class FieldQty(Field):
    """ Field in which the units are tied to the encoded value.
    The units attribute of instances of this class will always be empty.  The advantage of using this
    field type is that the units can be changed upstream and are not locked into the field type metadata.
    Uses a `pint.UnitRegistry.Quantity` as the underlying data store so we can do unit conversions easily """
    def __init__(self, encoded_value, **kwargs):
        if not QTY_CAPABLE:
            raise Exception("Not Qty-enabled.  You probably need to install Pint.")
        if isinstance(encoded_value, FieldFloat) or isinstance(encoded_value, FieldInt):
            super().__init__(Q_(str(encoded_value.value)+" "+str(encoded_value.units)),
                             desc=encoded_value.desc, units='', fmt=encoded_value.fmt)
        else:
            super().__init__(Q_(encoded_value), **kwargs)
        if 'units' in kwargs:
            raise ValueError("Units are tied to FieldQty values so the desc attribute should not be used")

    def encode(self):
        return str(self.value)

    def str_value(self):
        return ('{0:' + self.fmt + '} {1}').format(self.value.magnitude, str(self.value.units))

    def str_mag(self):
        return str(self.value.magnitude)

    def str_units(self):
        return str(self.value.units)

    def convert(self, new_units, new_fmt=None):
        """ Convert units using `pint` to intelligently transform to a new units string """
        self.value.ito(ureg.parse_units(new_units))
        if new_fmt is not None:
            self.fmt = new_fmt




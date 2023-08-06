try:
    from pint import UnitRegistry
    QTY_CAPABLE = True
    # instantiate the pint registry only once
    ureg = UnitRegistry()
    Q_ = ureg.Quantity
    # import the other internal modules afterwords because they import the instances ureg and Q_
except ImportError as e:
    QTY_CAPABLE = False

from fieldday.fieldclasses import *
from fieldday.helpers import *
from fieldday.fieldset import FieldSet

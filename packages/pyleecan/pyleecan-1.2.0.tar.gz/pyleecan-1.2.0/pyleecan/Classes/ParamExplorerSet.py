# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Simulation/ParamExplorerSet.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Simulation/ParamExplorerSet
"""

from os import linesep
from sys import getsizeof
from logging import getLogger
from ._check import check_var, raise_
from ..Functions.get_logger import get_logger
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .ParamExplorer import ParamExplorer

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Simulation.ParamExplorerSet.get_value import get_value
except ImportError as error:
    get_value = error

try:
    from ..Methods.Simulation.ParamExplorerSet.as_dict import as_dict
except ImportError as error:
    as_dict = error


from ntpath import basename
from os.path import isfile
from ._check import CheckTypeError
import numpy as np
import random
from ._check import InitUnKnowClassError


class ParamExplorerSet(ParamExplorer):
    """Abstract class for the multi-simulation"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Simulation.ParamExplorerSet.get_value
    if isinstance(get_value, ImportError):
        get_value = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use ParamExplorerSet method get_value: " + str(get_value)
                )
            )
        )
    else:
        get_value = get_value
    # cf Methods.Simulation.ParamExplorerSet.as_dict
    if isinstance(as_dict, ImportError):
        as_dict = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use ParamExplorerSet method as_dict: " + str(as_dict)
                )
            )
        )
    else:
        as_dict = as_dict
    # save and copy methods are available in all object
    save = save
    copy = copy
    # get_logger method is available in all object
    get_logger = get_logger

    def __init__(
        self,
        value=-1,
        name="",
        symbol="",
        unit="",
        setter=None,
        init_dict=None,
        init_str=None,
    ):
        """Constructor of the class. Can be use in three ways :
        - __init__ (arg1 = 1, arg3 = 5) every parameters have name and default values
            for pyleecan type, -1 will call the default constructor
        - __init__ (init_dict = d) d must be a dictionnary with property names as keys
        - __init__ (init_str = s) s must be a string
        s is the file path to load

        ndarray or list can be given for Vector and Matrix
        object or dict can be given for pyleecan Object"""

        if init_str is not None:  # Load from a file
            init_dict = load_init_dict(init_str)[1]
        if init_dict is not None:  # Initialisation by dict
            assert type(init_dict) is dict
            # Overwrite default value with init_dict content
            if "value" in list(init_dict.keys()):
                value = init_dict["value"]
            if "name" in list(init_dict.keys()):
                name = init_dict["name"]
            if "symbol" in list(init_dict.keys()):
                symbol = init_dict["symbol"]
            if "unit" in list(init_dict.keys()):
                unit = init_dict["unit"]
            if "setter" in list(init_dict.keys()):
                setter = init_dict["setter"]
        # Set the properties (value check and convertion are done in setter)
        self.value = value
        # Call ParamExplorer init
        super(ParamExplorerSet, self).__init__(
            name=name, symbol=symbol, unit=unit, setter=setter
        )
        # The class is frozen (in ParamExplorer init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        ParamExplorerSet_str = ""
        # Get the properties inherited from ParamExplorer
        ParamExplorerSet_str += super(ParamExplorerSet, self).__str__()
        ParamExplorerSet_str += (
            "value = "
            + linesep
            + str(self.value).replace(linesep, linesep + "\t")
            + linesep
        )
        return ParamExplorerSet_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from ParamExplorer
        if not super(ParamExplorerSet, self).__eq__(other):
            return False
        if other.value != self.value:
            return False
        return True

    def compare(self, other, name="self"):
        """Compare two objects and return list of differences"""

        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()

        # Check the properties inherited from ParamExplorer
        diff_list.extend(super(ParamExplorerSet, self).compare(other, name=name))
        if other._value != self._value:
            diff_list.append(name + ".value")
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from ParamExplorer
        S += super(ParamExplorerSet, self).__sizeof__()
        if self.value is not None:
            for value in self.value:
                S += getsizeof(value)
        return S

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.value = None
        # Set to None the properties inherited from ParamExplorer
        super(ParamExplorerSet, self)._set_None()

    def _get_value(self):
        """getter of value"""
        return self._value

    def _set_value(self, value):
        """setter of value"""
        if type(value) is int and value == -1:
            value = list()
        check_var("value", value, "list")
        self._value = value

    value = property(
        fget=_get_value,
        fset=_set_value,
        doc=u"""List containing the different parameter values to explore

        :Type: list
        """,
    )

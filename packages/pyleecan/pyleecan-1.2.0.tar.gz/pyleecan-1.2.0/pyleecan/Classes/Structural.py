# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Simulation/Structural.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Simulation/Structural
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
from ._frozen import FrozenClass

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Simulation.Structural.run import run
except ImportError as error:
    run = error

try:
    from ..Methods.Simulation.Structural.comp_axes import comp_axes
except ImportError as error:
    comp_axes = error


from ._check import InitUnKnowClassError


class Structural(FrozenClass):
    """Structural module abstract object"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Simulation.Structural.run
    if isinstance(run, ImportError):
        run = property(
            fget=lambda x: raise_(
                ImportError("Can't use Structural method run: " + str(run))
            )
        )
    else:
        run = run
    # cf Methods.Simulation.Structural.comp_axes
    if isinstance(comp_axes, ImportError):
        comp_axes = property(
            fget=lambda x: raise_(
                ImportError("Can't use Structural method comp_axes: " + str(comp_axes))
            )
        )
    else:
        comp_axes = comp_axes
    # save and copy methods are available in all object
    save = save
    copy = copy
    # get_logger method is available in all object
    get_logger = get_logger

    def __init__(
        self, logger_name="Pyleecan.Structural", init_dict=None, init_str=None
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
            if "logger_name" in list(init_dict.keys()):
                logger_name = init_dict["logger_name"]
        # Set the properties (value check and convertion are done in setter)
        self.parent = None
        self.logger_name = logger_name

        # The class is frozen, for now it's impossible to add new properties
        self._freeze()

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        Structural_str = ""
        if self.parent is None:
            Structural_str += "parent = None " + linesep
        else:
            Structural_str += "parent = " + str(type(self.parent)) + " object" + linesep
        Structural_str += 'logger_name = "' + str(self.logger_name) + '"' + linesep
        return Structural_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False
        if other.logger_name != self.logger_name:
            return False
        return True

    def compare(self, other, name="self"):
        """Compare two objects and return list of differences"""

        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()
        if other._logger_name != self._logger_name:
            diff_list.append(name + ".logger_name")
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object
        S += getsizeof(self.logger_name)
        return S

    def as_dict(self, **kwargs):
        """
        Convert this object in a json serializable dict (can be use in __init__).
        Optional keyword input parameter is for internal use only
        and may prevent json serializability.
        """

        Structural_dict = dict()
        Structural_dict["logger_name"] = self.logger_name
        # The class name is added to the dict for deserialisation purpose
        Structural_dict["__class__"] = "Structural"
        return Structural_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.logger_name = None

    def _get_logger_name(self):
        """getter of logger_name"""
        return self._logger_name

    def _set_logger_name(self, value):
        """setter of logger_name"""
        check_var("logger_name", value, "str")
        self._logger_name = value

    logger_name = property(
        fget=_get_logger_name,
        fset=_set_logger_name,
        doc=u"""Name of the logger to use

        :Type: str
        """,
    )

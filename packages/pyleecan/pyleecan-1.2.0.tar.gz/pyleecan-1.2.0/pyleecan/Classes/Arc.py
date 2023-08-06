# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Geometry/Arc.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Geometry/Arc
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
from .Line import Line

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Geometry.Arc.draw_FEMM import draw_FEMM
except ImportError as error:
    draw_FEMM = error

try:
    from ..Methods.Geometry.Arc.intersect_line import intersect_line
except ImportError as error:
    intersect_line = error

try:
    from ..Methods.Geometry.Arc.is_on_line import is_on_line
except ImportError as error:
    is_on_line = error

try:
    from ..Methods.Geometry.Arc.split_line import split_line
except ImportError as error:
    split_line = error

try:
    from ..Methods.Geometry.Arc.comp_distance import comp_distance
except ImportError as error:
    comp_distance = error

try:
    from ..Methods.Geometry.Arc.plot import plot
except ImportError as error:
    plot = error


from ._check import InitUnKnowClassError


class Arc(Line):
    """Abstract class for arc"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Geometry.Arc.draw_FEMM
    if isinstance(draw_FEMM, ImportError):
        draw_FEMM = property(
            fget=lambda x: raise_(
                ImportError("Can't use Arc method draw_FEMM: " + str(draw_FEMM))
            )
        )
    else:
        draw_FEMM = draw_FEMM
    # cf Methods.Geometry.Arc.intersect_line
    if isinstance(intersect_line, ImportError):
        intersect_line = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use Arc method intersect_line: " + str(intersect_line)
                )
            )
        )
    else:
        intersect_line = intersect_line
    # cf Methods.Geometry.Arc.is_on_line
    if isinstance(is_on_line, ImportError):
        is_on_line = property(
            fget=lambda x: raise_(
                ImportError("Can't use Arc method is_on_line: " + str(is_on_line))
            )
        )
    else:
        is_on_line = is_on_line
    # cf Methods.Geometry.Arc.split_line
    if isinstance(split_line, ImportError):
        split_line = property(
            fget=lambda x: raise_(
                ImportError("Can't use Arc method split_line: " + str(split_line))
            )
        )
    else:
        split_line = split_line
    # cf Methods.Geometry.Arc.comp_distance
    if isinstance(comp_distance, ImportError):
        comp_distance = property(
            fget=lambda x: raise_(
                ImportError("Can't use Arc method comp_distance: " + str(comp_distance))
            )
        )
    else:
        comp_distance = comp_distance
    # cf Methods.Geometry.Arc.plot
    if isinstance(plot, ImportError):
        plot = property(
            fget=lambda x: raise_(
                ImportError("Can't use Arc method plot: " + str(plot))
            )
        )
    else:
        plot = plot
    # save and copy methods are available in all object
    save = save
    copy = copy
    # get_logger method is available in all object
    get_logger = get_logger

    def __init__(self, label="", init_dict=None, init_str=None):
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
            if "label" in list(init_dict.keys()):
                label = init_dict["label"]
        # Set the properties (value check and convertion are done in setter)
        # Call Line init
        super(Arc, self).__init__(label=label)
        # The class is frozen (in Line init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        Arc_str = ""
        # Get the properties inherited from Line
        Arc_str += super(Arc, self).__str__()
        return Arc_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from Line
        if not super(Arc, self).__eq__(other):
            return False
        return True

    def compare(self, other, name="self"):
        """Compare two objects and return list of differences"""

        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()

        # Check the properties inherited from Line
        diff_list.extend(super(Arc, self).compare(other, name=name))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from Line
        S += super(Arc, self).__sizeof__()
        return S

    def as_dict(self, **kwargs):
        """
        Convert this object in a json serializable dict (can be use in __init__).
        Optional keyword input parameter is for internal use only
        and may prevent json serializability.
        """

        # Get the properties inherited from Line
        Arc_dict = super(Arc, self).as_dict(**kwargs)
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        Arc_dict["__class__"] = "Arc"
        return Arc_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        # Set to None the properties inherited from Line
        super(Arc, self)._set_None()

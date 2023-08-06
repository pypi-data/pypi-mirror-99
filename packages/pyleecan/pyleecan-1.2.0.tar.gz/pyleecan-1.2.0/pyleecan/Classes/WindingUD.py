# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Machine/WindingUD.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Machine/WindingUD
"""

from os import linesep
from sys import getsizeof
from logging import getLogger
from ._check import set_array, check_var, raise_
from ..Functions.get_logger import get_logger
from ..Functions.save import save
from ..Functions.copy import copy
from ..Functions.load import load_init_dict
from ..Functions.Load.import_class import import_class
from .Winding import Winding

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Machine.WindingUD.comp_connection_mat import comp_connection_mat
except ImportError as error:
    comp_connection_mat = error

try:
    from ..Methods.Machine.WindingUD.get_dim_wind import get_dim_wind
except ImportError as error:
    get_dim_wind = error


from numpy import array, array_equal
from ._check import InitUnKnowClassError
from .Conductor import Conductor


class WindingUD(Winding):
    """User defined winding"""

    VERSION = 1
    NAME = "User defined"

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Machine.WindingUD.comp_connection_mat
    if isinstance(comp_connection_mat, ImportError):
        comp_connection_mat = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use WindingUD method comp_connection_mat: "
                    + str(comp_connection_mat)
                )
            )
        )
    else:
        comp_connection_mat = comp_connection_mat
    # cf Methods.Machine.WindingUD.get_dim_wind
    if isinstance(get_dim_wind, ImportError):
        get_dim_wind = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use WindingUD method get_dim_wind: " + str(get_dim_wind)
                )
            )
        )
    else:
        get_dim_wind = get_dim_wind
    # save and copy methods are available in all object
    save = save
    copy = copy
    # get_logger method is available in all object
    get_logger = get_logger

    def __init__(
        self,
        user_wind_mat=None,
        is_reverse_wind=False,
        Nslot_shift_wind=0,
        qs=3,
        Ntcoil=7,
        Npcpp=2,
        type_connection=0,
        p=3,
        Lewout=0.015,
        conductor=-1,
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
            if "user_wind_mat" in list(init_dict.keys()):
                user_wind_mat = init_dict["user_wind_mat"]
            if "is_reverse_wind" in list(init_dict.keys()):
                is_reverse_wind = init_dict["is_reverse_wind"]
            if "Nslot_shift_wind" in list(init_dict.keys()):
                Nslot_shift_wind = init_dict["Nslot_shift_wind"]
            if "qs" in list(init_dict.keys()):
                qs = init_dict["qs"]
            if "Ntcoil" in list(init_dict.keys()):
                Ntcoil = init_dict["Ntcoil"]
            if "Npcpp" in list(init_dict.keys()):
                Npcpp = init_dict["Npcpp"]
            if "type_connection" in list(init_dict.keys()):
                type_connection = init_dict["type_connection"]
            if "p" in list(init_dict.keys()):
                p = init_dict["p"]
            if "Lewout" in list(init_dict.keys()):
                Lewout = init_dict["Lewout"]
            if "conductor" in list(init_dict.keys()):
                conductor = init_dict["conductor"]
        # Set the properties (value check and convertion are done in setter)
        self.user_wind_mat = user_wind_mat
        # Call Winding init
        super(WindingUD, self).__init__(
            is_reverse_wind=is_reverse_wind,
            Nslot_shift_wind=Nslot_shift_wind,
            qs=qs,
            Ntcoil=Ntcoil,
            Npcpp=Npcpp,
            type_connection=type_connection,
            p=p,
            Lewout=Lewout,
            conductor=conductor,
        )
        # The class is frozen (in Winding init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        WindingUD_str = ""
        # Get the properties inherited from Winding
        WindingUD_str += super(WindingUD, self).__str__()
        WindingUD_str += (
            "user_wind_mat = "
            + linesep
            + str(self.user_wind_mat).replace(linesep, linesep + "\t")
            + linesep
            + linesep
        )
        return WindingUD_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from Winding
        if not super(WindingUD, self).__eq__(other):
            return False
        if not array_equal(other.user_wind_mat, self.user_wind_mat):
            return False
        return True

    def compare(self, other, name="self"):
        """Compare two objects and return list of differences"""

        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()

        # Check the properties inherited from Winding
        diff_list.extend(super(WindingUD, self).compare(other, name=name))
        if not array_equal(other.user_wind_mat, self.user_wind_mat):
            diff_list.append(name + ".user_wind_mat")
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from Winding
        S += super(WindingUD, self).__sizeof__()
        S += getsizeof(self.user_wind_mat)
        return S

    def as_dict(self, **kwargs):
        """
        Convert this object in a json serializable dict (can be use in __init__).
        Optional keyword input parameter is for internal use only
        and may prevent json serializability.
        """

        # Get the properties inherited from Winding
        WindingUD_dict = super(WindingUD, self).as_dict(**kwargs)
        if self.user_wind_mat is None:
            WindingUD_dict["user_wind_mat"] = None
        else:
            WindingUD_dict["user_wind_mat"] = self.user_wind_mat.tolist()
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        WindingUD_dict["__class__"] = "WindingUD"
        return WindingUD_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.user_wind_mat = None
        # Set to None the properties inherited from Winding
        super(WindingUD, self)._set_None()

    def _get_user_wind_mat(self):
        """getter of user_wind_mat"""
        return self._user_wind_mat

    def _set_user_wind_mat(self, value):
        """setter of user_wind_mat"""
        if type(value) is int and value == -1:
            value = array([])
        elif type(value) is list:
            try:
                value = array(value)
            except:
                pass
        check_var("user_wind_mat", value, "ndarray")
        self._user_wind_mat = value

    user_wind_mat = property(
        fget=_get_user_wind_mat,
        fset=_set_user_wind_mat,
        doc=u"""user defined Winding matrix

        :Type: ndarray
        """,
    )

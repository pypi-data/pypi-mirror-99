# -*- coding: utf-8 -*-
# File generated according to Generator/ClassesRef/Mesh/MeshMat.csv
# WARNING! All changes made in this file will be lost!
"""Method code available at https://github.com/Eomys/pyleecan/tree/master/pyleecan/Methods/Mesh/MeshMat
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
from .Mesh import Mesh

# Import all class method
# Try/catch to remove unnecessary dependencies in unused method
try:
    from ..Methods.Mesh.MeshMat.get_point import get_point
except ImportError as error:
    get_point = error

try:
    from ..Methods.Mesh.MeshMat.get_cell import get_cell
except ImportError as error:
    get_cell = error

try:
    from ..Methods.Mesh.MeshMat.get_mesh_pv import get_mesh_pv
except ImportError as error:
    get_mesh_pv = error

try:
    from ..Methods.Mesh.MeshMat.get_cell_area import get_cell_area
except ImportError as error:
    get_cell_area = error

try:
    from ..Methods.Mesh.MeshMat.add_cell import add_cell
except ImportError as error:
    add_cell = error

try:
    from ..Methods.Mesh.MeshMat.get_vertice import get_vertice
except ImportError as error:
    get_vertice = error

try:
    from ..Methods.Mesh.MeshMat.get_point2cell import get_point2cell
except ImportError as error:
    get_point2cell = error

try:
    from ..Methods.Mesh.MeshMat.renum import renum
except ImportError as error:
    renum = error

try:
    from ..Methods.Mesh.MeshMat.find_cell import find_cell
except ImportError as error:
    find_cell = error

try:
    from ..Methods.Mesh.MeshMat.interface import interface
except ImportError as error:
    interface = error


from ._check import InitUnKnowClassError
from .CellMat import CellMat
from .PointMat import PointMat


class MeshMat(Mesh):
    """Gather the mesh storage format"""

    VERSION = 1

    # Check ImportError to remove unnecessary dependencies in unused method
    # cf Methods.Mesh.MeshMat.get_point
    if isinstance(get_point, ImportError):
        get_point = property(
            fget=lambda x: raise_(
                ImportError("Can't use MeshMat method get_point: " + str(get_point))
            )
        )
    else:
        get_point = get_point
    # cf Methods.Mesh.MeshMat.get_cell
    if isinstance(get_cell, ImportError):
        get_cell = property(
            fget=lambda x: raise_(
                ImportError("Can't use MeshMat method get_cell: " + str(get_cell))
            )
        )
    else:
        get_cell = get_cell
    # cf Methods.Mesh.MeshMat.get_mesh_pv
    if isinstance(get_mesh_pv, ImportError):
        get_mesh_pv = property(
            fget=lambda x: raise_(
                ImportError("Can't use MeshMat method get_mesh_pv: " + str(get_mesh_pv))
            )
        )
    else:
        get_mesh_pv = get_mesh_pv
    # cf Methods.Mesh.MeshMat.get_cell_area
    if isinstance(get_cell_area, ImportError):
        get_cell_area = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use MeshMat method get_cell_area: " + str(get_cell_area)
                )
            )
        )
    else:
        get_cell_area = get_cell_area
    # cf Methods.Mesh.MeshMat.add_cell
    if isinstance(add_cell, ImportError):
        add_cell = property(
            fget=lambda x: raise_(
                ImportError("Can't use MeshMat method add_cell: " + str(add_cell))
            )
        )
    else:
        add_cell = add_cell
    # cf Methods.Mesh.MeshMat.get_vertice
    if isinstance(get_vertice, ImportError):
        get_vertice = property(
            fget=lambda x: raise_(
                ImportError("Can't use MeshMat method get_vertice: " + str(get_vertice))
            )
        )
    else:
        get_vertice = get_vertice
    # cf Methods.Mesh.MeshMat.get_point2cell
    if isinstance(get_point2cell, ImportError):
        get_point2cell = property(
            fget=lambda x: raise_(
                ImportError(
                    "Can't use MeshMat method get_point2cell: " + str(get_point2cell)
                )
            )
        )
    else:
        get_point2cell = get_point2cell
    # cf Methods.Mesh.MeshMat.renum
    if isinstance(renum, ImportError):
        renum = property(
            fget=lambda x: raise_(
                ImportError("Can't use MeshMat method renum: " + str(renum))
            )
        )
    else:
        renum = renum
    # cf Methods.Mesh.MeshMat.find_cell
    if isinstance(find_cell, ImportError):
        find_cell = property(
            fget=lambda x: raise_(
                ImportError("Can't use MeshMat method find_cell: " + str(find_cell))
            )
        )
    else:
        find_cell = find_cell
    # cf Methods.Mesh.MeshMat.interface
    if isinstance(interface, ImportError):
        interface = property(
            fget=lambda x: raise_(
                ImportError("Can't use MeshMat method interface: " + str(interface))
            )
        )
    else:
        interface = interface
    # save and copy methods are available in all object
    save = save
    copy = copy
    # get_logger method is available in all object
    get_logger = get_logger

    def __init__(
        self, cell=-1, point=-1, label=None, dimension=2, init_dict=None, init_str=None
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
            if "cell" in list(init_dict.keys()):
                cell = init_dict["cell"]
            if "point" in list(init_dict.keys()):
                point = init_dict["point"]
            if "label" in list(init_dict.keys()):
                label = init_dict["label"]
            if "dimension" in list(init_dict.keys()):
                dimension = init_dict["dimension"]
        # Set the properties (value check and convertion are done in setter)
        self.cell = cell
        self.point = point
        # Call Mesh init
        super(MeshMat, self).__init__(label=label, dimension=dimension)
        # The class is frozen (in Mesh init), for now it's impossible to
        # add new properties

    def __str__(self):
        """Convert this object in a readeable string (for print)"""

        MeshMat_str = ""
        # Get the properties inherited from Mesh
        MeshMat_str += super(MeshMat, self).__str__()
        if len(self.cell) == 0:
            MeshMat_str += "cell = dict()" + linesep
        for key, obj in self.cell.items():
            tmp = self.cell[key].__str__().replace(linesep, linesep + "\t") + linesep
            MeshMat_str += "cell[" + key + "] =" + tmp + linesep + linesep
        if self.point is not None:
            tmp = self.point.__str__().replace(linesep, linesep + "\t").rstrip("\t")
            MeshMat_str += "point = " + tmp
        else:
            MeshMat_str += "point = None" + linesep + linesep
        return MeshMat_str

    def __eq__(self, other):
        """Compare two objects (skip parent)"""

        if type(other) != type(self):
            return False

        # Check the properties inherited from Mesh
        if not super(MeshMat, self).__eq__(other):
            return False
        if other.cell != self.cell:
            return False
        if other.point != self.point:
            return False
        return True

    def compare(self, other, name="self"):
        """Compare two objects and return list of differences"""

        if type(other) != type(self):
            return ["type(" + name + ")"]
        diff_list = list()

        # Check the properties inherited from Mesh
        diff_list.extend(super(MeshMat, self).compare(other, name=name))
        if (other.cell is None and self.cell is not None) or (
            other.cell is not None and self.cell is None
        ):
            diff_list.append(name + ".cell None mismatch")
        elif self.cell is None:
            pass
        elif len(other.cell) != len(self.cell):
            diff_list.append("len(" + name + "cell)")
        else:
            for key in self.cell:
                diff_list.extend(
                    self.cell[key].compare(other.cell[key], name=name + ".cell")
                )
        if (other.point is None and self.point is not None) or (
            other.point is not None and self.point is None
        ):
            diff_list.append(name + ".point None mismatch")
        elif self.point is not None:
            diff_list.extend(self.point.compare(other.point, name=name + ".point"))
        return diff_list

    def __sizeof__(self):
        """Return the size in memory of the object (including all subobject)"""

        S = 0  # Full size of the object

        # Get size of the properties inherited from Mesh
        S += super(MeshMat, self).__sizeof__()
        if self.cell is not None:
            for key, value in self.cell.items():
                S += getsizeof(value) + getsizeof(key)
        S += getsizeof(self.point)
        return S

    def as_dict(self, **kwargs):
        """
        Convert this object in a json serializable dict (can be use in __init__).
        Optional keyword input parameter is for internal use only
        and may prevent json serializability.
        """

        # Get the properties inherited from Mesh
        MeshMat_dict = super(MeshMat, self).as_dict(**kwargs)
        if self.cell is None:
            MeshMat_dict["cell"] = None
        else:
            MeshMat_dict["cell"] = dict()
            for key, obj in self.cell.items():
                if obj is not None:
                    MeshMat_dict["cell"][key] = obj.as_dict(**kwargs)
                else:
                    MeshMat_dict["cell"][key] = None
        if self.point is None:
            MeshMat_dict["point"] = None
        else:
            MeshMat_dict["point"] = self.point.as_dict(**kwargs)
        # The class name is added to the dict for deserialisation purpose
        # Overwrite the mother class name
        MeshMat_dict["__class__"] = "MeshMat"
        return MeshMat_dict

    def _set_None(self):
        """Set all the properties to None (except pyleecan object)"""

        self.cell = None
        if self.point is not None:
            self.point._set_None()
        # Set to None the properties inherited from Mesh
        super(MeshMat, self)._set_None()

    def _get_cell(self):
        """getter of cell"""
        if self._cell is not None:
            for key, obj in self._cell.items():
                if obj is not None:
                    obj.parent = self
        return self._cell

    def _set_cell(self, value):
        """setter of cell"""
        if type(value) is dict:
            for key, obj in value.items():
                if type(obj) is dict:
                    class_obj = import_class(
                        "pyleecan.Classes", obj.get("__class__"), "cell"
                    )
                    value[key] = class_obj(init_dict=obj)
        if type(value) is int and value == -1:
            value = dict()
        check_var("cell", value, "{CellMat}")
        self._cell = value

    cell = property(
        fget=_get_cell,
        fset=_set_cell,
        doc=u"""Storing connectivity

        :Type: {CellMat}
        """,
    )

    def _get_point(self):
        """getter of point"""
        return self._point

    def _set_point(self, value):
        """setter of point"""
        if isinstance(value, str):  # Load from file
            value = load_init_dict(value)[1]
        if isinstance(value, dict) and "__class__" in value:
            class_obj = import_class(
                "pyleecan.Classes", value.get("__class__"), "point"
            )
            value = class_obj(init_dict=value)
        elif type(value) is int and value == -1:  # Default constructor
            value = PointMat()
        check_var("point", value, "PointMat")
        self._point = value

        if self._point is not None:
            self._point.parent = self

    point = property(
        fget=_get_point,
        fset=_set_point,
        doc=u"""Storing nodes

        :Type: PointMat
        """,
    )

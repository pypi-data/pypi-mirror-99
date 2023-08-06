# -*- coding: utf-8 -*-


def get_point(self, indices=None):
    """Return a matrix of points coordinates.

    Parameters
    ----------
    self : Mesh
        an Mesh object
    indices : list
        Indices of the targeted points. If None, return all.
    is_indice: bool
        Option to return the points indices (useful for unsorted

    Returns
    -------
    coordinates: ndarray
        points coordinates
    indices : ndarray
        points indices

    """
    if indices is None:
        return self.point.coordinate
    else:
        if len(indices) == 0:
            return indices  # empty ndarray
        else:
            return self.point.coordinate[indices, :]

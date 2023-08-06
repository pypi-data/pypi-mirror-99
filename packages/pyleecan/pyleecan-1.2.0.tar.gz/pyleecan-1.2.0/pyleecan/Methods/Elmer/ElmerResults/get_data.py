# -*- coding: utf-8 -*-


def get_data(self):
    """Method to return the Elmer simulation results

    Parameter
    ---------


    Return
    ------
    data : list
        list of data

    """
    # check if data are loaded
    if not self.data:
        self.load_data()

    # output data as SciDataTool data
    # TODO

import itertools
import numpy as np
from ....Classes.ParamExplorerSet import ParamExplorerSet
from ....Functions.Simulation.VarLoad.setter_simu import setter_simu


def generate_simulation_list(self, ref_simu=None):
    """Generate all the simulation for the multi-simulation

    Parameters
    ----------
    self : VarSimu
        A VarSimu object
    ref_simu : Simulation
        Reference simulation to copy / update

    Returns
    -------
    multisim_dict : dict
        dictionary containing the simulation and paramexplorer list
    """

    # Get InputCurrent list
    list_input = self.get_input_list()

    multisim_dict = {
        "paramexplorer_list": [],  # Setter's values
        "simulation_list": [],
    }

    # Create Simulations 1 per load
    for input_obj in list_input:
        # Generate the simulation
        new_simu = ref_simu.copy(keep_function=True)

        # Edit simulation
        # setter current
        setter_simu(new_simu, input_obj)
        # Add simulation to the list
        multisim_dict["simulation_list"].append(new_simu)

    # Create ParamExplorerSet
    #   This version uses a single ParamExplorerSet to define the simulation
    #   Other parameters can be stored in a dedicated ParamExplorerSet if needed
    multisim_dict["paramexplorer_list"].append(
        ParamExplorerSet(
            name="InputCurrent",
            symbol="",
            unit="",
            setter=setter_simu,
            value=list_input,
        )
    )

    # Generate default datakeeper
    self.gen_datakeeper_list()

    return multisim_dict

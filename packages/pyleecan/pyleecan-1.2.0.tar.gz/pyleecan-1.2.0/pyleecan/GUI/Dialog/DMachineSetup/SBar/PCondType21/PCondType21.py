# -*- coding: utf-8 -*-

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget

from ......Classes.CondType21 import CondType21
from ......GUI import gui_option
from ......GUI.Dialog.DMachineSetup.SBar.PCondType21.Gen_PCondType21 import (
    Gen_PCondType21,
)


class PCondType21(Gen_PCondType21, QWidget):
    """Page to setup Conductor Type 21"""

    # Signal to DMachineSetup to know that the save popup is needed
    saveNeeded = Signal()
    # Information for SBar combobox
    cond_name = "Rectangular bar"
    cond_type = CondType21

    def __init__(self, machine=None, matlib=None):
        """Initialize the widget according to machine

        Parameters
        ----------
        self : PCondType21
            A PCondType21 widget
        machine : Machine
            current machine to edit
        matlib : MatLib
            Material Library
        """
        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)

        # Setup material combobox according to matlib names
        self.matlib = matlib
        self.w_mat.def_mat = "Copper1"

        # Set FloatEdit unit
        self.lf_Hbar.unit = "m"
        self.lf_Wbar.unit = "m"

        # Set unit name (m ou mm)
        self.u = gui_option.unit
        wid_list = [self.unit_Hbar, self.unit_Wbar]
        for wid in wid_list:
            wid.setText(self.u.get_m_name())

        # Fill the fields with the machine values (if they're filled)
        self.machine = machine

        conductor = machine.rotor.winding.conductor
        # Make sure that the rotor's conductor is a 2_1
        if conductor is None or not isinstance(conductor, CondType21):
            self.machine.rotor.winding.conductor = CondType21()
            self.machine.rotor.winding.conductor._set_None()
            # Make sure to re-set conductor with the new object
            conductor = machine.rotor.winding.conductor

        self.lf_Hbar.setValue(conductor.Hbar)
        self.lf_Wbar.setValue(conductor.Wbar)

        self.w_mat.update(conductor, "cond_mat", self.matlib)

        # Display the main output
        self.w_out.comp_output()

        # Connect the widget
        self.lf_Hbar.editingFinished.connect(self.set_Hbar)
        self.lf_Wbar.editingFinished.connect(self.set_Wbar)
        self.w_mat.saveNeeded.connect(self.emit_save)

    def emit_save(self):
        """Emit the saveNeeded signal"""
        self.saveNeeded.emit()

    def set_Hbar(self):
        """Signal to update the value of Hbar according to the line edit

        Parameters
        ----------
        self : PCondType21
            A PCondType21 object

        Returns
        -------

        """
        self.machine.rotor.winding.conductor.Hbar = self.lf_Hbar.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_Wbar(self):
        """Signal to update the value of Wbar according to the line edit

        Parameters
        ----------
        self : PCondType21
            A PCondType21 object

        Returns
        -------

        """
        self.machine.rotor.winding.conductor.Wbar = self.lf_Wbar.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

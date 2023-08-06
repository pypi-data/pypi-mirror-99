# -*- coding: utf-8 -*-

from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget

from ......Classes.CondType11 import CondType11
from ......GUI import gui_option
from ......GUI.Dialog.DMachineSetup.SWindCond.PCondType11.Gen_PCondType11 import (
    Gen_PCondType11,
)


class PCondType11(Gen_PCondType11, QWidget):
    """Page to set the Conductor Type 11"""

    # Signal to DMachineSetup to know that the save popup is needed
    saveNeeded = Signal()
    # Information for SWindCond combobox
    cond_type = CondType11
    cond_name = "Preformed Rectangular"

    def __init__(self, lamination=None):
        """Initialize the widget according to lamination

        Parameters
        ----------
        self : PCondType11
            A PCondType11 widget
        lamination : Lamination
            current lamination to edit
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)

        # Set FloatEdit unit
        self.lf_Wwire.unit = "m"
        self.lf_Hwire.unit = "m"
        self.lf_Wins_wire.unit = "m"
        self.lf_Lewout.unit = "m"
        self.u = gui_option.unit

        # Set unit name (m ou mm)
        wid_list = [
            self.unit_Wwire,
            self.unit_Hwire,
            self.unit_Wins_wire,
            self.unit_Lewout,
        ]
        for wid in wid_list:
            wid.setText("[" + self.u.get_m_name() + "]")

        # Fill the fields with the machine values (if they're filled)
        self.lam = lamination
        self.cond = self.lam.winding.conductor

        # Make sure that isinstance(cond, CondType11)
        if self.cond is None or not isinstance(self.cond, CondType11):
            self.cond = CondType11()
            self.cond._set_None()

        if self.cond.Nwppc_tan is None:
            self.cond.Nwppc_tan = 1  # Default value
        self.si_Nwpc1_tan.setValue(self.cond.Nwppc_tan)

        if self.cond.Nwppc_rad is None:
            self.cond.Nwppc_rad = 1  # Default value
        self.si_Nwpc1_rad.setValue(self.cond.Nwppc_rad)

        self.lf_Wwire.setValue(self.cond.Wwire)
        self.lf_Hwire.setValue(self.cond.Hwire)
        if self.cond.Wins_wire is None:
            self.cond.Wins_wire = 0  # Default value
        self.lf_Wins_wire.setValue(self.cond.Wins_wire)
        self.lf_Lewout.validator().setBottom(0)
        if self.lam.winding.Lewout is None:
            self.lam.winding.Lewout = 0
        self.lf_Lewout.setValue(self.lam.winding.Lewout)

        # Display the conductor main output
        self.w_out.comp_output()

        # Connect the slot/signal
        self.si_Nwpc1_tan.editingFinished.connect(self.set_Nwppc_tan)
        self.si_Nwpc1_rad.editingFinished.connect(self.set_Nwppc_rad)
        self.lf_Wwire.editingFinished.connect(self.set_Wwire)
        self.lf_Hwire.editingFinished.connect(self.set_Hwire)
        self.lf_Wins_wire.editingFinished.connect(self.set_Wins_wire)
        self.lf_Lewout.editingFinished.connect(self.set_Lewout)

    def set_Nwppc_tan(self):
        """Signal to update the value of Nwppc_tan according to the line edit

        Parameters
        ----------
        self : PCondType11
            A PCondType11 object
        """
        self.cond.Nwppc_tan = self.si_Nwpc1_tan.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_Nwppc_rad(self):
        """Signal to update the value of Nwppc_rad according to the line edit

        Parameters
        ----------
        self : PCondType11
            A PCondType11 object
        """
        self.cond.Nwppc_rad = self.si_Nwpc1_rad.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_Wwire(self):
        """Signal to update the value of Wwire according to the line edit

        Parameters
        ----------
        self : PCondType11
            A PCondType11 object
        """
        self.cond.Wwire = self.lf_Wwire.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_Hwire(self):
        """Signal to update the value of Hwire according to the line edit

        Parameters
        ----------
        self : PCondType11
            A PCondType11 object
        """
        self.cond.Hwire = self.lf_Hwire.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_Wins_coil(self):
        """Signal to update the value of Wins_coil according to the line edit

        Parameters
        ----------
        self : PCondType11
            A PCondType11 object
        """
        self.cond.Wins_coil = self.lf_Wins_coil.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_Wins_wire(self):
        """Signal to update the value of Wwire according to the line edit

        Parameters
        ----------
        self : PCondType11
            A PCondType11 object
        """
        self.cond.Wins_wire = self.lf_Wins_wire.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_Lewout(self):
        """Signal to update the value of Lewout according to the line edit

        Parameters
        ----------
        self : PCondType11
            A PCondType11 object
        """
        self.lam.winding.Lewout = self.lf_Lewout.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def check(self):
        """Check that the current machine have all the needed field set

        Parameters
        ----------
        self : PCondType11
            A PCondType11 object

        Returns
        -------
        error: str
            Error message (return None if no error)
        """

        # Check that everything is set
        if self.cond.Nwppc_tan is None:
            return self.tr("You must set Nwpc1_tan !")
        elif self.cond.Nwppc_rad is None:
            return self.tr("You must set Nwpc1_rad !")
        elif self.cond.Hwire is None:
            return self.tr("You must set Hwire !")
        elif self.cond.Wwire is None:
            return self.tr("You must set Wwire !")
        elif self.cond.Wins_wire is None:
            return self.tr("You must set Wins_wire !")
        elif self.lam.winding.Lewout is None:
            return self.tr("You must set Lewout !")

# -*- coding: utf-8 -*-

import PySide2.QtCore
from numpy import pi
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget

from ......Classes.SlotM13 import SlotM13
from ......GUI import gui_option
from ......GUI.Dialog.DMachineSetup.SMSlot.PMSlot13.Gen_PMSlot13 import Gen_PMSlot13
from ......Methods.Slot.Slot import SlotCheckError

translate = PySide2.QtCore.QCoreApplication.translate


class PMSlot13(Gen_PMSlot13, QWidget):
    """Page to set the Slot Magnet Type 13"""

    # Signal to DMachineSetup to know that the save popup is needed
    saveNeeded = Signal()
    # Information for Slot combobox
    slot_name = "Rectangular Magnet with curved top"
    slot_type = SlotM13

    def __init__(self, lamination=None):
        """Initialize the widget according to lamination

        Parameters
        ----------
        self : PMSlot13
            A PMSlot13 widget
        lamination : Lamination
            current lamination to edit
        """

        # Build the interface according to the .ui file
        QWidget.__init__(self)
        self.setupUi(self)
        self.lamination = lamination
        self.slot = lamination.slot

        # Set FloatEdit unit
        self.lf_W0.unit = "m"
        self.lf_Wmag.unit = "m"
        self.lf_H0.unit = "m"
        self.lf_Hmag.unit = "m"
        self.lf_Rtopm.unit = "m"
        # Set unit name (m ou mm)
        wid_list = [
            self.unit_W0,
            self.unit_Wmag,
            self.unit_H0,
            self.unit_Hmag,
            self.unit_Rtopm,
        ]
        for wid in wid_list:
            wid.setText("[" + gui_option.unit.get_m_name() + "]")

        # Fill the fields with the machine values (if they're filled)
        self.lf_W0.setValue(self.slot.W0)
        self.lf_Wmag.setValue(self.slot.Wmag)
        self.lf_H0.setValue(self.slot.H0)
        self.lf_Hmag.setValue(self.slot.Hmag)
        self.lf_Rtopm.setValue(self.slot.Rtopm)

        # Display the main output of the slot (surface, height...)
        self.w_out.comp_output()

        # Connect the signal
        self.lf_W0.editingFinished.connect(self.set_W0)
        self.lf_Wmag.editingFinished.connect(self.set_Wmag)
        self.lf_H0.editingFinished.connect(self.set_H0)
        self.lf_Hmag.editingFinished.connect(self.set_Hmag)
        self.lf_Rtopm.editingFinished.connect(self.set_Rtopm)

    def set_W0(self):
        """Signal to update the value of W0 according to the line edit

        Parameters
        ----------
        self : PMSlot13
            A PMSlot13 object
        """
        self.slot.W0 = self.lf_W0.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_Wmag(self):
        """Signal to update the value of Wmag according to the line edit

        Parameters
        ----------
        self : PMSlot13
            A PMSlot13 object
        """
        self.slot.Wmag = self.lf_Wmag.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_H0(self):
        """Signal to update the value of H0 according to the line edit

        Parameters
        ----------
        self : PMSlot13
            A PMSlot13 object
        """
        self.slot.H0 = self.lf_H0.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_Hmag(self):
        """Signal to update the value of Hmag according to the line edit

        Parameters
        ----------
        self : PMSlot13
            A PMSlot13 object
        """
        self.slot.Hmag = self.lf_Hmag.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_Rtopm(self):
        """Signal to update the value of Rtopm according to the line edit

        Parameters
        ----------
        self : PMSlot13
            A PMSlot13 object
        """
        self.slot.Rtopm = self.lf_Rtopm.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    @staticmethod
    def check(lam):
        """Check that the current machine have all the needed field set

        Parameters
        ----------
        lam: LamSlotMag
            Lamination to check

        Returns
        -------
        error: str
            Error message (return None if no error)
        """

        # Check that everything is set
        if lam.slot.W0 is None:
            return "You must set W0 !"
        elif lam.slot.Wmag is None:
            return "You must set Wmag !"
        elif lam.slot.H0 is None:
            return "You must set H0 !"
        elif lam.slot.Hmag is None:
            return "You must set Hmag !"
        elif lam.slot.Rtopm is None:
            return "You must set Rtopm !"

        # Constraints
        try:
            lam.slot.check()
        except SlotCheckError as error:
            return str(error)

        # Output
        try:
            yoke_height = lam.comp_height_yoke()
        except Exception as error:
            return "Unable to compute yoke height:" + str(error)

        if yoke_height <= 0:
            return "The slot height is greater than the lamination !"

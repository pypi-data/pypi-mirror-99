# -*- coding: utf-8 -*-

import PySide2.QtCore
from PySide2.QtCore import Signal
from PySide2.QtWidgets import QWidget

from ......Classes.SlotW23 import SlotW23
from ......GUI import gui_option
from ......GUI.Dialog.DMachineSetup.SWSlot.PWSlot23.Gen_PWSlot23 import Gen_PWSlot23
from ......Methods.Slot.Slot import SlotCheckError

translate = PySide2.QtCore.QCoreApplication.translate


class PWSlot23(Gen_PWSlot23, QWidget):
    """Page to set the Slot Type 23"""

    # Signal to DMachineSetup to know that the save popup is needed
    saveNeeded = Signal()
    # Information for Slot combobox
    slot_name = "Slot Type 23"
    slot_type = SlotW23

    def __init__(self, lamination=None):
        """Initialize the GUI according to current lamination

        Parameters
        ----------
        self : PWSlot23
            A PWSlot23 widget
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
        self.lf_W1.unit = "m"
        self.lf_W2.unit = "m"
        self.lf_W3.unit = "m"
        self.lf_H0.unit = "m"
        self.lf_H1.unit = "m"
        self.lf_H2.unit = "m"

        # Set unit name (m ou mm)
        wid_list = [
            self.unit_W0,
            self.unit_W1,
            self.unit_W2,
            self.unit_W3,
            self.unit_H0,
            self.unit_H1,
            self.unit_H2,
        ]
        for wid in wid_list:
            wid.setText("[" + gui_option.unit.get_m_name() + "]")

        # Fill the fields with the machine values (if they're filled)
        self.lf_W0.setValue(self.slot.W0)
        self.lf_H0.setValue(self.slot.H0)
        self.lf_H1.setValue(self.slot.H1)
        self.lf_H2.setValue(self.slot.H2)
        if self.slot.W3 is None:
            self.lf_W3.clear()
            self.is_cst_tooth.setChecked(False)
            self.lf_W3.setEnabled(False)
            # No W3 => Constant slot
            self.lf_W1.setValue(self.slot.W1)
            self.lf_W2.setValue(self.slot.W2)
        else:  # Cste tooth
            self.lf_W3.setValue(self.slot.W3)
            # W3 is set => constant Tooth so W1 and W2 should be disabled
            self.is_cst_tooth.setChecked(True)
            self.slot.W1 = None
            self.slot.W2 = None
            self.lf_W1.clear()
            self.lf_W2.clear()
            self.lf_W1.setEnabled(False)
            self.lf_W2.setEnabled(False)

        # Display the main output of the slot (surface, height...)
        self.w_out.comp_output()

        # Connect the signal
        self.lf_W0.editingFinished.connect(self.set_W0)
        self.lf_W1.editingFinished.connect(self.set_W1)
        self.lf_W2.editingFinished.connect(self.set_W2)
        self.lf_W3.editingFinished.connect(self.set_W3)
        self.lf_H0.editingFinished.connect(self.set_H0)
        self.lf_H1.editingFinished.connect(self.set_H1)
        self.lf_H2.editingFinished.connect(self.set_H2)
        self.is_cst_tooth.toggled.connect(self.set_is_cst_tooth)

    def set_W0(self):
        """Signal to update the value of W0 according to the line edit

        Parameters
        ----------
        self : PWSlot23
            A PWSlot23 object
        """
        self.slot.W0 = self.lf_W0.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_W1(self):
        """Signal to update the value of W1 according to the line edit

        Parameters
        ----------
        self : PWSlot23
            A PWSlot23 object
        """
        self.slot.W1 = self.lf_W1.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_W2(self):
        """Signal to update the value of W2 according to the line edit

        Parameters
        ----------
        self : PWSlot23
            A PWSlot23 object
        """
        self.slot.W2 = self.lf_W2.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_W3(self):
        """Signal to update the value of W3 according to the line edit

        Parameters
        ----------
        self : PWSlot23
            A PWSlot23 object
        """
        self.slot.W3 = self.lf_W3.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_H0(self):
        """Signal to update the value of H0 according to the line edit

        Parameters
        ----------
        self : PWSlot23
            A PWSlot23 object
        """
        self.slot.H0 = self.lf_H0.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_H1(self):
        """Signal to update the value of H1 according to the line edit

        Parameters
        ----------
        self : PWSlot23
            A PWSlot23 object
        """
        self.slot.H1 = self.lf_H1.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_H2(self):
        """Signal to update the value of H2 according to the line edit

        Parameters
        ----------
        self : PWSlot23
            A PWSlot23 object
        """
        self.slot.H2 = self.lf_H2.value()
        self.w_out.comp_output()
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    def set_is_cst_tooth(self, is_checked):
        """Signal to set the correct mode (constant tooth or slot) according to
        the checkbox

        Parameters
        ----------
        self : PWSlot23
            A PWSlot23 object
        is_checked : bool
            State of the checkbox
        """
        if is_checked:
            self.slot.W1 = None
            self.slot.W2 = None
            self.lf_W1.clear()
            self.lf_W2.clear()
            self.lf_W1.setEnabled(False)
            self.lf_W2.setEnabled(False)
            self.lf_W3.setEnabled(True)
        else:
            self.slot.W3 = None
            self.lf_W3.clear()
            self.lf_W3.setEnabled(False)
            self.lf_W1.setEnabled(True)
            self.lf_W2.setEnabled(True)
        # Notify the machine GUI that the machine has changed
        self.saveNeeded.emit()

    @staticmethod
    def check(lam):
        """Check that the current lamination have all the needed field set

        Parameters
        ----------
        lam: LamSlotWind
            Lamination to check

        Returns
        -------
        error: str
            Error message (return None if no error)
        """

        # Check that everything is set
        if lam.slot.W0 is None:
            return "You must set W0 !"
        elif lam.slot.H0 is None:
            return "You must set H0 !"
        elif lam.slot.H1 is None:
            return "You must set H1 !"
        elif lam.slot.H2 is None:
            return "You must set H2 !"
        # elif self.is_cst_tooth.isChecked() and self.slot.W3 is None:
        #     return translate("In constant tooth mode, you must set W3 !")
        # elif (not self.is_cst_tooth.isChecked()) and self.slot.W1 is None:
        #     return translate("In constant slot mode, you must set W1 !")
        # elif (not self.is_cst_tooth.isChecked()) and self.slot.W2 is None:
        #     return translate("In constant slot mode, you must set W2 !")

        # Check that everything is set right
        if lam.slot.W3 is not None:
            lam.slot._comp_W()

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

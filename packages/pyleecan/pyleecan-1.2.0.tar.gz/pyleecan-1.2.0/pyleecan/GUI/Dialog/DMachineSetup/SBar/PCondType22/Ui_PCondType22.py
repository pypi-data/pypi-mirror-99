# -*- coding: utf-8 -*-

# File generated according to PCondType22.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ......GUI.Dialog.DMatLib.WMatSelect.WMatSelect import WMatSelect
from ......GUI.Dialog.DMachineSetup.SBar.WBarOut.WBarOut import WBarOut


class Ui_PCondType22(object):
    def setupUi(self, PCondType22):
        if not PCondType22.objectName():
            PCondType22.setObjectName(u"PCondType22")
        PCondType22.resize(460, 124)
        self.horizontalLayout = QHBoxLayout(PCondType22)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.w_mat = WMatSelect(PCondType22)
        self.w_mat.setObjectName(u"w_mat")

        self.horizontalLayout.addWidget(self.w_mat)

        self.w_out = WBarOut(PCondType22)
        self.w_out.setObjectName(u"w_out")

        self.horizontalLayout.addWidget(self.w_out)

        self.retranslateUi(PCondType22)

        QMetaObject.connectSlotsByName(PCondType22)

    # setupUi

    def retranslateUi(self, PCondType22):
        PCondType22.setWindowTitle(
            QCoreApplication.translate("PCondType22", u"Form", None)
        )

    # retranslateUi

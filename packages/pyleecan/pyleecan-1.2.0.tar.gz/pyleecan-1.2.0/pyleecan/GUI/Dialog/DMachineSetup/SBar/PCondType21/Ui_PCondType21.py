# -*- coding: utf-8 -*-

# File generated according to PCondType21.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ......GUI.Tools.FloatEdit import FloatEdit
from ......GUI.Dialog.DMatLib.WMatSelect.WMatSelect import WMatSelect
from ......GUI.Dialog.DMachineSetup.SBar.WBarOut.WBarOut import WBarOut


class Ui_PCondType21(object):
    def setupUi(self, PCondType21):
        if not PCondType21.objectName():
            PCondType21.setObjectName(u"PCondType21")
        PCondType21.resize(416, 124)
        self.horizontalLayout = QHBoxLayout(PCondType21)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.lf_Hbar = FloatEdit(PCondType21)
        self.lf_Hbar.setObjectName(u"lf_Hbar")
        self.lf_Hbar.setMinimumSize(QSize(70, 0))
        self.lf_Hbar.setMaximumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.lf_Hbar, 0, 1, 1, 1)

        self.in_Hbar = QLabel(PCondType21)
        self.in_Hbar.setObjectName(u"in_Hbar")
        self.in_Hbar.setMinimumSize(QSize(40, 0))

        self.gridLayout.addWidget(self.in_Hbar, 0, 0, 1, 1)

        self.unit_Hbar = QLabel(PCondType21)
        self.unit_Hbar.setObjectName(u"unit_Hbar")
        self.unit_Hbar.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.unit_Hbar, 0, 2, 1, 1)

        self.lf_Wbar = FloatEdit(PCondType21)
        self.lf_Wbar.setObjectName(u"lf_Wbar")
        self.lf_Wbar.setMinimumSize(QSize(70, 0))
        self.lf_Wbar.setMaximumSize(QSize(100, 20))

        self.gridLayout.addWidget(self.lf_Wbar, 1, 1, 1, 1)

        self.unit_Wbar = QLabel(PCondType21)
        self.unit_Wbar.setObjectName(u"unit_Wbar")
        self.unit_Wbar.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.unit_Wbar, 1, 2, 1, 1)

        self.in_Wbar = QLabel(PCondType21)
        self.in_Wbar.setObjectName(u"in_Wbar")
        self.in_Wbar.setMinimumSize(QSize(40, 0))

        self.gridLayout.addWidget(self.in_Wbar, 1, 0, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.w_mat = WMatSelect(PCondType21)
        self.w_mat.setObjectName(u"w_mat")

        self.verticalLayout_2.addWidget(self.w_mat)

        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.w_out = WBarOut(PCondType21)
        self.w_out.setObjectName(u"w_out")

        self.horizontalLayout.addWidget(self.w_out)

        QWidget.setTabOrder(self.lf_Hbar, self.lf_Wbar)

        self.retranslateUi(PCondType21)

        QMetaObject.connectSlotsByName(PCondType21)

    # setupUi

    def retranslateUi(self, PCondType21):
        PCondType21.setWindowTitle(
            QCoreApplication.translate("PCondType21", u"Form", None)
        )
        self.in_Hbar.setText(QCoreApplication.translate("PCondType21", u"Hbar :", None))
        self.unit_Hbar.setText(QCoreApplication.translate("PCondType21", u"m", None))
        self.unit_Wbar.setText(QCoreApplication.translate("PCondType21", u"m", None))
        self.in_Wbar.setText(QCoreApplication.translate("PCondType21", u"Wbar :", None))

    # retranslateUi

# -*- coding: utf-8 -*-

# File generated according to WVent.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *


class Ui_WVent(object):
    def setupUi(self, WVent):
        if not WVent.objectName():
            WVent.setObjectName(u"WVent")
        WVent.resize(630, 470)
        WVent.setMinimumSize(QSize(630, 470))
        self.main_layout = QVBoxLayout(WVent)
        self.main_layout.setObjectName(u"main_layout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.in_vent_type = QLabel(WVent)
        self.in_vent_type.setObjectName(u"in_vent_type")

        self.horizontalLayout.addWidget(self.in_vent_type)

        self.c_vent_type = QComboBox(WVent)
        self.c_vent_type.addItem("")
        self.c_vent_type.addItem("")
        self.c_vent_type.addItem("")
        self.c_vent_type.setObjectName(u"c_vent_type")

        self.horizontalLayout.addWidget(self.c_vent_type)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout.addItem(self.horizontalSpacer)

        self.main_layout.addLayout(self.horizontalLayout)

        self.w_vent = QWidget(WVent)
        self.w_vent.setObjectName(u"w_vent")
        self.w_vent.setMinimumSize(QSize(640, 480))

        self.main_layout.addWidget(self.w_vent)

        self.retranslateUi(WVent)

        QMetaObject.connectSlotsByName(WVent)

    # setupUi

    def retranslateUi(self, WVent):
        WVent.setWindowTitle(QCoreApplication.translate("WVent", u"Form", None))
        self.in_vent_type.setText(
            QCoreApplication.translate("WVent", u"Ventilation Shape:", None)
        )
        self.c_vent_type.setItemText(
            0, QCoreApplication.translate("WVent", u"Circular", None)
        )
        self.c_vent_type.setItemText(
            1, QCoreApplication.translate("WVent", u"Polar", None)
        )
        self.c_vent_type.setItemText(
            2, QCoreApplication.translate("WVent", u"Trapeze", None)
        )

    # retranslateUi

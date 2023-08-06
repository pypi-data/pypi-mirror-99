# -*- coding: utf-8 -*-

# File generated according to PWSlotUD.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ......GUI.Dialog.DMachineSetup.SWSlot.WWSlotOut.WWSlotOut import WWSlotOut
from ......GUI.Tools.WPathSelector.WPathSelectorV import WPathSelectorV
from ......GUI.Tools.MPLCanvas import MPLCanvas2

from pyleecan.GUI.Resources import pyleecan_rc


class Ui_PWSlotUD(object):
    def setupUi(self, PWSlotUD):
        if not PWSlotUD.objectName():
            PWSlotUD.setObjectName(u"PWSlotUD")
        PWSlotUD.resize(740, 440)
        PWSlotUD.setMinimumSize(QSize(740, 440))
        PWSlotUD.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout = QHBoxLayout(PWSlotUD)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.w_viewer = MPLCanvas2(PWSlotUD)
        self.w_viewer.setObjectName(u"w_viewer")

        self.horizontalLayout.addWidget(self.w_viewer)

        self.widget = QWidget(PWSlotUD)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(250, 0))
        self.widget.setMaximumSize(QSize(250, 16777215))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.b_dxf = QPushButton(self.widget)
        self.b_dxf.setObjectName(u"b_dxf")

        self.verticalLayout.addWidget(self.b_dxf)

        self.w_path_json = WPathSelectorV(self.widget)
        self.w_path_json.setObjectName(u"w_path_json")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_path_json.sizePolicy().hasHeightForWidth())
        self.w_path_json.setSizePolicy(sizePolicy)

        self.verticalLayout.addWidget(self.w_path_json)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.w_out = WWSlotOut(self.widget)
        self.w_out.setObjectName(u"w_out")

        self.verticalLayout.addWidget(self.w_out)

        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(PWSlotUD)

        QMetaObject.connectSlotsByName(PWSlotUD)

    # setupUi

    def retranslateUi(self, PWSlotUD):
        PWSlotUD.setWindowTitle(QCoreApplication.translate("PWSlotUD", u"Form", None))
        self.b_dxf.setText(
            QCoreApplication.translate("PWSlotUD", u"Define Slot from DXF", None)
        )

    # retranslateUi

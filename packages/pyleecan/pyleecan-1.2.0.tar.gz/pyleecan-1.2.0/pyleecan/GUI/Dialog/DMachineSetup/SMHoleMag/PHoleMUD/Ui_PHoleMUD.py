# -*- coding: utf-8 -*-

# File generated according to PHoleMUD.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ......GUI.Tools.WPathSelector.WPathSelectorV import WPathSelectorV
from ......GUI.Tools.MPLCanvas import MPLCanvas2
from ......GUI.Dialog.DMatLib.WMatSelect.WMatSelect import WMatSelect

from pyleecan.GUI.Resources import pyleecan_rc


class Ui_PHoleMUD(object):
    def setupUi(self, PHoleMUD):
        if not PHoleMUD.objectName():
            PHoleMUD.setObjectName(u"PHoleMUD")
        PHoleMUD.resize(813, 467)
        PHoleMUD.setMinimumSize(QSize(740, 440))
        PHoleMUD.setMaximumSize(QSize(16777215, 16777215))
        self.horizontalLayout = QHBoxLayout(PHoleMUD)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.w_viewer = MPLCanvas2(PHoleMUD)
        self.w_viewer.setObjectName(u"w_viewer")

        self.horizontalLayout.addWidget(self.w_viewer)

        self.widget = QWidget(PHoleMUD)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(250, 0))
        self.widget.setMaximumSize(QSize(250, 16777215))
        self.verticalLayout_2 = QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.b_dxf = QPushButton(self.widget)
        self.b_dxf.setObjectName(u"b_dxf")

        self.verticalLayout_2.addWidget(self.b_dxf)

        self.w_path_json = WPathSelectorV(self.widget)
        self.w_path_json.setObjectName(u"w_path_json")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.w_path_json.sizePolicy().hasHeightForWidth())
        self.w_path_json.setSizePolicy(sizePolicy)

        self.verticalLayout_2.addWidget(self.w_path_json)

        self.g_mat = QGroupBox(self.widget)
        self.g_mat.setObjectName(u"g_mat")
        self.g_mat_layout = QVBoxLayout(self.g_mat)
        self.g_mat_layout.setObjectName(u"g_mat_layout")
        self.w_mat_0 = WMatSelect(self.g_mat)
        self.w_mat_0.setObjectName(u"w_mat_0")
        self.w_mat_0.setMinimumSize(QSize(100, 0))

        self.g_mat_layout.addWidget(self.w_mat_0)

        self.verticalLayout_2.addWidget(self.g_mat)

        self.verticalSpacer = QSpacerItem(
            20, 179, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.g_output = QGroupBox(self.widget)
        self.g_output.setObjectName(u"g_output")
        self.g_output.setMinimumSize(QSize(200, 0))
        self.verticalLayout = QVBoxLayout(self.g_output)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.out_slot_surface = QLabel(self.g_output)
        self.out_slot_surface.setObjectName(u"out_slot_surface")

        self.verticalLayout.addWidget(self.out_slot_surface)

        self.out_magnet_surface = QLabel(self.g_output)
        self.out_magnet_surface.setObjectName(u"out_magnet_surface")

        self.verticalLayout.addWidget(self.out_magnet_surface)

        self.out_Rmin = QLabel(self.g_output)
        self.out_Rmin.setObjectName(u"out_Rmin")

        self.verticalLayout.addWidget(self.out_Rmin)

        self.out_Rmax = QLabel(self.g_output)
        self.out_Rmax.setObjectName(u"out_Rmax")

        self.verticalLayout.addWidget(self.out_Rmax)

        self.verticalLayout_2.addWidget(self.g_output)

        self.horizontalLayout.addWidget(self.widget)

        self.retranslateUi(PHoleMUD)

        QMetaObject.connectSlotsByName(PHoleMUD)

    # setupUi

    def retranslateUi(self, PHoleMUD):
        PHoleMUD.setWindowTitle(QCoreApplication.translate("PHoleMUD", u"Form", None))
        self.b_dxf.setText(
            QCoreApplication.translate("PHoleMUD", u"Define Slot from DXF", None)
        )
        self.g_mat.setTitle(QCoreApplication.translate("PHoleMUD", u"Materials", None))
        self.g_output.setTitle(QCoreApplication.translate("PHoleMUD", u"Output", None))
        self.out_slot_surface.setText(
            QCoreApplication.translate("PHoleMUD", u"Hole full surface : ?", None)
        )
        self.out_magnet_surface.setText(
            QCoreApplication.translate("PHoleMUD", u"Hole magnet surface : ?", None)
        )
        self.out_Rmin.setText(QCoreApplication.translate("PHoleMUD", u"Rmin : ?", None))
        self.out_Rmax.setText(QCoreApplication.translate("PHoleMUD", u"Rmax : ?", None))

    # retranslateUi

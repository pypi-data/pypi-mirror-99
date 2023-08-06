# -*- coding: utf-8 -*-

# File generated according to PCondType11.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from ......GUI.Tools.FloatEdit import FloatEdit
from ......GUI.Dialog.DMachineSetup.SWindCond.WCondOut.WCondOut import WCondOut

from pyleecan.GUI.Resources import pyleecan_rc


class Ui_PCondType11(object):
    def setupUi(self, PCondType11):
        if not PCondType11.objectName():
            PCondType11.setObjectName(u"PCondType11")
        PCondType11.resize(1243, 544)
        self.horizontalLayout = QHBoxLayout(PCondType11)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.img_cond = QLabel(PCondType11)
        self.img_cond.setObjectName(u"img_cond")
        self.img_cond.setMinimumSize(QSize(0, 0))
        self.img_cond.setMaximumSize(QSize(16777215, 16777215))
        self.img_cond.setPixmap(
            QPixmap(u":/images/images/MachineSetup/WindParam/CondType11.png")
        )
        self.img_cond.setScaledContents(True)

        self.horizontalLayout.addWidget(self.img_cond)

        self.widget = QWidget(PCondType11)
        self.widget.setObjectName(u"widget")
        self.widget.setMinimumSize(QSize(250, 0))
        self.widget.setMaximumSize(QSize(250, 16777215))
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.in_Nwpc1_tan = QLabel(self.widget)
        self.in_Nwpc1_tan.setObjectName(u"in_Nwpc1_tan")
        self.in_Nwpc1_tan.setMinimumSize(QSize(70, 0))

        self.gridLayout.addWidget(self.in_Nwpc1_tan, 0, 0, 1, 1)

        self.si_Nwpc1_tan = QSpinBox(self.widget)
        self.si_Nwpc1_tan.setObjectName(u"si_Nwpc1_tan")
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.si_Nwpc1_tan.sizePolicy().hasHeightForWidth())
        self.si_Nwpc1_tan.setSizePolicy(sizePolicy)
        self.si_Nwpc1_tan.setMinimumSize(QSize(0, 0))
        self.si_Nwpc1_tan.setValue(99)

        self.gridLayout.addWidget(self.si_Nwpc1_tan, 0, 1, 1, 1)

        self.in_Nwpc1_rad = QLabel(self.widget)
        self.in_Nwpc1_rad.setObjectName(u"in_Nwpc1_rad")
        self.in_Nwpc1_rad.setMinimumSize(QSize(70, 0))

        self.gridLayout.addWidget(self.in_Nwpc1_rad, 1, 0, 1, 1)

        self.si_Nwpc1_rad = QSpinBox(self.widget)
        self.si_Nwpc1_rad.setObjectName(u"si_Nwpc1_rad")
        sizePolicy.setHeightForWidth(self.si_Nwpc1_rad.sizePolicy().hasHeightForWidth())
        self.si_Nwpc1_rad.setSizePolicy(sizePolicy)
        self.si_Nwpc1_rad.setValue(99)

        self.gridLayout.addWidget(self.si_Nwpc1_rad, 1, 1, 1, 1)

        self.in_Wwire = QLabel(self.widget)
        self.in_Wwire.setObjectName(u"in_Wwire")
        self.in_Wwire.setMinimumSize(QSize(40, 0))

        self.gridLayout.addWidget(self.in_Wwire, 2, 0, 1, 1)

        self.lf_Wwire = FloatEdit(self.widget)
        self.lf_Wwire.setObjectName(u"lf_Wwire")
        sizePolicy.setHeightForWidth(self.lf_Wwire.sizePolicy().hasHeightForWidth())
        self.lf_Wwire.setSizePolicy(sizePolicy)
        self.lf_Wwire.setMinimumSize(QSize(0, 0))
        self.lf_Wwire.setMaximumSize(QSize(16777215, 100))

        self.gridLayout.addWidget(self.lf_Wwire, 2, 1, 1, 1)

        self.unit_Wwire = QLabel(self.widget)
        self.unit_Wwire.setObjectName(u"unit_Wwire")
        self.unit_Wwire.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.unit_Wwire, 2, 2, 1, 1)

        self.in_Hwire = QLabel(self.widget)
        self.in_Hwire.setObjectName(u"in_Hwire")
        self.in_Hwire.setMinimumSize(QSize(40, 0))

        self.gridLayout.addWidget(self.in_Hwire, 3, 0, 1, 1)

        self.lf_Hwire = FloatEdit(self.widget)
        self.lf_Hwire.setObjectName(u"lf_Hwire")
        sizePolicy.setHeightForWidth(self.lf_Hwire.sizePolicy().hasHeightForWidth())
        self.lf_Hwire.setSizePolicy(sizePolicy)
        self.lf_Hwire.setMinimumSize(QSize(0, 0))
        self.lf_Hwire.setMaximumSize(QSize(16777215, 100))

        self.gridLayout.addWidget(self.lf_Hwire, 3, 1, 1, 1)

        self.unit_Hwire = QLabel(self.widget)
        self.unit_Hwire.setObjectName(u"unit_Hwire")
        self.unit_Hwire.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.unit_Hwire, 3, 2, 1, 1)

        self.in_Wins_wire = QLabel(self.widget)
        self.in_Wins_wire.setObjectName(u"in_Wins_wire")
        self.in_Wins_wire.setMinimumSize(QSize(40, 0))

        self.gridLayout.addWidget(self.in_Wins_wire, 4, 0, 1, 1)

        self.lf_Wins_wire = FloatEdit(self.widget)
        self.lf_Wins_wire.setObjectName(u"lf_Wins_wire")
        sizePolicy.setHeightForWidth(self.lf_Wins_wire.sizePolicy().hasHeightForWidth())
        self.lf_Wins_wire.setSizePolicy(sizePolicy)
        self.lf_Wins_wire.setMinimumSize(QSize(0, 0))
        self.lf_Wins_wire.setMaximumSize(QSize(16777215, 100))

        self.gridLayout.addWidget(self.lf_Wins_wire, 4, 1, 1, 1)

        self.unit_Wins_wire = QLabel(self.widget)
        self.unit_Wins_wire.setObjectName(u"unit_Wins_wire")
        self.unit_Wins_wire.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.unit_Wins_wire, 4, 2, 1, 1)

        self.in_Lewout = QLabel(self.widget)
        self.in_Lewout.setObjectName(u"in_Lewout")
        self.in_Lewout.setMinimumSize(QSize(40, 0))

        self.gridLayout.addWidget(self.in_Lewout, 5, 0, 1, 1)

        self.lf_Lewout = FloatEdit(self.widget)
        self.lf_Lewout.setObjectName(u"lf_Lewout")
        sizePolicy.setHeightForWidth(self.lf_Lewout.sizePolicy().hasHeightForWidth())
        self.lf_Lewout.setSizePolicy(sizePolicy)
        self.lf_Lewout.setMinimumSize(QSize(0, 0))
        self.lf_Lewout.setMaximumSize(QSize(16777215, 100))

        self.gridLayout.addWidget(self.lf_Lewout, 5, 1, 1, 1)

        self.unit_Lewout = QLabel(self.widget)
        self.unit_Lewout.setObjectName(u"unit_Lewout")
        self.unit_Lewout.setMinimumSize(QSize(0, 0))

        self.gridLayout.addWidget(self.unit_Lewout, 5, 2, 1, 1)

        self.verticalLayout.addLayout(self.gridLayout)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout.addItem(self.verticalSpacer)

        self.w_out = WCondOut(self.widget)
        self.w_out.setObjectName(u"w_out")

        self.verticalLayout.addWidget(self.w_out)

        self.horizontalLayout.addWidget(self.widget)

        QWidget.setTabOrder(self.si_Nwpc1_tan, self.si_Nwpc1_rad)
        QWidget.setTabOrder(self.si_Nwpc1_rad, self.lf_Wwire)
        QWidget.setTabOrder(self.lf_Wwire, self.lf_Hwire)
        QWidget.setTabOrder(self.lf_Hwire, self.lf_Wins_wire)

        self.retranslateUi(PCondType11)

        QMetaObject.connectSlotsByName(PCondType11)

    # setupUi

    def retranslateUi(self, PCondType11):
        PCondType11.setWindowTitle(
            QCoreApplication.translate("PCondType11", u"Form", None)
        )
        self.img_cond.setText("")
        self.in_Nwpc1_tan.setText(
            QCoreApplication.translate("PCondType11", u"Nwppc_tan", None)
        )
        self.in_Nwpc1_rad.setText(
            QCoreApplication.translate("PCondType11", u"Nwppc_rad", None)
        )
        self.in_Wwire.setText(QCoreApplication.translate("PCondType11", u"Wwire", None))
        self.unit_Wwire.setText(QCoreApplication.translate("PCondType11", u"m", None))
        self.in_Hwire.setText(QCoreApplication.translate("PCondType11", u"Hwire", None))
        self.unit_Hwire.setText(QCoreApplication.translate("PCondType11", u"m", None))
        self.in_Wins_wire.setText(
            QCoreApplication.translate("PCondType11", u"Wins_wire", None)
        )
        self.unit_Wins_wire.setText(
            QCoreApplication.translate("PCondType11", u"m", None)
        )
        # if QT_CONFIG(tooltip)
        self.in_Lewout.setToolTip(
            QCoreApplication.translate(
                "PCondType11", u"End-winding length on one side for a half-turn", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(whatsthis)
        self.in_Lewout.setWhatsThis(
            QCoreApplication.translate(
                "PCondType11", u"End-winding length on one side for a half-turn", None
            )
        )
        # endif // QT_CONFIG(whatsthis)
        self.in_Lewout.setText(
            QCoreApplication.translate("PCondType11", u"Lewout", None)
        )
        # if QT_CONFIG(tooltip)
        self.lf_Lewout.setToolTip(
            QCoreApplication.translate(
                "PCondType11", u"End-winding length on one side for a half-turn", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(whatsthis)
        self.lf_Lewout.setWhatsThis(
            QCoreApplication.translate(
                "PCondType11", u"End-winding length on one side for a half-turn", None
            )
        )
        # endif // QT_CONFIG(whatsthis)
        # if QT_CONFIG(tooltip)
        self.unit_Lewout.setToolTip(
            QCoreApplication.translate(
                "PCondType11", u"End-winding length on one side for a half-turn", None
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(whatsthis)
        self.unit_Lewout.setWhatsThis(
            QCoreApplication.translate(
                "PCondType11", u"End-winding length on one side for a half-turn", None
            )
        )
        # endif // QT_CONFIG(whatsthis)
        self.unit_Lewout.setText(QCoreApplication.translate("PCondType11", u"m", None))

    # retranslateUi

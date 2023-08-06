# -*- coding: utf-8 -*-

# File generated according to DMatSetup.ui
# WARNING! All changes made in this file will be lost!
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

from .....GUI.Tools.FloatEdit import FloatEdit
from .....GUI.Tools.WImport.WImport import WImport

from pyleecan.GUI.Resources import pyleecan_rc


class Ui_DMatSetup(object):
    def setupUi(self, DMatSetup):
        if not DMatSetup.objectName():
            DMatSetup.setObjectName(u"DMatSetup")
        DMatSetup.resize(642, 451)
        self.verticalLayout = QVBoxLayout(DMatSetup)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.in_name = QLabel(DMatSetup)
        self.in_name.setObjectName(u"in_name")

        self.horizontalLayout.addWidget(self.in_name)

        self.le_name = QLineEdit(DMatSetup)
        self.le_name.setObjectName(u"le_name")

        self.horizontalLayout.addWidget(self.le_name)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.is_isotropic = QCheckBox(DMatSetup)
        self.is_isotropic.setObjectName(u"is_isotropic")

        self.verticalLayout.addWidget(self.is_isotropic)

        self.nav_phy = QTabWidget(DMatSetup)
        self.nav_phy.setObjectName(u"nav_phy")
        self.nav_phy.setMinimumSize(QSize(370, 0))
        self.tab_elec = QWidget()
        self.tab_elec.setObjectName(u"tab_elec")
        self.gridLayout_2 = QGridLayout(self.tab_elec)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.lf_rho_elec = FloatEdit(self.tab_elec)
        self.lf_rho_elec.setObjectName(u"lf_rho_elec")

        self.gridLayout_2.addWidget(self.lf_rho_elec, 0, 1, 1, 1)

        self.lf_epsr = FloatEdit(self.tab_elec)
        self.lf_epsr.setObjectName(u"lf_epsr")

        self.gridLayout_2.addWidget(self.lf_epsr, 1, 1, 1, 1)

        self.unit_rho_elec = QLabel(self.tab_elec)
        self.unit_rho_elec.setObjectName(u"unit_rho_elec")
        font = QFont()
        font.setPointSize(8)
        font.setBold(False)
        font.setWeight(50)
        self.unit_rho_elec.setFont(font)

        self.gridLayout_2.addWidget(self.unit_rho_elec, 0, 2, 1, 1)

        self.in_epsr = QLabel(self.tab_elec)
        self.in_epsr.setObjectName(u"in_epsr")
        self.in_epsr.setFont(font)

        self.gridLayout_2.addWidget(self.in_epsr, 1, 0, 1, 1)

        self.in_rho_elec = QLabel(self.tab_elec)
        self.in_rho_elec.setObjectName(u"in_rho_elec")
        self.in_rho_elec.setFont(font)

        self.gridLayout_2.addWidget(self.in_rho_elec, 0, 0, 1, 1)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_2.addItem(self.verticalSpacer_2, 2, 1, 1, 1)

        self.nav_phy.addTab(self.tab_elec, "")
        self.tab_mag = QWidget()
        self.tab_mag.setObjectName(u"tab_mag")
        self.verticalLayout_3 = QVBoxLayout(self.tab_mag)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.in_mur_lin = QLabel(self.tab_mag)
        self.in_mur_lin.setObjectName(u"in_mur_lin")
        self.in_mur_lin.setFont(font)

        self.gridLayout.addWidget(self.in_mur_lin, 0, 0, 1, 1)

        self.lf_mur_lin = FloatEdit(self.tab_mag)
        self.lf_mur_lin.setObjectName(u"lf_mur_lin")

        self.gridLayout.addWidget(self.lf_mur_lin, 0, 1, 1, 1)

        self.in_Brm20 = QLabel(self.tab_mag)
        self.in_Brm20.setObjectName(u"in_Brm20")
        self.in_Brm20.setFont(font)

        self.gridLayout.addWidget(self.in_Brm20, 1, 0, 1, 1)

        self.lf_Brm20 = FloatEdit(self.tab_mag)
        self.lf_Brm20.setObjectName(u"lf_Brm20")

        self.gridLayout.addWidget(self.lf_Brm20, 1, 1, 1, 1)

        self.unit_Brm20 = QLabel(self.tab_mag)
        self.unit_Brm20.setObjectName(u"unit_Brm20")
        self.unit_Brm20.setFont(font)

        self.gridLayout.addWidget(self.unit_Brm20, 1, 2, 1, 1)

        self.in_alpha_Br = QLabel(self.tab_mag)
        self.in_alpha_Br.setObjectName(u"in_alpha_Br")
        self.in_alpha_Br.setFont(font)

        self.gridLayout.addWidget(self.in_alpha_Br, 2, 0, 1, 1)

        self.lf_alpha_Br = FloatEdit(self.tab_mag)
        self.lf_alpha_Br.setObjectName(u"lf_alpha_Br")

        self.gridLayout.addWidget(self.lf_alpha_Br, 2, 1, 1, 1)

        self.in_Wlam = QLabel(self.tab_mag)
        self.in_Wlam.setObjectName(u"in_Wlam")
        self.in_Wlam.setFont(font)

        self.gridLayout.addWidget(self.in_Wlam, 3, 0, 1, 1)

        self.lf_Wlam = FloatEdit(self.tab_mag)
        self.lf_Wlam.setObjectName(u"lf_Wlam")

        self.gridLayout.addWidget(self.lf_Wlam, 3, 1, 1, 1)

        self.unit_Wlam = QLabel(self.tab_mag)
        self.unit_Wlam.setObjectName(u"unit_Wlam")
        self.unit_Wlam.setFont(font)

        self.gridLayout.addWidget(self.unit_Wlam, 3, 2, 1, 1)

        self.verticalLayout_3.addLayout(self.gridLayout)

        self.w_BH_import = WImport(self.tab_mag)
        self.w_BH_import.setObjectName(u"w_BH_import")

        self.verticalLayout_3.addWidget(self.w_BH_import)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_3.addItem(self.verticalSpacer)

        self.nav_phy.addTab(self.tab_mag, "")
        self.tab_mec = QWidget()
        self.tab_mec.setObjectName(u"tab_mec")
        self.verticalLayout_12 = QVBoxLayout(self.tab_mec)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.horizontalLayout_41 = QHBoxLayout()
        self.horizontalLayout_41.setObjectName(u"horizontalLayout_41")
        self.in_rho_meca = QLabel(self.tab_mec)
        self.in_rho_meca.setObjectName(u"in_rho_meca")
        self.in_rho_meca.setFont(font)

        self.horizontalLayout_41.addWidget(self.in_rho_meca)

        self.lf_rho_meca = FloatEdit(self.tab_mec)
        self.lf_rho_meca.setObjectName(u"lf_rho_meca")

        self.horizontalLayout_41.addWidget(self.lf_rho_meca)

        self.unit_rho_meca = QLabel(self.tab_mec)
        self.unit_rho_meca.setObjectName(u"unit_rho_meca")
        self.unit_rho_meca.setFont(font)

        self.horizontalLayout_41.addWidget(self.unit_rho_meca)

        self.verticalLayout_12.addLayout(self.horizontalLayout_41)

        self.nav_meca = QStackedWidget(self.tab_mec)
        self.nav_meca.setObjectName(u"nav_meca")
        self.page_niso_mec = QWidget()
        self.page_niso_mec.setObjectName(u"page_niso_mec")
        self.verticalLayout_4 = QVBoxLayout(self.page_niso_mec)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.g_young = QGroupBox(self.page_niso_mec)
        self.g_young.setObjectName(u"g_young")
        self.horizontalLayout_2 = QHBoxLayout(self.g_young)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.in_Ex = QLabel(self.g_young)
        self.in_Ex.setObjectName(u"in_Ex")
        self.in_Ex.setFont(font)

        self.horizontalLayout_2.addWidget(self.in_Ex)

        self.lf_Ex = FloatEdit(self.g_young)
        self.lf_Ex.setObjectName(u"lf_Ex")

        self.horizontalLayout_2.addWidget(self.lf_Ex)

        self.in_Ey = QLabel(self.g_young)
        self.in_Ey.setObjectName(u"in_Ey")
        self.in_Ey.setFont(font)

        self.horizontalLayout_2.addWidget(self.in_Ey)

        self.lf_Ey = FloatEdit(self.g_young)
        self.lf_Ey.setObjectName(u"lf_Ey")

        self.horizontalLayout_2.addWidget(self.lf_Ey)

        self.in_Ez = QLabel(self.g_young)
        self.in_Ez.setObjectName(u"in_Ez")
        self.in_Ez.setFont(font)

        self.horizontalLayout_2.addWidget(self.in_Ez)

        self.lf_Ez = FloatEdit(self.g_young)
        self.lf_Ez.setObjectName(u"lf_Ez")

        self.horizontalLayout_2.addWidget(self.lf_Ez)

        self.verticalLayout_4.addWidget(self.g_young)

        self.g_poisson = QGroupBox(self.page_niso_mec)
        self.g_poisson.setObjectName(u"g_poisson")
        self.horizontalLayout_3 = QHBoxLayout(self.g_poisson)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.in_nu_xy = QLabel(self.g_poisson)
        self.in_nu_xy.setObjectName(u"in_nu_xy")
        self.in_nu_xy.setFont(font)

        self.horizontalLayout_3.addWidget(self.in_nu_xy)

        self.lf_nu_xy = FloatEdit(self.g_poisson)
        self.lf_nu_xy.setObjectName(u"lf_nu_xy")

        self.horizontalLayout_3.addWidget(self.lf_nu_xy)

        self.in_nu_xz = QLabel(self.g_poisson)
        self.in_nu_xz.setObjectName(u"in_nu_xz")
        self.in_nu_xz.setFont(font)

        self.horizontalLayout_3.addWidget(self.in_nu_xz)

        self.lf_nu_xz = FloatEdit(self.g_poisson)
        self.lf_nu_xz.setObjectName(u"lf_nu_xz")

        self.horizontalLayout_3.addWidget(self.lf_nu_xz)

        self.in_nu_yz = QLabel(self.g_poisson)
        self.in_nu_yz.setObjectName(u"in_nu_yz")
        self.in_nu_yz.setFont(font)

        self.horizontalLayout_3.addWidget(self.in_nu_yz)

        self.lf_nu_yz = FloatEdit(self.g_poisson)
        self.lf_nu_yz.setObjectName(u"lf_nu_yz")

        self.horizontalLayout_3.addWidget(self.lf_nu_yz)

        self.verticalLayout_4.addWidget(self.g_poisson)

        self.g_shear = QGroupBox(self.page_niso_mec)
        self.g_shear.setObjectName(u"g_shear")
        self.horizontalLayout_4 = QHBoxLayout(self.g_shear)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.in_Gxy = QLabel(self.g_shear)
        self.in_Gxy.setObjectName(u"in_Gxy")
        self.in_Gxy.setFont(font)

        self.horizontalLayout_4.addWidget(self.in_Gxy)

        self.lf_Gxy = FloatEdit(self.g_shear)
        self.lf_Gxy.setObjectName(u"lf_Gxy")

        self.horizontalLayout_4.addWidget(self.lf_Gxy)

        self.in_Gxz = QLabel(self.g_shear)
        self.in_Gxz.setObjectName(u"in_Gxz")
        self.in_Gxz.setFont(font)

        self.horizontalLayout_4.addWidget(self.in_Gxz)

        self.lf_Gxz = FloatEdit(self.g_shear)
        self.lf_Gxz.setObjectName(u"lf_Gxz")

        self.horizontalLayout_4.addWidget(self.lf_Gxz)

        self.in_Gyz = QLabel(self.g_shear)
        self.in_Gyz.setObjectName(u"in_Gyz")
        self.in_Gyz.setFont(font)

        self.horizontalLayout_4.addWidget(self.in_Gyz)

        self.lf_Gyz = FloatEdit(self.g_shear)
        self.lf_Gyz.setObjectName(u"lf_Gyz")

        self.horizontalLayout_4.addWidget(self.lf_Gyz)

        self.verticalLayout_4.addWidget(self.g_shear)

        self.verticalSpacer_5 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_4.addItem(self.verticalSpacer_5)

        self.nav_meca.addWidget(self.page_niso_mec)
        self.page_iso_mec = QWidget()
        self.page_iso_mec.setObjectName(u"page_iso_mec")
        self.gridLayout_6 = QGridLayout(self.page_iso_mec)
        self.gridLayout_6.setObjectName(u"gridLayout_6")
        self.in_E = QLabel(self.page_iso_mec)
        self.in_E.setObjectName(u"in_E")
        self.in_E.setFont(font)

        self.gridLayout_6.addWidget(self.in_E, 0, 0, 1, 1)

        self.lf_G = FloatEdit(self.page_iso_mec)
        self.lf_G.setObjectName(u"lf_G")

        self.gridLayout_6.addWidget(self.lf_G, 2, 2, 1, 2)

        self.verticalSpacer_6 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.gridLayout_6.addItem(self.verticalSpacer_6, 4, 3, 1, 1)

        self.unit_G = QLabel(self.page_iso_mec)
        self.unit_G.setObjectName(u"unit_G")

        self.gridLayout_6.addWidget(self.unit_G, 2, 4, 1, 1)

        self.lf_E = FloatEdit(self.page_iso_mec)
        self.lf_E.setObjectName(u"lf_E")

        self.gridLayout_6.addWidget(self.lf_E, 0, 1, 1, 3)

        self.in_G = QLabel(self.page_iso_mec)
        self.in_G.setObjectName(u"in_G")
        self.in_G.setFont(font)

        self.gridLayout_6.addWidget(self.in_G, 2, 0, 1, 2)

        self.in_nu = QLabel(self.page_iso_mec)
        self.in_nu.setObjectName(u"in_nu")
        self.in_nu.setFont(font)

        self.gridLayout_6.addWidget(self.in_nu, 1, 0, 1, 3)

        self.lf_nu = FloatEdit(self.page_iso_mec)
        self.lf_nu.setObjectName(u"lf_nu")

        self.gridLayout_6.addWidget(self.lf_nu, 1, 3, 1, 1)

        self.unit_E = QLabel(self.page_iso_mec)
        self.unit_E.setObjectName(u"unit_E")

        self.gridLayout_6.addWidget(self.unit_E, 0, 4, 1, 1)

        self.nav_meca.addWidget(self.page_iso_mec)

        self.verticalLayout_12.addWidget(self.nav_meca)

        self.nav_phy.addTab(self.tab_mec, "")
        self.tab_ther = QWidget()
        self.tab_ther.setObjectName(u"tab_ther")
        self.verticalLayout_2 = QVBoxLayout(self.tab_ther)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.g_lambda = QGroupBox(self.tab_ther)
        self.g_lambda.setObjectName(u"g_lambda")
        self.g_lambda.setMaximumSize(QSize(16777215, 80))
        self.verticalLayout_11 = QVBoxLayout(self.g_lambda)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.nav_ther = QStackedWidget(self.g_lambda)
        self.nav_ther.setObjectName(u"nav_ther")
        self.page_niso_ther = QWidget()
        self.page_niso_ther.setObjectName(u"page_niso_ther")
        self.horizontalLayout_5 = QHBoxLayout(self.page_niso_ther)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.in_Lx = QLabel(self.page_niso_ther)
        self.in_Lx.setObjectName(u"in_Lx")
        self.in_Lx.setFont(font)

        self.horizontalLayout_5.addWidget(self.in_Lx)

        self.lf_Lx = FloatEdit(self.page_niso_ther)
        self.lf_Lx.setObjectName(u"lf_Lx")

        self.horizontalLayout_5.addWidget(self.lf_Lx)

        self.in_Ly = QLabel(self.page_niso_ther)
        self.in_Ly.setObjectName(u"in_Ly")
        self.in_Ly.setFont(font)

        self.horizontalLayout_5.addWidget(self.in_Ly)

        self.lf_Ly = FloatEdit(self.page_niso_ther)
        self.lf_Ly.setObjectName(u"lf_Ly")

        self.horizontalLayout_5.addWidget(self.lf_Ly)

        self.in_Lz = QLabel(self.page_niso_ther)
        self.in_Lz.setObjectName(u"in_Lz")
        self.in_Lz.setFont(font)

        self.horizontalLayout_5.addWidget(self.in_Lz)

        self.lf_Lz = FloatEdit(self.page_niso_ther)
        self.lf_Lz.setObjectName(u"lf_Lz")

        self.horizontalLayout_5.addWidget(self.lf_Lz)

        self.nav_ther.addWidget(self.page_niso_ther)
        self.page_iso_ther = QWidget()
        self.page_iso_ther.setObjectName(u"page_iso_ther")
        self.horizontalLayout_7 = QHBoxLayout(self.page_iso_ther)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.in_L = QLabel(self.page_iso_ther)
        self.in_L.setObjectName(u"in_L")
        self.in_L.setFont(font)

        self.horizontalLayout_7.addWidget(self.in_L)

        self.lf_L = FloatEdit(self.page_iso_ther)
        self.lf_L.setObjectName(u"lf_L")

        self.horizontalLayout_7.addWidget(self.lf_L)

        self.unit_L = QLabel(self.page_iso_ther)
        self.unit_L.setObjectName(u"unit_L")

        self.horizontalLayout_7.addWidget(self.unit_L)

        self.nav_ther.addWidget(self.page_iso_ther)

        self.verticalLayout_11.addWidget(self.nav_ther)

        self.verticalLayout_2.addWidget(self.g_lambda)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.in_alpha = QLabel(self.tab_ther)
        self.in_alpha.setObjectName(u"in_alpha")
        self.in_alpha.setFont(font)

        self.gridLayout_3.addWidget(self.in_alpha, 1, 0, 1, 1)

        self.in_Cp = QLabel(self.tab_ther)
        self.in_Cp.setObjectName(u"in_Cp")
        self.in_Cp.setFont(font)

        self.gridLayout_3.addWidget(self.in_Cp, 0, 0, 1, 1)

        self.lf_alpha = FloatEdit(self.tab_ther)
        self.lf_alpha.setObjectName(u"lf_alpha")

        self.gridLayout_3.addWidget(self.lf_alpha, 1, 1, 1, 1)

        self.unit_Cp = QLabel(self.tab_ther)
        self.unit_Cp.setObjectName(u"unit_Cp")
        self.unit_Cp.setFont(font)

        self.gridLayout_3.addWidget(self.unit_Cp, 0, 2, 1, 1)

        self.lf_Cp = FloatEdit(self.tab_ther)
        self.lf_Cp.setObjectName(u"lf_Cp")

        self.gridLayout_3.addWidget(self.lf_Cp, 0, 1, 1, 1)

        self.verticalLayout_2.addLayout(self.gridLayout_3)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer_3)

        self.nav_phy.addTab(self.tab_ther, "")
        self.tab_eco = QWidget()
        self.tab_eco.setObjectName(u"tab_eco")
        self.verticalLayout_6 = QVBoxLayout(self.tab_eco)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.horizontalLayout_6 = QHBoxLayout()
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.in_cost_unit = QLabel(self.tab_eco)
        self.in_cost_unit.setObjectName(u"in_cost_unit")
        self.in_cost_unit.setFont(font)

        self.horizontalLayout_6.addWidget(self.in_cost_unit)

        self.lf_cost_unit = FloatEdit(self.tab_eco)
        self.lf_cost_unit.setObjectName(u"lf_cost_unit")

        self.horizontalLayout_6.addWidget(self.lf_cost_unit)

        self.unit_cost_unit = QLabel(self.tab_eco)
        self.unit_cost_unit.setObjectName(u"unit_cost_unit")

        self.horizontalLayout_6.addWidget(self.unit_cost_unit)

        self.verticalLayout_6.addLayout(self.horizontalLayout_6)

        self.verticalSpacer_4 = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_6.addItem(self.verticalSpacer_4)

        self.nav_phy.addTab(self.tab_eco, "")

        self.verticalLayout.addWidget(self.nav_phy)

        self.horizontalGroupBox = QGroupBox(DMatSetup)
        self.horizontalGroupBox.setObjectName(u"horizontalGroupBox")
        self.horizontalLayout_9 = QHBoxLayout(self.horizontalGroupBox)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum
        )

        self.horizontalLayout_9.addItem(self.horizontalSpacer_2)

        self.b_add_matlib = QPushButton(self.horizontalGroupBox)
        self.b_add_matlib.setObjectName(u"b_add_matlib")

        self.horizontalLayout_9.addWidget(self.b_add_matlib)

        self.b_save = QPushButton(self.horizontalGroupBox)
        self.b_save.setObjectName(u"b_save")

        self.horizontalLayout_9.addWidget(self.b_save)

        self.b_cancel = QPushButton(self.horizontalGroupBox)
        self.b_cancel.setObjectName(u"b_cancel")

        self.horizontalLayout_9.addWidget(self.b_cancel)

        self.verticalLayout.addWidget(self.horizontalGroupBox)

        self.retranslateUi(DMatSetup)

        self.nav_phy.setCurrentIndex(1)
        self.nav_meca.setCurrentIndex(1)
        self.nav_ther.setCurrentIndex(1)

        QMetaObject.connectSlotsByName(DMatSetup)

    # setupUi

    def retranslateUi(self, DMatSetup):
        DMatSetup.setWindowTitle(
            QCoreApplication.translate("DMatSetup", u"Edit Material", None)
        )
        self.in_name.setText(QCoreApplication.translate("DMatSetup", u"name", None))
        self.le_name.setText("")
        self.is_isotropic.setText(
            QCoreApplication.translate("DMatSetup", u"is_isotropic", None)
        )
        self.unit_rho_elec.setText(
            QCoreApplication.translate("DMatSetup", u"ohm.m", None)
        )
        self.in_epsr.setText(QCoreApplication.translate("DMatSetup", u"epsr", None))
        self.in_rho_elec.setText(QCoreApplication.translate("DMatSetup", u"rho", None))
        self.nav_phy.setTabText(
            self.nav_phy.indexOf(self.tab_elec),
            QCoreApplication.translate("DMatSetup", u"Electrical", None),
        )
        self.in_mur_lin.setText(
            QCoreApplication.translate("DMatSetup", u"mur_lin", None)
        )
        self.in_Brm20.setText(QCoreApplication.translate("DMatSetup", u"Brm20", None))
        self.unit_Brm20.setText(QCoreApplication.translate("DMatSetup", u"T", None))
        self.in_alpha_Br.setText(
            QCoreApplication.translate("DMatSetup", u"alphaBr", None)
        )
        self.in_Wlam.setText(QCoreApplication.translate("DMatSetup", u"Wlam", None))
        self.unit_Wlam.setText(QCoreApplication.translate("DMatSetup", u"m", None))
        self.nav_phy.setTabText(
            self.nav_phy.indexOf(self.tab_mag),
            QCoreApplication.translate("DMatSetup", u"Magnetics", None),
        )
        self.in_rho_meca.setText(QCoreApplication.translate("DMatSetup", u"rho", None))
        self.unit_rho_meca.setText(
            QCoreApplication.translate("DMatSetup", u"kg/m^3", None)
        )
        self.g_young.setTitle(
            QCoreApplication.translate(
                "DMatSetup", u"Equivalent Yong Modulus [Pa]", None
            )
        )
        self.in_Ex.setText(QCoreApplication.translate("DMatSetup", u"Ex", None))
        self.in_Ey.setText(QCoreApplication.translate("DMatSetup", u"Ey", None))
        self.in_Ez.setText(QCoreApplication.translate("DMatSetup", u"Ez", None))
        self.g_poisson.setTitle(
            QCoreApplication.translate(
                "DMatSetup", u"Equivalent Poisson ratio [ ]", None
            )
        )
        self.in_nu_xy.setText(QCoreApplication.translate("DMatSetup", u"nu_xy", None))
        self.in_nu_xz.setText(QCoreApplication.translate("DMatSetup", u"nu_xz", None))
        self.in_nu_yz.setText(QCoreApplication.translate("DMatSetup", u"nu_yz", None))
        self.g_shear.setTitle(
            QCoreApplication.translate("DMatSetup", u"Shear modulus [Pa]", None)
        )
        self.in_Gxy.setText(QCoreApplication.translate("DMatSetup", u"Gxy", None))
        self.in_Gxz.setText(QCoreApplication.translate("DMatSetup", u"Gxz", None))
        self.in_Gyz.setText(QCoreApplication.translate("DMatSetup", u"Gyz", None))
        self.in_E.setText(QCoreApplication.translate("DMatSetup", u"E", None))
        self.unit_G.setText(QCoreApplication.translate("DMatSetup", u"Pa", None))
        self.in_G.setText(QCoreApplication.translate("DMatSetup", u"G", None))
        self.in_nu.setText(QCoreApplication.translate("DMatSetup", u"nu", None))
        self.unit_E.setText(QCoreApplication.translate("DMatSetup", u"Pa", None))
        self.nav_phy.setTabText(
            self.nav_phy.indexOf(self.tab_mec),
            QCoreApplication.translate("DMatSetup", u"Mechanics", None),
        )
        self.g_lambda.setTitle(
            QCoreApplication.translate("DMatSetup", u"Lambda [W/K]", None)
        )
        self.in_Lx.setText(QCoreApplication.translate("DMatSetup", u"X", None))
        self.in_Ly.setText(QCoreApplication.translate("DMatSetup", u"Y", None))
        self.in_Lz.setText(QCoreApplication.translate("DMatSetup", u"Z", None))
        self.in_L.setText(QCoreApplication.translate("DMatSetup", u"Lambda", None))
        self.unit_L.setText(QCoreApplication.translate("DMatSetup", u"W / K", None))
        self.in_alpha.setText(QCoreApplication.translate("DMatSetup", u"alpha", None))
        self.in_Cp.setText(QCoreApplication.translate("DMatSetup", u"Cp", None))
        self.unit_Cp.setText(
            QCoreApplication.translate("DMatSetup", u"W / kg / K", None)
        )
        self.nav_phy.setTabText(
            self.nav_phy.indexOf(self.tab_ther),
            QCoreApplication.translate("DMatSetup", u"Thermics", None),
        )
        self.in_cost_unit.setText(
            QCoreApplication.translate("DMatSetup", u"cost_unit", None)
        )
        self.unit_cost_unit.setText(
            QCoreApplication.translate("DMatSetup", u"\u20ac / kg", None)
        )
        self.nav_phy.setTabText(
            self.nav_phy.indexOf(self.tab_eco),
            QCoreApplication.translate("DMatSetup", u"Economical", None),
        )
        self.b_add_matlib.setText(
            QCoreApplication.translate("DMatSetup", u"Add to MatLib", None)
        )
        self.b_save.setText(QCoreApplication.translate("DMatSetup", u"Save", None))
        self.b_cancel.setText(QCoreApplication.translate("DMatSetup", u"Cancel", None))

    # retranslateUi

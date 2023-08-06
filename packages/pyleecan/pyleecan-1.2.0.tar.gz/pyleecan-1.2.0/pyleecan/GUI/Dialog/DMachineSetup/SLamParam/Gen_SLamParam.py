# -*- coding: utf-8 -*-
"""File generated according to SLamParam/gen_list.json
WARNING! All changes made in this file will be lost!
"""
from pyleecan.GUI.Dialog.DMachineSetup.SLamParam.Ui_SLamParam import Ui_SLamParam


class Gen_SLamParam(Ui_SLamParam):
    def setupUi(self, SLamParam):
        """Abstract class to update the widget according to the csv doc"""
        Ui_SLamParam.setupUi(self, SLamParam)
        # Setup of in_L1
        txt = self.tr(
            u"""Lamination stack active length [m] without radial ventilation airducts but including insulation layers between lamination sheets"""
        )
        self.in_L1.setWhatsThis(txt)
        self.in_L1.setToolTip(txt)

        # Setup of lf_L1
        self.lf_L1.validator().setBottom(0)
        self.lf_L1.validator().setTop(100)
        txt = self.tr(
            u"""Lamination stack active length [m] without radial ventilation airducts but including insulation layers between lamination sheets"""
        )
        self.lf_L1.setWhatsThis(txt)
        self.lf_L1.setToolTip(txt)

        # Setup of in_Kf1
        txt = self.tr(u"""lamination stacking / packing factor""")
        self.in_Kf1.setWhatsThis(txt)
        self.in_Kf1.setToolTip(txt)

        # Setup of lf_Kf1
        self.lf_Kf1.validator().setBottom(0)
        self.lf_Kf1.validator().setTop(1)
        txt = self.tr(u"""lamination stacking / packing factor""")
        self.lf_Kf1.setWhatsThis(txt)
        self.lf_Kf1.setToolTip(txt)

        # Setup of w_mat
        txt = self.tr(u"""Lamination's material""")
        self.w_mat.setWhatsThis(txt)
        self.w_mat.setToolTip(txt)

        # Setup of in_Wrvd
        txt = self.tr(u"""axial width of ventilation ducts in lamination""")
        self.in_Wrvd.setWhatsThis(txt)
        self.in_Wrvd.setToolTip(txt)

        # Setup of lf_Wrvd
        self.lf_Wrvd.validator().setBottom(0)
        txt = self.tr(u"""axial width of ventilation ducts in lamination""")
        self.lf_Wrvd.setWhatsThis(txt)
        self.lf_Wrvd.setToolTip(txt)

        # Setup of in_Nrvd
        txt = self.tr(u"""number of radial air ventilation ducts in lamination""")
        self.in_Nrvd.setWhatsThis(txt)
        self.in_Nrvd.setToolTip(txt)

        # Setup of si_Nrvd
        self.si_Nrvd.setMinimum(0)
        self.si_Nrvd.setMaximum(999999)
        txt = self.tr(u"""number of radial air ventilation ducts in lamination""")
        self.si_Nrvd.setWhatsThis(txt)
        self.si_Nrvd.setToolTip(txt)

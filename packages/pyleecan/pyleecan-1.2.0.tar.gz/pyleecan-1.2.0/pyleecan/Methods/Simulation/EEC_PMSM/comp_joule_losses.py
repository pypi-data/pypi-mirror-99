# -*- coding: utf-8 -*-


def comp_joule_losses(self, output):
    """Compute the electrical Joule losses

    Parameters
    ----------
    self : Electrical
        an Electrical object
    output : Output
        an Output object
    """

    qs = output.simu.machine.stator.winding.qs
    Id = output.elec.Id_ref
    Iq = output.elec.Iq_ref
    R = self.parameters["R20"]

    # Id and Iq are in RMS
    Pj_losses = qs * R * (Id ** 2 + Iq ** 2)

    output.elec.Pj_losses = Pj_losses

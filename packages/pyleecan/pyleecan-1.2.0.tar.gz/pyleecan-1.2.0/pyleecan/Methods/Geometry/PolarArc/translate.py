# -*-- coding: utf-8 -*


def translate(self, Zt):
    """Do the translation of the PolarArc

    Parameters
    ----------
    self : PolarArc
        a PolarArc object

    Zt : complex
        Complex value for translation

    Returns
    -------
    None
    """
    # check if the PolarArc is correct
    self.check()
    self.point_ref += Zt

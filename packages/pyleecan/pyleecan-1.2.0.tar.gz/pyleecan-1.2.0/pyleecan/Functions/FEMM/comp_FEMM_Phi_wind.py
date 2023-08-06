from numpy import zeros


def comp_FEMM_Phi_wind(
    femm, qs, Npcpp, is_stator, Lfemm, L1, sym, is_rescale_flux=True
):
    """Compute the total fluxlinkage of the winding phases

    Parameters
    ----------
    femm : FEMMHandler
        client to send command to a FEMM instance
    qs : int
        number of phases
    Npcpp : int
        number of parallel circuits per phase (maximum 2p)
    is_stator : bool
        true if windings are stator windings
    Lfemm : float
        lenght of FEMM model
    L1 : float
        actual lenght for rescaling fluxlinkage
    sym : int
        symmetry factor (ie. 1 = full machine, 2 = half machine ...)
    is_rescale_flux : bool
        True if rescaling should be applied

    Returns
    -------
    Phi_wind : float
        fluxlinkage of the winding phases [Vs]

    """
    Phi_wind = zeros((1, qs))

    if is_stator:
        label = "Circs"
    else:
        label = "Circr"

    # For each phase/circuit
    for q in range(qs):
        try:
            PropCirc = femm.mo_getcircuitproperties(label + str(q))
            # rescaling to account for end winding flux
            if is_rescale_flux:
                Kphi = L1 / Lfemm
            else:
                Kphi = 1
            # flux linkage of phase q in Wb=Vs=HA
            Phi_wind[0, q] = sym * PropCirc[2] * Kphi / Npcpp
        except:
            Phi_wind[0, q] = None
    return Phi_wind

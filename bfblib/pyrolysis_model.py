import chemics as cm


class PyrolysisModel:
    """
    Pyrolysis model.

    Attributes
    ----------
    t_devol : float
        Devolatilization time of biomass particle [s]
    """

    def __init__(self, gas, params):
        self._dpbio = params.biomass['dp_mean'] * 1000
        self._tk = gas.tk
        self._calc_devol_time()

    def _calc_devol_time(self):
        """
        Calculate devolatilization time [s] of the biomass particle.
        """
        tv = cm.devol_time(self._dpbio, self._tk)
        self.t_devol = tv

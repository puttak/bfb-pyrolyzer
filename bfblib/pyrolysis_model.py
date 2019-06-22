import chemics as cm


class PyrolysisModel:

    def __init__(self, gas, params):
        self.dp_bio = params.biomass['dp_mean'] * 1000
        self.tk = gas.tk
        self._calc_devol_time()

    def _calc_devol_time(self):
        """
        Calculate devolatilization time [s] of the biomass particle.
        """
        tv = cm.devol_time(self.dp_bio, self.tk)
        self.t_devol = tv

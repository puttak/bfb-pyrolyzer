import chemics as cm


class PyrolysisModel:

    def __init__(self, gas, params):
        self._gas = gas
        self._params = params

    def calc_devol_time(self):
        """
        Returns
        -------
        tv : float
            Devolatilization time of the biomass particle [s]
        """
        dp = self._params.biomass['dp_mean'] * 1000
        tv = cm.devol_time(dp, self._gas.tk)
        return tv

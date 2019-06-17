import chemics as cm


class PyrolysisModel:

    def __init__(self, gas, params):
        self._gas = gas
        self._params = params

        self.t_devol = None

    def solve(self):
        """
        Solve pyrolysis model and store results.
        """
        t_devol = self.calc_devol_time()
        self.t_devol = t_devol

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

import chemics as cm


class PyrolysisModel:

    def __init__(self, gas, params):
        self.gas = gas
        self.params = params
        self.results = {}

    def solve(self):
        """
        Solve pyrolysis model and store results.
        """
        t_devol = self.calc_devol_time()

        # Store results from pyrolysis model calculations
        self.results = {
            't_devol': round(t_devol, 4)
        }

    def calc_devol_time(self):
        """
        Returns
        -------
        tv : float
            Devolatilization time of the biomass particle [s]
        """
        dp = self.params.biomass['dp_mean'] * 1000
        tv = cm.devol_time(dp, self.gas.tk)
        return tv

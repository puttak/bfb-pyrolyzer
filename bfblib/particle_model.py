import numpy as np
from .trans_heat_cond import hc2


class ParticleModel:

    def __init__(self, gas, params):
        self._gas = gas
        self._params = params

    def build_time_vector(self):
        """
        Returns
        -------
        t : vector
            Times for calculating transient heat conduction in biomass particle [s]
        """
        # nt is number of time steps
        nt = self._params.biomass['nt']
        tmax = self._params.biomass['t_max']
        dt = tmax / nt                      # time step [s]
        t = np.arange(0, tmax + dt, dt)     # time vector [s]
        return t

    def calc_trans_hc(self, t, tk_inf):
        """
        Parameters
        ----------
        t : vector
            Time values to calculate intra-particle heat conduction [s]
        tk_inf : float
            Ambient temperature [K]

        Returns
        -------
        tk : array
            Temperature profile inside the biomass particle [K]
        """
        # Calculate temperature profiles within particle.
        # rows = time step, columns = center to surface temperature
        dp = self._params.biomass['dp_mean']
        mc = self._params.biomass['mc']
        k = self._params.biomass['k']
        sg = self._params.biomass['sg']
        h = self._params.biomass['h']
        ti = self._params.biomass['tk_i']
        b = self._params.biomass['b']
        m = self._params.biomass['m']
        tk = hc2(dp, mc, k, sg, h, ti, tk_inf, b, m, t)     # temperature array [K]
        return tk

    def calc_time_tkinf(self, t_hc, tk_hc):
        """
        Returns
        -------
        t : float
            Time when biomass particle is near reactor temperature [s]
        """
        tk_ref = self._gas.tk - 1                       # value near reactor temperature [K]
        idx = np.where(tk_hc[:, 0] > tk_ref)[0][0]      # index where T > Tinf
        t_ref = t_hc[idx]                               # time where T > Tinf
        return t_ref

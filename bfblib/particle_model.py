import numpy as np
from .trans_heat_cond import hc2


class ParticleModel:
    """
    Particle model.

    Attributes
    ----------
    t_vec : vector
        Time vector for intra-particle temperature profile [s]
    tk_array : array
        Temperature profile for intra-particle heat conduction [K]
    t_ref : float
        Time when center of particle is near reactor temperature [s]
    """

    def __init__(self, gas, params):
        self._b = params.biomass['b']
        self._dpbio = params.biomass['dp_mean']
        self._h = params.biomass['h']
        self._k = params.biomass['k']
        self._m = params.biomass['m']
        self._mc = params.biomass['mc']
        self._nt = params.biomass['nt']
        self._sg = params.biomass['sg']
        self._tmax = params.biomass['t_max']
        self._tki = params.biomass['tk_i']
        self._tkinf = gas.tk
        self._build_time_vector()
        self._calc_trans_hc()
        self._calc_time_tkinf()

    def _build_time_vector(self):
        """
        Times [s] for calculating transient heat conduction in biomass particle.
        """
        # nt is number of time steps
        dt = self._tmax / self._nt                    # time step [s]
        t_vec = np.arange(0, self._tmax + dt, dt)    # time vector [s]
        self.t_vec = t_vec

    def _calc_trans_hc(self,):
        """
        Calculate intra-particle temperature profile [K] for biomass particle.
        """
        # rows = time step, columns = center to surface temperature
        tk = hc2(self._dpbio, self._mc, self._k, self._sg, self._h, self._tki, self._tkinf, self._b, self._m, self.t_vec)     # temperature array [K]
        self.tk_array = tk

    def _calc_time_tkinf(self):
        """
        Time [s] when biomass particle is near reactor temperature.
        """
        tk_ref = self._tkinf - 1                            # value near reactor temperature [K]
        idx = np.where(self.tk_array[:, 0] > tk_ref)[0][0]  # index where T > Tinf
        t_ref = self.t_vec[idx]                             # time where T > Tinf
        self.t_ref = t_ref

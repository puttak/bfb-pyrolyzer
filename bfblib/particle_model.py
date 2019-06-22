import numpy as np
from .trans_heat_cond import hc2


class ParticleModel:

    def __init__(self, gas, params):
        self.b = params.biomass['b']
        self.dp_bio = params.biomass['dp_mean']
        self.h = params.biomass['h']
        self.k = params.biomass['k']
        self.m = params.biomass['m']
        self.mc = params.biomass['mc']
        self.nt = params.biomass['nt']
        self.sg = params.biomass['sg']
        self.tmax = params.biomass['t_max']
        self.tk_i = params.biomass['tk_i']
        self.tk_inf = gas.tk
        self._build_time_vector()
        self._calc_trans_hc()
        self._calc_time_tkinf()

    def _build_time_vector(self):
        """
        Times [s] for calculating transient heat conduction in biomass particle.
        """
        # nt is number of time steps
        dt = self.tmax / self.nt                    # time step [s]
        t_vec = np.arange(0, self.tmax + dt, dt)    # time vector [s]
        self.t_vec = t_vec

    def _calc_trans_hc(self,):
        """
        Calculate intra-particle temperature profile [K] for biomass particle.
        """
        # rows = time step, columns = center to surface temperature
        tk = hc2(self.dp_bio, self.mc, self.k, self.sg, self.h, self.tk_i, self.tk_inf, self.b, self.m, self.t_vec)     # temperature array [K]
        self.tk_array = tk

    def _calc_time_tkinf(self):
        """
        Time [s] when biomass particle is near reactor temperature.
        """
        tk_ref = self.tk_inf - 1                            # value near reactor temperature [K]
        idx = np.where(self.tk_array[:, 0] > tk_ref)[0][0]  # index where T > Tinf
        t_ref = self.t_vec[idx]                             # time where T > Tinf
        self.t_ref = t_ref

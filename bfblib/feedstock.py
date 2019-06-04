import chemics as cm
import numpy as np
from .trans_heat_cond import hc2


class Feedstock():

    def __init__(self, params):
        self.dp = params.feedstock['dp']
        self.h = params.feedstock['h']
        self.k = params.feedstock['k']
        self.mc = params.feedstock['mc']
        self.sg = params.feedstock['sg']
        self.ti = params.feedstock['ti']
        self.tinf = params.feedstock['tinf']
        self.tmax = params.feedstock['tmax']
        self.m = params.feedstock['m']

    def devol_time(self, t):
        dp = self.dp * 1000
        tv = cm.devol_time(dp, t)
        return tv

    def hc_time_vector(self, nt=1000):
        # nt is number of time steps
        dt = self.tmax / nt                      # time step [s]
        t = np.arange(0, self.tmax + dt, dt)     # time vector [s]
        return t

    def heat_cond(self, t, b=2, m=1000):
        # Calculate temperature profiles within particle.
        # rows = time step, columns = center to surface temperature
        tk = hc2(self.dp, self.mc, self.k, self.sg, self.h, self.ti, self.tinf, b, m, t)    # temperature array [K]
        return tk

    def get_time_tinf(self, t, tk):
        # Determine time when particle has reached near reactor temperature.
        tk_ref = self.tinf - 1                      # value near reactor temperature [K]
        idx = np.where(tk[:, 0] > tk_ref)[0][0]     # index where T > Tinf
        t_ref = t[idx]                                # time where T > Tinf
        return t_ref

import chemics as cm
import numpy as np
from .trans_heat_cond import hc2


class BfbModel:

    def __init__(self, gas, params):
        self.gas = gas

        self.di_rct = params.reactor['di']
        self.ac_rct = (np.pi * self.di_rct**2) / 4

        self.dp_bed = params.bed['dps'][0]
        self.dp_min_bed = params.bed['dps'][1]
        self.dp_max_bed = params.bed['dps'][2]
        self.ep_bed = params.bed['ep']
        self.phi_bed = params.bed['phi']
        self.rhos_bed = params.bed['rhos']
        self.zmf_bed = params.bed['zmf']
        self.us_bed = None
        self.umf_ergun_bed = None
        self.umf_wenyu_bed = None
        self.zexp_bed = None

        self.dp_feed = params.feed['dp_mean']
        self.h_feed = params.feed['h']
        self.mc_feed = params.feed['mc']
        self.k_feed = params.feed['k']
        self.sg_feed = params.feed['sg']
        self.ti_feed = params.feed['ti']
        self.tv_feed = None

        self.b_hc = params.sim['b']
        self.m_hc = params.sim['m']
        self.nt_hc = params.sim['nt']
        self.tmax_hc = params.sim['tmax']
        self.t_hc = None
        self.t_tinf = None
        self.tk_hc = None

        self._build_t_hc()
        self._calc_us()
        self._calc_devol_time()
        self._calc_trans_hc()
        self._calc_time_to_tinf()

    def _build_t_hc(self):
        # nt is number of time steps
        dt = self.tmax_hc / self.nt_hc                # time step [s]
        t = np.arange(0, self.tmax_hc + dt, dt)    # time vector [s]
        self.t_hc = t

    def _calc_us(self):
        p_kPa = self.gas.p / 1000
        q_lpm = cm.slm_to_lpm(self.gas.q, p_kPa, self.gas.tk)
        q_m3s = q_lpm / 60_000
        us = q_m3s / self.ac_rct
        self.us_bed = us

    def _calc_devol_time(self):
        dp = self.dp_feed * 1000
        tv = cm.devol_time(dp, self.gas.tk)
        self.tv_feed = tv

    def _calc_trans_hc(self):
        # Calculate temperature profiles within particle.
        # rows = time step, columns = center to surface temperature
        tinf = self.gas.tk
        tk = hc2(self.dp_feed, self.mc_feed, self.k_feed, self.sg_feed, self.h_feed, self.ti_feed, tinf, self.b_hc, self.m_hc, self.t_hc)    # temperature array [K]
        self.tk_hc = tk

    def _calc_time_to_tinf(self):
        # Determine time when particle has reached near reactor temperature.
        tk_ref = self.gas.tk - 1                            # value near reactor temperature [K]
        idx = np.where(self.tk_hc[:, 0] > tk_ref)[0][0]     # index where T > Tinf
        t_ref = self.t_hc[idx]                              # time where T > Tinf
        self.t_tinf = t_ref

    def calc_umf_ergun(self, mu_option):
        # Conversion for kg/ms = µP * 1e-7
        if mu_option == 'graham':
            mug = self.gas.mu_graham * 1e-7
        elif mu_option == 'herning':
            mug = self.gas.mu_herning * 1e-7
        else:
            mug = self.gas.mu * 1e-7
        rhog = self.gas.rho
        umf = cm.umf_ergun(self.dp_bed, self.ep_bed, mug, self.phi_bed, rhog, self.rhos_bed)
        self.umf_ergun_bed = umf

    def calc_zexp(self, umf_option):
        if umf_option == 'ergun':
            umf = self.umf_ergun_bed
        elif umf_option == 'wenyu':
            umf = self.umf_wenyu_bed
        rhog = self.gas.rho
        fbexp = cm.fbexp(self.di_rct, self.dp_bed, rhog, self.rhos_bed, umf, self.us_bed)
        zexp = self.zmf_bed * fbexp
        self.zexp_bed = zexp

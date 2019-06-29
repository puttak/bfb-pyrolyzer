import chemics as cm
import numpy as np


class BfbModel:
    """
    Bubbling fluidized bed model.

    Attributes
    ----------
    ac : float
        Inner cross section area of the reactor [m²]
    di : float
        Inner diameter of the reactor [m]
    q : float
        Volumetric flowrate of gas into reactor [SLM]
    tdh_chan : float
        Transport disengaging height from Chan equation [m]
    tdh_horio : float
        Transport disengaging height from Horio equation [m]
    us : float
        Superficial gas velocity [m/s]
    us_umf_ergun : float
        Ratio of Us/Umf based on Ergun equation [-]
    us_umf_wenyu : float
        Ratio of Us/Umf based on Wen and Yu equation [-]
    zexp_ergun : float
        Expanded bed height based on Ergun equation [m]
    zexp_wenyu : float
        Expanded bed height based on Wen and Yu equation [m]
    zmf : float
        Bed height at minimum fluidization [m]
    """

    def __init__(self, di, q, zmf):
        self.di = di
        self.q = q
        self.zmf = zmf
        self._calc_ac()

    def _calc_ac(self):
        """
        Calculate inner cross section area [m²] of the reactor.
        """
        area = (np.pi * self.di**2) / 4
        self.ac = area

    def calc_us(self, gas):
        """
        Calculate superficial gas velocity [m/s].
        """
        p_kpa = gas.p / 1000
        q_lpm = cm.slm_to_lpm(self.q, p_kpa, gas.tk)
        q_m3s = q_lpm / 60_000
        us = q_m3s / self.ac
        self.us = us

    def calc_us_umf(self, bed):
        """
        Calculate ratio of Us/Umf.
        """
        self.us_umf_ergun = self.us / bed.umf_ergun
        self.us_umf_wenyu = self.us / bed.umf_wenyu

    def calc_tdh(self):
        """
        Calculate transport disengaging height [m] from Chan and Horio equations.
        """
        tdh_chan = 0.85 * (self.us**1.2) * (7.33 - 1.2 * np.log(self.us))
        tdh_horio = ((2.7 * self.di ** -0.36) - 0.7) * self.di * np.exp(0.74 * self.us * self.di ** -0.23)
        self.tdh_chan = tdh_chan
        self.tdh_horio = tdh_horio

    def calc_zexp(self, bed, gas):
        """
        Calculate expanded bed height [m] from the bed expansion factor.
        """
        fbexp_ergun = cm.fbexp(self.di, bed.dp, gas.rho, bed.rho, bed.umf_ergun, self.us)
        zexp_ergun = self.zmf * fbexp_ergun
        fbexp_wenyu = cm.fbexp(self.di, bed.dp, gas.rho, bed.rho, bed.umf_wenyu, self.us)
        zexp_wenyu = self.zmf * fbexp_wenyu
        self.zexp_ergun = zexp_ergun
        self.zexp_wenyu = zexp_wenyu

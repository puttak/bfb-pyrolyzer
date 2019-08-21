import chemics as cm
import numpy as np


class BfbReactor:
    """
    Bubbling fluidized bed reactor model.

    Attributes
    ----------
    ac : float
        Inner cross section area of the reactor [m²]
    di : float
        Inner diameter of the reactor [m]
    q : float
        Volumetric flowrate of gas into reactor [SLM]
    zmf : float
        Bed height at minimum fluidization [m]
    """

    def __init__(self, di, q, zmf):
        self.ac = (np.pi * di**2) / 4
        self.di = di
        self.q = q
        self.zmf = zmf

    def calc_us(self, gas):
        """
        Calculate superficial gas velocity [m/s].
        """
        p_kpa = gas.p / 1000
        q_lpm = cm.slm_to_lpm(self.q, p_kpa, gas.tk)
        q_m3s = q_lpm / 60_000
        us = q_m3s / self.ac
        return us

    @staticmethod
    def calc_us_umf(us, umf):
        """
        Calculate ratio of Us/Umf [-].
        """
        us_umf = us / umf
        return us_umf

    @staticmethod
    def calc_tdh_chan(us):
        """
        Calculate transport disengaging height [m] from Chan correlation.
        """
        tdh_chan = cm.tdh_chan(us)
        return tdh_chan

    def calc_tdh_horio(self, us):
        """
        Calculate transport disengaging height [m] from Horio correlation.
        """
        tdh_horio = cm.tdh_horio(self.di, us)
        return tdh_horio

    def calc_zexp_ergun(self, bed, gas, umf_ergun, us):
        """
        Calculate expanded bed height [m] based on Umf from Ergun equation.
        """
        fbexp_ergun = cm.fbexp(self.di, bed.dp, gas.rho, bed.rho, umf_ergun, us)
        zexp_ergun = self.zmf * fbexp_ergun
        return zexp_ergun

    def calc_zexp_wenyu(self, bed, gas, umf_wenyu, us):
        """
        Calculate expanded bed height [m] based on Umf from WenYu equation.
        """
        fbexp_wenyu = cm.fbexp(self.di, bed.dp, gas.rho, bed.rho, umf_wenyu, us)
        zexp_wenyu = self.zmf * fbexp_wenyu
        return zexp_wenyu

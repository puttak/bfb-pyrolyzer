import chemics as cm
import numpy as np
from helpers import Tdh, UsUmf, Zexp


class BfbReactor:
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
    tdh : namedtuple
        Transport disengaging height [m]. Values available for `chan` and `horio`.
    us : float
        Superficial gas velocity [m/s]
    us_umf : namedtuple
        Ratio of Us/Umf [-]. Values available for `ergun` and `wenyu`.
    zexp : namedtuple
        Expanded bed height [m]. Values available for `ergun` and `wenyu`.
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
        self.us = us

    def calc_us_umf(self, bed):
        """
        Calculate ratio of Us/Umf.
        """
        us_umf_ergun = self.us / bed.umf.ergun
        us_umf_wenyu = self.us / bed.umf.wenyu
        self.us_umf = UsUmf(us_umf_ergun, us_umf_wenyu)

    def calc_tdh(self):
        """
        Calculate transport disengaging height [m] from Chan and Horio correlations.
        """
        tdh_chan = cm.tdh_chan(self.us)
        tdh_horio = cm.tdh_horio(self.di, self.us)
        self.tdh = Tdh(tdh_chan, tdh_horio)

    def calc_zexp(self, bed, gas):
        """
        Calculate expanded bed height [m] from the bed expansion factor.
        """
        fbexp_ergun = cm.fbexp(self.di, bed.dp, gas.rho, bed.rho, bed.umf.ergun, self.us)
        zexp_ergun = self.zmf * fbexp_ergun
        fbexp_wenyu = cm.fbexp(self.di, bed.dp, gas.rho, bed.rho, bed.umf.wenyu, self.us)
        zexp_wenyu = self.zmf * fbexp_wenyu
        self.zexp = Zexp(zexp_ergun, zexp_wenyu)

import chemics as cm
import numpy as np


class BfbModel:
    """
    Bubbling fluidized bed model.

    Attributes
    ----------
    ac : float
        Inner cross section area of the reactor [m²]
    tdh_chan : float
        Transport disengaging height from Chan equation [m]
    tdh_horio : float
        Transport disengaging height from Horio equation [m]
    umf_ergun : float
        Minimum fluidization velocity from Ergun equation [m/s]
    umf_wenyu : float
        Minimum fluidization velocity from Wen and Yu equation [m/s]
    us : float
        Superficial gas velocity [m/s]
    us_umf_ergun : float
        Ratio of Us/Umf based on Ergun equation [-]
    us_umf_wenyu : float
        Ratio of Us/Umf based on Wen and Yu equation [-]
    ut_bed_ganser : float
        Bed particle terminal velocity from Ganser equation [m/s]
    ut_bed_haider : float
        Bed particle terminal velocity from Haider equation [m/s]
    ut_bio_ganser : float
        Biomass particle terminal velocity from Ganser equation [m/s]
    ut_bio_haider : float
        Biomass particle terminal velocity from Haider equation [m/s]
    ut_char_ganser : float
        Char particle terminal velocity from Ganser equation [m/s]
    ut_char_haider : float
        Char particle terminal velocity from Haider equation [m/s]
    zexp_ergun : float
        Expanded bed height based on Ergun equation [m]
    zexp_wenyu : float
        Expanded bed height based on Wen and Yu equation [m]
    """

    def __init__(self, gas, params):
        self._di = params.reactor['di']
        self._dpbed = params.bed['dp'][0]
        self._dpbio = params.biomass['dp_mean']
        self._ep = params.bed['ep']
        self._mu = gas.mu * 1e-7     # convert to kg/ms = µP * 1e-7
        self._p = gas.p
        self._phibed = params.bed['phi']
        self._phibio = params.biomass['phi']
        self._q = params.reactor['q']
        self._rhog = gas.rho
        self._rhosbed = params.bed['rhos']
        self._rhosbio = params.biomass['sg'] * 1000
        self._rhoschar = params.bed['rhos_char']
        self._tk = gas.tk
        self._zmf = params.bed['zmf']
        self._calc_ac()
        self._calc_us()
        self._calc_umf()
        self._calc_us_umf()
        self._calc_ut()
        self._calc_tdh()
        self._calc_zexp()

    def _calc_ac(self):
        """
        Calculate inner cross section area [m²] of the reactor.
        """
        area = (np.pi * self._di**2) / 4
        self.ac = area

    def _calc_us(self):
        """
        Calculate superficial gas velocity [m/s].
        """
        p_kpa = self._p / 1000
        q_lpm = cm.slm_to_lpm(self._q, p_kpa, self._tk)
        q_m3s = q_lpm / 60_000
        us = q_m3s / self.ac
        self.us = us

    def _calc_umf(self):
        """
        Calculate minimum fluidization velocity [m/s] for bed particles.
        """
        umf_ergun = cm.umf_ergun(self._dpbed, self._ep, self._mu, self._phibed, self._rhog, self._rhosbed)
        umf_wenyu = cm.umf_coeff(self._dpbed, self._mu, self._rhog, self._rhosbed, coeff='wenyu')
        self.umf = {'ergun': umf_ergun, 'wenyu': umf_wenyu}

    def _calc_us_umf(self):
        """
        Calculate ratio of Us/Umf.
        """
        us_umf_ergun = self.us / self.umf_ergun
        us_umf_wenyu = self.us / self.umf_wenyu
        self.us_umf = {'ergun': us_umf_ergun, 'wenyu': us_umf_wenyu}

    def _calc_ut(self):
        """
        Calculate terminal velocity [m/s] for bed, biomass, and char particles.
        """
        _, _, ut_bed_ganser = cm.ut_ganser(self._dpbed, self._mu, self._phibed, self._rhog, self._rhosbed)
        ut_bed_haider = cm.ut_haider(self._dpbed, self._mu, self._phibed, self._rhog, self._rhosbed)
        self.ut_bed = {'ganser': ut_bed_ganser, 'haider': ut_bed_haider}

        _, _, ut_bio_ganser = cm.ut_ganser(self._dpbio, self._mu, self._phibio, self._rhog, self._rhosbio)
        ut_bio_haider = cm.ut_haider(self._dpbio, self._mu, self._phibio, self._rhog, self._rhosbio)
        self.ut_bio = {'ganser': ut_bio_ganser, 'haider': ut_bio_haider}

        _, _, ut_char_ganser = cm.ut_ganser(self._dpbio, self._mu, self._phibio, self._rhog, self._rhoschar)
        ut_char_haider = cm.ut_haider(self._dpbio, self._mu, self._phibio, self._rhog, self._rhoschar)
        self.ut_char = {'ganser': ut_char_ganser, 'haider': ut_char_haider}

    def _calc_tdh(self):
        """
        Calculate transport disengaging height [m] from Chan and Horio equations.
        """
        tdh_chan = 0.85 * (self.us**1.2) * (7.33 - 1.2 * np.log(self.us))
        tdh_horio = ((2.7 * self._di ** -0.36) - 0.7) * self._di * np.exp(0.74 * self.us * self._di ** -0.23)
        self.tdh_chan = tdh_chan
        self.tdh_horio = tdh_horio

    def _calc_zexp(self):
        """
        Calculate expanded bed height [m] from the bed expansion factor.
        """
        fbexp_ergun = cm.fbexp(self._di, self._dpbed, self._rhog, self._rhosbed, self.umf_ergun, self.us)
        zexp_ergun = self._zmf * fbexp_ergun
        fbexp_wenyu = cm.fbexp(self._di, self._dpbed, self._rhog, self._rhosbed, self.umf_wenyu, self.us)
        zexp_wenyu = self._zmf * fbexp_wenyu
        self.zexp_ergun = zexp_ergun
        self.zexp_wenyu = zexp_wenyu

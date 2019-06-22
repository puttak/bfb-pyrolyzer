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
    dp_bed : float
        Bed particle diameter [m]
    dp_bio : float
        Biomass particle diameter [m]
    ep : float
        Void fraction of the bed [-]
    mu : float
        Gas viscosity [kg/ms]
    p : float
        Gas pressure [Pa]
    phi_bed : float
        Bed particle sphericity [-]
    phi_bio : float
        Biomass particle sphericity [-]
    q : float
        Gas volumetric flow rate [SLM]
    rhog : float
        Gas density [kg/m³]
    rhos_bed : float
        Bed particle density [kg/m³]
    rhos_bio : float
        Biomass particle density [kg/m³]
    rhos_char : float
        Char particle density [kg/m³]
    tdh_chan : float
        Transport disengaging height from Chan equation [m]
    tdh_horio : float
        Transport disengaging height from Horio equation [m]
    tk : float
        Gas temperature [K]
    umf_ergun : float
        Minimum fluidization velocity from Ergun equation [m/s]
    umf_wenyu : float
        Minimum fluidization velocity from Wen and Yu equation [m/s]
    us_umf_ergun : float
        Ratio of Us/Umf based on Ergun equation [-]
    us_umf_wenyu : float
        Ratio of Us/Umf based on Wen and Yu equation [-]
    us : float
        Superficial gas velocity [m/s]
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
    zmf : float
        Bed height at minimum fluidization [m]
    """

    def __init__(self, gas, params):
        self.di = params.reactor['di']
        self.dp_bed = params.bed['dp'][0]
        self.dp_bio = params.biomass['dp_mean']
        self.ep = params.bed['ep']
        self.mu = gas.mu * 1e-7     # convert to kg/ms = µP * 1e-7
        self.p = gas.p
        self.phi_bed = params.bed['phi']
        self.phi_bio = params.biomass['phi']
        self.q = params.reactor['q']
        self.rhog = gas.rho
        self.rhos_bed = params.bed['rhos']
        self.rhos_bio = params.biomass['sg'] * 1000
        self.rhos_char = params.bed['rhos_char']
        self.tk = gas.tk
        self.zmf = params.bed['zmf']
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
        area = (np.pi * self.di**2) / 4
        self.ac = area

    def _calc_us(self):
        """
        Calculate superficial gas velocity [m/s].
        """
        p_kpa = self.p / 1000
        q_lpm = cm.slm_to_lpm(self.q, p_kpa, self.tk)
        q_m3s = q_lpm / 60_000
        us = q_m3s / self.ac
        self.us = us

    def _calc_umf(self):
        """
        Calculate minimum fluidization velocity [m/s] for bed particles.
        """
        umf_ergun = cm.umf_ergun(self.dp_bed, self.ep, self.mu, self.phi_bed, self.rhog, self.rhos_bed)
        umf_wenyu = cm.umf_coeff(self.dp_bed, self.mu, self.rhog, self.rhos_bed, coeff='wenyu')
        self.umf_ergun = umf_ergun
        self.umf_wenyu = umf_wenyu

    def _calc_us_umf(self):
        """
        Calculate ratio of Us/Umf.
        """
        us_umf_ergun = self.us / self.umf_ergun
        us_umf_wenyu = self.us / self.umf_wenyu
        self.us_umf_ergun = us_umf_ergun
        self.us_umf_wenyu = us_umf_wenyu

    def _calc_ut(self):
        """
        Calculate terminal velocity [m/s] for bed, biomass, and char particles.
        """
        _, _, ut_bed_ganser = cm.ut_ganser(self.dp_bed, self.mu, self.phi_bed, self.rhog, self.rhos_bed)
        ut_bed_haider = cm.ut_haider(self.dp_bed, self.mu, self.phi_bed, self.rhog, self.rhos_bed)
        self.ut_bed_ganser = ut_bed_ganser
        self.ut_bed_haider = ut_bed_haider

        _, _, ut_bio_ganser = cm.ut_ganser(self.dp_bio, self.mu, self.phi_bio, self.rhog, self.rhos_bio)
        ut_bio_haider = cm.ut_haider(self.dp_bio, self.mu, self.phi_bio, self.rhog, self.rhos_bio)
        self.ut_bio_ganser = ut_bio_ganser
        self.ut_bio_haider = ut_bio_haider

        _, _, ut_char_ganser = cm.ut_ganser(self.dp_bio, self.mu, self.phi_bio, self.rhog, self.rhos_char)
        ut_char_haider = cm.ut_haider(self.dp_bio, self.mu, self.phi_bio, self.rhog, self.rhos_char)
        self.ut_char_ganser = ut_char_ganser
        self.ut_char_haider = ut_char_haider

    def _calc_tdh(self):
        """
        Calculate transport disengaging height [m] from Chan and Horio equations.
        """
        tdh_chan = 0.85 * (self.us**1.2) * (7.33 - 1.2 * np.log(self.us))
        tdh_horio = ((2.7 * self.di ** -0.36) - 0.7) * self.di * np.exp(0.74 * self.us * self.di ** -0.23)
        self.tdh_chan = tdh_chan
        self.tdh_horio = tdh_horio

    def _calc_zexp(self):
        """
        Calculate expanded bed height [m] from the bed expansion factor.
        """
        fbexp_ergun = cm.fbexp(self.di, self.dp_bed, self.rhog, self.rhos_bed, self.umf_ergun, self.us)
        zexp_ergun = self.zmf * fbexp_ergun
        fbexp_wenyu = cm.fbexp(self.di, self.dp_bed, self.rhog, self.rhos_bed, self.umf_wenyu, self.us)
        zexp_wenyu = self.zmf * fbexp_wenyu
        self.zexp_ergun = zexp_ergun
        self.zexp_wenyu = zexp_wenyu

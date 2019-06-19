import chemics as cm
import numpy as np
from collections import namedtuple


Umf = namedtuple('Umf', 'ergun wenyu')
UsUmf = namedtuple('UsUmf', 'ergun wenyu')
Zexp = namedtuple('Zexp', 'ergun wenyu')
Ut = namedtuple('Ut', 'ganser haider')


class BfbModel:

    def __init__(self, gas, params):
        self._gas = gas
        self._params = params

    @property
    def ac(self):
        """
        float
            Inner cross section area of the reactor [m²]
        """
        di = self._params.reactor['di']
        area = (np.pi * di**2) / 4
        return area

    def calc_us(self):
        """
        Returns
        -------
        us : float
            Superficial gas velocity [m/s]
        """
        p_kpa = self._gas.p / 1000
        q_lpm = cm.slm_to_lpm(self._gas.q, p_kpa, self._gas.tk)
        q_m3s = q_lpm / 60_000
        us = q_m3s / self.ac
        return us

    def calc_umf(self):
        """
        Minimum fluidization velocity (Umf).

        Returns
        -------
        namedtuple
            Umf from Ergun and Wen and Yu equations. Namedtuple fields are
            `ergun` and `wenyu`. Units are in [m/s].
        """
        dp = self._params.bed['dp'][0]
        ep = self._params.bed['ep']
        mug = self._gas.mu * 1e-7       # convert to kg/ms = µP * 1e-7
        phi = self._params.bed['phi']
        rhog = self._gas.rho
        rhos = self._params.bed['rhos']
        umf_ergun = cm.umf_ergun(dp, ep, mug, phi, rhog, rhos)
        umf_wenyu = cm.umf_coeff(dp, mug, rhog, rhos, coeff='wenyu')
        umf = Umf(umf_ergun, umf_wenyu)
        return umf

    def calc_ut_bed(self):
        """
        here
        """
        dp = self._params.bed['dp'][0]
        mug = self._gas.mu * 1e-7       # convert to kg/ms = µP * 1e-7
        phi = self._params.bed['phi']
        rhog = self._gas.rho
        rhos = self._params.bed['rhos']
        _, _, ut_ganser = cm.ut_ganser(dp, mug, phi, rhog, rhos)
        ut_haider = cm.ut_haider(dp, mug, phi, rhog, rhos)
        ut = Ut(ut_ganser, ut_haider)
        return ut

    def calc_ut_biomass(self):
        """
        here
        """
        dp = self._params.biomass['dp_mean']
        mug = self._gas.mu * 1e-7       # convert to kg/ms = µP * 1e-7
        phi = self._params.biomass['phi']
        rhog = self._gas.rho
        rhos = self._params.biomass['sg'] * 1000
        _, _, ut_ganser = cm.ut_ganser(dp, mug, phi, rhog, rhos)
        ut_haider = cm.ut_haider(dp, mug, phi, rhog, rhos)
        ut = Ut(ut_ganser, ut_haider)
        return ut

    def calc_ut_char(self):
        """
        here
        """
        dp = self._params.biomass['dp_mean']
        mug = self._gas.mu * 1e-7       # convert to kg/ms = µP * 1e-7
        phi = self._params.biomass['phi']
        rhog = self._gas.rho
        rhos = self._params.bed['rhos_char']
        _, _, ut_ganser = cm.ut_ganser(dp, mug, phi, rhog, rhos)
        ut_haider = cm.ut_haider(dp, mug, phi, rhog, rhos)
        ut = Ut(ut_ganser, ut_haider)
        return ut

    def calc_us_umf(self, umf, us):
        """
        Parameters
        ----------
        us : float
            Superficial gas velocity [m/s]
        umf : namedtuple
            Minimum fluidization velocity [m/s]

        Returns
        -------
        us_umf : float
            Ratio of Us to Umf [-]
        """
        usumf_ergun = us / umf.ergun
        usumf_wenyu = us / umf.wenyu
        usumf = UsUmf(usumf_ergun, usumf_wenyu)
        return usumf

    def calc_zexp(self, umf, us):
        """
        Parameters
        ----------
        umf : namedtuple
            Minimum fluidization velocity [m/s]
        us : float
            Superficial gas velocity [m/s]

        Returns
        -------
        zexp : float
            Bed expansion height [m]
        """
        di = self._params.reactor['di']
        dp = self._params.bed['dp'][0]
        rhog = self._gas.rho
        rhos = self._params.bed['rhos']
        zmf = self._params.bed['zmf']
        fbexp_ergun = cm.fbexp(di, dp, rhog, rhos, umf.ergun, us)
        zexp_ergun = zmf * fbexp_ergun
        fbexp_wenyu = cm.fbexp(di, dp, rhog, rhos, umf.wenyu, us)
        zexp_wenyu = zmf * fbexp_wenyu
        zexp = Zexp(zexp_ergun, zexp_wenyu)
        return zexp

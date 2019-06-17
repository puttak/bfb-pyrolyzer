import chemics as cm
import numpy as np


class BfbModel:

    def __init__(self, gas, params):
        """
        Model object representing a BFB biomass pyrolysis reactor.

        Attributes
        ----------
        ac : float
            Inner cross section area of the reactor [m²]
        us : float
            Superficial gas velocity [m/s]

        # TODO : define attributes
        """
        self._gas = gas
        self._params = params

        self.ac = None
        self.us = None

        self.umf_ergun = None
        self.us_umf_ergun = None
        self.zexp_ergun = None

        self.umf_wenyu = None
        self.us_umf_wenyu = None
        self.zexp_wenyu = None

        self.ut_ganser = None
        self.ut_haider = None

    def solve(self):
        """
        Solve BFB model and store results.
        """
        ac = self.calc_inner_ac()
        us = self.calc_us(ac)

        umf_ergun = self.calc_umf_ergun()
        us_umf_ergun = self.calc_us_umf(us, umf_ergun)
        zexp_ergun = self.calc_zexp(umf_ergun, us)

        umf_wenyu = self.calc_umf_wenyu()
        us_umf_wenyu = self.calc_us_umf(us, umf_wenyu)
        zexp_wenyu = self.calc_zexp(umf_wenyu, us)

        ut_ganser = self.calc_ut_ganser()
        ut_haider = self.calc_ut_haider()

        # Assign values to class attributes
        self.ac = ac
        self.us = us
        self.umf_ergun = umf_ergun
        self.us_umf_ergun = us_umf_ergun
        self.zexp_ergun = zexp_ergun
        self.umf_wenyu = umf_wenyu
        self.us_umf_wenyu = us_umf_wenyu
        self.zexp_wenyu = zexp_wenyu
        self.ut_ganser = ut_ganser
        self.ut_haider = ut_haider

    def calc_inner_ac(self):
        """
        Returns
        -------
        ac : float
            Inner cross section area of the rector [m²]
        """
        di = self._params.reactor['di']
        ac = (np.pi * di**2) / 4
        return ac

    def calc_us(self, ac):
        """
        Parameters
        ----------
        ac : float
            Inner cross section area of the reactor [m²]

        Returns
        -------
        us : float
            Superficial gas velocity [m/s]
        """
        p_kpa = self._gas.p / 1000
        q_lpm = cm.slm_to_lpm(self._gas.q, p_kpa, self._gas.tk)
        q_m3s = q_lpm / 60_000
        us = q_m3s / ac
        return us

    def calc_umf_ergun(self):
        """
        Returns
        -------
        umf : float
            Minimum fluidization velocity based on Ergun equation [m/s]
        """
        # Conversion for kg/ms = µP * 1e-7
        dp = self._params.bed['dp'][0]
        ep = self._params.bed['ep']
        mug = self._gas.mu * 1e-7
        phi = self._params.bed['phi']
        rhog = self._gas.rho
        rhos = self._params.bed['rhos']
        umf = cm.umf_ergun(dp, ep, mug, phi, rhog, rhos)
        return umf

    def calc_umf_wenyu(self):
        """
        Returns
        -------
        umf : float
            Minimum fluidization velocity based on Wen and Yu equation [m/s]
        """
        dp = self._params.bed['dp'][0]
        mug = self._gas.mu * 1e-7
        rhog = self._gas.rho
        rhos = self._params.bed['rhos']
        umf = cm.umf_coeff(dp, mug, rhog, rhos, coeff='wenyu')
        return umf

    def calc_us_umf(self, us, umf):
        """
        Parameters
        ----------
        us : float
            Superficial gas velocity [m/s]
        umf : float
            Minimum fluidization velocity [m/s]

        Returns
        -------
        us_umf : float
            Ratio of Us to Umf [-]
        """
        us_umf = us / umf
        return us_umf

    def calc_ut_ganser(self):
        """
        here
        """
        dp_bed = self._params.bed['dp'][0]
        phi_bed = self._params.bed['phi']
        rhos_bed = self._params.bed['rhos']
        rhos_char = self._params.bed['rhos_char']

        dp_bio = self._params.biomass['dp_mean']
        phi_bio = self._params.biomass['phi']
        rhos_bio = self._params.biomass['sg'] * 1000

        mug = self._gas.mu * 1e-7
        rhog = self._gas.rho

        _, _, ut_bed = cm.ut_ganser(dp_bed, mug, phi_bed, rhog, rhos_bed)
        _, _, ut_bio = cm.ut_ganser(dp_bio, mug, phi_bio, rhog, rhos_bio)
        _, _, ut_char = cm.ut_ganser(dp_bio, mug, phi_bio, rhog, rhos_char)
        return ut_bed, ut_bio, ut_char

    def calc_ut_haider(self):
        """
        here
        """
        dp_bed = self._params.bed['dp'][0]
        phi_bed = self._params.bed['phi']
        rhos_bed = self._params.bed['rhos']
        rhos_char = self._params.bed['rhos_char']

        dp_bio = self._params.biomass['dp_mean']
        phi_bio = self._params.biomass['phi']
        rhos_bio = self._params.biomass['sg'] * 1000

        mug = self._gas.mu * 1e-7
        rhog = self._gas.rho

        ut_bed = cm.ut_haider(dp_bed, mug, phi_bed, rhog, rhos_bed)
        ut_bio = cm.ut_haider(dp_bio, mug, phi_bio, rhog, rhos_bio)
        ut_char = cm.ut_haider(dp_bio, mug, phi_bio, rhog, rhos_char)
        return ut_bed, ut_bio, ut_char

    def calc_zexp(self, umf, us):
        """
        Parameters
        ----------
        umf : float
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
        fbexp = cm.fbexp(di, dp, rhog, rhos, umf, us)
        zexp = zmf * fbexp
        return zexp

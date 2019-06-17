import chemics as cm
import numpy as np


class BfbModel:

    def __init__(self, gas, params):
        """
        Model object representing a BFB biomass pyrolysis reactor.

        Attributes
        ----------
        gas : Gas or GasMix object
            Gas or gas mixture properties.
        params : module
            Parameters for model calculations.
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

    def solve_params(self):
        """
        Solve BFB model and store results.
        """
        mug = self._gas.mu
        ac = self.calc_inner_ac()
        us = self.calc_us(ac)

        umf_ergun = self.calc_umf_ergun(mug)
        us_umf_ergun = self.calc_us_umf(us, umf_ergun)
        zexp_ergun = self.calc_zexp(umf_ergun, us)

        umf_wenyu = self.calc_umf_wenyu(mug)
        us_umf_wenyu = self.calc_us_umf(us, umf_wenyu)
        zexp_wenyu = self.calc_zexp(umf_wenyu, us)

        # Assign values to class attributes
        self.ac = ac
        self.us = us
        self.umf_ergun = umf_ergun
        self.us_umf_ergun = us_umf_ergun
        self.zexp_ergun = zexp_ergun
        self.umf_wenyu = umf_wenyu
        self.us_umf_wenyu = us_umf_wenyu
        self.zexp_wenyu = zexp_wenyu

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

    def calc_umf_ergun(self, mug):
        """
        Parameters
        ----------
        mug : float
            Gas viscosity [µP]

        Returns
        -------
        umf : float
            Minimum fluidization velocity based on Ergun equation [m/s]
        """
        # Conversion for kg/ms = µP * 1e-7
        dp = self._params.bed['dp'][0]
        ep = self._params.bed['ep']
        mug = mug * 1e-7
        phi = self._params.bed['phi']
        rhog = self._gas.rho
        rhos = self._params.bed['rhos']
        umf = cm.umf_ergun(dp, ep, mug, phi, rhog, rhos)
        return umf

    def calc_umf_wenyu(self, mug):
        """
        Parameters
        ----------
        mug : float
            Gas viscosity [µP]

        Returns
        -------
        umf : float
            Minimum fluidization velocity based on Wen and Yu equation [m/s]
        """
        dp = self._params.bed['dp'][0]
        mug = mug * 1e-7
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

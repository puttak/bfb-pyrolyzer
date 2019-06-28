import chemics as cm


class Particle:

    def __init__(self, dp, ep, gas, phi, rhos):
        self.dp = dp
        self.ep = ep
        self.mu = gas.mu * 1e-7  # convert to kg/ms = µP * 1e-7
        self.phi = phi
        self.rhog = gas.rho
        self.rhos = rhos
        self._calc_umf()
        self._calc_ut()

    def _calc_umf(self):
        """
        Calculate minimum fluidization velocity [m/s] of the particle.
        """
        umf_ergun = cm.umf_ergun(self.dp, self.ep, self.mu, self.phi, self.rhog, self.rhos)
        umf_wenyu = cm.umf_coeff(self.dp, self.mu, self.rhog, self.rhos, coeff='wenyu')
        self.umf_ergun = umf_ergun
        self.umf_wenyu = umf_wenyu

    def _calc_ut(self):
        """
        Calculate terminal velocity [m/s] of the particle.
        """
        _, _, ut_ganser = cm.ut_ganser(self.dp, self.mu, self.phi, self.rhog, self.rhos)
        ut_haider = cm.ut_haider(self.dp, self.mu, self.phi, self.rhog, self.rhos)
        self.ut_ganser = ut_ganser
        self.ut_haider = ut_haider

import chemics as cm


class Bfb:

    def __init__(self, params):
        self.d_inner = params.d_inner
        self.dp = params.dp
        self.ep = params.ep
        self.p_gas = params.p_gas
        self.phi = params.phi
        self.rhos = params.rhos
        self.zmf = params.zmf

    def calc_umf(self, gas):
        mu = gas.mu * 1e-7
        umf = cm.umf_ergun(self.dp, self.ep, mu, self.phi, gas.rho, self.rhos)
        return umf

    def calc_us(self, umf, x):
        us = x * umf
        return us

    def calc_zexp(self, gas, umf, us):
        fbexp = cm.fbexp(self.d_inner, self.dp, gas.rho, self.rhos, umf, us)
        zexp = self.zmf * fbexp
        return zexp

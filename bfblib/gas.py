import chemics as cm
import numpy as np


class Gas:

    def __init__(self, formula, x, params, reactor):
        self.formula = formula
        self.press = params.pgas
        self.q = params.qgas
        self.temp = params.tgas
        self.x = x
        self.a_inner = reactor.a_inner

    @property
    def mw(self):
        mw_gas = cm.molecular_weight(self.formula)
        return mw_gas

    @property
    def mu(self):
        mu_gas = cm.mu_gas(self.formula, self.temp)
        return mu_gas

    @property
    def rho(self):
        rho_gas = cm.rhog(self.mw, self.press, self.temp)
        return rho_gas

    @property
    def us(self):
        q_lpm = cm.slm_to_lpm(self.q, self.press / 1000, self.temp)
        q_m3s = q_lpm / 60_000
        u_gas = q_m3s / self.a_inner
        return u_gas


class GasMix:

    def __init__(self, *gas):
        self.gases = gas

    @property
    def mu_graham(self):
        mu = np.asarray([gas.mu for gas in self.gases])
        x = np.asarray([gas.x for gas in self.gases])
        mu_mix = np.sum(mu * x)
        return mu_mix

    @property
    def mu_herning(self):
        mu = np.asarray([gas.mu for gas in self.gases])
        mw = np.asarray([gas.mw for gas in self.gases])
        x = np.asarray([gas.x for gas in self.gases])
        mu_mix = np.sum(mu * x * np.sqrt(mw)) / np.sum(x * np.sqrt(mw))
        return mu_mix

    @property
    def mw(self):
        mw = np.asarray([gas.mw for gas in self.gases])
        x = np.asarray([gas.x for gas in self.gases])
        mw_mix = np.average(mw, weights=x)
        return mw_mix

    @property
    def rho(self):
        mw = self.mw
        press = self.gases[0].press
        temp = self.gases[0].temp
        rho_mix = cm.rhog(mw, press, temp)
        return rho_mix

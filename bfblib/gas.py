import chemics as cm
import numpy as np


class Gas:

    def __init__(self, formula, press, temp, x=1):
        self.formula = formula
        self.press = press
        self.temp = temp
        self.x = x

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


class GasMix:

    def __init__(self, gases):
        self.gases = gases

    def mu_graham(self):
        mu = np.asarray([gas.mu for gas in self.gases])
        x = np.asarray([gas.x for gas in self.gases])
        mu_mix = np.sum(mu * x)
        return mu_mix

    def mu_herning(self):
        mu = np.asarray([gas.mu for gas in self.gases])
        mw = np.asarray([gas.mw for gas in self.gases])
        x = np.asarray([gas.x for gas in self.gases])
        mu_mix = np.sum(mu * x * np.sqrt(mw)) / np.sum(x * np.sqrt(mw))
        return mu_mix

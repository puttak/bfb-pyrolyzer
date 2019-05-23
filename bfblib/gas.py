import chemics as cm


class Gas:

    def __init__(self, name, press, temp):
        self.name = name
        self.press = press
        self.temp = temp

    @property
    def mw(self):
        mw_gas = cm.molecular_weight(self.name)
        return mw_gas

    @property
    def mu(self):
        mu_gas = cm.mu_gas(self.name, self.temp) * 1e-7
        return mu_gas

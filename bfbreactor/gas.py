import chemics as cm


class Gas:
    """
    Gas object for reactor calculations.
    """

    def __init__(self, formula, p, tk):
        self.formula = formula
        self.p = p
        self.tk = tk

    @property
    def mw(self):
        _mw = cm.molecular_weight(self.formula)
        return _mw

    @property
    def mu(self):
        _mu = cm.mu_gas(self.formula, self.tk)
        return _mu

    @property
    def rho(self):
        _rho = cm.rhog(self.mw, self.p, self.tk)
        return _rho


class GasMixture:
    """
    Gas mixture object for reactor calculations.
    """

    def __init__(self, mixture, p, tk, wts):
        self.mixture = mixture
        self.p = p
        self.tk = tk
        self.wts = wts

    @property
    def mw(self):
        _mw = cm.mw_mix(self.mixture, self.wts)
        return _mw

    @property
    def mu(self):
        _mu = cm.mu_gas_mix(self.mixture, self.tk, self.wts)
        return _mu

    @property
    def rho(self):
        _rho = cm.rhog(self.mw, self.p, self.tk)
        return _rho

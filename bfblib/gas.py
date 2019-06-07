import chemics as cm


class Gas:

    def __init__(self, sp, x, p, q, tk):
        self.sp = sp
        self.x = x
        self.p = p
        self.q = q
        self.tk = tk
        self.mw = None
        self.mu = None
        self.rho = None
        self._calc_properties()

    def _calc_properties(self):
        self.mw = cm.mw(self.sp)
        self.mu = cm.mu_gas(self.sp, self.tk)
        self.rho = cm.rhog(self.mw, self.p, self.tk)


class GasMix:

    def __init__(self, mus, mws, xs, p, q, tk):
        self.mus = mus
        self.mws = mws
        self.xs = xs
        self.p = p
        self.q = q
        self.tk = tk
        self.mu_graham = None
        self.mu_herning = None
        self.mw = None
        self.rho = None
        self._calc_properties()

    def _calc_properties(self):
        self.mw = cm.mw_mix(self.mws, self.xs)
        self.mu_graham = cm.mu_graham(self.mus, self.xs)
        self.mu_herning = cm.mu_herning(self.mus, self.mws, self.xs)
        self.rho = cm.rhog(self.mw, self.p, self.tk)

import chemics as cm


class GasMix:

    def __init__(self, mus, mws, xs, params):
        """
        Gas mixture properties as determined from gas components.

        Parameters
        ----------
        mus : list or tuple
            Viscosity of each gas component [µP]
        mws : list or tuple
            Molecular weight of each gas component [g/mol]
        xs : list or tuple
            Mole fraction of each gas component.
        params : dataclass
            Parameters for calculating gas mixture properties.

        Attributes
        ----------
        mus : list or tuple
            Viscosity of each gas component [µP]
        mws : list or tuple
            Molecular weight of each gas component [g/mol]
        xs : list or tuple
            Mole fraction of each gas component.
        params : module
            Parameters for calculating gas mixture properties.
        q : float
            Volumetric flow rate of the gas mixture into the reactor [SLM]
        tk : float
            Temperature of the gas in the reactor [K]
        mu_graham : float
            Viscosity of the gas mixture according to Graham method [µP]
        mu_herning : float
            Viscosity of the gas mixture according to Herning method [µP]
        mw : float
            Molecular weight of the gas mixture [g/mol]
        rho : float
            Density of the gas mixture [kg/m³]
        """
        self.mus = mus
        self.mws = mws
        self.xs = xs
        self.p = params.p
        self.q = params.q
        self.tk = params.tk
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

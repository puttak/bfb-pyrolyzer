import chemics as cm


class Gas:

    def __init__(self, sp, x, params):
        """
        Gas properties for a single gas component.

        Parameters
        ----------
        sp : str
            Species representing gas component.
        x : float
            Mole fraction of gas component.
        params : dataclass
            Parameters for calculating gas properties.

        Attributes
        ----------
        sp : str
            Species representing gas component.
        x : float
            Mole fraction of gas component.
        p : float
            Pressure of the gas [Pa]
        q : float
            Volumetric flow rate of the gas into the reactor [SLM]
        tk : float
            Temperature of the gas in the reactor [K]
        mw : float
            Molecular weight of the gas [g/mol]
        mu : float
            Viscosity of the gas [µP]
        rho : float
            Density of the gas [kg/m³]
        """
        self.sp = sp
        self.x = x
        self.p = params.p
        self.q = params.q
        self.tk = params.tk
        self.mw = None
        self.mu = None
        self.rho = None
        self._calc_properties()

    def _calc_properties(self):
        self.mw = cm.mw(self.sp)
        self.mu = cm.mu_gas(self.sp, self.tk)
        self.rho = cm.rhog(self.mw, self.p, self.tk)

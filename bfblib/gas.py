import chemics as cm
from dataclasses import dataclass


@dataclass
class Gas:
    """
    Gas or gas mixture properties.

    Attributes
    ----------
    p : float
        Pressure [Pa]
    q : float
        Volumetric flow rate [SLM]
    sp : list
        Species representing gas or gas mixture.
    tk : float
        Temperature [K]
    x : list
        Mole fraction of gas or gas mixture.
    mw : float
        Molecular weight [g/mol]
    mu : float
        Viscosity [µP]
    rho : float
        Density [kg/m³]
    """
    p: float
    q: float
    sp: list
    tk: float
    x: list
    mw: float = 0
    mu: float = 0
    rho: float = 0

    def calc_properties(self, mu_method='herning'):
        """
        Determine gas or gas mixture properties.

        Parameters
        ----------
        mu_method : str, optional
            Method used to calculate gas mixture viscosity.
        """
        n = len(self.sp)

        if n == 1:
            # single gas component
            self.mw = cm.mw(self.sp[0])
            self.mu = cm.mu_gas(self.sp[0], self.tk)
        else:
            # gas mixture containing multiple gas components
            mws = []
            mus = []
            for i in range(n):
                mw = cm.mw(self.sp[i])
                mu = cm.mu_gas(self.sp[i], self.tk)
                mws.append(mw)
                mus.append(mu)
            self.mw = cm.mw_mix(mws, self.x)
            if mu_method == 'graham':
                self.mu = cm.mu_graham(mus, self.x)
            elif mu_method == 'herning':
                self.mu = cm.mu_herning(mus, mws, self.x)
            else:
                raise ValueError(f'Viscosity method `{mu_method}` not available.')

        self.rho = cm.rhog(self.mw, self.p, self.tk)

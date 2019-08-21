import chemics as cm
import numpy as np
from trans_heat_cond import hc2


class Particle:
    """
    Particle model.

    Attributes
    ----------
    dp : float
        Mean diameter of bed particle [m]
    phi : float
        Sphericity of bed particle [-]
    rho : float
        Density of a bed particle [kg/m³]
    t : vector
        Times for calculating transient heat conduction in particle [s]
    t_devol : float
        Devolatilization time for 95% conversion [s]
    t_ref : float
        Time when particle is near reactor temperature [s]
    tk : array
        Intra-particle temperature [K]
    ut : namedtuple
        Terminal velocity [m/s]. Values available for `ganser` and `haider`.
    """

    def __init__(self, dp, dp_min, dp_max, phi, rho):
        self.dp = dp
        self.dp_min = dp_min
        self.dp_max = dp_max
        self.phi = phi
        self.rho = rho

    @classmethod
    def from_params(cls, params):
        """
        Create class from parameters dictionary.
        """
        dp = params['dp']
        dp_min = params['dp_min']
        dp_max = params['dp_max']
        phi = params['phi']
        rho = params['rho']
        return cls(dp, dp_min, dp_max, phi, rho)

    def calc_umb(self, gas):
        """
        Calculate minimum bubbling velocity [m/s] from Abrahamsen correlation.
        """
        frac = 0.001            # wt. fraction of fines < 45 um
        mug = gas.mu * 1e-7     # convert to kg/ms = µP * 1e-7
        umb = 2.07 * np.exp(0.716 * frac) * (self.dp * gas.rho**0.06) / (mug**0.347)
        return umb

    def calc_umb_umf(self, gas):
        """
        Calculate Umb/Umf [-] according to the Abrahamsen paper. Note that Umf
        is based on the Baeyens equation.
        """
        frac = 0.001            # wt. fraction of fines < 45 um
        g = 9.81                # acceleration due to gravity [m/s²]
        mug = gas.mu * 1e-7     # convert to kg/ms = µP * 1e-7
        rhop = self.rho

        x = 2300 * gas.rho**0.126 * mug**0.523 * np.exp(0.716 * frac)
        y = self.dp**0.8 * g**0.934 * (rhop - gas.rho)**0.934
        umb_umf = x / y
        return umb_umf

    def calc_umf_ergun(self, ep, gas):
        """
        Calculate minimum fluidization velocity [m/s] based on the Ergun
        equation.
        """
        mug = gas.mu * 1e-7     # convert to kg/ms = µP * 1e-7
        umf_ergun = cm.umf_ergun(self.dp, ep, mug, self.phi, gas.rho, self.rho)
        return umf_ergun

    def calc_umf_wenyu(self, gas):
        """
        Calculate minimum fluidization velocity [m/s] based on the Ergun
        equation.
        """
        mug = gas.mu * 1e-7     # convert to kg/ms = µP * 1e-7
        umf_wenyu = cm.umf_coeff(self.dp, mug, gas.rho, self.rho, coeff='wenyu')
        return umf_wenyu

    def calc_ut_ganser(self, gas):
        """
        Calculate terminal velocity [m/s] of the particle.
        """
        mug = gas.mu * 1e-7     # convert to kg/ms = µP * 1e-7
        ut_ganser = cm.ut_ganser(self.dp, mug, self.phi, gas.rho, self.rho)
        return ut_ganser

    def calc_ut_haider(self, gas):
        """
        Calculate terminal velocity [m/s] of the particle.
        """
        mug = gas.mu * 1e-7     # convert to kg/ms = µP * 1e-7
        ut_haider = cm.ut_haider(self.dp, mug, self.phi, gas.rho, self.rho)
        return ut_haider

    @staticmethod
    def build_time_vector(nt, t_max):
        """
        Times [s] for calculating transient heat conduction in biomass particle.
        """
        # nt is number of time steps
        # dt is time step [s]
        # t is time vector [s]
        dt = t_max / nt
        t_hc = np.arange(0, t_max + dt, dt)
        return t_hc

    def calc_trans_hc(self, b, h, k, m, mc, t, tki, tkinf):
        """
        Calculate intra-particle temperature profile [K] for biomass particle.
        """
        # tk is temperature array [K]
        # rows = time step
        # columns = center to surface temperature
        sg = self.rho / 1000
        tk_hc = hc2(self.dp, mc, k, sg, h, tki, tkinf, b, m, t)
        return tk_hc

    @staticmethod
    def calc_time_tkinf(t_hc, tk_hc, tk_inf):
        """
        Time [s] when biomass particle is near reactor temperature.
        """
        tk_ref = tk_inf - 1                             # value near reactor temperature [K]
        idx = np.where(tk_hc[:, 0] > tk_ref)[0][0]      # index where T > Tinf
        t_ref = t_hc[idx]                               # time where T > Tinf
        return t_ref

    def calc_devol_time(self, tk):
        """
        Calculate devolatilization time [s] of the biomass particle.
        """
        dp = self.dp * 1000
        dp_min = self.dp_min * 1000
        dp_max = self.dp_max * 1000
        tv = cm.devol_time(dp, tk)
        tv_min = cm.devol_time(dp_min, tk)
        tv_max = cm.devol_time(dp_max, tk)
        return tv, tv_min, tv_max

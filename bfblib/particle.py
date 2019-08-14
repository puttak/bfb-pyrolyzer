import chemics as cm
import numpy as np
from helpers import Umf, Ut
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
    umb : float
        Minimum bubbling velocity [m/s]
    umf : namedtuple
        Minimum fluidization velocity [m/s]. Values available for `ergun` and `wenyu`.
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

    def calc_dps(self, dpmin=0.00001, dpmax=0.001):
        """
        Range of particle diameters for certain calculations.
        """
        dps = np.linspace(dpmin, dpmax)
        self.dps = dps

    def calc_umb(self, mug, rhog):
        """
        Calculate minimum bubbling velocity [m/s] from Abrahamsen correlation.
        """
        frac = 0.001        # wt. fraction of fines < 45 um
        mug = mug * 1e-7    # convert to kg/ms = µP * 1e-7
        umb = 2.07 * np.exp(0.716 * frac) * (self.dp * rhog**0.06) / (mug**0.347)
        self.umb = umb

    def calc_umb_umf(self, mug, rhog):
        """
        Calculate Umb/Umf according to the Abrahamsen paper. Note that Umf is
        the Baeyens equation.
        """
        frac = 0.001        # wt. fraction of fines < 45 um
        g = 9.81            # acceleration due to gravity [m/s²]
        mug = mug * 1e-7    # convert to kg/ms = µP * 1e-7
        rhop = self.rho

        x = 2300 * rhog**0.126 * mug**0.523 * np.exp(0.716 * frac)
        y = self.dp**0.8 * g**0.934 * (rhop - rhog)**0.934
        umb_umf = x / y
        self.umb_umf = umb_umf

    def calc_umf(self, ep, mug, rhog):
        """
        Calculate minimum fluidization velocity [m/s] of the particle.
        """
        mug = mug * 1e-7  # convert to kg/ms = µP * 1e-7
        umf_ergun = cm.umf_ergun(self.dp, ep, mug, self.phi, rhog, self.rho)
        umf_wenyu = cm.umf_coeff(self.dp, mug, rhog, self.rho, coeff='wenyu')
        self.umf = Umf(umf_ergun, umf_wenyu)

    def calc_ut(self, mug, rhog):
        """
        Calculate terminal velocity [m/s] of the particle.
        """
        mug = mug * 1e-7  # convert to kg/ms = µP * 1e-7
        ut_ganser = cm.ut_ganser(self.dp, mug, self.phi, rhog, self.rho)
        ut_haider = cm.ut_haider(self.dp, mug, self.phi, rhog, self.rho)
        self.ut = Ut(ut_ganser, ut_haider)

    def calc_uts_dps(self, mug, rhog, dpmin=0.00001, dpmax=0.001):
        """
        Calculate terminal velocity [m/s] for a range of particle diameters.
        """
        mug = mug * 1e-7  # convert to kg/ms = µP * 1e-7
        ut_ganser = []
        ut_haider = []

        for dp in self.dps:
            ut_ganser.append(cm.ut_ganser(dp, mug, self.phi, rhog, self.rho))
            ut_haider.append(cm.ut_haider(dp, mug, self.phi, rhog, self.rho))

        self.uts_ganser = ut_ganser
        self.uts_haider = ut_haider

    def build_time_vector(self, nt, t_max):
        """
        Times [s] for calculating transient heat conduction in biomass particle.
        """
        # nt is number of time steps
        # dt is time step [s]
        # t is time vector [s]
        dt = t_max / nt
        self.t = np.arange(0, t_max + dt, dt)

    def calc_trans_hc(self, b, h, k, m, mc, tki, tkinf):
        """
        Calculate intra-particle temperature profile [K] for biomass particle.
        """
        # tk is temperature array [K]
        # rows = time step
        # columns = center to surface temperature
        sg = self.rho / 1000
        self.tk = hc2(self.dp, mc, k, sg, h, tki, tkinf, b, m, self.t)

    def calc_time_tkinf(self, tkinf):
        """
        Time [s] when biomass particle is near reactor temperature.
        """
        tk_ref = tkinf - 1                              # value near reactor temperature [K]
        idx = np.where(self.tk[:, 0] > tk_ref)[0][0]    # index where T > Tinf
        self.t_ref = self.t[idx]                        # time where T > Tinf

    def calc_devol_time(self, tk):
        """
        Calculate devolatilization time [s] of the biomass particle.
        """
        dp = self.dp * 1000
        dp_min = self.dp_min * 1000
        dp_max = self.dp_max * 1000
        self.t_devol = cm.devol_time(dp, tk)
        self.t_devol_min = cm.devol_time(dp_min, tk)
        self.t_devol_max = cm.devol_time(dp_max, tk)

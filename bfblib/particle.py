import chemics as cm
import numpy as np
from .trans_heat_cond import hc2


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
    umf_ergun : float
        Minimum fluidization velocity from Ergun equation [m/s]
    umf_wenyu : float
        Minimum fluidization velocity from Wen and Yu equation [m/s]
    ut_ganser : float
        Terminal velocity from Ganser equation [m/s]
    ut_haider : float
        Terminal velocity from Haider equation [m/s]
    """

    def __init__(self, dp, phi, rho):
        self.dp = dp
        self.phi = phi
        self.rho = rho

    def calc_umf(self, ep, mug, rhog):
        """
        Calculate minimum fluidization velocity [m/s] of the particle.
        """
        mug = mug * 1e-7  # convert to kg/ms = µP * 1e-7
        umf_ergun = cm.umf_ergun(self.dp, ep, mug, self.phi, rhog, self.rho)
        umf_wenyu = cm.umf_coeff(self.dp, mug, rhog, self.rho, coeff='wenyu')
        self.umf_ergun = umf_ergun
        self.umf_wenyu = umf_wenyu

    def calc_ut(self, mug, rhog):
        """
        Calculate terminal velocity [m/s] of the particle.
        """
        mug = mug * 1e-7  # convert to kg/ms = µP * 1e-7
        _, _, ut_ganser = cm.ut_ganser(self.dp, mug, self.phi, rhog, self.rho)
        ut_haider = cm.ut_haider(self.dp, mug, self.phi, rhog, self.rho)
        self.ut_ganser = ut_ganser
        self.ut_haider = ut_haider

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
        self.t_devol = cm.devol_time(dp, tk)

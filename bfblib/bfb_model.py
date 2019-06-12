import chemics as cm
import matplotlib.pyplot as plt
import numpy as np
from .trans_heat_cond import hc2


class BfbModel:

    def __init__(self, gas, params):
        self.gas = gas
        self.params = params

    """
    Fluidization methods.
    """

    def calc_inner_ac(self):
        """
        Returns
        -------
        ac : float
            Inner cross section area of the rector [m²]
        """
        di = self.params.reactor['di']
        ac = (np.pi * di**2) / 4
        return ac

    def calc_us(self, ac):
        """
        Parameters
        ----------
        ac : float
            Inner cross section area of the reactor [m²]

        Returns
        -------
        us : float
            Superficial gas velocity [m/s]
        """
        p_kPa = self.gas.p / 1000
        q_lpm = cm.slm_to_lpm(self.gas.q, p_kPa, self.gas.tk)
        q_m3s = q_lpm / 60_000
        us = q_m3s / ac
        return us

    def calc_umf_ergun(self, mug):
        """
        Parameters
        ----------
        mug : float
            Gas viscosity [µP]

        Returns
        -------
        umf : float
            Minimum fluidization velocity based on Ergun equation [m/s]
        """
        # Conversion for kg/ms = µP * 1e-7
        dp = self.params.bed['dps'][0]
        ep = self.params.bed['ep']
        mug = mug * 1e-7
        phi = self.params.bed['phi']
        rhog = self.gas.rho
        rhos = self.params.bed['rhos']
        umf = cm.umf_ergun(dp, ep, mug, phi, rhog, rhos)
        return umf

    def calc_umf_wenyu(self, mug):
        """
        Parameters
        ----------
        mug : float
            Gas viscosity [µP]

        Returns
        -------
        umf : float
            Minimum fluidization velocity based on Wen and Yu equation [m/s]
        """
        dp = self.params.bed['dps'][0]
        mug = mug * 1e-7
        rhog = self.gas.rho
        rhos = self.params.bed['rhos']
        umf = cm.umf_coeff(dp, mug, rhog, rhos, coeff='wenyu')
        return umf

    def calc_us_umf(self, us, umf):
        """
        Parameters
        ----------
        us : float
            Superficial gas velocity [m/s]
        umf : float
            Minimum fluidization velocity [m/s]

        Returns
        -------
        us_umf : float
            Ratio of Us to Umf [-]
        """
        us_umf = us / umf
        return us_umf

    def calc_zexp(self, umf, us):
        """
        Parameters
        ----------
        umf : float
            Minimum fluidization velocity [m/s]
        us : float
            Superficial gas velocity [m/s]

        Returns
        -------
        zexp : float
            Bed expansion height [m]
        """
        di = self.params.reactor['di']
        dp = self.params.bed['dps'][0]
        rhog = self.gas.rho
        rhos = self.params.bed['rhos']
        zmf = self.params.bed['zmf']
        fbexp = cm.fbexp(di, dp, rhog, rhos, umf, us)
        zexp = zmf * fbexp
        return zexp

    def build_geldart_figure(self):
        # Conversion for m = µm * 1e6
        # Conversion for g/cm³ = kg/m³ * 0.001
        dp = self.params.bed['dps'][0] * 1e6
        dpmin = self.params.bed['dps'][1] * 1e6
        dpmax = self.params.bed['dps'][2] * 1e6
        rhog = self.gas.rho * 0.001
        rhos = self.params.bed['rhos'] * 0.001
        fig = cm.geldart_chart(dp, rhog, rhos, dpmin, dpmax)
        return fig

    """
    Transient heat conduction methods.
    """

    def build_time_vector(self):
        """
        Returns
        -------
        t : vector
            Times for calculating transient heat conduction in biomass particle [s]
        """
        # nt is number of time steps
        nt = self.params.sim['nt']
        tmax = self.params.sim['tmax']
        dt = tmax / nt                      # time step [s]
        t = np.arange(0, tmax + dt, dt)     # time vector [s]
        return t

    def calc_trans_hc(self, t, tk_inf):
        """
        Returns
        -------
        tk : array
            Temperature profile inside the biomass particle.
        """
        # Calculate temperature profiles within particle.
        # rows = time step, columns = center to surface temperature
        dp = self.params.biomass['dp_mean']
        mc = self.params.biomass['mc']
        k = self.params.biomass['k']
        sg = self.params.biomass['sg']
        h = self.params.biomass['h']
        ti = self.params.biomass['ti']
        b = self.params.sim['b']
        m = self.params.sim['m']
        tk = hc2(dp, mc, k, sg, h, ti, tk_inf, b, m, t)     # temperature array [K]
        return tk

    def calc_time_tkinf(self, t_hc, tk_hc):
        """
        Returns
        -------
        t : float
            Time when biomass particle is near reactor temperature [s]
        """
        tk_ref = self.gas.tk - 1                        # value near reactor temperature [K]
        idx = np.where(tk_hc[:, 0] > tk_ref)[0][0]      # index where T > Tinf
        t_ref = t_hc[idx]                               # time where T > Tinf
        return t_ref

    def build_heat_cond_figure(self, t, tk, t_tkinf):
        """
        here
        """
        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(t, tk[:, 0], lw=2, label='center')
        ax.plot(t, tk[:, -1], lw=2, label='surface')
        ax.axvline(t_tkinf, alpha=0.5, c='k', ls='--', label='Tinf')
        ax.set_xlabel('Time [s]')
        ax.set_ylabel('Temperature [K]')
        ax.grid(color='0.9')
        ax.legend(loc='best')
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')
        return fig

    """
    Pyrolysis methods.
    """

    def calc_devol_time(self):
        """
        Returns
        -------
        tv : float
            Devolatilization time of the biomass particle [s]
        """
        dp = self.params.biomass['dp_mean'] * 1000
        tv = cm.devol_time(dp, self.gas.tk)
        return tv

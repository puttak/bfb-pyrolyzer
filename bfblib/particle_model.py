import numpy as np
import matplotlib.pyplot as plt

from .trans_heat_cond import hc2


class ParticleModel:

    def __init__(self, gas, params):
        self.gas = gas
        self.params = params
        self.results = {}
        self.figures = {}

    def solve(self, build_figures=False):
        """
        Solve particle model and store results.
        """
        t_hc = self.build_time_vector()
        tk_hc = self.calc_trans_hc(t_hc, self.gas.tk)
        t_tkinf = self.calc_time_tkinf(t_hc, tk_hc)

        # Store results from particle model calculations
        self.results = {
            't_tkinf': round(t_tkinf, 4),
        }

        # Store Matplotlib figures generated from particle model results
        if build_figures:
            fig_intra_prt_hc = self.plot_intra_particle_heat_cond(t_hc, tk_hc, t_tkinf)

            self.figures = {
                'fig_intra_prt_hc': fig_intra_prt_hc
            }

    def build_time_vector(self):
        """
        Returns
        -------
        t : vector
            Times for calculating transient heat conduction in biomass particle [s]
        """
        # nt is number of time steps
        nt = self.params.biomass['nt']
        tmax = self.params.biomass['t_max']
        dt = tmax / nt                      # time step [s]
        t = np.arange(0, tmax + dt, dt)     # time vector [s]
        return t

    def calc_trans_hc(self, t, tk_inf):
        """
        Parameters
        ----------
        t : vector
            Time values to calculate intra-particle heat conduction [s]
        tk_inf : float
            Ambient temperature [K]

        Returns
        -------
        tk : array
            Temperature profile inside the biomass particle [K]
        """
        # Calculate temperature profiles within particle.
        # rows = time step, columns = center to surface temperature
        dp = self.params.biomass['dp_mean']
        mc = self.params.biomass['mc']
        k = self.params.biomass['k']
        sg = self.params.biomass['sg']
        h = self.params.biomass['h']
        ti = self.params.biomass['tk_i']
        b = self.params.biomass['b']
        m = self.params.biomass['m']
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

    def plot_intra_particle_heat_cond(self, t, tk, t_tkinf):
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

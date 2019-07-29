import chemics as cm
import matplotlib.pyplot as plt
import numpy as np


def _config(ax, xlabel, ylabel):
    ax.grid(color='0.9')
    ax.set_axisbelow(True)
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')


def _autolabel(ax, bars):
    """
    Attach a text label above each bar in *rects*, displaying its height.
    """
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2f}',
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center',
                    va='bottom')


class Plotter:

    def __init__(self, solver, path):
        self._results_params = solver.results_params
        self._results_temps = solver.results_temps
        self._path = path

    def plot_geldart(self):
        """
        Plot the Geldart chart for particle size classification.
        """
        # Conversion for m = µm * 1e6
        # Conversion for g/cm³ = kg/m³ * 0.001
        dp = self._results_params['bed']['dp'] * 1e6
        dpmin = self._results_params['bed']['dp_min'] * 1e6
        dpmax = self._results_params['bed']['dp_max'] * 1e6
        rhog = self._results_params['gas']['rho'] * 0.001
        rhos = self._results_params['bed']['rho'] * 0.001
        fig = cm.geldart_chart(dp, rhog, rhos, dpmin, dpmax)
        fig.savefig(f'{self._path}/fig_geldart.pdf')

    def plot_intra_particle_heat_cond(self):
        """
        Plot intra-particle heat conduction at center and surface of biomass particle.
        """
        t_devol = self._results_params['bio']['t_devol']
        t_ref = self._results_params['bio']['t_ref']

        t = self._results_params['bio']['t_hc']
        tk_center = self._results_params['bio']['tk_center_hc']
        tk_surface = self._results_params['bio']['tk_surface_hc']

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(t, tk_center, label='center')
        ax.plot(t, tk_surface, label='surface')
        ax.axvline(t_devol, c='m', ls='--', label='t_devol')
        ax.axvline(t_ref, c='k', ls='--', label='t_ref')
        ax.legend(loc='best')
        _config(ax, 'Time [s]', 'Temperature [K]')
        fig.savefig(f'{self._path}/fig_intra_hc.pdf')

    def plot_tdevol_temps(self):
        """
        Plot devolatilization time of a biomass particle.
        """
        temps = self._results_temps['temps']
        t_devol = self._results_temps['bio']['t_devol']
        t_devol_min = self._results_temps['bio']['t_devol_min']
        t_devol_max = self._results_temps['bio']['t_devol_max']

        x = np.arange(len(temps))   # x-axis label locations
        width = 0.25                # width of the bars

        fig, ax = plt.subplots(tight_layout=True)
        bars_min = ax.bar(x, t_devol_min, width, label='dp_min')
        bars = ax.bar(x + width, t_devol, width, label='dp')
        bars_max = ax.bar(x + width * 2, t_devol_max, width, label='dp_max')
        ax.yaxis.grid(True, color='0.9')
        ax.legend(loc='best')
        ax.set_xticks(x + width)
        ax.set_xticklabels(temps)
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Devolatilization time [s]')
        ax.set_axisbelow(True)
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')
        _autolabel(ax, bars_min)
        _autolabel(ax, bars)
        _autolabel(ax, bars_max)
        fig.savefig(f'{self._path}/fig_tdevol_temps.pdf')

    def plot_umf_temps(self):
        """
        Plot Umf of bed particle for all cases.
        """
        temps = self._results_temps['temps']
        us = self._results_params['bfb']['us']
        umf_bed_ergun = self._results_temps['bed']['umf_ergun']
        umf_bed_wenyu = self._results_temps['bed']['umf_wenyu']

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(temps, umf_bed_ergun, 'k-', marker='.', label='Ergun')
        ax.plot(temps, umf_bed_wenyu, 'k--', marker='.', label='WenYu')
        ax.fill_between(temps, umf_bed_ergun, umf_bed_wenyu)
        ax.axhline(us, color='r', label='us')
        ax.legend(loc='best')
        _config(ax, 'Temperature [K]', 'Umf [m/s]')
        fig.savefig(f'{self._path}/fig_umf_bed.pdf')

    def plot_ut_temps(self):
        """
        Plot terminal velocity for a range of temperatures.
        """
        temps = self._results_temps['temps']
        us = self._results_params['bfb']['us']
        ut_bed_ganser = self._results_temps['bed']['ut_ganser']
        ut_bed_haider = self._results_temps['bed']['ut_haider']
        ut_bio_ganser = self._results_temps['bio']['ut_ganser']
        ut_bio_haider = self._results_temps['bio']['ut_haider']

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(temps, ut_bed_ganser, 'k--', marker='.', label='Ganser')
        ax.plot(temps, ut_bed_haider, 'k-', marker='.', label='Haider')
        ax.fill_between(temps, ut_bed_ganser, ut_bed_haider, label='bed')
        ax.plot(temps, ut_bio_ganser, 'k--', marker='.')
        ax.plot(temps, ut_bio_haider, 'k-', marker='.')
        ax.fill_between(temps, ut_bio_ganser, ut_bio_haider, label='bio')
        ax.axhline(us, color='r', label='us')
        ax.legend(bbox_to_anchor=(0., 1.02, 1, 0.102), loc=3, ncol=5, mode='expand', frameon=False)
        _config(ax, 'Temperature [K]', 'Terminal velocity, Ut [m/s]')
        fig.savefig(f'{self._path}/fig_ut_temps.pdf')

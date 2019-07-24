import chemics as cm
import matplotlib.pyplot as plt


def _config(ax, xlabel, ylabel):
    ax.grid(color='0.9')
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')


class Plotter:

    def __init__(self, params, solver, path):
        self._params = params
        self._results_params = solver.results_params
        self._results_temps = solver.results_temps
        self._path = path

    def plot_geldart(self):
        """
        Plot the Geldart chart for particle size classification.
        """
        # Conversion for m = µm * 1e6
        # Conversion for g/cm³ = kg/m³ * 0.001
        dp = self._params.bed['dp'] * 1e6
        dpmin = self._params.bed['dp_min'] * 1e6
        dpmax = self._params.bed['dp_max'] * 1e6
        rhog = self._results_params['gas']['rho'] * 0.001
        rhos = self._params.bed['rho'] * 0.001
        fig = cm.geldart_chart(dp, rhog, rhos, dpmin, dpmax)
        fig.savefig(f'{self._path}/fig_geldart.pdf')

    def plot_tdevol_temps(self):
        """
        Plot devolatilization time of a biomass particle.
        """
        temps = self._results_temps['temps']
        t_devol = self._results_temps['bio']['t_devol']

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(temps, t_devol, '.-')
        _config(ax, 'Temperature [K]', 'Devolatilization time [s]')
        fig.savefig(f'{self._path}/fig_tdevol_temps.pdf')

    def plot_umf_temps(self):
        """
        Plot minimum fluidization velocity for a range of temperatures.
        """
        temps = self._results_temps['temps']
        umf_bed_ergun = self._results_temps['bed']['umf_ergun']
        umf_bed_wenyu = self._results_temps['bed']['umf_wenyu']

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(temps, umf_bed_ergun, '.-', label='Ergun')
        ax.plot(temps, umf_bed_wenyu, '.-', label='WenYu')
        ax.legend(loc='best')
        _config(ax, 'Temperature [K]', 'Min. fluidization velocity, Umf [m/s]')
        fig.savefig(f'{self._path}/fig_umf_temps.pdf')

    def plot_ut_temps(self):
        """
        Plot terminal velocity for a range of temperatures.
        """
        temps = self._results_temps['temps']
        ut_bed_ganser = self._results_temps['bed']['ut_ganser']
        ut_bed_haider = self._results_temps['bed']['ut_haider']
        ut_bio_ganser = self._results_temps['bio']['ut_ganser']
        ut_bio_haider = self._results_temps['bio']['ut_haider']
        # ut_char_ganser = [x.ganser for x in ut_char]
        # ut_char_haider = [x.haider for x in ut_char]

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(temps, ut_bed_ganser, 'k--', label='Ganser')
        ax.plot(temps, ut_bed_haider, 'k-', label='Haider')
        ax.fill_between(temps, ut_bed_ganser, ut_bed_haider, alpha=0.6, facecolor='khaki', label='bed')
        ax.plot(temps, ut_bio_ganser, 'k--')
        ax.plot(temps, ut_bio_haider, 'k-')
        ax.fill_between(temps, ut_bio_ganser, ut_bio_haider, alpha=0.6, facecolor='lightgreen', label='bio')
        # ax.plot(tks, ut_char_ganser, 'k--')
        # ax.plot(tks, ut_char_haider, 'k-')
        # ax.fill_between(tks, ut_char_ganser, ut_char_haider, alpha=0.6, facecolor='grey', label='char')
        _config(ax, 'Temperature [K]', 'Terminal velocity, Ut [m/s]')
        ax.legend(bbox_to_anchor=(0., 1.02, 1, 0.102), loc=3, ncol=5, mode='expand', frameon=False)
        fig.savefig(f'{self._path}/fig_ut_temps.pdf')

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

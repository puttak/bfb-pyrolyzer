import chemics as cm
import json
import matplotlib.pyplot as plt


def _config(ax, xlabel, ylabel):
    ax.grid(color='0.9')
    ax.set_axisbelow(True)
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')


class Plotter:

    def __init__(self, project_path, case_paths):
        self._project_path = project_path
        self._case_paths = case_paths

    def plot_umf_bed(self):
        """
        Plot Umf of bed particle for all cases.
        """
        fig, ax = plt.subplots(tight_layout=True)

        for i, path in enumerate(self._case_paths):

            with open(path / 'results_temps.json', 'r') as f:
                results_dict = json.load(f)

            temps = results_dict['temps']
            umf_bed_ergun = results_dict['bed']['umf_ergun']
            umf_bed_wenyu = results_dict['bed']['umf_wenyu']

            ax.plot(temps, umf_bed_ergun, 'k-', label='Ergun' if i == 0 else '')
            ax.plot(temps, umf_bed_wenyu, 'k--', label='WenYu' if i == 0 else '')
            ax.fill_between(temps, umf_bed_ergun, umf_bed_wenyu, label=f'Case {i + 1}')

        ax.legend(loc='best')
        _config(ax, 'Temperature [K]', 'Umf [m/s]')
        fig.savefig(f'{self._project_path}/fig_cases_umf.pdf')

    def plot_geldart(self):
        """
        Plot the Geldart chart for particle size classification.
        """
        # Conversion for m = µm * 1e6
        # Conversion for g/cm³ = kg/m³ * 0.001

        for i, path in enumerate(self._case_paths):
            with open(path / 'results_params.json', 'r') as f:
                results_dict = json.load(f)

            dp = results_dict['bed']['dp'] * 1e6
            dpmin = results_dict['bed']['dp_min'] * 1e6
            dpmax = results_dict['bed']['dp_max'] * 1e6
            rhog = results_dict['gas']['rho'] * 0.001
            rhos = results_dict['bed']['rho'] * 0.001
            fig = cm.geldart_chart(dp, rhog, rhos, dpmin, dpmax)
            fig.savefig(f'{self._project_path}/fig_geldart_{i + 1}.pdf')

    def plot_tdevol_temps(self):
        """
        Plot devolatilization time of a biomass particle.
        """
        fig, ax = plt.subplots(tight_layout=True)

        for i, path in enumerate(self._case_paths):
            with open(path / 'results_temps.json', 'r') as f:
                results_dict = json.load(f)

            temps = results_dict['temps']
            t_devol = results_dict['bio']['t_devol']
            ax.plot(temps, t_devol, '.-', label=f'Case {i + 1}')

        ax.legend(loc='best')
        _config(ax, 'Temperature [K]', 'Devolatilization time [s]')
        fig.savefig(f'{self._project_path}/fig_tdevol_temps.pdf')

    def plot_ut_temps(self):
        """
        Plot terminal velocity for a range of temperatures.
        """
        fig, ax = plt.subplots(tight_layout=True)

        for i, path in enumerate(self._case_paths):
            with open(path / 'results_temps.json', 'r') as f:
                results_dict = json.load(f)

            temps = results_dict['temps']
            ut_bed_ganser = results_dict['bed']['ut_ganser']
            ut_bed_haider = results_dict['bed']['ut_haider']

            ax.plot(temps, ut_bed_ganser, 'k--', label='Ganser' if i == 0 else '')
            ax.plot(temps, ut_bed_haider, 'k-', label='Haider' if i == 0 else '')
            ax.fill_between(temps, ut_bed_ganser, ut_bed_haider, label=f'Case {i + 1}')

        _config(ax, 'Temperature [K]', 'Terminal velocity, Ut [m/s]')
        ax.legend(bbox_to_anchor=(0., 1.02, 1, 0.102), loc=3, ncol=5, mode='expand', frameon=False)
        fig.savefig(f'{self._project_path}/fig_ut_temps.pdf')

    def plot_intra_particle_heat_cond(self):
        """
        Plot intra-particle heat conduction at center and surface of biomass particle.
        """

        for i, path in enumerate(self._case_paths):
            with open(path / 'results_params.json', 'r') as f:
                results_dict = json.load(f)

            t_devol = results_dict['bio']['t_devol']
            t_ref = results_dict['bio']['t_ref']

            t = results_dict['bio']['t_hc']
            tk_center = results_dict['bio']['tk_center_hc']
            tk_surface = results_dict['bio']['tk_surface_hc']

            fig, ax = plt.subplots(tight_layout=True)
            ax.plot(t, tk_center, label='center')
            ax.plot(t, tk_surface, label='surface')
            ax.axvline(t_devol, c='m', ls='--', label='t_devol')
            ax.axvline(t_ref, c='k', ls='--', label='t_ref')
            ax.legend(loc='best')
            _config(ax, 'Time [s]', 'Temperature [K]')
            fig.savefig(f'{self._project_path}/fig_intra_hc_{i + 1}.pdf')

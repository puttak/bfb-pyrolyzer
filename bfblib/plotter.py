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


def _config_axis(ax):
    ax.grid(color='0.9')
    ax.set_axisbelow(True)
    ax.set_frame_on(False)
    ax.tick_params(color='0.9')


def _autolabel(ax, bars):
    """
    Attach a text label above each bar in *rects*, displaying its height.
    """
    for bar in bars:
        height = bar.get_height()
        ax.annotate(f'{height:.2g}',
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
        ax.legend(loc='lower right')
        _config(ax, 'Time [s]', 'Temperature [K]')
        fig.savefig(f'{self._path}/fig_intra_hc.pdf')

    def plot_umb_umf_ut_params(self):
        """
        """
        us = self._results_params['bfb']['us']

        umb = self._results_params['bed']['umb']
        umf_ergun = self._results_params['bed']['umf_ergun']
        umf_wenyu = self._results_params['bed']['umf_wenyu']

        ut_bed_ganser = self._results_params['bed']['ut_ganser']
        ut_bed_haider = self._results_params['bed']['ut_haider']

        ut_bio_ganser = self._results_params['bio']['ut_ganser']
        ut_bio_haider = self._results_params['bio']['ut_haider']
        ut_char_ganser = self._results_params['char']['ut_ganser']
        ut_char_haider = self._results_params['char']['ut_haider']

        gs = {'width_ratios': [1, 3]}
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.4, 4.8), gridspec_kw=gs, tight_layout=True)

        b1, = ax1.bar('umb_bed', umb, color='tan')
        b2, = ax1.bar('umf_bed_ergun', umf_ergun, color='tan')
        b3, = ax1.bar('umf_bed_wenYu', umf_wenyu, color='tan')
        ax1.set_xticklabels(['Umb', 'Umf\nErgun', 'Umf\nWenYu'])
        ax1.set_ylabel('Velocity [m/s]')
        _autolabel(ax1, [b1, b2, b3])
        _config_axis(ax1)

        b4, = ax2.bar('ut_bed_ganser', ut_bed_ganser, color='tan')
        b5, = ax2.bar('ut_bed_haider', ut_bed_haider, color='tan')
        b6, = ax2.bar('ut_bio_ganser', ut_bio_ganser, color='forestgreen')
        b7, = ax2.bar('ut_bio_haider', ut_bio_haider, color='forestgreen')
        b8, = ax2.bar('ut_char_ganser', ut_char_ganser, color='slategrey')
        b9, = ax2.bar('ut_char_haider', ut_char_haider, color='slategrey')
        l1 = ax2.axhline(us, color='r', alpha=0.6)
        ax2.set_xticklabels(['Ut\nGanser', 'Ut\nHaider', 'Ut\nGanser', 'Ut\nHaider', 'Ut\nGanser', 'Ut\nHaider'])
        ax2.set_ylabel('Velocity [m/s]')
        _autolabel(ax2, [b4, b5, b6, b7, b8, b9])
        _config_axis(ax2)

        bars = [l1, b1, b6, b8]
        labels = ['Us', 'Bed', 'Biomass', 'Char']
        ax2.legend(bars, labels, loc='upper right')
        fig.savefig(f'{self._path}/fig_umb_umf_ut_params.pdf')

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
        bars_min = ax.bar(x, t_devol_min, width, color='lightgreen', label='dp_min')
        bars = ax.bar(x + width, t_devol, width, color='limegreen', label='dp_mean')
        bars_max = ax.bar(x + width * 2, t_devol_max, width, color='forestgreen', label='dp_max')
        ax.yaxis.grid(True, color='0.9')
        ax.legend(loc='upper right')
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

    def plot_umb_umf_temps(self):
        """
        Plot Umf of bed particle for all cases.
        """
        temps = self._results_temps['temps']
        umb_bed = self._results_temps['bed']['umb']
        umb_umf_bed = self._results_temps['bed']['umb_umf']
        umf_bed_ergun = self._results_temps['bed']['umf_ergun']
        umf_bed_wenyu = self._results_temps['bed']['umf_wenyu']
        us_umf_ergun = self._results_temps['bfb']['us_umf_ergun']
        us_umf_wenyu = self._results_temps['bfb']['us_umf_wenyu']

        fig, (ax1, ax2) = plt.subplots(1, 2, tight_layout=True)

        ax1.plot(temps, umb_bed, marker='.', label='Umb')
        ax1.plot(temps, umf_bed_ergun, marker='.', label='Umf_Ergun')
        ax1.plot(temps, umf_bed_wenyu, marker='.', label='Umf_WenYu')
        ax1.legend(loc='best')
        ax1.set_xticks([int(x) for x in temps])
        _config(ax1, 'Temperature [K]', 'Velocity [m/s]')

        ax2.plot(temps, umb_umf_bed, marker='.', label='Umb/Umf')
        ax2.plot(temps, us_umf_ergun, marker='.', label='Ergun')
        ax2.plot(temps, us_umf_wenyu, marker='.', label='WenYu')
        ax2.set_xticks([int(x) for x in temps])
        _config(ax2, 'Temperature [K]', 'Velocity ratio [-]')

        fig.savefig(f'{self._path}/fig_umb_umf_temps.pdf')

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
        ut_char_ganser = self._results_temps['char']['ut_ganser']
        ut_char_haider = self._results_temps['char']['ut_haider']

        fig, (ax1, ax2, ax3) = plt.subplots(1, 3, tight_layout=True)

        ax1.plot(temps, ut_bed_ganser, 'k--', marker='.')
        ax1.plot(temps, ut_bed_haider, 'k-', marker='.')
        ax1.fill_between(temps, ut_bed_ganser, ut_bed_haider, color='tan')
        ax1.axhline(us, color='r')
        ax1.set_xticks([int(x) for x in temps])
        ax1.set_ylabel('Terminal velocity, Ut [m/s]')
        ax1.set_title('Bed')
        _config_axis(ax1)

        ax2.plot(temps, ut_bio_ganser, 'k--', marker='.')
        ax2.plot(temps, ut_bio_haider, 'k-', marker='.')
        ax2.fill_between(temps, ut_bio_ganser, ut_bio_haider, color='forestgreen')
        ax2.axhline(us, color='r')
        ax2.set_xticks([int(x) for x in temps])
        ax2.set_xlabel('Temperature [K]')
        ax2.set_title('Biomass')
        _config_axis(ax2)

        ax3.plot(temps, ut_char_ganser, 'k--', marker='.', label='Ganser')
        ax3.plot(temps, ut_char_haider, 'k-', marker='.', label='Haider')
        ax3.fill_between(temps, ut_char_ganser, ut_char_haider, color='slategrey')
        ax3.axhline(us, color='r', label='Us')
        ax3.set_xticks([int(x) for x in temps])
        ax3.set_title('Char')
        ax3.legend(loc='center left', bbox_to_anchor=(1.0, 0.5), frameon=False)
        _config_axis(ax3)

        fig.savefig(f'{self._path}/fig_ut_temps.pdf')

    def plot_uts_dps(self):
        """
        """
        dps = self._results_params['bio']['dps']
        dps = [dp * 1000 for dp in dps]

        dp = self._results_params['bio']['dp']
        dp_min = self._results_params['bio']['dp_min']
        dp_max = self._results_params['bio']['dp_max']
        ut_ganser = self._results_params['bio']['uts_ganser']
        ut_haider = self._results_params['bio']['uts_haider']
        us = self._results_params['bfb']['us']

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(dps, ut_ganser, label='Ganser')
        ax.plot(dps, ut_haider, label='Haider')
        ax.fill_between(dps, ut_ganser, ut_haider, alpha=0.2, color='gray')
        ax.axhline(us, color='r', zorder=1, label='Us')
        ax.axvline(dp_min * 1000, color='c', linestyle='--', label='Dp min')
        ax.axvline(dp * 1000, color='k', linestyle='--', label='Dp mean')
        ax.axvline(dp_max * 1000, color='m', linestyle='--', label='Dp max')
        ax.set_xlabel('Diameter [mm]')
        ax.set_ylabel('Terminal velocity, Ut [m/s]')
        ax.grid(color='0.9')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        ax.set_axisbelow(True)
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')

        fig.savefig(f'{self._path}/fig_uts_dps.pdf')

import matplotlib.pyplot as plt
import numpy as np


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


class PlotTemperatures:

    def __init__(self, solver, path):
        self._solver = solver
        self._params = solver.params
        self._path = path

    def plot_tv_temps(self):
        """
        Plot devolatilization time of a biomass particle.
        """
        tks = self._solver.tks
        t_devol = self._solver.tv
        t_devol_min = self._solver.tv_min
        t_devol_max = self._solver.tv_max

        x = np.arange(len(tks))   # x-axis label locations
        width = 0.25                # width of the bars

        fig, ax = plt.subplots(tight_layout=True)
        bars_min = ax.bar(x, t_devol_min, width, color='lightgreen', label='dp_min')
        bars = ax.bar(x + width, t_devol, width, color='limegreen', label='dp_mean')
        bars_max = ax.bar(x + width * 2, t_devol_max, width, color='forestgreen', label='dp_max')
        ax.yaxis.grid(True, color='0.9')
        ax.legend(loc='upper right')
        ax.set_xticks(x + width)
        ax.set_xticklabels(tks)
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Devolatilization time [s]')
        ax.set_axisbelow(True)
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')
        _autolabel(ax, bars_min)
        _autolabel(ax, bars)
        _autolabel(ax, bars_max)
        fig.savefig(f'{self._path}/fig_tv_temps.pdf')

    def plot_umb_umf_temps(self):
        """
        Plot Umf of bed particle for all cases.
        """
        tks = self._solver.tks
        umb = self._solver.umb
        umf_ergun = self._solver.umf_ergun
        umf_wenyu = self._solver.umf_wenyu

        x = np.arange(len(tks))   # x-axis label locations
        width = 0.25                # width of the bars

        fig, ax = plt.subplots(tight_layout=True)
        bars_umb = ax.bar(x, umb, width, label='Umb')
        bars_umf_ergun = ax.bar(x + width, umf_ergun, width, label='Umf Ergun')
        bars_umf_wenyu = ax.bar(x + width * 2, umf_wenyu, width, label='Umf WenYu')
        ax.yaxis.grid(True, color='0.9')
        # ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1), frameon=False, ncol=3)
        ax.set_xticks(x + width)
        ax.set_xticklabels(tks)
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Velocity [s]')
        ax.set_axisbelow(True)
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')
        _autolabel(ax, bars_umb)
        _autolabel(ax, bars_umf_ergun)
        _autolabel(ax, bars_umf_wenyu)

        fig.savefig(f'{self._path}/fig_umb_umf_temps.pdf')

    def plot_ut_temps(self):
        """
        Plot terminal velocity for a range of temperatures.
        """
        temps = self._solver.tks
        us = self._solver.us
        ut_bed_ganser = self._solver.ut_bed_ganser
        ut_bed_haider = self._solver.ut_bed_haider
        ut_bio_ganser = self._solver.ut_biomass_ganser
        ut_bio_haider = self._solver.ut_biomass_haider

        fig, (ax1, ax2) = plt.subplots(1, 2, tight_layout=True)

        ln1, = ax1.plot(temps, ut_bed_ganser, 'k--', marker='.')
        ln2, = ax1.plot(temps, ut_bed_haider, 'k-', marker='.')
        f1 = ax1.fill_between(temps, ut_bed_ganser, ut_bed_haider, color='tan', label='bed')
        ln3 = ax1.axhline(us, color='r')
        ax1.set_xticks([int(x) for x in temps])
        ax1.set_xlabel('Temperature [K]')
        ax1.set_ylabel('Terminal velocity [m/s]')
        _config_axis(ax1)

        ax2.plot(temps, ut_bio_ganser, 'k--', marker='.')
        ax2.plot(temps, ut_bio_haider, 'k-', marker='.')
        f2 = ax2.fill_between(temps, ut_bio_ganser, ut_bio_haider, color='forestgreen', label='biomass')
        ax2.axhline(us, color='r', label='Us')
        ax2.set_xticks([int(x) for x in temps])
        ax2.set_xlabel('Temperature [K]')
        ax2.legend([ln1, ln2, ln3, f1, f2], ['Ganser', 'Haider', 'Us', 'bed', 'biomass'], loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        _config_axis(ax2)

        fig.savefig(f'{self._path}/fig_ut_temps.pdf')

    def plot_umf_ratios_temps(self):
        """
        """
        temps = self._solver.tks
        umb_umf = self._solver.umb_umf
        us_umf_ergun = self._solver.us_umf_ergun
        us_umf_wenyu = self._solver.us_umf_wenyu

        x = np.arange(len(temps))   # x-axis label locations
        width = 0.25                # width of the bars

        fig, ax = plt.subplots(tight_layout=True)
        bars_umb = ax.bar(x, umb_umf, width, label='Umb/Umf')
        bars_usumf_ergun = ax.bar(x + width, us_umf_ergun, width, label='Us/Umf Ergun')
        bars_usumf_wenyu = ax.bar(x + width * 2, us_umf_wenyu, width, label='Us/Umf WenYu')
        ax.yaxis.grid(True, color='0.9')
        ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1), frameon=False, ncol=3)
        ax.set_xticks(x + width)
        ax.set_xticklabels(temps)
        ax.set_xlabel('Temperature [K]')
        ax.set_ylabel('Velocity [s]')
        ax.set_axisbelow(True)
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')
        _autolabel(ax, bars_umb)
        _autolabel(ax, bars_usumf_ergun)
        _autolabel(ax, bars_usumf_wenyu)

        fig.savefig(f'{self._path}/fig_umf_ratios_temps.pdf')

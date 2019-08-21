import chemics as cm
import matplotlib.pyplot as plt


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


def _config_axis(ax):
    ax.grid(color='0.9')
    ax.set_axisbelow(True)
    ax.set_frame_on(False)
    ax.tick_params(color='0.9')


def _config(ax, xlabel, ylabel):
    ax.grid(color='0.9')
    ax.set_axisbelow(True)
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')


class PlotParameters:

    def __init__(self, params, results, path):
        self._params = params
        self._results = results
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
        rhog = self._results['rhog'] * 0.001
        rhos = self._params.bed['rho'] * 0.001
        fig = cm.geldart_chart(dp, rhog, rhos, dpmin, dpmax)
        fig.savefig(f'{self._path}/fig_geldart.pdf')

    def plot_intra_particle_heat_cond(self):
        """
        Plot intra-particle heat conduction at center and surface of biomass particle.
        """
        t_devol = self._results['tv']
        t_ref = self._results['t_ref']

        t = self._results['t_hc']
        tk_center = self._results['tk_hc'][:, 0]
        tk_surface = self._results['tk_hc'][:, -1]

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(t, tk_center, label='center')
        ax.plot(t, tk_surface, label='surface')
        ax.axvline(t_devol, c='m', ls='--', label='t_devol')
        ax.axvline(t_ref, c='k', ls='--', label='t_ref')
        ax.legend(loc='lower right')
        _config(ax, 'Time [s]', 'Temperature [K]')
        fig.savefig(f'{self._path}/fig_intra_hc.pdf')

    def plot_umb_umf_ut(self):
        """
        """
        us = self._results['us']
        umb = self._results['umb']
        umf_ergun = self._results['umf_ergun']
        umf_wenyu = self._results['umf_wenyu']

        ut_bed_ganser = self._results['ut_bed_ganser']
        ut_bed_haider = self._results['ut_bed_haider']
        ut_bio_ganser = self._results['ut_bio_ganser']
        ut_bio_haider = self._results['ut_bio_haider']

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
        l1 = ax2.axhline(us, color='r', alpha=0.6)
        ax2.set_xticklabels(['Ut\nGanser', 'Ut\nHaider', 'Ut\nGanser', 'Ut\nHaider'])
        ax2.set_ylabel('Velocity [m/s]')
        _autolabel(ax2, [b4, b5, b6, b7])
        _config_axis(ax2)

        bars = [l1, b1, b6]
        labels = ['Us', 'Bed', 'Biomass']
        ax2.legend(bars, labels, loc='upper right')
        fig.savefig(f'{self._path}/fig_umb_umf_ut.pdf')

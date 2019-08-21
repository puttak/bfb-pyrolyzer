import matplotlib.pyplot as plt


class PlotDiameters:

    def __init__(self, params, results, path):
        self._params = params
        self._results = results
        self._path = path

    def plot_umf(self):
        """
        Plot minimum fluidization velocity for a range of bed particle diameters.
        """
        dps = self._results['dps']
        dps = [dp * 1000 for dp in dps]

        dp = self._params.bed['dp']
        dp_min = self._params.bed['dp_min']
        dp_max = self._params.bed['dp_max']

        umf_ergun = self._results['umf_ergun']
        umf_wenyu = self._results['umf_wenyu']

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(dps, umf_ergun, label='Ergun')
        ax.plot(dps, umf_wenyu, label='WenYu')
        ax.fill_between(dps, umf_ergun, umf_wenyu, alpha=0.2, color='gray')
        ax.axvline(dp_min * 1000, color='c', linestyle='--', label='Dp min')
        ax.axvline(dp * 1000, color='k', linestyle='--', label='Dp mean')
        ax.axvline(dp_max * 1000, color='m', linestyle='--', label='Dp max')
        ax.set_xlabel('Bed particle diameter [mm]')
        ax.set_ylabel('Min. fluidization velocity [m/s]')
        ax.grid(color='0.9')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        ax.set_axisbelow(True)
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')
        fig.savefig(f'{self._path}/fig_umf.pdf')

    def plot_ut_bed(self):
        """
        Plot terminal velocity for a range of bed particle diameters.
        """
        dps = self._results['dps']
        dps = [dp * 1000 for dp in dps]

        dp = self._params.bed['dp']
        dp_min = self._params.bed['dp_min']
        dp_max = self._params.bed['dp_max']

        us = self._results['us']
        ut_bed_ganser = self._results['ut_bed_ganser']
        ut_bed_haider = self._results['ut_bed_haider']

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(dps, ut_bed_ganser, label='Ganser')
        ax.plot(dps, ut_bed_haider, label='Haider')
        ax.fill_between(dps, ut_bed_ganser, ut_bed_haider, alpha=0.2, color='gray')
        ax.axhline(us, color='r', zorder=1, label='Us')
        ax.axvline(dp_min * 1000, color='c', linestyle='--', label='Dp min')
        ax.axvline(dp * 1000, color='k', linestyle='--', label='Dp mean')
        ax.axvline(dp_max * 1000, color='m', linestyle='--', label='Dp max')
        ax.set_xlabel('Bed particle diameter [mm]')
        ax.set_ylabel('Terminal velocity [m/s]')
        ax.grid(color='0.9')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        ax.set_axisbelow(True)
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')
        fig.savefig(f'{self._path}/fig_ut_bed.pdf')

    def plot_ut_bio(self):
        """
        Plot terminal velocity for a range of biomass particle diameters.
        """
        dps = self._results['dps']
        dps = [dp * 1000 for dp in dps]

        dp = self._params.biomass['dp']
        dp_min = self._params.biomass['dp_min']
        dp_max = self._params.biomass['dp_max']

        us = self._results['us']
        ut_bio_ganser = self._results['ut_bio_ganser']
        ut_bio_haider = self._results['ut_bio_haider']

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(dps, ut_bio_ganser, label='Ganser')
        ax.plot(dps, ut_bio_haider, label='Haider')
        ax.fill_between(dps, ut_bio_ganser, ut_bio_haider, alpha=0.2, color='gray')
        ax.axhline(us, color='r', zorder=1, label='Us')
        ax.axvline(dp_min * 1000, color='c', linestyle='--', label='Dp min')
        ax.axvline(dp * 1000, color='k', linestyle='--', label='Dp mean')
        ax.axvline(dp_max * 1000, color='m', linestyle='--', label='Dp max')
        ax.set_xlabel('Biomass particle diameter [mm]')
        ax.set_ylabel('Terminal velocity [m/s]')
        ax.grid(color='0.9')
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), frameon=False)
        ax.set_axisbelow(True)
        ax.set_frame_on(False)
        ax.tick_params(color='0.9')
        fig.savefig(f'{self._path}/fig_ut_bio.pdf')

import matplotlib.pyplot as plt


class PlotDiameters:

    def __init__(self, solver, path):
        self._solver = solver
        self._params = solver.params
        self._path = path

    def plot_umf_bed(self):
        """
        Plot minimum fluidization velocity for a range of bed particle diameters.
        """
        dps = self._solver.dps
        dps = [dp * 1000 for dp in dps]

        dp = self._params.bed['dp']
        dp_min = self._params.bed['dp_min']
        dp_max = self._params.bed['dp_max']

        umf_ergun = self._solver.umf_ergun
        umf_wenyu = self._solver.umf_wenyu

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
        fig.savefig(f'{self._path}/fig_umf_bed.pdf')

    def plot_ut_bed(self):
        """
        Plot terminal velocity for a range of bed particle diameters.
        """
        dps = self._solver.dps
        dps = [dp * 1000 for dp in dps]

        dp = self._params.bed['dp']
        dp_min = self._params.bed['dp_min']
        dp_max = self._params.bed['dp_max']

        us = self._solver.us
        ut_bed_ganser = self._solver.ut_bed_ganser
        ut_bed_haider = self._solver.ut_bed_haider

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

    def plot_ut_biomass(self):
        """
        Plot terminal velocity for a range of biomass particle diameters.
        """
        dps = self._solver.dps
        dps = [dp * 1000 for dp in dps]

        dp = self._params.biomass['dp']
        dp_min = self._params.biomass['dp_min']
        dp_max = self._params.biomass['dp_max']

        us = self._solver.us
        ut_biomass_ganser = self._solver.ut_biomass_ganser
        ut_biomass_haider = self._solver.ut_biomass_haider

        fig, ax = plt.subplots(tight_layout=True)
        ax.plot(dps, ut_biomass_ganser, label='Ganser')
        ax.plot(dps, ut_biomass_haider, label='Haider')
        ax.fill_between(dps, ut_biomass_ganser, ut_biomass_haider, alpha=0.2, color='gray')
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
        fig.savefig(f'{self._path}/fig_ut_biomass.pdf')

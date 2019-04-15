import matplotlib.pyplot as plt

_sub = str.maketrans('0123456789', '₀₁₂₃₄₅₆₇₈₉')


def _config(ax, xlabel, ylabel, title=None, loc=None):
    """
    Configure labels and appearance of the plot figure.
    """
    ax.grid(True, color='0.9')
    ax.set_frame_on(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.tick_params(color='0.9')
    if title is not None:
        ax.set_title(title)
    if loc is not None:
        ax.legend(loc=loc)


def plot_gas_properties(gases):
    """
    Plot molecular weight, viscosity, and density of several gases.
    """
    xticks_gas = range(len(gases))
    xlabels_gas = [x.formula.translate(_sub) for x in gases]

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4), tight_layout=True)
    for idx in range(len(gases)):
        ax1.bar(xticks_gas[idx], gases[idx].mw, align='center', color='C0')
        ax2.bar(xticks_gas[idx], gases[idx].mu, align='center', color='C4')
        ax3.bar(xticks_gas[idx], gases[idx].rho, align='center', color='C9')
    ax1.set_xticks(xticks_gas)
    ax1.set_xticklabels(xlabels_gas)
    ax1.set_ylabel('Molecular weight [g/mol]')
    ax1.set_frame_on(False)
    ax2.set_xticks(xticks_gas)
    ax2.set_xticklabels(xlabels_gas)
    ax2.set_ylabel('Viscosity [µP]')
    ax2.set_frame_on(False)
    ax3.set_xticks(xticks_gas)
    ax3.set_xticklabels(xlabels_gas)
    ax3.set_ylabel('Density [kg/m³]')
    ax3.set_frame_on(False)


def plot_mixture_properties(mixes, wts):
    """
    Plot molecular weight, viscosity, and density of several mixtures.
    """
    xticks_mix = range(len(mixes))
    xlabels_mix = ['+'.join(x.mixture).translate(_sub) for x in mixes]

    fig2, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(12, 4), tight_layout=True)
    for idx in range(len(mixes)):
        ax1.bar(xticks_mix[idx], mixes[idx].mw, align='center', color='C0')
        ax1.text(xticks_mix[idx] - 0.3, mixes[idx].mw + 0.4, f'{wts[idx][0]}+{wts[idx][1]}', fontsize=9)
        ax2.bar(xticks_mix[idx], mixes[idx].mu, align='center', color='C4')
        ax2.text(xticks_mix[idx] - 0.3, mixes[idx].mu + 4, f'{wts[idx][0]}+{wts[idx][1]}', fontsize=9)
        ax3.bar(xticks_mix[idx], mixes[idx].rho, align='center', color='C9')
        ax3.text(xticks_mix[idx] - 0.3, mixes[idx].rho + 0.008, f'{wts[idx][0]}+{wts[idx][1]}', fontsize=9)
    ax1.set_xticks(xticks_mix)
    ax1.set_xticklabels(xlabels_mix)
    ax1.set_ylabel('Molecular weight [g/mol]')
    ax1.set_frame_on(False)
    ax2.set_xticks(xticks_mix)
    ax2.set_xticklabels(xlabels_mix)
    ax2.set_ylabel('Viscosity [µP]')
    ax2.set_frame_on(False)
    ax3.set_xticks(xticks_mix)
    ax3.set_xticklabels(xlabels_mix)
    ax3.set_ylabel('Density [kg/m³]')
    ax3.set_frame_on(False)


def plot_umf_zexp(species, tc, umf, zexp):
    """
    Plot minimum fluidization velocity for a range of temperatures for different
    gases. Plot expanded bed height for a range of minimum fluidization
    velocities.
    """
    if type(species[0]) is tuple:
        species = ['+'.join(s) for s in species]

    fig, ax = plt.subplots(tight_layout=True)
    for idx, u in enumerate(umf):
        ax.plot(tc, u, marker='.', label=species[idx].translate(_sub))
    ax.grid(True, color='0.9')
    ax.legend(bbox_to_anchor=(1.04, 1), borderaxespad=0, frameon=False)
    ax.set_frame_on(False)
    ax.set_xlabel('Temperature [°C]')
    ax.set_ylabel('Minimum fluidization velocity [m/s]')
    ax.tick_params(color='0.9')
    plt.subplots_adjust(right=0.8)

    fig, ax = plt.subplots(tight_layout=True)
    for idx, u in enumerate(umf):
        ax.plot(u, zexp[idx], marker='.', label=species[idx].translate(_sub))
    _config(ax, 'Minimum fluidization velocity [m/s]', 'Bed expansion [m]', loc='best')


def plot_devol_bedtemp(dp, dvs, labels):
    """
    Plot devolatilization time for a range of biomass particles sizes at
    different bed temperatures.
    """
    fig, ax = plt.subplots(tight_layout=True)
    for idx, dv in enumerate(dvs):
        ax.plot(dp, dv, label=labels[idx])
    ax.legend(loc='best')
    _config(ax, 'Particle diameter [mm]', 'Devolatilization time [s]')


def plot_devol_diam(tbed, dvs, labels):
    """
    Plot devolatilization time for a range of temperatures at different biomass
    particle sizes. Note that bed temperature is converted from K to Celsius.
    """
    tbed = tbed - 273.15
    fig, ax = plt.subplots(tight_layout=True)
    for idx, dv in enumerate(dvs):
        ax.plot(tbed, dv, label=labels[idx])
    ax.legend(loc='best')
    _config(ax, 'Bed temperature [°C]', 'Devolatilization time [s]')


def show_plots():
    """
    Display all plot figures.
    """
    plt.show()

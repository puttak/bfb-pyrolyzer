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

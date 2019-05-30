import pathlib


def save_figure(name, fig, cwd):
    """
    Save figure as a PDF to the `results/` directory.

    Parameters
    ----------
    name : str
        Filename for saving plot figure.
    fig : Matplotlib figure
        Figure object of the plot to be saved.
    cwd : pathlib.PosixPath
        Path to current working directory.
    """
    results_dir = pathlib.Path(cwd, 'results')
    if not results_dir.exists():
        results_dir.mkdir()
    fig.savefig(f'results/{name}.pdf')

import pathlib


def save_figures(cwd, figs):
    """
    Save figures as a PDF to the `results` directory.

    Parameters
    ----------
    cwd : pathlib.PosixPath
        Path to current working directory.
    figs : dict
        Each key is used to name file. Each value is a Matplotlib figure.
    """
    results_dir = pathlib.Path(cwd, 'results')
    if not results_dir.exists():
        results_dir.mkdir()

    for name, fig in figs.items():
        fig.savefig(f'results/{name}.pdf')

    print('Plot figures saved to `results` folder.\n')

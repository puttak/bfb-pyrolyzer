import chemics as cm
from .plotter import geldart_figure


class Bed:

    def __init__(self, params, gas):
        self.dp = params.dp
        self.ep = params.ep
        self.phi = params.phi
        self.rhos = params.rhos

        self.mug = gas.mu_herning
        self.rhog = gas.rho

    @property
    def umf(self):
        mu = self.mug * 1e-7
        umf = cm.umf_ergun(self.dp, self.ep, mu, self.phi, self.rhog, self.rhos)
        return umf

    def geldart_fig(self, dpmin, dpmax):
        # Note that 1 m is 1e6 µm and 1 g/cm³ is 1000 kg/m³
        dp = self.dp * 1e6
        rhog = self.rhog / 1000
        rhos = self.rhos / 1000
        fig = geldart_figure(dp, rhog, rhos, dpmin, dpmax)
        return fig

import chemics as cm
from .plotter import geldart_figure


class Particle:

    def __init__(self, dp, phi, rho):
        self.dp = dp
        self.phi = phi
        self.rho = rho

    def geldart_fig(self, rhog, dpmin, dpmax):
        # Note that 1 m is 1e6 µm and 1 g/cm³ is 1000 kg/m³
        dp = self.dp * 1e6
        rhog = rhog / 1000
        rhos = self.rho / 1000
        fig = geldart_figure(dp, rhog, rhos, dpmin, dpmax)
        return fig

    def umf(self, ep, mu, rhog):
        mu = mu * 1e-7
        umf = cm.umf_ergun(self.dp, ep, mu, self.phi, rhog, self.rho)
        return umf

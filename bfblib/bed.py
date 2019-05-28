import chemics as cm
from .plotter import geldart_figure


class Bed:

    def __init__(self, params, mug, rhog):
        self.di = params.di
        self.dp = params.dp
        self.ep = params.ep
        self.phi = params.phi
        self.rhos = params.rhos
        self.zmf = params.zmf
        self.mug = mug
        self.rhog = rhog

    @property
    def umf(self):
        mug = self.mug * 1e-7
        umf = cm.umf_ergun(self.dp, self.ep, mug, self.phi, self.rhog, self.rhos)
        return umf

    def zexp(self, umf, us):
        fbexp = cm.fbexp(self.di, self.dp, self.rhog, self.rhos, umf, us)
        zexp = self.zmf * fbexp
        return zexp

    def geldart_fig(self, rhog, dpmin, dpmax):
        # Note that 1 m is 1e6 µm and 1 g/cm³ is 1000 kg/m³
        dp = self.dp * 1e6
        rhog = rhog / 1000
        rhos = self.rhos / 1000
        fig = geldart_figure(dp, rhog, rhos, dpmin, dpmax)
        return fig

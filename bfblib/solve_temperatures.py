from gas import Gas
from particle import Particle
from bfbreactor import BfbReactor


class SolveTemperatures:

    def __init__(self, params):
        self.params = params
        self.tks = None

        self.tv = None
        self.tv_min = None
        self.tv_max = None

        self.umb = None
        self.umb_umf = None

        self.umf_ergun = None
        self.umf_wenyu = None

        self.us = None
        self.us_umf_ergun = None
        self.us_umf_wenyu = None

        self.ut_bed_ganser = None
        self.ut_bed_haider = None
        self.ut_biomass_ganser = None
        self.ut_biomass_haider = None

    def get_temperatures(self):
        """
        Range of temperatures for solver calculations.
        """
        tk = self.params.gas['tk']
        tk_min = self.params.gas['tk_min']
        tk_max = self.params.gas['tk_max']
        self.tks = [tk_min, tk, tk_max]

    def calc_tv(self):
        """
        """
        pm = self.params
        biomass = Particle.from_params(pm.biomass)

        tv = []
        tv_min = []
        tv_max = []

        for tk in self.tks:
            biomass.calc_devol_time(tk)
            tv.append(biomass.t_devol)
            tv_min.append(biomass.t_devol_min)
            tv_max.append(biomass.t_devol_max)

        self.tv = tv
        self.tv_min = tv_min
        self.tv_max = tv_max

    def calc_us(self):
        """
        Calculate superficial gas velocity of BFB reactor.
        """
        pm = self.params
        gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], pm.gas['tk'])
        bfbreactor = BfbReactor(pm.reactor['di'], pm.reactor['q'], pm.reactor['zmf'])
        bfbreactor.calc_us(gas)
        self.us = bfbreactor.us

    def calc_us_umf(self):
        """
        """
        pm = self.params
        bed = Particle.from_params(self.params.bed)
        bfbreactor = BfbReactor(pm.reactor['di'], pm.reactor['q'], pm.reactor['zmf'])
        us_umf_ergun = []
        us_umf_wenyu = []

        for tk in self.tks:
            gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], tk)
            bed.calc_umf(pm.reactor['ep'], gas.mu, gas.rho)
            bfbreactor.calc_us(gas)
            bfbreactor.calc_us_umf(bed)
            us_umf_ergun.append(bfbreactor.us_umf.ergun)
            us_umf_wenyu.append(bfbreactor.us_umf.wenyu)

        self.us_umf_ergun = us_umf_ergun
        self.us_umf_wenyu = us_umf_wenyu

    def calc_umb(self):
        """
        """
        pm = self.params
        bed = Particle.from_params(self.params.bed)
        umb = []

        for tk in self.tks:
            gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], tk)
            bed.calc_umb(gas.mu, gas.rho)
            umb.append(bed.umb)

        self.umb = umb

    def calc_umb_umf(self):
        """
        """
        pm = self.params
        bed = Particle.from_params(self.params.bed)
        umb_umf = []

        for tk in self.tks:
            gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], tk)
            bed.calc_umb(gas.mu, gas.rho)
            bed.calc_umb_umf(gas.mu, gas.rho)
            umb_umf.append(bed.umb_umf)

        self.umb_umf = umb_umf

    def calc_umf(self):
        """
        """
        pm = self.params
        bed = Particle.from_params(self.params.bed)

        ep = pm.reactor['ep']
        umf_ergun = []
        umf_wenyu = []

        for tk in self.tks:
            gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], tk)
            bed.calc_umf(ep, gas.mu, gas.rho)
            umf_ergun.append(bed.umf.ergun)
            umf_wenyu.append(bed.umf.wenyu)

        self.umf_ergun = umf_ergun
        self.umf_wenyu = umf_wenyu

    def calc_ut(self):
        """
        Calculate terminal velocity [m/s] for a range of bed and biomass
        particle diameters.
        """
        pm = self.params
        bed = Particle.from_params(pm.bed)
        biomass = Particle.from_params(pm.biomass)

        ut_bed_ganser = []
        ut_bed_haider = []
        ut_biomass_ganser = []
        ut_biomass_haider = []

        for tk in self.tks:
            gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], tk)
            bed.calc_ut(gas.mu, gas.rho)
            ut_bed_ganser.append(bed.ut.ganser)
            ut_bed_haider.append(bed.ut.haider)

            biomass.calc_ut(gas.mu, gas.rho)
            ut_biomass_ganser.append(biomass.ut.ganser)
            ut_biomass_haider.append(biomass.ut.haider)

        self.ut_bed_ganser = ut_bed_ganser
        self.ut_bed_haider = ut_bed_haider
        self.ut_biomass_ganser = ut_biomass_ganser
        self.ut_biomass_haider = ut_biomass_haider

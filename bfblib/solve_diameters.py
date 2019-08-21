import numpy as np

from gas import Gas
from particle import Particle
from bfbreactor import BfbReactor


class SolveDiameters:

    def __init__(self, params):
        self.params = params

        # calculated attributes
        self.dps = None
        self.us = None
        self.umf_ergun = None
        self.umf_wenyu = None
        self.ut_bed_ganser = None
        self.ut_bed_haider = None
        self.ut_biomass_ganser = None
        self.ut_biomass_haider = None

    def calc_diameters(self, dpmin=0.00001, dpmax=0.001):
        """
        Range of particle diameters for solver calculations.
        """
        dps = np.linspace(dpmin, dpmax)
        self.dps = dps

    def calc_us(self):
        """
        Calculate superficial gas velocity of BFB reactor.
        """
        pm = self.params
        gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], pm.gas['tk'])
        bfbreactor = BfbReactor(pm.reactor['di'], pm.reactor['q'], pm.reactor['zmf'])
        bfbreactor.calc_us(gas)
        self.us = bfbreactor.us

    def calc_umf(self):
        """
        """
        pm = self.params
        gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], pm.gas['tk'])
        bed = Particle.from_params(pm.bed)

        ep = pm.reactor['ep']
        umf_ergun = []
        umf_wenyu = []

        for dp in self.dps:
            bed.dp = dp
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
        gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], pm.gas['tk'])
        bed = Particle.from_params(pm.bed)
        biomass = Particle.from_params(pm.biomass)

        ut_bed_ganser = []
        ut_bed_haider = []
        ut_biomass_ganser = []
        ut_biomass_haider = []

        for dp in self.dps:
            bed.dp = dp
            bed.calc_ut(gas.mu, gas.rho)
            ut_bed_ganser.append(bed.ut.ganser)
            ut_bed_haider.append(bed.ut.haider)

            biomass.dp = dp
            biomass.calc_ut(gas.mu, gas.rho)
            ut_biomass_ganser.append(biomass.ut.ganser)
            ut_biomass_haider.append(biomass.ut.haider)

        self.ut_bed_ganser = ut_bed_ganser
        self.ut_bed_haider = ut_bed_haider
        self.ut_biomass_ganser = ut_biomass_ganser
        self.ut_biomass_haider = ut_biomass_haider

from gas import Gas
from particle import Particle
from bfbreactor import BfbReactor


class SolveParameters:

    def __init__(self, params):
        self.params = params

        # Initialize gas, particle, and reactor objects
        # Note that gas mixture uses the Herning calculation for viscosity
        self.gas = Gas(params.gas['sp'], params.gas['x'], params.gas['p'], params.gas['tk'])
        self.bed = Particle.from_params(params.bed)
        self.biomass = Particle.from_params(params.biomass)
        self.bfbreactor = BfbReactor(params.reactor['di'], params.reactor['q'], params.reactor['zmf'])

    def calc_results(self):
        """
        Calculate results for particles and reactor.
        """
        gas = self.gas
        bed = self.bed
        biomass = self.biomass
        bfbreactor = self.bfbreactor

        # Bed particle results
        bed.calc_umb(gas.mu, gas.rho)
        bed.calc_umb_umf(gas.mu, gas.rho)
        bed.calc_umf(self.params.reactor['ep'], gas.mu, gas.rho)
        bed.calc_ut(gas.mu, gas.rho)

        # Biomass particle results
        biomass.calc_umf(self.params.reactor['ep'], gas.mu, gas.rho)
        biomass.calc_ut(gas.mu, gas.rho)
        biomass.build_time_vector(self.params.biomass['nt'], self.params.biomass['t_max'])
        biomass.calc_trans_hc(self.params.biomass['b'], self.params.biomass['h'], self.params.biomass['k'], self.params.biomass['m'], self.params.biomass['mc'], self.params.biomass['tk_init'], gas.tk)
        biomass.calc_time_tkinf(gas.tk)
        biomass.calc_devol_time(gas.tk)

        # BFB reactor results
        bfbreactor.calc_us(gas)
        bfbreactor.calc_us_umf(bed)
        bfbreactor.calc_tdh()
        bfbreactor.calc_zexp(bed, gas)

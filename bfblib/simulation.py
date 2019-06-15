import json
import numpy as np
import textwrap

from .gas import Gas
from .bfb_model import BfbModel


class Simulation:

    def __init__(self, params, path=None):
        self.params = params
        self.path = path
        self.results = {}
        self.figures = {}
        self.results_case = []

    def run_params(self):

        # Gas properties
        # Note that gas mixture uses the Herning calculation for viscosity
        gas = Gas(**self.params.gas)
        gas.calc_properties()

        # BFB model for fluidization and biomass pyrolysis
        bfb = BfbModel(gas, self.params)

        if self.path is not None:
            bfb.solve(build_figures=True)
            self.results = bfb.results
            self.figures = bfb.figures
            self.save_results()
            self.save_figures()
        else:
            bfb.solve()
            self.results = bfb.results
            self.print_parameters()
            self.print_results()

    def run_temps(self):

        print('>>>>>>>> Simulate Temperatures <<<<<<<<')
        tk_min = self.params.case['tk'][0]
        tk_max = self.params.case['tk'][1]
        tks = np.arange(tk_min, tk_max + 10, 10)

        for tk in tks:
            print(f'Running case at {tk} K ...')

            # Gas properties
            # Note that gas mixture uses the Herning calculation for viscosity
            gas = Gas(**self.params.gas)
            gas.tk = tk
            gas.calc_properties()

            # BFB model for fluidization and biomass pyrolysis
            bfb = BfbModel(gas, self.params)
            bfb.solve()
            self.results_case.append(bfb.results)

        print('Done.')
        self.save_results()

    def print_parameters(self):
        """
        Print parameter names, values, and descriptions to terminal.
        """
        params_bed = self.params.bed
        params_biomass = self.params.biomass
        params_gas = self.params.gas
        params_reactor = self.params.reactor

        sp = ', '.join(params_gas['sp'])
        x = ', '.join([str(gx) for gx in params_gas['x']])
        w = 12  # width specifier

        pm_string = f"""
        >>>>>>>>>> Parameters <<<<<<<<<<

        ------------- Bed --------------\n
        {'dp_mean':<{w}} {params_bed['dp'][0]:<{w}} Mean particle diameter [m]
        {'dp_min':<{w}} {params_bed['dp'][1]:<{w}} Minimum particle diameter [m]
        {'dp_max':<{w}} {params_bed['dp'][2]:<{w}} Maximum particle diameter [m]
        {'ep':<{w}} {params_bed['ep']:<{w}} Void fraction of bed [-]
        {'phi':<{w}} {params_bed['phi']:<{w}} Particle sphericity [-]
        {'rhos':<{w}} {params_bed['rhos']:<{w}} Density of a bed particle [kg/m³]
        {'zmf':<{w}} {params_bed['zmf']:<{w}} Bed height at minimum fluidization [m]

        ----------- Biomass ------------\n
        {'dp_mean':<{w}} {params_biomass['dp_mean']:<{w}} Mean particle diameter [m]
        {'h':<{w}} {params_biomass['h']:<{w}} Heat transfer coefficient for convection [W/m²K]
        {'k':<{w}} {params_biomass['k']:<{w}} Thermal conductivity of loblolly pine [W/mK]
        {'mc':<{w}} {params_biomass['mc']:<{w}} Moisture content [%]
        {'sg':<{w}} {params_biomass['sg']:<{w}} Specific gravity of loblolly pine [-]
        {'tk_i':<{w}} {params_biomass['tk_i']:<{w}} Initial particle temperature [K]

        ------------- Gas --------------\n
        {'p':<{w}} {params_gas['p']:<{w},} Gas pressure in reactor [Pa]
        {'q':<{w}} {params_gas['q']:<{w}} Volumetric flowrate of gas into reactor [SLM]
        {'sp':<{w}} {sp:<{w}} Components of gas mixture [-]
        {'tk':<{w}} {params_gas['tk']:<{w}} Gas temperature in reactor [K]
        {'x':<{w}} {x:<{w}} Mole fractions of components in gas mixture [-]

        ------------ Reactor -----------\n
        {'di':<{w}} {params_reactor['di']:<{w}} Inner diameter of reactor [m]
        """
        print(textwrap.dedent(pm_string))

    def print_results(self):
        """
        Print BFB model results to terminal.
        """
        w = 12  # width specifier

        res_string = f"""
        >>>>>>>>>>> Results <<<<<<<<<<<<

        -------- Gas Properties --------\n
        {'mw':<{w}} {self.results['gas_mw']:<{w}.4f} Molecular weight [g/mol]
        {'mu':<{w}} {self.results['gas_mu']:<{w}.2f} Viscosity [µP]
        {'rho':<{w}} {self.results['gas_rho']:<{w}.4f} Density [kg/m³]

        ----------- BFB Model ----------\n
        {'ac':<{w}} {self.results['ac']:<{w}.4f} Inner cross section area [m²]
        {'us':<{w}} {self.results['us']:<{w}.4f} Superficial gas velocity [m/s]

        Ergun
        {'umf':<{w}} {self.results['umf_ergun']:<{w}.4f} Minimum fluidization velocity [m/s]
        {'us_umf':<{w}} {self.results['us_umf_ergun']:<{w}.2f} Us/Umf for gas and bed particles [-]
        {'zexp':<{w}} {self.results['zexp_ergun']:<{w}.2f} Height of expanded bed [m]

        Wen and Yu
        {'umf':<{w}} {self.results['umf_wenyu']:<{w}.4f} Minimum fluidization velocity [m/s]
        {'us_umf':<{w}} {self.results['us_umf_wenyu']:<{w}.2f} Us/Umf for gas and bed particles [-]
        {'zexp':<{w}} {self.results['zexp_wenyu']:<{w}.2f} Height of expanded bed [m]

        {'t_devol':<{w}} {self.results['t_devol']:<{w}.2f} Devolatilization time for 95% conversion [s]
        {'t_tkinf':<{w}} {self.results['t_tkinf']:<{w}.2f} Time for particle center to reach T∞ [s]
        """
        print(textwrap.dedent(res_string))

    def save_results(self):
        """
        Save BFB model results as a JSON file.
        """
        with open(f'{self.path}/results.json', 'w') as file:
            if bool(self.results) is False:
                file.write(json.dumps(self.results_case, indent=4))
            else:
                file.write(json.dumps(self.results, indent=4))

        print(f'Results saved to `{self.path.name}` folder.')

    def save_figures(self):
        """
        Save BFB model figures as PDF files to the `results` folder.
        """
        for name, fig in self.figures.items():
            fig.savefig(f'{self.path}/{name}.pdf')

        print(f'Matplotlib figures saved to `{self.path.name}` folder.')

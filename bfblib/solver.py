import json

from gas import Gas
from particle import Particle
from bfbreactor import BfbReactor


class Solver:
    """
    Perform calculations for BFB pyrolyzer.

    Parameters
    ----------
    params : module
        Parameters needed for calculations.
    path : pathlib.PosixPath
        Path to directory containing file for parameters module.

    Attributes
    ----------
    results_params : dict
        Results calculated from parameters.
    results_temps : dict
        Results calculated for each temperature.
    """

    def __init__(self, params, path):
        self._params = params
        self._path = path

    def solve_params(self):
        """
        """
        pm = self._params

        # Gas properties
        # Note that gas mixture uses the Herning calculation for viscosity
        gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], pm.gas['tk'])

        # Bed particle
        bed = Particle.from_params(pm.bed)
        bed.calc_umb(gas.mu, gas.rho)
        bed.calc_umb_umf(gas.mu, gas.rho)
        bed.calc_umf(pm.reactor['ep'], gas.mu, gas.rho)
        bed.calc_ut(gas.mu, gas.rho)

        # Biomass particle
        bio = Particle.from_params(pm.biomass)
        bio.calc_umf(pm.reactor['ep'], gas.mu, gas.rho)
        bio.calc_ut(gas.mu, gas.rho)
        bio.build_time_vector(pm.biomass['nt'], pm.biomass['t_max'])
        bio.calc_trans_hc(pm.biomass['b'], pm.biomass['h'], pm.biomass['k'], pm.biomass['m'], pm.biomass['mc'], pm.biomass['tk_init'], gas.tk)
        bio.calc_time_tkinf(gas.tk)
        bio.calc_devol_time(gas.tk)
        bio.calc_dps()
        bio.calc_uts_dps(gas.mu, gas.rho)

        # Char particle
        char = Particle.from_params(pm.char)
        char.calc_umf(pm.reactor['ep'], gas.mu, gas.rho)
        char.calc_ut(gas.mu, gas.rho)

        # BFB reactor
        bfb = BfbReactor(pm.reactor['di'], pm.reactor['q'], pm.reactor['zmf'])
        bfb.calc_us(gas)
        bfb.calc_us_umf(bed)
        bfb.calc_tdh()
        bfb.calc_zexp(bed, gas)

        results_params = {
            'name': 'results_params',
            'case': {
                'desc': pm.case['case_desc'],
                'num': pm.case['case_num']
            },
            'gas': {
                'mw': gas.mw,
                'mu': gas.mu,
                'rho': gas.rho
            },
            'bed': {
                'dp': pm.bed['dp'],
                'dp_min': pm.bed['dp_min'],
                'dp_max': pm.bed['dp_max'],
                'rho': pm.bed['rho'],
                'umb': bed.umb,
                'umb_umf': bed.umb_umf,
                'umf_ergun': bed.umf.ergun,
                'umf_wenyu': bed.umf.wenyu,
                'ut_ganser': bed.ut.ganser,
                'ut_haider': bed.ut.haider
            },
            'bio': {
                't_devol': bio.t_devol,
                't_devol_min': bio.t_devol_min,
                't_devol_max': bio.t_devol_max,
                't_ref': bio.t_ref,
                'umf_ergun': bio.umf.ergun,
                'umf_wenyu': bio.umf.wenyu,
                'ut_ganser': bio.ut.ganser,
                'ut_haider': bio.ut.haider,
                't_hc': bio.t.tolist(),
                'tk_center_hc': bio.tk[:, 0].tolist(),
                'tk_surface_hc': bio.tk[:, -1].tolist(),
                'dps': bio.dps.tolist(),
                'dp': bio.dp,
                'dp_min': bio.dp_min,
                'dp_max': bio.dp_max,
                'uts_ganser': bio.uts_ganser,
                'uts_haider': bio.uts_haider
            },
            'char': {
                'umf_ergun': char.umf.ergun,
                'umf_wenyu': char.umf.wenyu,
                'ut_ganser': char.ut.ganser,
                'ut_haider': char.ut.haider
            },
            'bfb': {
                'ac': bfb.ac,
                'us': bfb.us,
                'tdh_chan': bfb.tdh.chan,
                'tdh_horio': bfb.tdh.horio,
                'us_umf_ergun': bfb.us_umf.ergun,
                'us_umf_wenyu': bfb.us_umf.wenyu,
                'zexp_ergun': bfb.zexp.ergun,
                'zexp_wenyu': bfb.zexp.wenyu
            }
        }

        self.results_params = results_params

    def solve_temps(self):
        """
        """
        pm = self._params
        temps = pm.solve['temps']

        bed = Particle.from_params(pm.bed)
        bio = Particle.from_params(pm.biomass)
        char = Particle.from_params(pm.char)

        mu = []
        rho = []

        umb_bed = []
        umb_umf_bed = []
        umf_bed_ergun = []
        umf_bed_wenyu = []
        ut_bed_ganser = []
        ut_bed_haider = []

        ut_bio_ganser = []
        ut_bio_haider = []
        t_devol = []
        t_devol_min = []
        t_devol_max = []

        ut_char_ganser = []
        ut_char_haider = []

        us_umf_ergun = []
        us_umf_wenyu = []

        for tk in temps:
            # Gas properties at temperature
            # Note that gas mixture uses the Herning calculation for viscosity
            gas = Gas(pm.gas['sp'], pm.gas['x'], pm.gas['p'], tk)

            # Bed particle
            bed.calc_umb(gas.mu, gas.rho)
            bed.calc_umb_umf(gas.mu, gas.rho)
            bed.calc_umf(pm.reactor['ep'], gas.mu, gas.rho)
            bed.calc_ut(gas.mu, gas.rho)

            # Biomass particle
            bio.calc_ut(gas.mu, gas.rho)
            bio.calc_devol_time(gas.tk)

            # Char particle
            char.calc_ut(gas.mu, gas.rho)

            # BFB reactor
            bfb = BfbReactor(pm.reactor['di'], pm.reactor['q'], pm.reactor['zmf'])
            bfb.calc_us(gas)
            bfb.calc_us_umf(bed)

            # Store results for temperature
            mu.append(gas.mu)
            rho.append(gas.rho)

            umb_bed.append(bed.umb)
            umb_umf_bed.append(bed.umb_umf)
            umf_bed_ergun.append(bed.umf.ergun)
            umf_bed_wenyu.append(bed.umf.wenyu)
            ut_bed_ganser.append(bed.ut.ganser)
            ut_bed_haider.append(bed.ut.haider)

            t_devol.append(bio.t_devol)
            t_devol_min.append(bio.t_devol_min)
            t_devol_max.append(bio.t_devol_max)

            ut_bio_ganser.append(bio.ut.ganser)
            ut_bio_haider.append(bio.ut.haider)

            ut_char_ganser.append(char.ut.ganser)
            ut_char_haider.append(char.ut.haider)

            us_umf_ergun.append(bfb.us_umf.ergun)
            us_umf_wenyu.append(bfb.us_umf.wenyu)

        results_temps = {
            'name': 'results_temps',
            'temps': temps,
            'gas': {
                'mu': mu,
                'rho': rho
            },
            'bed': {
                'umb': umb_bed,
                'umb_umf': umb_umf_bed,
                'umf_ergun': umf_bed_ergun,
                'umf_wenyu': umf_bed_wenyu,
                'ut_ganser': ut_bed_ganser,
                'ut_haider': ut_bed_haider
            },
            'bio': {
                't_devol': t_devol,
                't_devol_min': t_devol_min,
                't_devol_max': t_devol_max,
                'ut_ganser': ut_bio_ganser,
                'ut_haider': ut_bio_haider
            },
            'char': {
                'ut_ganser': ut_char_ganser,
                'ut_haider': ut_char_haider
            },
            'bfb': {
                'us_umf_ergun': us_umf_ergun,
                'us_umf_wenyu': us_umf_wenyu
            }
        }

        self.results_temps = results_temps

    def save_results(self):
        """
        Write each results dictionary as JSON file to case directory.
        """
        with open(self._path / 'results_params.json', 'w') as fp:
            json.dump(self.results_params, fp, indent=4)

        with open(self._path / 'results_temps.json', 'w') as fp:
            json.dump(self.results_temps, fp, indent=4)

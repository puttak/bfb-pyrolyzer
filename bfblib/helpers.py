from collections import namedtuple


Tdh = namedtuple('Tdh', ['chan', 'horio'])

Umf = namedtuple('Umf', ['ergun', 'wenyu'])

UsUmf = namedtuple('UsUmf', ['ergun', 'wenyu'])

Ut = namedtuple('Ut', ['ganser', 'haider'])

Zexp = namedtuple('Zexp', ['ergun', 'wenyu'])


def results_params(pm, gas, bed, bio, char, bfb):
    """
    Store results in dictionary which will be written to a JSON file.
    """
    results = {
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
            'umf_ergun': bed.umf.ergun,
            'umf_wenyu': bed.umf.wenyu,
            'ut_ganser': bed.ut.ganser,
            'ut_haider': bed.ut.haider
        },
        'bio': {
            't_devol': bio.t_devol,
            't_ref': bio.t_ref,
            'umf_ergun': bio.umf.ergun,
            'umf_wenyu': bio.umf.wenyu,
            'ut_ganser': bio.ut.ganser,
            'ut_haider': bio.ut.haider
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
    return results

from astropy.table import Table
from scipy.interpolate import LinearNDInterpolator
from .filters import filters
# from pkg_resources import resource_filename
from importlib import resources


def build_subinterpolator(BB_table, bands):
    interpolator = dict()
    teff = BB_table['Teff']
    logg = BB_table['log(g)']
    for band in bands:
        temps = BB_table['T_BB_{}'.format(band)]
        coords_in = list(zip(teff, logg))
        coords_out = list(temps)
        interpolator[band] = LinearNDInterpolator(coords_in, coords_out, rescale=True)
    return interpolator


def build_bb_interpolator():
    """
    Creates interpolators for use in utils.teff_to_tbb function.
    Interpolates precomputed tables of effective temperature to blackbody
    equivalent temperature required by LCURVE.

    Outputs interpolators as dictionary
    >>> bb_interpolator = build_bb_interpolator()
    >>> bb_interpolator[star_type][band](Teff, log(g))
    """
    
    wd_models = ['Koester']
    ms_models = ['PHOENIX-HiRes', 'BT-SETTL', 'BT-SETTL-CIFIST']
    instruments = ['hcam', 'ucam', 'ucam_sloan', 'sdss', 'tess', 'ztf']
    
    # fpath = resource_filename('pylcurve', 'data/blackbody_temps/')
    ref = resources.files('pylcurve') / 'data' / 'blackbody_temps'
    with resources.as_file(ref) as fpath:
    
        ms_interpolator = dict()
        for model in ms_models:
            ms_instr_interpolator = dict()
            for instrument in instruments:
                cam = filters(instrument)
                tab_MS = Table.read(f"{fpath}/Tms_to_Tbb_{model}_{instrument}.dat", format='ascii.tab')
                ms_instr_interpolator[instrument] = build_subinterpolator(tab_MS, cam.bands)
            ms_interpolator[model] = ms_instr_interpolator

        wd_interpolator = dict()
        for model in wd_models:
            wd_instr_interpolator = dict()
            for instrument in instruments:
                cam = filters(instrument)
                tab_WD = Table.read(f"{fpath}/Twd_to_Tbb_{model}_{instrument}.dat", format='ascii.tab')
                wd_instr_interpolator[instrument] = build_subinterpolator(tab_WD, cam.bands)
            wd_interpolator[model] = wd_instr_interpolator
        hcam = filters("hcam")
        ucam = filters("ucam")
        tess = filters("tess")
        wd_instr_interpolator = dict()
        tab_WD = Table.read(f"{fpath}/Twd_to_Tbb_Claret_hcam.dat", format='ascii.tab')
        wd_instr_interpolator['hcam'] = build_subinterpolator(tab_WD, hcam.bands)
        wd_instr_interpolator['ucam'] = build_subinterpolator(tab_WD, ucam.bands)
        tab_WD = Table.read(f"{fpath}/Twd_to_Tbb_Claret_tess.dat", format='ascii.tab')
    wd_instr_interpolator['tess'] = build_subinterpolator(tab_WD, tess.bands)
    wd_interpolator['Claret'] = wd_instr_interpolator

    bb_interpolator = dict()
    bb_interpolator['MS'] = ms_interpolator
    bb_interpolator['WD'] = wd_interpolator

    return bb_interpolator


bb_interpolator = build_bb_interpolator()
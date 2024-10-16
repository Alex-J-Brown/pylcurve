import numpy as np
from scipy.interpolate import LinearNDInterpolator
from pkg_resources import resource_filename


def build_roche_interpolator():
    """
    Creates interpolator for converting from volume-averaged radii to radii
    measured towards L1.
    
    Outputs interpolator
    """
    fname = resource_filename('pylcurve', 'data/roche_conversion/roche_grid_new_corr.dat')

    q, r2_a_L1, r2_va_a = np.loadtxt(fname, unpack=True)

    coords_in = list(zip(q, r2_va_a))
    coords_out = list(r2_a_L1)
    roche_interpolator = LinearNDInterpolator(coords_in, coords_out, rescale=True)
    return roche_interpolator

roche_interpolator = build_roche_interpolator()
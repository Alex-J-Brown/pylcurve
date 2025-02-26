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

    coords_in_l1 = list(zip(q, r2_va_a))
    coords_out_l1 = list(r2_a_L1)

    coords_in_va = list(zip(q, r2_a_L1))
    coords_out_va = list(r2_va_a)

    roche_interpolator_l1 = LinearNDInterpolator(coords_in_l1, coords_out_l1, rescale=True)
    roche_interpolator_va = LinearNDInterpolator(coords_in_va, coords_out_va, rescale=True)
    return roche_interpolator_l1, roche_interpolator_va

roche_interpolator_l1, roche_interpolator_va = build_roche_interpolator()